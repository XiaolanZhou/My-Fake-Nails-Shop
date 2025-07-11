import React, { useEffect, useState } from 'react';

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/orders')
      .then(res => res.json())
      .then(data => setOrders(data))
      .catch(err => console.error('Error fetching orders:', err));
  }, []);

  if (orders.length === 0) {
    return (
      <div className="p-4">
        <h1 className="text-2xl font-bold mb-4">Your Orders</h1>
        <p>You haven’t placed any orders yet.</p>
      </div>
    );
  }

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Your Orders</h1>
      <ul className="space-y-6">
        {orders.map(o => (
          <li key={o.order_item_id} className="border p-4 rounded flex gap-4">
            {/* product image */}
            <img src={o.image_url}
                 alt={o.name}
                 className="w-20 h-20 object-cover rounded"
            />

            <div>
              <p className="font-semibold">{o.name}</p>
              <p className="text-sm text-gray-600">
                {new Date(o.created_at).toLocaleString()}
              </p>
              <p>Quantity: {o.quantity}</p>
              <p className="font-bold">${parseFloat(o.price).toFixed(2)}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default OrdersPage;
