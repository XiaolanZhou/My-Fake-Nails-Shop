import os
import stripe
from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.db import get_db_connection
from typing import Any, Dict, cast, Sequence
from math import floor

# Initialize Stripe with the secret key from environment variables
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

payments_bp = Blueprint("payments", __name__)


def _build_line_items(items):
    """Helper to convert cart DB rows to Stripe line_items structure"""
    line_items = []
    for item in items:
        # Stripe requires the amount in the smallest currency unit (cents)
        unit_amount = int(float(item["price"]) * 100)
        line_items.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": item["name"]},
                    "unit_amount": unit_amount,
                },
                "quantity": int(item["quantity"]),
            }
        )
    return line_items


@payments_bp.route("/create-checkout-session", methods=["POST"])
def create_checkout_session():
    """Creates a Stripe Checkout Session from the current cart."""
    # JWT is optional – allow guest checkout
    verify_jwt_in_request(optional=True)
    user_id = get_jwt_identity()  # None if not logged in

    db = get_db_connection()
    cur = db.cursor()

    # Check if client asked to apply loyalty points (for logged-in users)
    data = request.get_json(silent=True) or {}
    apply_points = bool(data.get("applyPoints")) and user_id is not None

    if user_id is None:
        cur.execute(
            """
            SELECT ci.*, p.name, p.price
            FROM cart_items ci
            JOIN products p ON p.id = ci.product_id
            WHERE ci.user_id IS NULL
            """
        )
    else:
        cur.execute(
            """
            SELECT ci.*, p.name, p.price
            FROM cart_items ci
            JOIN products p ON p.id = ci.product_id
            WHERE ci.user_id = %s
            """,
            (user_id,),
        )
    items = cur.fetchall()

    if not items:
        cur.close(); db.close()
        return jsonify({"message": "Cart is empty"}), 400

    # Insert unpaid orders so they appear immediately if payment is abandoned
    for it in items:
        r = cast(Dict[str, Any], it)
        cur.execute(
            """
            INSERT INTO orders (user_id, product_id, quantity, status)
            VALUES (%s, %s, %s, 'unpaid')
            """,
            (user_id, int(r["product_id"]), int(r["quantity"])),
        )
    db.commit()

    line_items = _build_line_items(items)

    # Loyalty points discount
    discounts_param = None
    points_used = 0
    if apply_points:
        cur.execute("SELECT points FROM users WHERE id=%s", (user_id,))
        row = cast(Dict[str, Any] | None, cur.fetchone())
        if row and row["points"]:
            available_pts = int(row["points"])
            # $1 discount per 100 pts
            discount_cents = (available_pts // 100) * 100  # in cents
            if discount_cents > 0:
                # Make sure discount doesn't exceed cart total
                total_cents = sum(int(float(i["price"])*100)*int(i["quantity"]) for i in items)
                discount_cents = min(discount_cents, total_cents)
                if discount_cents > 0:
                    coupon = stripe.Coupon.create(amount_off=discount_cents, currency="usd", duration="once")
                    discounts_param = [{"coupon": coupon.id}]
                    points_used = (discount_cents // 100) * 100  # back to points (1$=100pts)
    # Metadata lets us associate the session (and later, the payment) back to a user
    metadata: Dict[str, str] = {}
    # Promo code discount
    promo_code = data.get("promoCode") if data else None
    if promo_code:
        cur.execute(
            """
            SELECT id, amount_off_cents, percent_off, type,
                   active, max_redemptions, times_redeemed
            FROM promo_codes
            WHERE code=%s
            """,
            (promo_code,)
        )
        pr = cast(Dict[str, Any] | None, cur.fetchone())

        if pr and pr["active"] and (
            pr["max_redemptions"] is None or
            pr["times_redeemed"] < pr["max_redemptions"]
        ):
            # ---------- create a Stripe coupon ----------
            if pr["type"] == "amount":
                coupon = stripe.Coupon.create(
                    amount_off = pr["amount_off_cents"],
                    currency   = "usd",
                    duration   = "once",
                )
            else:  # percent
                coupon = stripe.Coupon.create(
                    percent_off = pr["percent_off"],
                    duration    = "once",
                )
            # --------------------------------------------

            if discounts_param is None:
                discounts_param = []
            discounts_param.append({"coupon": coupon.id})

            metadata["promo_id"]   = str(pr["id"]) if user_id else "guest"
            metadata["promo_code"] = promo_code

    if user_id:
        metadata["user_id"] = str(user_id)
        metadata["points_used"] = str(points_used)

    try:
        session = stripe.checkout.Session.create(  # type: ignore[arg-type]
            # Support cards (includes Apple Pay when domain-verified), PayPal, and WeChat Pay
            payment_method_types=["card", "wechat_pay"],
            # Disable Link/Shop Pay so it doesn’t show up alongside Apple Pay
            payment_method_options=cast(Any, {
                # Required option for web WeChat Pay
                "wechat_pay": {"client": "web"},
            }),
            mode="payment",
            line_items=line_items,
            success_url=os.getenv("FRONTEND_URL", "http://localhost:5173")
            + "/orders?success=true",
            cancel_url=os.getenv("FRONTEND_URL", "http://localhost:5173")
            + "/cart?canceled=true",
            metadata=metadata,
            discounts=discounts_param,
        )
    except Exception as e:
        cur.close(); db.close()
        return jsonify({"message": "Stripe error", "detail": str(e)}), 500

    cur.close(); db.close()
    # Stripe-hosted Checkout page URL – frontend simply redirects the browser
    return jsonify({"url": session.url}), 200


@payments_bp.route("/webhook", methods=["POST"])
def stripe_webhook():
    """Stripe webhook to finalise orders once payment succeeds."""
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
    except (ValueError, stripe.error.SignatureVerificationError):  # type: ignore[attr-defined]
        # Invalid payload or signature
        return "", 400

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        meta = session.get("metadata", {})
        user_id     = meta.get("user_id")
        points_used = int(meta.get("points_used", "0"))      # <- from metadata
        promo_id    = meta.get("promo_id")

        # Retrieve the line items so we know what was purchased
        line_items = stripe.checkout.Session.list_line_items(session["id"])

        db = get_db_connection()
        cur = db.cursor()

        for li in line_items:
            product_name = li["description"]
            quantity = li["quantity"]
            cur.execute("SELECT id, price FROM products WHERE name=%s", (product_name,))
            product = cur.fetchone()
            if not product:
                continue  # skip items we cannot map back

            cur.execute(
                """
                INSERT INTO orders (user_id, product_id, quantity, status)
                VALUES (%s, %s, %s, 'PAID')
                """,
                (user_id, product["id"], quantity),  # type: ignore[arg-type]
            )

        # Deduct points if used
        if user_id and points_used:
            cur.execute("UPDATE users SET points = points - %s WHERE id = %s", (points_used, user_id))

        # Clear this user's cart after successful payment
        if user_id is None:
            cur.execute("DELETE FROM cart_items WHERE user_id IS NULL")
        else:
            cur.execute("DELETE FROM cart_items WHERE user_id = %s", (user_id,))
        db.commit()

        # Back-end redemption counter
        if promo_id and promo_id.isdigit():
            cur.execute(
                "UPDATE promo_codes SET times_redeemed = times_redeemed + 1 WHERE id=%s",
                (promo_id,)
            )
        cur.close(); db.close()

    # Return 200 to acknowledge receipt of the event
    return "", 200 

# server/app/routes/promos.py
@payments_bp.route('/validate-code', methods=['POST'])
def validate_code():
    code = request.get_json().get('code', '').strip()
    db = get_db_connection()
    cur = db.cursor()
    cur.execute("""
        SELECT amount_off_cents, percent_off, type
        FROM promo_codes
        WHERE code=%s AND active=1
          AND (max_redemptions IS NULL OR times_redeemed < max_redemptions)
    """, (code,))
    row = cast(Dict[str, Any] | None, cur.fetchone())
    if not row:
        cur.close(); 
        db.close()
        return jsonify({"valid": False}), 200
    cur.close(); 
    db.close()
    return jsonify({
        "valid": True,
        "type": row["type"],
        "amount_off": row["amount_off_cents"] / 100,
        "percent_off": row["percent_off"],
    }), 200