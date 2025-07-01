import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import ProductList from './components/ProductList';
// Add more as you build them
// import CartPage from './components/CartPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<ProductList />} />
        {/* <Route path="/cart" element={<CartPage />} /> */}
      </Routes>
    </Router>
  );
}

export default App;
