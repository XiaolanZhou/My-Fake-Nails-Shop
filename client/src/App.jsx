import React from 'react';
import ProductList from './components/ProductList';
import CartPage from './components/CartPage';
import Navbar from './Navbar';
import { Routes, Route } from 'react-router-dom';

const App = () => (
  <>
    <Navbar />
    <Routes>
      <Route path="/" element={<ProductList />} />
      <Route path="/cart" element={<CartPage />} />
    </Routes>
  </>
);

export default App;
