import React, { useEffect, useState } from 'react';
import { Users, AlertTriangle, ShieldCheck, ShieldAlert, CheckCircle, XCircle } from 'lucide-react';
import { api } from '../api/client';

export default function CollusionRingsView({ user, onOpenAuth }) {
  const [clusters, setClusters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState(null);

  const fetchClusters = async () => {
    try {
      const data = await api.getCollusionClusters();
      setClusters(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClusters();
  }, []);

  const handleAuditAction = async (clusterId, actionType) => {
    if (!user) {
      onOpenAuth();
      return;
    }
    try {
      await api.recordAuditAction({
        action_type: actionType,
        target_entity: 'CLUSTER',
        target_id: clusterId,
        notes: `Auditor review action: ${actionType}`
      });
      setActionSuccess(`Cluster #${clusterId} marked as ${actionType}`);
      setTimeout(() => setActionSuccess(null), 3000);
      fetchClusters();
    } catch (err) {
      alert(err.message || 'Action failed');
    }
  };

  if (loading) {
    return <p style={{ color: 'var(--text-muted)' }}>Mining collusion rings with NetworkX...</p>;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
      <div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 700 }}>Coordinated Reviewer Collusion Rings</h2>
        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
          Latent reviewer rings detected via NetworkX bipartite graph projection and clique analysis.
        </p>
      </div>

      {actionSuccess && (
        <div style={{ padding: '0.75rem', background: 'var(--success-bg)', border: '1px solid rgba(16, 185, 129, 0.3)', borderRadius: 6, color: '#34d399', fontSize: '0.85rem' }}>
          {actionSuccess}
        </div>
      )}

      {clusters.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
          <ShieldCheck size={40} color="#10b981" style={{ margin: '0 auto 1rem' }} />
          <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>No Collusion Rings Detected</h3>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: 4 }}>
            All reviewer co-review topologies are currently beneath the anomalous coordination threshold.
          </p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(380px, 1fr))', gap: '1.25rem' }}>
          {clusters.map((c) => (
            <div key={c.id} className="card" style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span className={`badge ${c.status === 'DETECTED' ? 'badge-danger' : 'badge-neutral'}`}>
                  {c.status}
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  Detected: {new Date(c.detected_at).toLocaleDateString()}
                </span>
              </div>

              <div>
                <h3 style={{ fontSize: '1.1rem', fontWeight: 600 }}>{c.cluster_name}</h3>
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {c.member_count} Coordinated Accounts | Graph Density: <b>{(c.density * 100).toFixed(0)}%</b>
                </p>
              </div>

              <div style={{ background: 'var(--bg-primary)', padding: '0.75rem', borderRadius: 8, border: '1px solid var(--border-subtle)' }}>
                <h4 style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem', textTransform: 'uppercase' }}>
                  Identified Ring Members:
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
                  {c.members.map((m) => (
                    <div key={m.reviewer_id} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem' }}>
                      <span style={{ fontFamily: 'var(--font-mono)' }}>{m.alias}</span>
                      <span style={{ color: 'var(--text-faint)' }}>Centrality: {m.centrality.toFixed(2)}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Human-in-the-Loop Actions */}
              <div style={{ display: 'flex', gap: '0.5rem', marginTop: 'auto', paddingTop: '0.5rem' }}>
                <button
                  onClick={() => handleAuditAction(c.id, 'QUARANTINED')}
                  className="btn btn-secondary"
                  style={{ flex: 1, fontSize: '0.75rem', justifyContent: 'center', borderColor: 'rgba(239, 68, 68, 0.4)', color: '#f87171' }}
                >
                  <AlertTriangle size={14} />
                  <span>Quarantine Ring</span>
                </button>
                <button
                  onClick={() => handleAuditAction(c.id, 'DISMISSED')}
                  className="btn btn-secondary"
                  style={{ flex: 1, fontSize: '0.75rem', justifyContent: 'center' }}
                >
                  <CheckCircle size={14} />
                  <span>Dismiss Flag</span>
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
