// ProductList.jsx
import React, { useEffect, useState } from 'react'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import ProductCard from './ProductCard'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProductList() {
  const [products, setProducts] = useState([])
  const { token } = useAuth()

  useEffect(() => {
    fetch('http://localhost:5001/api/products')
      .then(r => r.json())
      .then(setProducts)
      .catch(console.error)
  }, [])

  const handleAdd = product => {
    fetch('http://localhost:5001/api/cart/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
      body: JSON.stringify(product),
    })
      .then(r => r.json())
      .then(({ message }) => toast.success(message, { autoClose: 2000 }))
      .catch(() => toast.error('Could not add to cart'))
  }

  return (
    <>
      <div className="px-4">
        {/* 4 columns of fixed width 16rem, centered */}
        <div
          className="grid gap-6 justify-center"
          style={{ gridTemplateColumns: 'repeat(4,16rem)' }}
        >
          {products.map(p => (
            <div key={p.id} className="w-64">
              <ProductCard product={p} onAddToCart={handleAdd} />
            </div>
          ))}
        </div>
      </div>
      <ToastContainer />
    </>
  )
}
