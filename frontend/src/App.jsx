import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/auth/ProtectedRoute';
import { useAuth } from './hooks/useAuth';

// Pages
import AuthPage from './pages/AuthPage';
import ChatPage from './pages/ChatPage';

const RootRoute = () => {
  const { user, loading } = useAuth();
  
  if (loading) return <div className="min-h-screen bg-primary flex items-center justify-center text-white">Loading...</div>;
  
  return user ? <Navigate to="/chat" /> : <AuthPage />;
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="w-full h-screen bg-background overflow-hidden flex flex-col">
          <main className="flex-1 flex flex-col overflow-hidden">
            <Routes>
              <Route path="/" element={<RootRoute />} />
              <Route element={<ProtectedRoute />}>
                <Route path="/chat" element={<ChatPage />} />
              </Route>
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </main>
        </div>
        <Toaster position="top-right" toastOptions={{
          style: {
            background: '#1e293b',
            color: '#fff',
          },
        }} />
      </Router>
    </AuthProvider>
  );
}

export default App;
