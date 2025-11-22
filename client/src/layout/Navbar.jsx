import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import { ShoppingBag, User, Search } from 'lucide-react';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <>
      <div className="bg-pink-500 text-white text-xs md:text-sm tracking-wide text-center py-2">
        ★ FREE SHIPPING ON USA ORDERS OVER $30 ★
      </div>

      <nav className="bg-white/90 backdrop-blur border-b border-pink-100 shadow-sm">
        <div className="max-w-6xl mx-auto px-4 lg:px-8 h-16 flex items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <Link to="/" className="text-2xl font-display font-semibold text-pink-700 tracking-wider">
              PHEW
            </Link>
            <Link
              to="/orders"
              className="inline-flex items-center gap-1 text-sm font-medium text-pink-600 hover:text-pink-700 transition"
            >
              Orders
            </Link>
            <Link
              to="/cart"
              className="inline-flex items-center gap-2 rounded-full border border-pink-200 px-4 py-2 text-sm font-medium text-pink-600 hover:border-pink-400 hover:text-pink-700 transition"
            >
              <ShoppingBag size={16} />
              Cart
            </Link>
          </div>

          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-700">
            <Link to="/" className="hover:text-pink-600 transition">Best Sellers</Link>
            <Link to="/" className="hover:text-pink-600 transition">All Nails</Link>
            <Link to="/" className="hover:text-pink-600 transition">Bundle &amp; Save</Link>
            <Link to="/" className="hover:text-pink-600 transition">Tutorials</Link>
            <Link to="/" className="hover:text-pink-600 transition">About</Link>
          </div>

          <div className="flex items-center gap-4 text-gray-700">
            <button className="hidden sm:inline-flex items-center justify-center w-9 h-9 rounded-full border border-pink-100 shadow-sm hover:text-pink-600 hover:border-pink-300 transition">
              <Search size={18} />
            </button>

            {isAuthenticated ? (
              <div className="flex flex-col items-end leading-tight">
                <span className="text-xs text-gray-500">Hi, {user?.username || 'User'}</span>
                <span className="text-xs text-gray-500">{user?.points ?? 0} pts</span>
                <button onClick={handleLogout} className="text-xs text-pink-600 hover:underline">
                  Logout
                </button>
              </div>
            ) : (
              <Link to="/login" className="inline-flex items-center gap-1 text-sm font-medium text-gray-700 hover:text-pink-600 transition">
                <User size={18} />
                Login
              </Link>
            )}
          </div>
        </div>
      </nav>
    </>
  );
};

export default Navbar;
