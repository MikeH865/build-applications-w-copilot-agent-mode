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
      <div className="row align-items-center">
        <div className="col-lg-4 text-center mb-4 mb-lg-0">
          <img 
            src={logoSrc} 
            alt="OctoFit Tracker Logo" 
            className="home-logo"
            style={{
              maxWidth: '300px',
              width: '100%',
              filter: 'drop-shadow(0 0 30px rgba(59, 130, 246, 0.4))',
            }}
          />
          <p className="mt-3 text-muted fw-bold">Your Personal Fitness Companion</p>
        </div>
        <div className="col-lg-8">
          <div className="hero-card p-5 rounded-4 shadow-lg">
            <h1 className="display-5 mb-4">Welcome to OctoFit Tracker</h1>
            <p className="lead mb-3">
              Your all-in-one fitness dashboard for tracking activities, monitoring leaderboard performance, managing teams, and reviewing personalized workouts.
            </p>
            <hr className="my-4" style={{ borderColor: 'rgba(59, 130, 246, 0.3)' }} />
            <p className="text-muted mb-4 fs-5">
              Use the navigation menu above to explore each section and view live data pulled directly from your Django REST API backend in real-time.
            </p>
            <div className="d-grid gap-2 d-sm-flex">
              <NavLink to="/activities" className="btn btn-secondary btn-lg px-5">
                Get Started
              </NavLink>
              <NavLink to="/leaderboard" className="btn btn-outline-primary btn-lg px-5">
                View Leaderboard
              </NavLink>
            </div>
          </div>
        </div>
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
                <NavLink className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} to="/activities">
                  Activities
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} to="/leaderboard">
                  Leaderboard
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} to="/teams">
                  Teams
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} to="/users">
                  Users
                </NavLink>
              </li>
              <li className="nav-item">
                <NavLink className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`} to="/workouts">
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
