import React, { useEffect, useState } from 'react';
import { Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const { token, user } = useAuth();
    const [applyPoints, setApplyPoints] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        fetch('http://localhost:5001/api/cart/', {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
        })
            .then(res => res.json())
            .then(data => setCartItems(data))
            .catch(err => console.error('Error fetching cart:', err));
    }, [token]);

    const handleRemove = (cartItemId) => {
        fetch(`http://localhost:5001/api/cart/remove/${cartItemId}`, {
            method: 'DELETE',
            headers: token ? { Authorization: `Bearer ${token}` } : {},
        })
            .then(() =>
                setCartItems(items => items.filter(item => item.cart_item_id !== cartItemId))
            )
            .catch(err => console.error('Error removing item:', err));
    };

    const updateQuantity = (cartItemId, type) => {
        const route = type === 'increase' ? 'increase' : 'decrease';
        fetch(`http://localhost:5001/api/cart/${route}/${cartItemId}`, {
            method: 'PATCH',
            headers: token ? { Authorization: `Bearer ${token}` } : {},
        })
            .then(res => {
                if (res.ok) return res.json();
                if (!res.ok && type === 'decrease') {
                    return fetch(`http://localhost:5001/api/cart/remove/${cartItemId}`, {
                        method: 'DELETE',
                        headers: token ? { Authorization: `Bearer ${token}` } : {},
                    }).then(() => ({ removed: true }));
                }
                throw new Error('Quantity update failed');
            })
            .then(({ removed }) => {
                setCartItems(items =>
                    items
                        .map(item => {
                            if (item.cart_item_id !== cartItemId) return item;
                            if (removed) return null; // will be filtered out
                            const newQty =
                                type === 'increase'
                                    ? item.quantity + 1
                                    : Math.max(item.quantity - 1, 0);
                            return { ...item, quantity: newQty };
                        })
                        .filter(Boolean)
                );
            })
            .catch(err => console.error(err));
    };

    const handleDecreaseOrRemove = (item) => {
        if (item.quantity > 1) {
            updateQuantity(item.cart_item_id, 'decrease');
        } else {
            handleRemove(item.cart_item_id);
        }
    };

    const total = cartItems.reduce(
        (sum, item) => sum + parseFloat(item.price) * item.quantity,
        0
    );

    const pointsAvailable = user?.points ?? 0;        // 10 pts per $1 earned
    const pointsDollarValue = (pointsAvailable / 100); // $1 off per 100 pts
    const discount = applyPoints ? Math.min(pointsDollarValue, total) : 0;
    const grandTotal = (total - discount).toFixed(2);

    const handleCheckout = () => {
        fetch('http://localhost:5001/api/payments/create-checkout-session', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(token ? { Authorization: `Bearer ${token}` } : {}),
            },
            body: JSON.stringify({ applyPoints }),
        })
            .then(res => res.json())
            .then(({ url }) => {
                if (!url) throw new Error('Unable to initiate payment')
                window.location.href = url // Redirect browser to Stripe Checkout
            })
            .catch(err => console.error('Checkout failed:', err))
    }

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Your Cart</h1>
            {cartItems.length === 0 ? (
                <p>Your cart is empty.</p>
            ) : (
                cartItems.map(item => (
                    <div key={item.cart_item_id} className="border p-3 mb-2 rounded">
                        <h2 className="font-semibold">{item.name}</h2>
                        <p>{item.description}</p>
                        <div className="flex gap-2 items-center mt-2">
                            <button
                                onClick={() => handleDecreaseOrRemove(item)}
                                className="p-1 rounded hover:bg-gray-200"
                            >
                                {item.quantity > 1 ? (
                                    <span className="text-xl">−</span>
                                ) : (
                                    <Trash2 size={16} />
                                )}
                            </button>
                            <span>{item.quantity}</span>
                            <button
                                onClick={() => updateQuantity(item.cart_item_id, 'increase')}
                                className="p-1 rounded hover:bg-gray-200"
                            >
                                +
                            </button>
                        </div>
                        <p className="mt-1">
                            ${(parseFloat(item.price) * item.quantity).toFixed(2)}
                        </p>
                        <button
                            onClick={() => handleRemove(item.cart_item_id)}
                            className="mt-1 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                        >
                            Remove
                        </button>
                    </div>
                ))
            )}
            {cartItems.length > 0 && (
                <>
                    {token && (
                        <div className="mt-2">
                            <label className="inline-flex items-center gap-2">
                                <input
                                  type="checkbox"
                                  className="form-checkbox"
                                  checked={applyPoints}
                                  onChange={e => setApplyPoints(e.target.checked)}
                                />
                                Apply my points
                            </label>
                        </div>
                    )}
                    <div className="mt-4">
                      {applyPoints && discount > 0 ? (
                        <>
                          <span className="text-gray-500 line-through mr-2 text-lg">
                            ${total.toFixed(2)}
                          </span>
                          <span className="text-4xl font-bold text-red-600">
                            ${grandTotal}
                          </span>
                        </>
                      ) : (
                        <span className="text-lg font-bold">${total.toFixed(2)}</span>
                      )}
                    </div>
                    <button
                        onClick={handleCheckout}
                        className="mt-2 bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                    >
                        Checkout
                    </button>
                </>
            )}

        </div>
    );
};

export default CartPage;
