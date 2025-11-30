/**
 * Display list of detected issues.
 */
import React from 'react';
import '../styles/IssueList.css';

const SEVERITY_COLORS = {
  low: '#52c41a',
  medium: '#faad14',
  high: '#ff7a45',
  critical: '#f5222d',
};

const ISSUE_ICONS = {
  schema_change: '🔄',
  distribution_drift: '📈',
  semantic_drift: '🏷️',
  null_spike: '❌',
  cardinality_anomaly: '📊',
  label_flip: '🔀',
};

export function IssueList({ issues }) {
  if (!issues || issues.length === 0) {
    return (
      <div className="issue-list">
        <p className="empty-state">✅ No issues detected!</p>
      </div>
    );
  }

  return (
    <div className="issue-list">
      <div className="issues-header">
        <h3>Detected Issues ({issues.length})</h3>
      </div>

      {issues.map((issue) => (
        <div key={issue.id} className="issue-card">
          <div
            className="issue-severity"
            style={{ backgroundColor: SEVERITY_COLORS[issue.severity] }}
          ></div>

          <div className="issue-content">
            <div className="issue-title">
              <span className="issue-icon">
                {ISSUE_ICONS[issue.issue_type] || '⚠️'}
              </span>
              <span className="issue-type">{issue.issue_type}</span>
              {issue.column_name && (
                <span className="issue-column">Column: {issue.column_name}</span>
              )}
            </div>

            <p className="issue-description">{issue.description}</p>

            {issue.evidence && (
              <details className="issue-evidence">
                <summary>View Evidence</summary>
                <pre>{JSON.stringify(issue.evidence, null, 2)}</pre>
              </details>
            )}

            <div className="issue-footer">
              <span className="issue-severity-label">{issue.severity}</span>
              <span className="issue-date">
                {new Date(issue.detected_at).toLocaleString()}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
