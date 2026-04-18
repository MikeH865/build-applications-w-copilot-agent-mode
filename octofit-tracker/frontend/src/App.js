import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Teams from './components/Teams';
import Users from './components/Users';
import Workouts from './components/Workouts';

const logoSrc = `${process.env.PUBLIC_URL}/octofitapp-small.svg`;

function Home() {
  return (
    <div className="container py-5">
      <div className="hero-card p-4 rounded-4 shadow-lg">
        <h1 className="display-5 text-white mb-3">Welcome to OctoFit Tracker</h1>
        <p className="lead text-info-light">
          Track activities, compare leaderboard performance, manage teams, and review workouts from your REST API.
        </p>
        <p className="text-muted">
          Use the navigation menu above to open each section and view live data pulled from your Django backend.
        </p>
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar navbar-expand-lg navbar-dark navbar-custom shadow-sm">
        <div className="container-fluid">
          <NavLink className="navbar-brand d-flex align-items-center gap-3" to="/">
            <img src={logoSrc} alt="OctoFit logo" className="octo-logo" />
            <div>
              <div className="brand-title">OctoFit Tracker</div>
              <small className="text-info-light brand-subtitle">Fitness dashboard</small>
            </div>
          </NavLink>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon" />
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <NavLink className="nav-link" to="/activities">
                  Activities
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/leaderboard">
                  Leaderboard
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/teams">
                  Teams
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/users">
                  Users
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className="nav-link" to="/workouts">
                  Workouts
                </NavLink>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <main className="container mt-4">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/users" element={<Users />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>
      </main>
    </BrowserRouter>
  );
}

export default App;
