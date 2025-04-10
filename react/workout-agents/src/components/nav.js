import { Link } from 'react-router-dom';

function Nav() {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-blue-700 shadow-md py-4">
      <div className="max-w-7xl mx-auto px-4 flex flex-col items-center text-white">
        <h1 className="text-3xl font-bold mb-2 text-center tracking-wide">🏋️‍♀️ Workout Efficiency Evaluator</h1>

        <nav className="flex space-x-6 text-lg font-medium">
          <Link to="/" className="hover:text-yellow-300 transition">Domov</Link>
          <Link to="/predict" className="hover:text-yellow-300 transition">Napoved</Link>
          <Link to="/about" className="hover:text-yellow-300 transition">O projektu</Link>
        </nav>
      </div>
    </header>
  );
}

export default Nav;
