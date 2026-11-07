import React from 'react';
import { ShieldAlert, BarChart3, Network, ShoppingBag, UploadCloud, Users, FileDown, LogIn, LogOut } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, user, onOpenAuth, onLogout, onDownloadPDF, isDownloading }) {
  const tabs = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: BarChart3 },
    { id: 'graph', label: 'Network Graph', icon: Network },
    { id: 'products', label: 'Products & Reviews', icon: ShoppingBag },
    { id: 'ingest', label: 'Ingest & Scan', icon: UploadCloud },
    { id: 'clusters', label: 'Collusion Rings', icon: Users }
  ];

  return (
    <nav style={{
      background: 'var(--bg-surface)',
      borderBottom: '1px solid var(--border-subtle)',
      position: 'sticky',
      top: 0,
      zIndex: 50,
      padding: '0.75rem 1.5rem'
    }}>
      <div style={{
        maxWidth: 1400,
        margin: '0 auto',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexWrap: 'wrap',
        gap: '1rem'
      }}>
        {/* Logo & Brand */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            background: 'linear-gradient(135deg, #2563eb, #8b5cf6)',
            padding: '0.5rem',
            borderRadius: 8,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <ShieldAlert size={22} color="#ffffff" />
          </div>
          <div>
            <h1 style={{ fontSize: '1.05rem', fontWeight: 700, letterSpacing: '-0.01em' }}>
              SENTINEL<span style={{ color: '#3b82f6' }}>AI</span>
            </h1>
            <p style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>
              Fake Review & Network Detector
            </p>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', overflowX: 'auto' }}>
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  padding: '0.5rem 0.85rem',
                  borderRadius: 6,
                  border: 'none',
                  fontSize: '0.825rem',
                  fontWeight: 500,
                  cursor: 'pointer',
                  transition: 'all 0.15s ease',
                  background: isActive ? 'var(--primary)' : 'transparent',
                  color: isActive ? '#ffffff' : 'var(--text-muted)'
                }}
              >
                <Icon size={16} />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Action Controls & User Profile */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <button
            onClick={onDownloadPDF}
            disabled={isDownloading}
            className="btn btn-secondary"
            style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
          >
            <FileDown size={15} />
            <span>{isDownloading ? 'Generating...' : 'Export Dossier (PDF)'}</span>
          </button>

          {user ? (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
              <div style={{ textAlign: 'right' }}>
                <span className={`badge ${user.role === 'admin' ? 'badge-danger' : 'badge-neutral'}`} style={{ fontSize: '0.65rem' }}>
                  {user.role}
                </span>
                <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: 2 }}>
                  {user.email.split('@')[0]}
                </div>
              </div>
              <button
                onClick={onLogout}
                className="btn btn-secondary"
                style={{ padding: '0.45rem', borderRadius: '50%' }}
                title="Logout"
              >
                <LogOut size={16} />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="btn btn-primary"
              style={{ fontSize: '0.8rem', padding: '0.45rem 0.85rem' }}
            >
              <LogIn size={15} />
              <span>Sign In / Demo</span>
            </button>
          )}
        </div>
      </div>
    </nav>
  );
}
