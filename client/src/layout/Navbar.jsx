import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="p-4 bg-pink-200 shadow mb-4 flex gap-4 items-center">
      <Link to="/" className="text-pink-700 font-bold">Home</Link>
      <Link to="/cart" className="text-pink-700 font-bold">Cart</Link>
      <Link to="/orders" className="text-pink-700 font-bold">Orders</Link>

      <div className="ml-auto flex gap-3 items-center">
        {isAuthenticated ? (
          <>
            <span className="text-sm text-gray-700">Hi, {user?.username || 'User'} ({user?.points ?? 0} pts)</span>
            <button onClick={handleLogout} className="text-sm text-red-600 hover:underline">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" className="text-pink-700 font-bold">Login</Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
