import React from 'react';
import ProductList from '../components/ProductList';

const Home = () => {
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Our Products</h1>
      <ProductList />
    </div>
  );
};

export default Home;
