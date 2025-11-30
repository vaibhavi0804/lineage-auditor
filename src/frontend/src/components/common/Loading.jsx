/**
 * Loading spinner component.
 */
import React from 'react';
import '../styles/Loading.css';

export function Loading() {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>Loading...</p>
    </div>
  );
}
