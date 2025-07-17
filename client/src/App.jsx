import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer';
import Home from './pages/Home';
import Cart from './pages/Cart';
import OrdersPage from './pages/Orders';
import ProductDetails from './components/ProductDetails';


const App = () => (
  <div className="flex flex-col min-h-screen">
    <Navbar />
    <main className="flex-grow">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/products/:id" element={<ProductDetails />} />
      </Routes>
    </main>
    <Footer />
  </div>
);

export default App;
