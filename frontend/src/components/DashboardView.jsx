import React, { useEffect, useState } from 'react';
import { AlertTriangle, CheckCircle2, ShieldAlert, Sparkles, TrendingDown, Users, ChevronDown, ChevronUp, FileText } from 'lucide-react';
import { api } from '../api/client';

export default function DashboardView({ onNavigateTab }) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRow, setExpandedRow] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await api.getMetrics();
        setMetrics(data);
      } catch (err) {
        setError(err.message || 'Failed to fetch executive dashboard metrics');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
        <p style={{ color: 'var(--text-muted)' }}>Loading AI threat statistics...</p>
      </div>
    );
  }

  if (error || !metrics) {
    return (
      <div className="card" style={{ borderColor: 'var(--danger)', color: '#fca5a5' }}>
        <p>Error: {error || 'Unable to connect to backend server'}</p>
      </div>
    );
  }

  const kpis = [
    {
      title: 'Total Ingested Reviews',
      value: metrics.total_reviews,
      subtitle: `${metrics.total_products} Products | ${metrics.total_reviewers} Reviewers`,
      icon: FileText,
      color: '#3b82f6'
    },
    {
      title: 'Suspicious Reviews Flagged',
      value: `${metrics.suspicious_reviews_count}`,
      subtitle: `${metrics.suspicious_reviews_percentage}% of total corpus`,
      icon: ShieldAlert,
      color: metrics.suspicious_reviews_percentage > 25 ? '#ef4444' : '#f59e0b'
    },
    {
      title: 'Identified Collusion Rings',
      value: metrics.detected_clusters_count,
      subtitle: 'Coordinated reviewer subgraphs',
      icon: Users,
      color: '#8b5cf6'
    },
    {
      title: 'Catalog Health & Trust Index',
      value: `${metrics.average_trust_score.toFixed(1)}%`,
      subtitle: 'Composite reliability index',
      icon: CheckCircle2,
      color: '#10b981'
    }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* KPI Cards Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem' }}>
        {kpis.map((kpi, idx) => {
          const Icon = kpi.icon;
          return (
            <div key={idx} className="card" style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
              <div>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontWeight: 500 }}>
                  {kpi.title}
                </p>
                <h3 style={{ fontSize: '1.75rem', fontWeight: 700, margin: '0.35rem 0' }}>
                  {kpi.value}
                </h3>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-faint)' }}>
                  {kpi.subtitle}
                </p>
              </div>
              <div style={{
                background: `${kpi.color}1a`,
                padding: '0.65rem',
                borderRadius: 8,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center'
              }}>
                <Icon size={22} color={kpi.color} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Middle Row: Risk Distribution & At-Risk Products */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem' }}>
        {/* Risk Distribution Breakdown */}
        <div className="card">
          <h3 style={{ fontSize: '1rem', fontWeight: 600, marginBottom: '1rem' }}>
            Risk Classification Distribution
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: 4 }}>
                <span style={{ color: '#f87171' }}>High Risk (Score &gt; 65)</span>
                <b>{metrics.risk_tier_breakdown.HIGH || 0} reviews</b>
              </div>
              <div style={{ height: 8, background: '#1f2937', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{
                  height: '100%',
                  width: `${((metrics.risk_tier_breakdown.HIGH || 0) / Math.max(metrics.total_reviews, 1)) * 100}%`,
                  background: '#ef4444'
                }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: 4 }}>
                <span style={{ color: '#fbbf24' }}>Medium Risk (Score 35 - 65)</span>
                <b>{metrics.risk_tier_breakdown.MEDIUM || 0} reviews</b>
              </div>
              <div style={{ height: 8, background: '#1f2937', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{
                  height: '100%',
                  width: `${((metrics.risk_tier_breakdown.MEDIUM || 0) / Math.max(metrics.total_reviews, 1)) * 100}%`,
                  background: '#f59e0b'
                }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.825rem', marginBottom: 4 }}>
                <span style={{ color: '#34d399' }}>Low Risk / Organic (&lt; 35)</span>
                <b>{metrics.risk_tier_breakdown.LOW || 0} reviews</b>
              </div>
              <div style={{ height: 8, background: '#1f2937', borderRadius: 4, overflow: 'hidden' }}>
                <div style={{
                  height: '100%',
                  width: `${((metrics.risk_tier_breakdown.LOW || 0) / Math.max(metrics.total_reviews, 1)) * 100}%`,
                  background: '#10b981'
                }} />
              </div>
            </div>
          </div>
        </div>

        {/* At-Risk Products */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
            <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>Top Flagged Catalog Items</h3>
            <button onClick={() => onNavigateTab('products')} className="btn btn-secondary" style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}>
              View Catalog
            </button>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
            {metrics.top_flagged_products.slice(0, 4).map((p) => (
              <div key={p.id} style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0.5rem 0', borderBottom: '1px solid #1f2937' }}>
                <div>
                  <h4 style={{ fontSize: '0.85rem', fontWeight: 500 }}>{p.title}</h4>
                  <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                    SKU: {p.sku} | {p.total_reviews} reviews ({p.avg_rating}★)
                  </span>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span className={`badge ${p.trust_score < 60 ? 'badge-danger' : 'badge-warning'}`}>
                    {p.trust_score.toFixed(0)}% Trust
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* High Priority Flagged Reviews Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h3 style={{ fontSize: '1rem', fontWeight: 600 }}>High-Priority Reviews Requiring Inspection</h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
              Click on any row to expand Explainable AI (XAI) factors and algorithmic evidence breakdown.
            </p>
          </div>
        </div>

        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th style={{ width: 40 }}></th>
                <th>ID</th>
                <th>Product SKU</th>
                <th>Rating</th>
                <th>Suspicion Score</th>
                <th>Risk Tier</th>
                <th>Primary Trigger</th>
              </tr>
            </thead>
            <tbody>
              {metrics.recent_suspicious_reviews.map((r) => {
                const isExpanded = expandedRow === r.review_id;
                return (
                  <React.Fragment key={r.review_id}>
                    <tr
                      onClick={() => setExpandedRow(isExpanded ? null : r.review_id)}
                      style={{ cursor: 'pointer' }}
                    >
                      <td>
                        {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                      </td>
                      <td style={{ fontFamily: 'var(--font-mono)' }}>#{r.review_id}</td>
                      <td style={{ fontWeight: 500 }}>{r.product_sku}</td>
                      <td>
                        <span style={{ color: '#fbbf24' }}>★ {r.rating.toFixed(1)}</span>
                      </td>
                      <td>
                        <b style={{ color: r.composite_suspicion_score >= 65 ? '#ef4444' : '#f59e0b' }}>
                          {r.composite_suspicion_score.toFixed(1)} / 100
                        </b>
                      </td>
                      <td>
                        <span className={`badge ${r.risk_tier === 'HIGH' ? 'badge-danger' : 'badge-warning'}`}>
                          {r.risk_tier}
                        </span>
                      </td>
                      <td style={{ color: 'var(--text-muted)', fontSize: '0.8rem' }}>
                        {r.top_reason}
                      </td>
                    </tr>
                    {isExpanded && (
                      <tr>
                        <td colSpan={7} style={{ background: 'var(--bg-surface-elevated)', padding: '1rem' }}>
                          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                            <div>
                              <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
                                Full Review Text:
                              </span>
                              <p style={{ fontSize: '0.85rem', color: '#e5e7eb', marginTop: 4, fontStyle: 'italic' }}>
                                "{r.snippet}"
                              </p>
                            </div>
                            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                              <div style={{ background: 'var(--bg-primary)', padding: '0.5rem 0.75rem', borderRadius: 6, border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                                <span style={{ color: 'var(--text-muted)' }}>Trigger Reason: </span>
                                <b style={{ color: '#f87171' }}>{r.top_reason}</b>
                              </div>
                              <div style={{ background: 'var(--bg-primary)', padding: '0.5rem 0.75rem', borderRadius: 6, border: '1px solid var(--border-subtle)', fontSize: '0.75rem' }}>
                                <span style={{ color: 'var(--text-muted)' }}>Status: </span>
                                <b>Pending Auditor Verification</b>
                              </div>
                            </div>
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
