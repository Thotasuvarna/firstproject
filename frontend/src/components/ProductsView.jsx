import React, { useEffect, useState } from 'react';
import { ShoppingBag, Plus, Search, ShieldCheck, ShieldAlert, Star, MessageSquare } from 'lucide-react';
import { api } from '../api/client';

export default function ProductsView({ user, onOpenAuth }) {
  const [products, setProducts] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [showAddModal, setShowAddModal] = useState(false);
  const [newProduct, setNewProduct] = useState({ product_sku: '', title: '', category: 'Electronics', description: '' });
  const [submitting, setSubmitting] = useState(false);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [productReviews, setProductReviews] = useState([]);
  const [loadingReviews, setLoadingReviews] = useState(false);

  const fetchProducts = async () => {
    try {
      const data = await api.getProducts();
      setProducts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, []);

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    if (!user) {
      onOpenAuth();
      return;
    }
    setSubmitting(true);
    try {
      await api.createProduct(newProduct);
      setNewProduct({ product_sku: '', title: '', category: 'Electronics', description: '' });
      setShowAddModal(false);
      fetchProducts();
    } catch (err) {
      alert(err.message || 'Failed to create product');
    } finally {
      setSubmitting(false);
    }
  };

  const handleViewReviews = async (p) => {
    setSelectedProduct(p);
    setLoadingReviews(true);
    try {
      const reviews = await api.getReviews({ product_sku: p.product_sku });
      setProductReviews(reviews);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingReviews(false);
    }
  };

  const filtered = products.filter((p) =>
    p.title.toLowerCase().includes(search.toLowerCase()) ||
    p.product_sku.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      {/* Top Header & Search */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Catalog & Reputation Intelligence</h2>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
            Real-time trust scores and review provenance monitoring per SKU.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{ position: 'relative' }}>
            <Search size={16} color="var(--text-muted)" style={{ position: 'absolute', left: 10, top: 10 }} />
            <input
              type="text"
              placeholder="Search product or SKU..."
              className="input"
              style={{ paddingLeft: '2.25rem', width: 240 }}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>

          <button
            onClick={() => user ? setShowAddModal(true) : onOpenAuth()}
            className="btn btn-primary"
          >
            <Plus size={16} />
            <span>Add Product</span>
          </button>
        </div>
      </div>

      {/* Products Table */}
      <div className="card">
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>SKU</th>
                <th>Title</th>
                <th>Category</th>
                <th>Average Rating</th>
                <th>Reviews</th>
                <th>Catalog Trust Score</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((p) => (
                <tr key={p.id}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 500 }}>{p.product_sku}</td>
                  <td style={{ fontWeight: 600 }}>{p.title}</td>
                  <td>
                    <span className="badge badge-neutral">{p.category}</span>
                  </td>
                  <td>
                    <span style={{ color: '#fbbf24', display: 'flex', alignItems: 'center', gap: 3 }}>
                      <Star size={14} fill="#fbbf24" /> {p.average_rating.toFixed(1)}
                    </span>
                  </td>
                  <td>{p.total_reviews}</td>
                  <td>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                      <span className={`badge ${p.product_trust_score >= 80 ? 'badge-success' : p.product_trust_score >= 50 ? 'badge-warning' : 'badge-danger'}`}>
                        {p.product_trust_score.toFixed(0)}%
                      </span>
                    </div>
                  </td>
                  <td>
                    <button
                      onClick={() => handleViewReviews(p)}
                      className="btn btn-secondary"
                      style={{ fontSize: '0.75rem', padding: '0.35rem 0.65rem' }}
                    >
                      <MessageSquare size={13} />
                      <span>Inspect Reviews</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Reviews Drawer Modal */}
      {selectedProduct && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0, 0, 0, 0.7)',
          backdropFilter: 'blur(4px)',
          display: 'flex',
          justifyContent: 'flex-end',
          zIndex: 100
        }}>
          <div style={{
            width: '100%',
            maxWidth: 580,
            background: 'var(--bg-surface)',
            borderLeft: '1px solid var(--border-subtle)',
            padding: '1.5rem',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '1rem'
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.75rem' }}>
              <div>
                <span className="badge badge-neutral">Product Reviews</span>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginTop: 4 }}>
                  {selectedProduct.title}
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                  SKU: {selectedProduct.product_sku}
                </p>
              </div>
              <button
                onClick={() => setSelectedProduct(null)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1.25rem' }}
              >
                ✕
              </button>
            </div>

            {loadingReviews ? (
              <p style={{ color: 'var(--text-muted)' }}>Loading reviews...</p>
            ) : productReviews.length === 0 ? (
              <p style={{ color: 'var(--text-muted)' }}>No reviews recorded for this product yet.</p>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {productReviews.map((rev) => (
                  <div key={rev.id} style={{ background: 'var(--bg-primary)', padding: '0.85rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                      <span style={{ color: '#fbbf24', fontSize: '0.85rem' }}>
                        {'★'.repeat(Math.round(rev.rating))} ({rev.rating.toFixed(1)})
                      </span>
                      {rev.analysis && (
                        <span className={`badge ${rev.analysis.risk_tier === 'HIGH' ? 'badge-danger' : rev.analysis.risk_tier === 'MEDIUM' ? 'badge-warning' : 'badge-success'}`}>
                          {rev.analysis.composite_suspicion_score.toFixed(0)} Score ({rev.analysis.risk_tier})
                        </span>
                      )}
                    </div>
                    {rev.review_title && (
                      <h4 style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 4 }}>{rev.review_title}</h4>
                    )}
                    <p style={{ fontSize: '0.8rem', color: '#d1d5db', lineHeight: 1.4 }}>
                      {rev.review_text}
                    </p>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8, fontSize: '0.7rem', color: 'var(--text-faint)' }}>
                      <span>Verified: {rev.is_verified_purchase ? 'Yes' : 'No'}</span>
                      <span>{new Date(rev.review_date).toLocaleDateString()}</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Add Product Modal */}
      {showAddModal && (
        <div style={{
          position: 'fixed',
          inset: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100,
          padding: '1rem'
        }}>
          <div className="card" style={{ width: '100%', maxWidth: 460 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Register New Product SKU</h3>
              <button onClick={() => setShowAddModal(false)} style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer' }}>✕</button>
            </div>
            <form onSubmit={handleCreateProduct} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Product SKU / ASIN *</label>
                <input
                  required
                  placeholder="e.g. ELEC-NOISE-CANCEL-99"
                  className="input"
                  value={newProduct.product_sku}
                  onChange={(e) => setNewProduct({ ...newProduct, product_sku: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Product Title *</label>
                <input
                  required
                  placeholder="Full marketing title"
                  className="input"
                  value={newProduct.title}
                  onChange={(e) => setNewProduct({ ...newProduct, title: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Category</label>
                <input
                  placeholder="Electronics, Health, etc."
                  className="input"
                  value={newProduct.category}
                  onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
                />
              </div>
              <div>
                <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Description</label>
                <textarea
                  rows={3}
                  className="textarea"
                  value={newProduct.description}
                  onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
                />
              </div>
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', marginTop: '0.5rem' }}>
                <button type="button" onClick={() => setShowAddModal(false)} className="btn btn-secondary">Cancel</button>
                <button type="submit" disabled={submitting} className="btn btn-primary">
                  {submitting ? 'Registering...' : 'Create SKU'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
