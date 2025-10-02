'use client'

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react'
import { apiClient } from '@/services/api'

interface User {
  id: number
  email: string
  name: string
  company?: string
}

interface AuthContextType {
  user: User | null
  login: (email: string, password: string) => Promise<void>
  register: (userData: RegisterData) => Promise<void>
  logout: () => void
  loading: boolean
}

interface RegisterData {
  name: string
  email: string
  password: string
  company?: string
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

interface AuthProviderProps {
  children: ReactNode
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is already logged in
    checkAuthStatus()
  }, [])

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('authToken')
      if (!token) {
        setLoading(false)
        return
      }

      // For demo purposes, we'll use a mock user
      // In a real app, you'd verify the token with your backend
      const mockUser: User = {
        id: 1,
        email: 'demo@hydroai.com',
        name: 'Demo User',
        company: 'HydroAI Demo Farm'
      }
      
      setUser(mockUser)
    } catch (error) {
      console.error('Auth check failed:', error)
      localStorage.removeItem('authToken')
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    try {
      // Demo login - in a real app, you'd call your authentication API
      if (email === 'demo@hydroai.com' && password === 'demo123') {
        const mockUser: User = {
          id: 1,
          email: 'demo@hydroai.com',
          name: 'Demo User',
          company: 'HydroAI Demo Farm'
        }
        
        // Store a demo token
        localStorage.setItem('authToken', 'demo-token-12345')
        setUser(mockUser)
        return
      }

      // For other credentials, attempt actual API call
      const response = await apiClient.post('/auth/login', {
        email,
        password
      })

      const { user, token } = response.data
      localStorage.setItem('authToken', token)
      setUser(user)
    } catch (error: any) {
      // If API fails, throw error for UI to handle
      const errorMessage = error.response?.data?.message || 'Login failed'
      throw new Error(errorMessage)
    }
  }

  const register = async (userData: RegisterData) => {
    try {
      const response = await apiClient.post('/auth/register', userData)
      const { user, token } = response.data
      localStorage.setItem('authToken', token)
      setUser(user)
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Registration failed'
      throw new Error(errorMessage)
    }
  }

  const logout = () => {
    localStorage.removeItem('authToken')
    setUser(null)
    // Redirect to login page
    window.location.href = '/auth/login'
  }

  const value: AuthContextType = {
    user,
    login,
    register,
    logout,
    loading
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}
