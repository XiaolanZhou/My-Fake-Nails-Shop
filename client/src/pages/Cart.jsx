import React, { useEffect, useState } from 'react';
import { Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        fetch('http://localhost:5001/api/cart/')
            .then(res => res.json())
            .then(data => setCartItems(data))
            .catch(err => console.error('Error fetching cart:', err));
    }, []);

    const handleRemove = (cartItemId) => {
        fetch(`http://localhost:5001/api/cart/remove/${cartItemId}`, { method: 'DELETE' })
            .then(() =>
                setCartItems(items => items.filter(item => item.cart_item_id !== cartItemId))
            )
            .catch(err => console.error('Error removing item:', err));
    };

    const updateQuantity = (cartItemId, type) => {
        const route = type === 'increase' ? 'increase' : 'decrease';
        fetch(`http://localhost:5001/api/cart/${route}/${cartItemId}`, { method: 'PATCH' })
            .then(res => {
                if (res.ok) return res.json();
                // if we tried to decrease below 1, fall back to remove
                if (!res.ok && type === 'decrease') {
                    return fetch(`http://localhost:5001/api/cart/remove/${cartItemId}`, {
                        method: 'DELETE',
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

    const handleCheckout = () => {
        fetch('http://localhost:5001/api/cart/checkout', { method: 'POST' })
            .then(res => res.json())
            .then(({ message }) => {
                alert(message);
                setCartItems([]);
                navigate('/orders');
            })
            .catch(err => console.error('Checkout failed:', err));
    };

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
                    <div className="mt-4 font-bold text-lg">
                        Total: ${total.toFixed(2)}
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
