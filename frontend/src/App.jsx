import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardView from './components/DashboardView';
import NetworkGraph from './components/NetworkGraph';
import ProductsView from './components/ProductsView';
import IngestionView from './components/IngestionView';
import CollusionRingsView from './components/CollusionRingsView';
import AuthModal from './components/AuthModal';
import { api, getStoredUser, clearAuthSession } from './api/client';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [user, setUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);

  useEffect(() => {
    const stored = getStoredUser();
    if (stored) {
      setUser(stored);
    }
  }, []);

  const handleLogout = () => {
    clearAuthSession();
    setUser(null);
  };

  const handleDownloadPDF = async () => {
    setIsDownloading(true);
    try {
      await api.downloadPDF();
    } catch (err) {
      alert(err.message || 'Failed to download PDF dossier');
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        user={user}
        onOpenAuth={() => setShowAuthModal(true)}
        onLogout={handleLogout}
        onDownloadPDF={handleDownloadPDF}
        isDownloading={isDownloading}
      />

      {/* Main Content Area */}
      <main style={{ flex: 1, maxWidth: 1400, width: '100%', margin: '0 auto', padding: '1.5rem' }}>
        {activeTab === 'dashboard' && <DashboardView onNavigateTab={setActiveTab} />}
        {activeTab === 'graph' && <NetworkGraph />}
        {activeTab === 'products' && <ProductsView user={user} onOpenAuth={() => setShowAuthModal(true)} />}
        {activeTab === 'ingest' && <IngestionView user={user} onOpenAuth={() => setShowAuthModal(true)} />}
        {activeTab === 'clusters' && <CollusionRingsView user={user} onOpenAuth={() => setShowAuthModal(true)} />}
      </main>

      {/* Footer */}
      <footer style={{
        borderTop: '1px solid var(--border-subtle)',
        background: 'var(--bg-surface)',
        padding: '1rem 1.5rem',
        fontSize: '0.75rem',
        color: 'var(--text-faint)',
        textAlign: 'center'
      }}>
        <div style={{ maxWidth: 1400, margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.5rem' }}>
          <span>SENTINEL AI™ — Fake Review & Coordinated Reviewer Network Detection System</span>
          <span>Responsible AI & Human-in-the-Loop Architecture | Built with FastAPI, React & NetworkX</span>
        </div>
      </footer>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={showAuthModal}
        onClose={() => setShowAuthModal(false)}
        onAuthSuccess={(u) => setUser(u)}
      />
    </div>
  );
}
