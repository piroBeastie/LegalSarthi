import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Scale, Mail, Lock, User, ArrowRight } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

const AuthPage = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  
  const { login, register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    let success = false;
    if (isLogin) {
      success = await login(email, password);
    } else {
      success = await register(name, email, password);
    }
    
    if (success) {
      navigate('/chat');
    }
    setIsSubmitting(false);
  };

  return (
    <div className="flex h-screen bg-primary text-text overflow-hidden">
      {/* Left Panel - Auth Form */}
      <div className="w-full lg:w-1/2 flex flex-col items-center justify-center p-8 sm:p-12 relative h-full">
        <div className="w-full max-w-md my-auto">
          <div className="flex items-center space-x-3 mb-10">
            <Scale className="h-10 w-10 text-accent" />
            <span className="font-bold text-3xl tracking-tight text-white">LegalSarthi</span>
          </div>

          <h1 className="text-4xl font-bold text-white mb-2">
            {isLogin ? 'Welcome back' : 'Create an account'}
          </h1>
          <p className="text-text-muted mb-8 text-lg">
            {isLogin 
              ? 'Sign in to continue your legal journey.' 
              : 'Join to get AI-powered legal guidance based on Indian law.'}
          </p>

          <form onSubmit={handleSubmit} className="space-y-5">
            {!isLogin && (
              <div>
                <label className="block text-sm font-medium text-text-muted mb-1">Full Name</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <User className="h-5 w-5 text-gray-500" />
                  </div>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="block w-full pl-10 pr-3 py-3 border border-border-color rounded-xl bg-secondary text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent transition-all"
                    placeholder="John Doe"
                  />
                </div>
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-text-muted mb-1">Email Address</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Mail className="h-5 w-5 text-gray-500" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-border-color rounded-xl bg-secondary text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent transition-all"
                  placeholder="you@example.com"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-text-muted mb-1">Password</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Lock className="h-5 w-5 text-gray-500" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="block w-full pl-10 pr-3 py-3 border border-border-color rounded-xl bg-secondary text-white placeholder-gray-500 focus:outline-none focus:ring-1 focus:ring-accent focus:border-accent transition-all"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isSubmitting}
              className="w-full flex items-center justify-center py-3 px-4 border border-transparent rounded-xl shadow-sm text-lg font-semibold text-primary bg-accent hover:bg-amber-400 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-accent focus:ring-offset-primary disabled:opacity-50 disabled:cursor-not-allowed transition-all mt-4"
            >
              {isSubmitting 
                ? (isLogin ? 'Signing in...' : 'Creating account...') 
                : (isLogin ? 'Sign In' : 'Create Account')}
              {!isSubmitting && <ArrowRight className="ml-2 h-5 w-5" />}
            </button>
          </form>

          <div className="mt-8 text-center">
            <button 
              onClick={() => setIsLogin(!isLogin)}
              className="text-text-muted hover:text-white transition-colors"
            >
              {isLogin 
                ? "Don't have an account? Sign up" 
                : "Already have an account? Sign in"}
            </button>
          </div>
        </div>
      </div>

      {/* Right Panel - Centered Shorter Image */}
      <div className="hidden lg:flex w-1/2 bg-secondary border-l border-border-color items-center justify-center p-16">
        <div className="w-full max-w-lg h-3/4 max-h-[800px] relative rounded-3xl overflow-hidden shadow-2xl flex flex-col justify-end">
          <img 
            src="https://images.unsplash.com/photo-1589829085413-56de8ae18c73?q=80&w=2000&auto=format&fit=crop" 
            alt="Scales of Justice" 
            className="absolute inset-0 w-full h-full object-cover opacity-60 mix-blend-luminosity"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-primary via-primary/50 to-transparent"></div>
          
          <div className="relative z-10 p-10 text-center">
            <Scale className="h-12 w-12 text-accent mx-auto mb-6 opacity-90" />
            <h2 className="text-3xl font-semibold text-white mb-3 leading-tight font-quote tracking-widest">
              "The law is reason, free from passion."
            </h2>
            <p className="text-text-muted text-base">
              Empowering citizens with accessible, AI-driven legal guidance based on the Constitution of India.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
