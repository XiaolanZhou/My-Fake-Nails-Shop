import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
// ← new imports:
import { ShoppingCart, User } from 'lucide-react';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="p-4 bg-pink-200 shadow mb-4 flex gap-4 items-center">
      {/* Brand name */}
      <Link to="/" className="text-pink-700 font-bold text-2xl">
        PHEW
      </Link>



      {/* Cart with icon */}
      <Link
        to="/cart"
        className="flex items-center text-pink-700 font-bold gap-1"
      >
        <ShoppingCart size={18} /> 
        <span>Cart</span>
      </Link>

      {/* Other links */}
      <Link to="/orders"   className="text-pink-700 font-bold">Orders</Link>

      {/* Free-shipping banner */}
      <div className="bg-pink-500 text-white text-center py-2 px-4">
        <div className="flex items-center justify-center gap-2">
          <span className="text-xs">★</span>
          <span className="text-sm font-medium">
            FREE SHIPPING ON USA ORDERS OVER $30+
          </span>
          <span className="text-xs">★</span>
        </div>
      </div>

      {/* Auth controls */}
      <div className="ml-auto flex gap-3 items-center">
        {isAuthenticated ? (
          <>
            <span className="text-sm text-gray-700">
              Hi, {user?.username || 'User'} ({user?.points ?? 0} pts)
            </span>
            <button
              onClick={handleLogout}
              className="text-sm text-red-600 hover:underline"
            >
              Logout
            </button>
          </>
        ) : (
          <Link
            to="/login"
            className="flex items-center text-pink-700 font-bold gap-1"
          >
            <User size={18} />
            <span>Login</span>
          </Link>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
