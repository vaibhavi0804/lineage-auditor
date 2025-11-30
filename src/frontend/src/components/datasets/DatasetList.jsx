/**
 * Display list of datasets with upload functionality.
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { datasets } from '../../utils/api';
import { Loading } from '../common/Loading';
import { Error } from '../common/Error';
import '../styles/DatasetList.css';

export function DatasetList() {
  const [datasetList, setDatasetList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [uploading, setUploading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDatasets();
  }, []);

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const response = await datasets.list();
      setDatasetList(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to load datasets');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      const response = await datasets.upload(file);
      setDatasetList([...datasetList, response.data]);
      setUploading(false);
      // Reset input
      event.target.value = '';
    } catch (err) {
      setError(`Upload failed: ${err.message}`);
      setUploading(false);
    }
  };

  if (loading) return <Loading />;
  if (error) return <Error message={error} onRetry={fetchDatasets} />;

  return (
    <div className="dataset-list">
      <div className="dataset-header">
        <h2>Datasets</h2>
        <label className="btn-upload">
          📤 Upload Dataset
          <input
            type="file"
            accept=".csv,.parquet"
            onChange={handleFileUpload}
            disabled={uploading}
            hidden
          />
        </label>
      </div>

      {uploading && <p className="uploading">Uploading...</p>}

      {datasetList.length === 0 ? (
        <p className="empty-state">No datasets yet. Upload one to get started!</p>
      ) : (
        <div className="dataset-grid">
          {datasetList.map((ds) => (
            <div
              key={ds.id}
              className="dataset-card"
              onClick={() => navigate(`/datasets/${ds.id}`)}
            >
              <h3>{ds.name}</h3>
              <p className="meta">
                📊 {ds.row_count || '?'} rows × {ds.column_count || '?'} columns
              </p>
              <p className="created">
                {new Date(ds.created_at).toLocaleDateString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
