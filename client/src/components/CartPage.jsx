import React, { useEffect, useState } from 'react';

const CartPage = () => {
    const [cartItems, setCartItems] = useState([]);

    useEffect(() => {
        fetch('http://localhost:5000/api/cart')
            .then(res => res.json())
            .then(data => setCartItems(data))
            .catch(err => console.error('Error fetching cart:', err));
    }, []);

    const handleRemove = (id) => {
        fetch(`http://localhost:5000/api/cart/remove/${id}`, {
            method: 'DELETE',
        })
            .then(() => setCartItems(cartItems.filter(item => item.id !== id)))
            .catch(err => console.error('Error removing item:', err));
    };

    const total = cartItems.reduce((sum, item) => sum + item.price * (item.quantity || 1), 0);

    const updateQuantity = (id, type) => {
        const route = type === 'increase' ? 'increase' : 'decrease';
        fetch(`http://localhost:5000/api/cart/${route}/${id}`, {
            method: 'PATCH',
        })
            .then(() => {
                setCartItems(prev =>
                    prev.map(item =>
                        item.id === id
                            ? { ...item, quantity: type === 'increase' ? item.quantity + 1 : Math.max(item.quantity - 1, 1) }
                            : item
                    )
                );
            })
            .catch(err => console.error('Quantity update failed:', err));
    };

    const handleCheckout = () => {
        fetch('http://localhost:5000/api/cart/checkout', {
            method: 'POST',
        })
            .then(res => res.json())
            .then(data => {
                alert(data.message);
                setCartItems([]); // clear cart on screen
            })
            .catch(err => console.error('Checkout failed:', err));
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Your Cart</h1>
            {cartItems.length === 0 ? (
                <p>Your cart is empty.</p>
            ) : (
                <>
                    {cartItems.map(item => (
                        <div key={item.id} className="border p-3 mb-2 rounded">
                            <h2 className="font-semibold">{item.name}</h2>
                            <p>{item.description}</p>
                            <div className="flex gap-2 items-center mt-2">
                                <button
                                    className="px-2 py-1 bg-gray-300 rounded hover:bg-gray-400"
                                    onClick={() => updateQuantity(item.id, 'decrease')}
                                >−</button>
                                <span>{item.quantity || 1}</span>
                                <button
                                    className="px-2 py-1 bg-gray-300 rounded hover:bg-gray-400"
                                    onClick={() => updateQuantity(item.id, 'increase')}
                                >+</button>
                            </div>
                            <p className="mt-1">${(item.price * (item.quantity || 1)).toFixed(2)}</p>
                            <button
                                onClick={() => handleRemove(item.id)}
                                className="mt-1 bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                            >
                                Remove
                            </button>
                        </div>


                    ))}
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
