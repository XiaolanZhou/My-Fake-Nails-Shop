import React, { useEffect, useState } from 'react';
import ProductCard from './ProductCard';
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

const ProductList = () => {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5001/api/products')
      .then(res => res.json())
      .then(data => {
        console.log('fetched products:', data);
        setProducts(data)
      })
      .catch(err => console.error('Error fetching products:', err));
  }, []);

  const handleAddToCart = (product) => {
    fetch('http://localhost:5001/api/cart/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product),
    })
      .then(res => res.json())
      .then(data => {
        toast.success(data.message, {
          position: 'top-right',
          autoClose: 2000,
          hideProgressBar: true,
          pauseOnHover: false,
        })
      })
      .catch(err => {
        console.error(err)
        toast.error('Could not add to cart')
      })
  };

  return (
    <>
      <div className="grid grid-cols-2 gap-4 p-4">
        {products.map(product => (
          <ProductCard
            key={product.id}
            product={product}
            onAddToCart={handleAddToCart}
          />
        ))}
      </div>
      {/* this renders the container for all toasts */}
      <ToastContainer />
    </>
  );
};




export default ProductList;
