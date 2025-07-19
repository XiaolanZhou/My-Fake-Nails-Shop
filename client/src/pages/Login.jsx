// client/src/pages/Login.jsx
import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext.jsx'
import { ToastContainer, toast } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ identifier: '', password: '' })
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      await login(form.identifier, form.password)
      toast.success('Login successful', { autoClose: 1500 })
      navigate('/')
    } catch (err) {
      toast.error(err.message || 'Login failed', { autoClose: 2000 })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex justify-center items-center h-[80vh] p-4">
      <form onSubmit={handleSubmit} className="bg-white shadow p-6 rounded w-80 space-y-4">
        <h1 className="text-xl font-bold text-center">Login</h1>
        <input
          type="text"
          name="identifier"
          placeholder="Username or Email"
          value={form.identifier}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
          required
        />
        <input
          type="password"
          name="password"
          placeholder="Password"
          value={form.password}
          onChange={handleChange}
          className="w-full border px-3 py-2 rounded"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-pink-600 hover:bg-pink-700 text-white py-2 rounded font-semibold disabled:opacity-50"
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
        <p className="text-sm text-center">
          No account?{' '}
          <Link to="/register" className="text-pink-600 hover:underline">
            Register
          </Link>
        </p>
      </form>
      <ToastContainer />
    </div>
  )
} 