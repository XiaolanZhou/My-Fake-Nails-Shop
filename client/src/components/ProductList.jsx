import React, { useEffect, useState } from 'react';
import ProductCard from './ProductCard';

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/api/products') // Flask runs on 5000
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(err => console.error('Error fetching products:', err));
  }, []);

  return (
    <div className="grid grid-cols-2 gap-4 p-4">
      {products.map(product => (
        <ProductCard key={product.id} product={product} onAddToCart={handleAddToCart} />
      ))}
    </div>
  );


  function handleAddToCart(product) {
    fetch('http://localhost:5000/api/cart/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    })
      .then(res => res.json())
      .then(data => alert(data.message))
      .catch(err => console.error('Add to cart failed:', err));
  }
};

export default ProductList;
