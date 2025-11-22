import React from 'react';
import ProductList from '../components/ProductList';

const Home = () => {
  return (
    <section className="py-10 lg:py-16">
      <div className="max-w-6xl mx-auto px-4 lg:px-8">
        <div className="text-center space-y-3 mb-10">
          <p className="text-sm uppercase tracking-[0.35em] text-pink-500">Sweet new styles</p>
          <h1 className="text-4xl md:text-5xl font-display font-semibold text-gray-900">Our Products</h1>
          <p className="text-sm md:text-base text-gray-600 max-w-2xl mx-auto">
            Discover vivid color stories, salon-quality finishes, and limited-edition collections crafted to make every day feel like a treat.
          </p>
        </div>
        <ProductList />
      </div>
    </section>
  );
};

export default Home;
