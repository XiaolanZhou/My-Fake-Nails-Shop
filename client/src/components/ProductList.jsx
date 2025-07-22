// ProductList.jsx
import React, { useEffect, useState, useCallback } from 'react'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import ProductCard from './ProductCard'
import { useAuth } from '../context/AuthContext.jsx'

export default function ProductList() {
  const [products, setProducts] = useState([])
  const { token } = useAuth()

  // search / filter / pagination state
  const [q, setQ] = useState('')
  const [priceMin, setPriceMin] = useState('')
  const [priceMax, setPriceMax] = useState('')
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [sort, setSort] = useState('')

  const fetchProducts = useCallback(() => {
    const params = new URLSearchParams()
    if (q) params.append('q', q)
    if (priceMin) params.append('price_min', priceMin)
    if (priceMax) params.append('price_max', priceMax)
    if (sort) params.append('sort', sort)
    params.append('page', page)
    params.append('per_page', 8)

    fetch(`http://localhost:5001/api/products?${params.toString()}`)
      .then(r => r.json())
      .then(data => {
        setProducts(data.items)
        setTotalPages(data.total_pages)
      })
      .catch(console.error)
  }, [q, priceMin, priceMax, page, sort])

  useEffect(() => {
    fetchProducts()
  }, [fetchProducts])

  const handleSearchSubmit = (e) => {
    e.preventDefault()
    setPage(1)
    fetchProducts()
  }

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
      <div className="px-4 max-w-6xl mx-auto">
        {/* Search / filter form */}
        <form onSubmit={handleSearchSubmit} className="flex flex-wrap gap-4 mb-6 items-end">
          <div>
            <label className="block text-sm font-medium mb-1">Search</label>
            <input
              type="text"
              value={q}
              onChange={e => setQ(e.target.value)}
              className="border px-2 py-1 rounded w-48"
              placeholder="keywords"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Sort by</label>
            <select
              value={sort}
              onChange={e => { setSort(e.target.value); setPage(1); }}
              className="border px-2 py-1 rounded"
            >
              <option value="">Default</option>
              <option value="rating">Rating</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Min price</label>
            <input
              type="number"
              step="0.01"
              value={priceMin}
              onChange={e => setPriceMin(e.target.value)}
              className="border px-2 py-1 rounded w-28"
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Max price</label>
            <input
              type="number"
              step="0.01"
              value={priceMax}
              onChange={e => setPriceMax(e.target.value)}
              className="border px-2 py-1 rounded w-28"
            />
          </div>
          <button className="bg-pink-600 text-white px-4 py-2 rounded hover:bg-pink-700" type="submit">
            Apply
          </button>
        </form>
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
        {/* Pagination */}
        <div className="flex justify-center gap-4 mt-6">
          <button
            className="px-3 py-1 border rounded disabled:opacity-50"
            disabled={page <= 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
          >
            Previous
          </button>
          <span className="self-center font-medium">
            Page {page} of {totalPages}
          </span>
          <button
            className="px-3 py-1 border rounded disabled:opacity-50"
            disabled={page >= totalPages}
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
          >
            Next
          </button>
        </div>
      </div>
      <ToastContainer />
    </>
  )
}
