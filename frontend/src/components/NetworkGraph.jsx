import React, { useEffect, useRef, useState } from 'react';
import { Network as VisNetwork } from 'vis-network/standalone';
import { Network, ZoomIn, ZoomOut, RefreshCw, AlertTriangle, ShieldCheck, Info } from 'lucide-react';
import { api } from '../api/client';

export default function NetworkGraph() {
  const containerRef = useRef(null);
  const networkInstance = useRef(null);
  const [graphData, setGraphData] = useState(null);
  const [minShared, setMinShared] = useState(1);
  const [selectedNode, setSelectedNode] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchGraph = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getNetworkGraph(minShared);
      setGraphData(data);
    } catch (err) {
      setError(err.message || 'Failed to load network topology');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, [minShared]);

  useEffect(() => {
    if (!containerRef.current || !graphData) return;

    // Format nodes for Vis.js
    const nodes = graphData.nodes.map((n) => {
      const isProduct = n.node_type === 'product';
      let color = '#3b82f6'; // default blue for product

      if (!isProduct) {
        if (n.risk_score >= 65) color = '#ef4444'; // Red for high risk
        else if (n.risk_score >= 35) color = '#f59e0b'; // Amber for medium risk
        else color = '#10b981'; // Green for normal
      }

      return {
        id: n.id,
        label: n.label.length > 20 ? n.label.slice(0, 18) + '...' : n.label,
        shape: isProduct ? 'box' : 'dot',
        size: isProduct ? 24 : 18,
        color: {
          background: color,
          border: isProduct ? '#60a5fa' : '#ffffff',
          highlight: {
            background: color,
            border: '#fbbf24'
          }
        },
        font: {
          color: '#f3f4f6',
          size: 11,
          face: 'Inter',
          strokeWidth: 2,
          strokeColor: '#111827'
        },
        raw: n
      };
    });

    // Format edges for Vis.js
    const edges = graphData.edges.map((e) => ({
      id: e.id,
      from: e.source,
      to: e.target,
      color: { color: 'rgba(156, 163, 175, 0.4)', highlight: '#38bdf8' },
      width: Math.min(e.weight * 1.5, 4),
      smooth: { type: 'continuous' },
      raw: e
    }));

    const data = { nodes, edges };

    const options = {
      physics: {
        stabilization: { iterations: 120 },
        barnesHut: {
          gravitationalConstant: -3500,
          springConstant: 0.04,
          springLength: 95
        }
      },
      interaction: {
        hover: true,
        tooltipDelay: 200,
        navigationButtons: true,
        keyboard: true
      }
    };

    if (networkInstance.current) {
      networkInstance.current.destroy();
    }

    const network = new VisNetwork(containerRef.current, data, options);
    networkInstance.current = network;

    network.on('click', (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const found = graphData.nodes.find((n) => n.id === nodeId);
        setSelectedNode(found || null);
      } else {
        setSelectedNode(null);
      }
    });

    return () => {
      if (networkInstance.current) {
        networkInstance.current.destroy();
      }
    };
  }, [graphData]);

  const fitNetwork = () => {
    if (networkInstance.current) {
      networkInstance.current.fit({ animation: { duration: 500 } });
    }
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: selectedNode ? '1fr 340px' : '1fr', gap: '1rem', height: 'calc(100vh - 120px)' }}>
      {/* Main Canvas Area */}
      <div className="card" style={{ display: 'flex', flexDirection: 'column', padding: 0, overflow: 'hidden', position: 'relative' }}>
        {/* Controls Toolbar */}
        <div style={{
          padding: '0.75rem 1.25rem',
          background: 'var(--bg-surface-elevated)',
          borderBottom: '1px solid var(--border-subtle)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexWrap: 'wrap',
          gap: '0.75rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <Network size={18} color="#3b82f6" />
            <span style={{ fontWeight: 600, fontSize: '0.9rem' }}>Bipartite Reviewer-Product Network</span>
            {graphData && (
              <span className="badge badge-neutral">
                {graphData.total_nodes} Nodes | {graphData.total_edges} Edges
              </span>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <label style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Co-Review Filter:</label>
            <select
              className="select"
              style={{ width: 'auto', padding: '0.35rem 0.65rem', fontSize: '0.8rem' }}
              value={minShared}
              onChange={(e) => setMinShared(Number(e.target.value))}
            >
              <option value={1}>≥ 1 Shared Review</option>
              <option value={2}>≥ 2 Shared Reviews (Tighter Rings)</option>
              <option value={3}>≥ 3 Shared Reviews (Core Collusion)</option>
            </select>

            <button onClick={fitNetwork} className="btn btn-secondary" style={{ padding: '0.35rem 0.65rem' }} title="Reset View">
              <ZoomIn size={15} />
            </button>
            <button onClick={fetchGraph} className="btn btn-secondary" style={{ padding: '0.35rem 0.65rem' }} title="Reload Topology">
              <RefreshCw size={15} />
            </button>
          </div>
        </div>

        {/* Legend */}
        <div style={{
          position: 'absolute',
          top: '3.75rem',
          left: '1rem',
          zIndex: 10,
          background: 'rgba(17, 24, 39, 0.85)',
          backdropFilter: 'blur(8px)',
          padding: '0.5rem 0.75rem',
          borderRadius: 8,
          border: '1px solid var(--border-subtle)',
          fontSize: '0.75rem',
          display: 'flex',
          flexDirection: 'column',
          gap: '0.35rem'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: 12, height: 12, background: '#3b82f6', borderRadius: 2 }} />
            <span>Product Node</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: 12, height: 12, background: '#ef4444', borderRadius: '50%' }} />
            <span>High Anomaly Reviewer (&gt; 65)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: 12, height: 12, background: '#f59e0b', borderRadius: '50%' }} />
            <span>Moderate Anomaly (35-65)</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ width: 12, height: 12, background: '#10b981', borderRadius: '50%' }} />
            <span>Low Risk / Organic</span>
          </div>
        </div>

        {/* Canvas */}
        <div ref={containerRef} style={{ flex: 1, width: '100%', height: '100%', background: '#090d16' }} />

        {loading && (
          <div style={{
            position: 'absolute',
            inset: 0,
            background: 'rgba(11, 15, 25, 0.75)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 20
          }}>
            <div style={{ textAlign: 'center' }}>
              <RefreshCw size={28} className="animate-spin" color="#3b82f6" />
              <p style={{ marginTop: '0.5rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                Constructing Bipartite Graph with NetworkX...
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Node Inspector Drawer */}
      {selectedNode && (
        <div className="card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', overflowY: 'auto' }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', borderBottom: '1px solid var(--border-subtle)', paddingBottom: '0.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Node Inspection
            </span>
            <button
              onClick={() => setSelectedNode(null)}
              style={{ background: 'transparent', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '1rem' }}
            >
              ✕
            </button>
          </div>

          <div>
            <span className={`badge ${selectedNode.node_type === 'product' ? 'badge-neutral' : selectedNode.risk_score >= 65 ? 'badge-danger' : 'badge-warning'}`}>
              {selectedNode.node_type.toUpperCase()}
            </span>
            <h3 style={{ fontSize: '1.1rem', fontWeight: 600, marginTop: '0.5rem' }}>
              {selectedNode.label}
            </h3>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', marginTop: 4 }}>
              ID: {selectedNode.id}
            </p>
          </div>

          <div style={{ background: 'var(--bg-surface-elevated)', padding: '0.85rem', borderRadius: 8 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Suspicion Anomaly Metric:</span>
              <span style={{ fontSize: '1.1rem', fontWeight: 700, color: selectedNode.risk_score >= 65 ? '#ef4444' : '#10b981' }}>
                {selectedNode.risk_score.toFixed(1)} / 100
              </span>
            </div>
            <div style={{
              width: '100%',
              height: 6,
              background: '#374151',
              borderRadius: 3,
              marginTop: '0.5rem',
              overflow: 'hidden'
            }}>
              <div style={{
                width: `${selectedNode.risk_score}%`,
                height: '100%',
                background: selectedNode.risk_score >= 65 ? '#ef4444' : '#3b82f6'
              }} />
            </div>
          </div>

          <div>
            <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.5rem' }}>
              Network Cluster Association
            </h4>
            <div style={{ padding: '0.65rem', background: 'var(--bg-primary)', borderRadius: 6, border: '1px solid var(--border-subtle)', fontSize: '0.8rem' }}>
              {selectedNode.group !== 'Normal' && selectedNode.group !== 'Product' ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#f87171' }}>
                  <AlertTriangle size={15} />
                  <span>Member of <b>{selectedNode.group}</b></span>
                </div>
              ) : (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#34d399' }}>
                  <ShieldCheck size={15} />
                  <span>Standard Non-Clustered Topology</span>
                </div>
              )}
            </div>
          </div>

          <div style={{ marginTop: 'auto', fontSize: '0.75rem', color: 'var(--text-faint)' }}>
            * Identifiers are pseudonymized via salted SHA-256 for privacy compliance.
          </div>
        </div>
      )}
    </div>
  );
}
