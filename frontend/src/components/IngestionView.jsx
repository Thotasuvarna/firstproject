import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertTriangle, ShieldAlert, Sparkles, Send } from 'lucide-react';
import { api } from '../api/client';

export default function IngestionView({ user, onOpenAuth }) {
  const [sku, setSku] = useState('TECH-SONY-XM5');
  const [reviewerId, setReviewerId] = useState('');
  const [rating, setRating] = useState(5.0);
  const [title, setTitle] = useState('');
  const [text, setText] = useState('');
  const [verified, setVerified] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [scanResult, setScanResult] = useState(null);

  // CSV State
  const [csvFile, setCsvFile] = useState(null);
  const [csvUploading, setCsvUploading] = useState(false);
  const [csvMessage, setCsvMessage] = useState(null);

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    if (!user) {
      onOpenAuth();
      return;
    }
    setSubmitting(true);
    setScanResult(null);

    try {
      const reviewPayload = {
        product_sku: sku,
        reviewer_identifier: reviewerId || `user_${Math.random().toString(36).substring(7)}@test.com`,
        rating: Number(rating),
        review_title: title,
        review_text: text,
        is_verified_purchase: verified
      };
      const res = await api.submitReview(reviewPayload);
      setScanResult(res.analysis);
      setText('');
      setTitle('');
    } catch (err) {
      alert(err.message || 'Failed to submit review');
    } finally {
      setSubmitting(false);
    }
  };

  const handleUploadCSV = async (e) => {
    e.preventDefault();
    if (!csvFile) return;
    if (!user) {
      onOpenAuth();
      return;
    }
    setCsvUploading(true);
    setCsvMessage(null);
    try {
      const res = await api.uploadCSV(csvFile);
      setCsvMessage(res.message);
      setCsvFile(null);
    } catch (err) {
      alert(err.message || 'CSV upload failed');
    } finally {
      setCsvUploading(false);
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(360px, 1fr))', gap: '1.5rem' }}>
      {/* Real-time Single Review Scanner */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
          <Sparkles size={20} color="#3b82f6" />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Real-Time Review Analysis Engine</h3>
        </div>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1.25rem' }}>
          Evaluate review text against TF-IDF duplication matrices, sentiment divergence, and behavioral heuristics.
        </p>

        <form onSubmit={handleSubmitReview} style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Target Product SKU *</label>
              <input
                required
                className="input"
                placeholder="e.g. TECH-SONY-XM5"
                value={sku}
                onChange={(e) => setSku(e.target.value)}
              />
            </div>
            <div>
              <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Rating Given *</label>
              <select
                className="select"
                value={rating}
                onChange={(e) => setRating(e.target.value)}
              >
                <option value={5.0}>5 Stars ★★★★★</option>
                <option value={4.0}>4 Stars ★★★★☆</option>
                <option value={3.0}>3 Stars ★★★☆☆</option>
                <option value={2.0}>2 Stars ★★☆☆☆</option>
                <option value={1.0}>1 Star ★☆☆☆☆</option>
              </select>
            </div>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Reviewer Identifier (Pseudonymized on Ingestion) *</label>
            <input
              required
              className="input"
              placeholder="e.g. buyer_account@domain.com"
              value={reviewerId}
              onChange={(e) => setReviewerId(e.target.value)}
            />
            <span style={{ fontSize: '0.7rem', color: 'var(--text-faint)' }}>
              🔒 Converted to Salted SHA-256 before persistence to guarantee privacy.
            </span>
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Review Headline / Title</label>
            <input
              className="input"
              placeholder="Short title summary"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
          </div>

          <div>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Review Content *</label>
            <textarea
              required
              rows={4}
              className="textarea"
              placeholder="Paste or write review text here..."
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <input
              type="checkbox"
              id="verifiedCheck"
              checked={verified}
              onChange={(e) => setVerified(e.target.checked)}
            />
            <label htmlFor="verifiedCheck" style={{ fontSize: '0.825rem', color: 'var(--text-main)', cursor: 'pointer' }}>
              Verified Purchase Account
            </label>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="btn btn-primary"
            style={{ justifyContent: 'center', marginTop: '0.5rem' }}
          >
            <Send size={15} />
            <span>{submitting ? 'Running ML & NLP Inference...' : 'Submit & Analyze'}</span>
          </button>
        </form>

        {/* Live Analysis Feedback Box */}
        {scanResult && (
          <div style={{
            marginTop: '1.25rem',
            padding: '1rem',
            borderRadius: 8,
            background: 'var(--bg-surface-elevated)',
            border: `1px solid ${scanResult.risk_tier === 'HIGH' ? '#ef4444' : scanResult.risk_tier === 'MEDIUM' ? '#f59e0b' : '#10b981'}`
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <span className={`badge ${scanResult.risk_tier === 'HIGH' ? 'badge-danger' : scanResult.risk_tier === 'MEDIUM' ? 'badge-warning' : 'badge-success'}`}>
                {scanResult.risk_tier} RISK
              </span>
              <span style={{ fontSize: '1.1rem', fontWeight: 700 }}>
                Score: {scanResult.composite_suspicion_score.toFixed(1)} / 100
              </span>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.5rem', fontSize: '0.75rem', marginTop: '0.5rem' }}>
              <div>Duplicate Similarity: <b>{(scanResult.duplicate_similarity_score * 100).toFixed(0)}%</b></div>
              <div>Sentiment Polarity: <b>{scanResult.sentiment_polarity.toFixed(2)}</b></div>
              <div>Rating Divergence: <b>{(scanResult.rating_divergence_score * 100).toFixed(0)}%</b></div>
              <div>AI Deception Confidence: <b>{(scanResult.ml_prediction_prob * 100).toFixed(0)}%</b></div>
            </div>

            {scanResult.explainability_factors?.primary_drivers?.length > 0 && (
              <div style={{ marginTop: '0.75rem', borderTop: '1px solid var(--border-subtle)', paddingTop: '0.5rem' }}>
                <p style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)' }}>Primary Triggers:</p>
                <ul style={{ fontSize: '0.75rem', paddingLeft: '1.25rem', marginTop: 4, color: '#fca5a5' }}>
                  {scanResult.explainability_factors.primary_drivers.map((d, i) => (
                    <li key={i}>{d.description}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Batch CSV Uploader */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <UploadCloud size={20} color="#8b5cf6" />
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Batch Dataset Ingestion</h3>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
            Upload customer review datasets in CSV format. The pipeline automatically batches ingestion, vectorizes content, and evaluates network clusters.
          </p>

          <div style={{
            background: 'var(--bg-primary)',
            border: '2px dashed var(--border-subtle)',
            borderRadius: 8,
            padding: '2rem',
            textAlign: 'center',
            marginBottom: '1rem'
          }}>
            <FileText size={36} color="var(--text-muted)" style={{ margin: '0 auto 0.75rem' }} />
            <p style={{ fontSize: '0.85rem', fontWeight: 500, marginBottom: '0.25rem' }}>
              {csvFile ? csvFile.name : 'Select or drop a CSV review dataset'}
            </p>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-faint)', marginBottom: '1rem' }}>
              Columns: product_sku, reviewer_identifier, rating, review_text
            </p>
            <input
              type="file"
              accept=".csv"
              id="csvFileInput"
              style={{ display: 'none' }}
              onChange={(e) => setCsvFile(e.target.files[0] || null)}
            />
            <label htmlFor="csvFileInput" className="btn btn-secondary" style={{ cursor: 'pointer', display: 'inline-flex' }}>
              Browse File
            </label>
          </div>

          {csvMessage && (
            <div style={{ padding: '0.75rem', background: 'var(--success-bg)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: 6, color: '#34d399', fontSize: '0.8rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <CheckCircle2 size={16} />
              <span>{csvMessage}</span>
            </div>
          )}
        </div>

        <form onSubmit={handleUploadCSV}>
          <button
            type="submit"
            disabled={!csvFile || csvUploading}
            className="btn btn-primary"
            style={{ width: '100%', justifyContent: 'center' }}
          >
            <UploadCloud size={16} />
            <span>{csvUploading ? 'Ingesting & Analyzing Dataset...' : 'Start Batch Processing'}</span>
          </button>
        </form>
      </div>
    </div>
  );
}
