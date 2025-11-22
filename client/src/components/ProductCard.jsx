// ProductCard.jsx
import React from 'react'
import { Link } from 'react-router-dom'
import { ShoppingCart, Star } from 'lucide-react'

export default function ProductCard({ product, onAddToCart }) {
  const ratingValue = product.rating ? Number(product.rating).toFixed(1) : null
  const ratingCount = product.rating_count ?? 0

  return (
    <div className="w-full max-w-[260px] rounded-[28px] border border-pink-100 bg-white/80 backdrop-blur shadow-sm transition-transform duration-200 hover:-translate-y-1 hover:shadow-lg">
      <div className="relative">
        <Link to={`/products/${product.id}`} className="block overflow-hidden rounded-t-[28px]">
          <img
            src={product.image_url}
            alt={product.name}
            className="h-48 w-full object-cover transition-transform duration-300 group-hover:scale-105"
          />
        </Link>
      </div>

      <div className="p-4 flex flex-col gap-3">
        <Link
          to={`/products/${product.id}`}
          className="text-base font-semibold text-gray-900 hover:text-pink-600 transition"
        >
          {product.name}
        </Link>

        <div className="flex items-center gap-2 text-xs text-gray-500">
          <div className="flex items-center gap-1 text-yellow-400">
            {[...Array(5)].map((_, i) => (
              <Star key={i} size={12} fill={i < Math.round(product.rating || 0) ? 'currentColor' : 'none'} strokeWidth={1.5} className={i < Math.round(product.rating || 0) ? '' : 'text-gray-300'} />
            ))}
          </div>
          {ratingValue ? (
            <span>{ratingValue} • {ratingCount} reviews</span>
          ) : (
            <span>Be the first to review</span>
          )}
        </div>

        <div className="flex items-baseline justify-between">
          <span className="text-lg font-semibold text-pink-600">
            ${parseFloat(product.price).toFixed(2)}
          </span>
          {product.originalPrice && (
            <span className="text-sm text-gray-400 line-through">
              ${parseFloat(product.originalPrice).toFixed(2)}
            </span>
          )}
        </div>

        <button
          onClick={() => onAddToCart(product)}
          className="mt-2 inline-flex w-full items-center justify-center gap-2 rounded-full bg-pink-500 px-4 py-2 text-sm font-semibold text-white shadow hover:bg-pink-600 transition"
        >
          <ShoppingCart size={16} />
          Add to cart
        </button>
      </div>
    </div>
  )
}
