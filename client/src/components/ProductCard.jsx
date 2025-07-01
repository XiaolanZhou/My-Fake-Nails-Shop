import React from 'react';

const ProductCard = ({ product, onAddToCart }) => (
  <div className="border rounded-xl p-4 shadow">
    <img src={product.image_url} alt={product.name} className="w-full h-48 object-cover mb-2 rounded" />
    <h2 className="text-lg font-bold">{product.name}</h2>
    <p className="text-sm text-gray-600">{product.description}</p>
    <p className="font-semibold text-pink-500">${product.price}</p>
    <button
      className="mt-2 bg-pink-600 text-white px-3 py-1 rounded hover:bg-pink-700"
      onClick={() => onAddToCart(product)}
    >
      Add to Cart
    </button>
  </div>
);

export default ProductCard;

