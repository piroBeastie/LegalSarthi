import React, { createContext, useState, useEffect, useContext } from 'react';
import client from '../api/client';
import toast from 'react-hot-toast';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem('legalsarthi_token');
      const storedUser = localStorage.getItem('legalsarthi_user');

      if (token && storedUser) {
        setUser(JSON.parse(storedUser));
        try {
          const res = await client.get('/auth/me');
          setUser(res.data);
          localStorage.setItem('legalsarthi_user', JSON.stringify(res.data));
        } catch (error) {
          console.error("Auth init failed:", error);
          localStorage.removeItem('legalsarthi_token');
          localStorage.removeItem('legalsarthi_user');
          setUser(null);
        }
      }
      setLoading(false);
    };

    initAuth();
  }, []);

  const login = async (email, password) => {
    try {
      const res = await client.post('/auth/login', { email, password });
      const { access_token, user } = res.data;
      localStorage.setItem('legalsarthi_token', access_token);
      localStorage.setItem('legalsarthi_user', JSON.stringify(user));
      setUser(user);
      toast.success('Logged in successfully!');
      return true;
    } catch (error) {
      toast.error(error.response?.data?.detail || 'Login failed');
      return false;
    }
  };

  const register = async (name, email, password) => {
    try {
      const res = await client.post('/auth/register', { name, email, password });
      const { access_token, user } = res.data;
      localStorage.setItem('legalsarthi_token', access_token);
      localStorage.setItem('legalsarthi_user', JSON.stringify(user));
      setUser(user);
      toast.success('Registered successfully!');
      return true;
    } catch (error) {
      const errorDetail = error.response?.data?.detail;
      if (Array.isArray(errorDetail)) {
         toast.error(errorDetail[0]?.msg || 'Registration failed');
      } else {
         toast.error(errorDetail || 'Registration failed');
      }
      return false;
    }
  };

  const logout = () => {
    localStorage.removeItem('legalsarthi_token');
    localStorage.removeItem('legalsarthi_user');
    setUser(null);
    toast.success('Logged out successfully');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
