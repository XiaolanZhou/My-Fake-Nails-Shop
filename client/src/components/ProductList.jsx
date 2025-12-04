// ProductList.jsx
import React, { useEffect, useState, useCallback } from 'react'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import ProductCard from './ProductCard'
import { useAuth } from '../context/AuthContext.jsx'
import { api } from '../config/api'

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

    fetch(api(`/api/products?${params.toString()}`))
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
    fetch(api('/api/cart/add'), {
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
      <div className="space-y-10">
        {/* Search / filter form */}
        <form
          onSubmit={handleSearchSubmit}
          className="bg-white/80 backdrop-blur border border-pink-100 rounded-3xl shadow-sm px-5 py-6 flex flex-wrap items-end gap-4"
        >
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium uppercase text-gray-500 tracking-wide">Search</label>
            <input
              type="text"
              value={q}
              onChange={e => setQ(e.target.value)}
              className="border border-pink-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-200"
              placeholder="keywords"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium uppercase text-gray-500 tracking-wide">Sort by</label>
            <select
              value={sort}
              onChange={e => { setSort(e.target.value); setPage(1); }}
              className="border border-pink-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-200"
            >
              <option value="">Default</option>
              <option value="rating">Rating</option>
              <option value="price_asc">Price: Low to High</option>
              <option value="price_desc">Price: High to Low</option>
            </select>
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium uppercase text-gray-500 tracking-wide">Min price</label>
            <input
              type="number"
              step="0.01"
              value={priceMin}
              onChange={e => setPriceMin(e.target.value)}
              className="border border-pink-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-200"
            />
          </div>
          <div className="flex flex-col gap-1">
            <label className="text-xs font-medium uppercase text-gray-500 tracking-wide">Max price</label>
            <input
              type="number"
              step="0.01"
              value={priceMax}
              onChange={e => setPriceMax(e.target.value)}
              className="border border-pink-100 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-200"
            />
          </div>
          <button
            className="ml-auto inline-flex items-center gap-2 rounded-full bg-pink-500 px-5 py-2 text-sm font-semibold text-white shadow hover:bg-pink-600 transition"
            type="submit"
          >
            Apply
          </button>
        </form>

        {/* Product grid */}
        <div className="grid gap-10 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 justify-items-center">
          {products.map(p => (
            <ProductCard key={p.id} product={p} onAddToCart={handleAdd} />
          ))}
        </div>

        {/* Pagination */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-center gap-4 mt-4 text-sm">
          <button
            className="px-4 py-2 border border-pink-200 rounded-full disabled:opacity-40 disabled:cursor-not-allowed hover:border-pink-400 transition"
            disabled={page <= 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
          >
            Previous
          </button>
          <span className="font-medium text-gray-600">
            Page {page} of {totalPages}
          </span>
          <button
            className="px-4 py-2 border border-pink-200 rounded-full disabled:opacity-40 disabled:cursor-not-allowed hover:border-pink-400 transition"
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
