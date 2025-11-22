import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer';
import Home from './pages/Home';
import Cart from './pages/Cart';
import OrdersPage from './pages/Orders';
import ProductDetails from './components/ProductDetails';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import PetalCanvas from './components/PetalCanvas';


const App = () => (
  <div className="flex flex-col min-h-screen">
    <Navbar />
    <PetalCanvas />
    <main className="flex justify-center">
      <div className="w-full max-w-[1200px] px-4">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<Cart />} />
        <Route path="/orders" element={<OrdersPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/products/:id" element={<ProductDetails />} />
      </Routes>
      </div>
    </main>
    <Footer />
  </div>
);

export default App;
