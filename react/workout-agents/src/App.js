import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './sites/home';
import Header from './components/nav';

function App() {
  return (
    <Router>
        {/* <Header /> */}
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
