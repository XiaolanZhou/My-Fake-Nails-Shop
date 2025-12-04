// client/src/context/AuthContext.jsx
import React, { createContext, useContext, useState, useEffect, useCallback } from 'react'
import { api } from '../config/api'

const AuthContext = createContext({
  token: null,
  user: null,
  isAuthenticated: false,
  login: async (_u, _p) => {},
  logout: () => {},
})

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => localStorage.getItem('token'))
  const [user, setUser] = useState(null)

  const fetchUser = useCallback(async (tok) => {
    if (!tok) return setUser(null)
    try {
      const res = await fetch(api('/api/auth/me'), {
        headers: { Authorization: `Bearer ${tok}` },
      })
      if (res.ok) {
        const data = await res.json()
        setUser(data)
      } else {
        // token invalid
        logout()
      }
    } catch {
      logout()
    }
  }, [])

  useEffect(() => {
    if (token) {
      localStorage.setItem('token', token)
      fetchUser(token)
    } else {
      localStorage.removeItem('token')
    }
  }, [token, fetchUser])

  const login = async (identifier, password) => {
    const res = await fetch(api('/api/auth/login'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ identifier, password }),
    })
    if (!res.ok) {
      const { msg } = await res.json()
      throw new Error(msg || 'Login failed')
    }
    const { access_token } = await res.json()
    setToken(access_token)
    return access_token
  }

  const logout = () => {
    setToken(null)
    setUser(null)
    localStorage.removeItem('token')
  }

  return (
    <AuthContext.Provider
      value={{ token, user, isAuthenticated: !!token, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
