import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Home from './sites/home';

function App() {
  return (
    <Router>
      <nav style={{ padding: "1rem", background: "#f0f0f0" }}>
        <Link to="/" style={{ marginRight: "1rem" }}>Home</Link>
      </nav>

      <div style={{ padding: "2rem" }}>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
