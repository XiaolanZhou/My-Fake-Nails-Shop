import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './layout/Navbar';
import Footer from './layout/Footer';
import Home from './pages/Home';
import Cart from './pages/Cart';

const App = () => (
  <div className="flex flex-col min-h-screen">
    <Navbar />
    <main className="flex-grow">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/cart" element={<Cart />} />
      </Routes>
    </main>
    <Footer />
  </div>
);

export default App;
