/**
 * Display dataset profile (statistics and metadata).
 */
import React from 'react';
import '../styles/DatasetProfile.css';

export function DatasetProfile({ profile }) {
  const { columns_metadata, statistics, sample_rows } = profile;

  return (
    <div className="dataset-profile">
      <section className="profile-section">
        <h3>Column Metadata</h3>
        <div className="table-responsive">
          <table className="metadata-table">
            <thead>
              <tr>
                <th>Column</th>
                <th>Type</th>
                <th>Nulls</th>
                <th>Cardinality</th>
              </tr>
            </thead>
            <tbody>
              {columns_metadata &&
                Object.entries(columns_metadata).map(([col, meta]) => (
                  <tr key={col}>
                    <td>{col}</td>
                    <td>{meta.dtype}</td>
                    <td>
                      {meta.null_count} ({meta.null_percentage.toFixed(1)}%)
                    </td>
                    <td>{meta.cardinality}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="profile-section">
        <h3>Statistics</h3>
        <div className="table-responsive">
          <table className="stats-table">
            <thead>
              <tr>
                <th>Column</th>
                <th>Mean</th>
                <th>Std Dev</th>
                <th>Min</th>
                <th>Max</th>
              </tr>
            </thead>
            <tbody>
              {statistics &&
                Object.entries(statistics).map(([col, stats]) => (
                  <tr key={col}>
                    <td>{col}</td>
                    <td>{stats.mean?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.std?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.min?.toFixed(2) || 'N/A'}</td>
                    <td>{stats.max?.toFixed(2) || 'N/A'}</td>
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>

      <section className="profile-section">
        <h3>Sample Rows</h3>
        <div className="table-responsive">
          <table className="sample-table">
            <thead>
              <tr>
                {sample_rows && sample_rows[0] &&
                  Object.keys(sample_rows[0]).map((col) => <th key={col}>{col}</th>)}
              </tr>
            </thead>
            <tbody>
              {sample_rows &&
                sample_rows.map((row, idx) => (
                  <tr key={idx}>
                    {Object.values(row).map((val, i) => (
                      <td key={i}>{String(val).substring(0, 50)}</td>
                    ))}
                  </tr>
                ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
