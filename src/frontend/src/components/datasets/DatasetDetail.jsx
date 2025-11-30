/**
 * Display detailed view of a dataset with profile and issues.
 */
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { datasets, profiles, issues, lineage } from '../../utils/api';
import { Loading } from '../common/Loading';
import { Error } from '../common/Error';
import { DatasetProfile } from './DatasetProfile';
import { IssueList } from '../issues/IssueList';
import { LineageGraph } from '../lineage/LineageGraph';
import '../styles/DatasetDetail.css';

export function DatasetDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [dataset, setDataset] = useState(null);
  const [profile, setProfile] = useState(null);
  const [datasetIssues, setIssues] = useState([]);
  const [lineageData, setLineageData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('profile');

  useEffect(() => {
    fetchData();
  }, [id]);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [dsRes, profRes, issuesRes, lineRes] = await Promise.all([
        datasets.get(id),
        profiles.latest(id),
        issues.byDataset(id),
        lineage.get(id),
      ]);

      setDataset(dsRes.data);
      setProfile(profRes.data);
      setIssues(issuesRes.data);
      setLineageData(lineRes.data);
      setError(null);
    } catch (err) {
      setError('Failed to load dataset details');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <Error message={error} onRetry={fetchData} />;

  return (
    <div className="dataset-detail">
      <button className="btn-back" onClick={() => navigate('/')}>
        ← Back to Datasets
      </button>

      {dataset && (
        <div className="dataset-header">
          <h1>{dataset.name}</h1>
          <div className="dataset-meta">
            <span>📊 {dataset.row_count} rows</span>
            <span>📋 {dataset.column_count} columns</span>
            <span>📅 {new Date(dataset.created_at).toLocaleDateString()}</span>
          </div>
        </div>
      )}

      <div className="tabs">
        {['profile', 'issues', 'lineage'].map((tab) => (
          <button
            key={tab}
            className={`tab ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab.charAt(0).toUpperCase() + tab.slice(1)}
          </button>
        ))}
      </div>

      <div className="tab-content">
        {activeTab === 'profile' && profile && <DatasetProfile profile={profile} />}
        {activeTab === 'issues' && <IssueList issues={datasetIssues} />}
        {activeTab === 'lineage' && lineageData && (
          <LineageGraph lineageData={lineageData} />
        )}
      </div>
    </div>
  );
}
