import { Link } from 'react-router-dom';

const Navbar = () => (
  <nav className="p-4 bg-pink-200 shadow mb-4 flex gap-4">
    <Link to="/" className="text-pink-700 font-bold">Home</Link>
    <Link to="/cart" className="text-pink-700 font-bold">Cart</Link>
  </nav>
);

export default Navbar;
