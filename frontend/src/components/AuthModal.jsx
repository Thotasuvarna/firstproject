import React, { useState } from 'react';
import { LogIn, KeyRound } from 'lucide-react';
import { api } from '../api/client';

export default function AuthModal({ isOpen, onClose, onAuthSuccess }) {
  const [tab, setTab] = useState('login'); // 'login' or 'register'
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      if (tab === 'login') {
        const data = await api.login(email, password);
        onAuthSuccess({ id: data.user_id, email: data.email, role: data.role });
        onClose();
      } else {
        await api.register(email, password, fullName);
        // Automatically login after register
        const data = await api.login(email, password);
        onAuthSuccess({ id: data.user_id, email: data.email, role: data.role });
        onClose();
      }
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  const setDemoCredentials = (roleType) => {
    if (roleType === 'admin') {
      setEmail('admin@gmail.com');
      setPassword('Admin@12345');
    } else {
      setEmail('analyst@gmail.com');
      setPassword('Analyst@12345');
    }
  };

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(0, 0, 0, 0.75)',
      backdropFilter: 'blur(5px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 100,
      padding: '1rem'
    }}>
      <div className="card" style={{ width: '100%', maxWidth: 420 }}>
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <KeyRound size={20} color="#3b82f6" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>
              {tab === 'login' ? 'System Authentication' : 'Create Analyst Account'}
            </h3>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1.25rem' }}
          >
            ✕
          </button>
        </div>

        {/* Tab Toggle */}
        <div style={{ display: 'flex', background: 'var(--bg-primary)', borderRadius: 8, padding: 3, marginBottom: '1rem' }}>
          <button
            onClick={() => { setTab('login'); setError(null); }}
            style={{
              flex: 1,
              padding: '0.45rem',
              borderRadius: 6,
              border: 'none',
              background: tab === 'login' ? 'var(--bg-surface-elevated)' : 'transparent',
              color: tab === 'login' ? '#ffffff' : 'var(--text-muted)',
              fontSize: '0.8rem',
              fontWeight: 500,
              cursor: 'pointer'
            }}
          >
            Sign In
          </button>
          <button
            onClick={() => { setTab('register'); setError(null); }}
            style={{
              flex: 1,
              padding: '0.45rem',
              borderRadius: 6,
              border: 'none',
              background: tab === 'register' ? 'var(--bg-surface-elevated)' : 'transparent',
              color: tab === 'register' ? '#ffffff' : 'var(--text-muted)',
              fontSize: '0.8rem',
              fontWeight: 500,
              cursor: 'pointer'
            }}
          >
            Register
          </button>
        </div>

        {/* Quick Demo Fill Buttons */}
        {tab === 'login' && (
          <div style={{ background: 'var(--bg-surface-elevated)', padding: '0.65rem 0.85rem', borderRadius: 8, marginBottom: '1rem', border: '1px solid var(--border-subtle)' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 600 }}>1-CLICK DEMO LOGIN:</span>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                type="button"
                onClick={() => setDemoCredentials('admin')}
                className="btn btn-secondary"
                style={{ flex: 1, fontSize: '0.725rem', padding: '0.35rem 0.5rem', justifyContent: 'center' }}
              >
                Chief Officer (Admin)
              </button>
              <button
                type="button"
                onClick={() => setDemoCredentials('analyst')}
                className="btn btn-secondary"
                style={{ flex: 1, fontSize: '0.725rem', padding: '0.35rem 0.5rem', justifyContent: 'center' }}
              >
                Trust Auditor (Analyst)
              </button>
            </div>
          </div>
        )}

        {error && (
          <div style={{ padding: '0.65rem', background: 'var(--danger-bg)', border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: 6, color: '#f87171', fontSize: '0.8rem', marginBottom: '1rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          {tab === 'register' && (
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Full Name *</label>
              <input
                required
                className="input"
                placeholder="Auditor Name"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
              />
            </div>
          )}

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Email Address *</label>
            <input
              required
              type="email"
              className="input"
              placeholder="analyst@gmail.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Password *</label>
            <input
              required
              type="password"
              className="input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center', marginTop: '0.5rem' }}
          >
            <LogIn size={15} />
            <span>{loading ? 'Authenticating...' : tab === 'login' ? 'Sign In' : 'Create Account'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
