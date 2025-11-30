/**
 * Display dataset lineage graph.
 */
import React from 'react';
import '../styles/LineageGraph.css';

export function LineageGraph({ lineageData }) {
  const { upstream, downstream } = lineageData;

  return (
    <div className="lineage-graph">
      <section className="lineage-section">
        <h3>📥 Upstream (Data Sources)</h3>
        {upstream && upstream.length > 0 ? (
          <div className="lineage-list">
            {upstream.map((edge, idx) => (
              <div key={idx} className="lineage-edge">
                <div className="lineage-dataset">{edge.source_id}</div>
                <div className="lineage-arrow">→</div>
                <div className="lineage-job">
                  {edge.job_name || edge.job_type || 'Unknown Job'}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No upstream dependencies</p>
        )}
      </section>

      <section className="lineage-section">
        <h3>📤 Downstream (Consumers)</h3>
        {downstream && downstream.length > 0 ? (
          <div className="lineage-list">
            {downstream.map((edge, idx) => (
              <div key={idx} className="lineage-edge">
                <div className="lineage-job">
                  {edge.job_name || edge.job_type || 'Unknown Job'}
                </div>
                <div className="lineage-arrow">→</div>
                <div className="lineage-dataset">{edge.target_id}</div>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No downstream dependencies</p>
        )}
      </section>
    </div>
  );
}
