import { Link } from 'react-router-dom';

function Nav() {
  return (
    <header className="bg-white border-b shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-4 flex flex-col items-center">
        <h1 className="text-5xl font-semibold text-gray-800 mb-2 text-center">
          Workout Efficiency Evaluator
        </h1>
        <nav className="flex space-x-6 text-base font-medium text-gray-700">
          <Link to="/" className="hover:text-blue-600 transition">Domov</Link>
        </nav>
      </div>
    </header>
  );
}

export default Nav;
