import React, { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext.jsx'
import { useNavigate } from 'react-router-dom'
import { api } from '../config/api'

const TABS = ['All Orders', 'Unpaid', 'Processing', 'Shipped', 'Review']

function classNames(...classes) {
  return classes.filter(Boolean).join(' ')
}

export default function OrdersPage() {
  const [orders, setOrders] = useState([])
  const { isAuthenticated, token } = useAuth()
  const navigate = useNavigate()
  const [selectedTab, setSelectedTab] = useState(TABS[0])

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login')
      return
    }
    fetch(api('/api/orders'), {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((res) => res.json())
      .then((data) => setOrders(data))
      .catch((err) => console.error('Error fetching orders:', err))
  }, [])

  function filterByTab(tab) {
    if (tab === 'All Orders') return orders
    return orders.filter((o) => o.status === tab.toLowerCase())
  }

  const filteredOrders = filterByTab(selectedTab)

  return (
    <div className="p-4">
      <h1 className="text-3xl font-bold mb-6">Your Orders</h1>

      {/* Tab Navigation */}
      <div className="flex space-x-4 border-b pb-2 mb-6">
        {TABS.map((tab) => (
          <button
            key={tab}
            onClick={() => setSelectedTab(tab)}
            className={classNames(
              'px-4 py-2 text-sm font-medium transition-colors',
              selectedTab === tab
                ? 'border-b-2 border-pink-600 text-pink-600'
                : 'text-gray-600 hover:text-gray-800'
            )}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Orders Content */}
      <div className="space-y-6">
        {filteredOrders.length === 0 ? (
          <p className="text-gray-500">No orders in "{selectedTab}"</p>
        ) : (
          filteredOrders.map(order => (
            <div key={order.order_id} className="border rounded-lg p-4 space-y-2 shadow bg-white">
              <div className="flex justify-between items-center">
                <div className="font-semibold text-sm">Order: {order.order_id}</div>
                <div className="capitalize text-sm font-semibold text-green-600">{order.status}</div>
              </div>
              <div className="text-xs text-gray-500">
                {new Date(order.created_at).toLocaleString('en-US', { timeZone: 'America/New_York' })} EDT
              </div>

              {/* Image Row */}
              <div
                onClick={() => window.location.href = `/orders/${order.order_id}`}
                className="flex space-x-2 overflow-x-auto cursor-pointer p-2 border rounded-md"
              >
                {order.items.map(item => (
                  <div key={item.id} className="relative w-20 flex-shrink-0">
                    <img
                      src={item.image_url}
                      alt={item.name}
                      className="w-20 h-20 object-cover rounded-md"
                    />
                    <div className="absolute bottom-1 right-1 text-xs bg-black text-white rounded px-1">
                      x{item.quantity}
                    </div>
                  </div>
                ))}
              </div>

              {/* Footer Row */}
              <div className="flex justify-between items-center text-sm mt-2">
                <div>Item(s): {order.items.reduce((sum, i) => sum + i.quantity, 0)}</div>
                <div className="font-bold">Total: ${order.total.toFixed(2)}</div>
              </div>

              <div className="flex space-x-2 pt-2">
                <button className="flex-1 px-3 py-2 border rounded text-sm">Customer Service</button>
                <button className="flex-1 px-3 py-2 border rounded text-white bg-red-500 hover:bg-red-600 text-sm">Track</button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}
