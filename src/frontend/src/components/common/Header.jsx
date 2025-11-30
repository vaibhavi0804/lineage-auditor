/**
 * Header component with navigation.
 */
import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Header.css';

export function Header() {
  return (
    <header className="header">
      <div className="header-container">
        <Link to="/" className="header-logo">
          <h1>📊 Lineage Auditor</h1>
        </Link>
        <nav className="header-nav">
          <Link to="/">Datasets</Link>
          <Link to="/issues">Issues</Link>
          <Link to="/about">About</Link>
        </nav>
      </div>
    </header>
  );
}
