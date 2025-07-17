// ProductCard.jsx
import React from 'react'
import { Link } from 'react-router-dom'
import { ShoppingCart, Star, ChevronDown } from 'lucide-react'

export default function ProductCard({ product, onAddToCart }) {
  return (
    <div className="w-64 bg-white rounded-2xl shadow-md hover:shadow-lg transition relative overflow-hidden">
      {/* “Low Price” badge */}
      <div className="absolute top-2 left-2 bg-pink-50 text-pink-600 text-xs font-medium px-2 py-0.5 rounded-full flex items-center">
        Low Price <ChevronDown size={12} className="ml-1" />
      </div>

      {/* Image + cart button */}
      <div className="relative">
        <Link to={`/products/${product.id}`}>
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-40 object-cover rounded-t-2xl"
          />
        </Link>
      </div>

      {/* Content */}
      <div className="p-3 flex flex-col relative">
        {/* Title clickable too */}
        <Link
          to={`/products/${product.id}`}
          className="text-sm font-medium text-gray-900 line-clamp-2 hover:underline"
        >
          {product.name}
        </Link>

        {/* Rating */}
        <div className="mt-1 flex items-center text-xs">
          {[...Array(5)].map((_, i) => (
            <Star
              key={i}
              size={12}
              className={i < (product.rating || 0) ? 'text-yellow-500' : 'text-gray-300'}
            />
          ))}
        </div>

        {/* Price and Cart Button Row */}
        <div className="mt-2 flex items-center justify-between">
          <span className="text-lg font-bold text-red-600">
            ${parseFloat(product.price).toFixed(2)}
          </span>
          {product.originalPrice && (
            <span className="text-sm text-gray-400 line-through">
              ${parseFloat(product.originalPrice).toFixed(2)}
            </span>
          )}
          <button
            onClick={() => onAddToCart(product)}
            className="ml-2 bg-white p-2 rounded-full shadow hover:bg-gray-100 focus:outline-none"
          >
            <ShoppingCart size={16} className="text-gray-800" />
          </button>
        </div>
      </div>
    </div>
  )
}
