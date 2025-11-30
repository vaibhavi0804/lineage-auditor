import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Header } from './components/common/Header';
import { DatasetList } from './components/datasets/DatasetList';
import { DatasetDetail } from './components/datasets/DatasetDetail';
import { IssueList } from './components/issues/IssueList';
import './App.css';

function App() {
  return (
    <Router>
      <Header />
      <main>
        <Routes>
          <Route path="/" element={<DatasetList />} />
          <Route path="/datasets/:id" element={<DatasetDetail />} />
          <Route path="/issues" element={<IssueList issues={[]} />} />
        </Routes>
      </main>
    </Router>
  );
}

export default App;
