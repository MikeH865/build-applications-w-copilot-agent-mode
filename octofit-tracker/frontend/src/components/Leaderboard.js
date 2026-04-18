import { useEffect, useMemo, useState } from 'react';

const COMPONENT_NAME = 'leaderboard';
const API_BASE = process.env.REACT_APP_CODESPACE_NAME
  ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api`
  : 'http://localhost:8000/api';
const endpoint = `${API_BASE}/${COMPONENT_NAME}/`;

function Leaderboard() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeItem, setActiveItem] = useState(null);

  const fetchData = () => {
    setLoading(true);
    setError(null);
    console.log('Fetching Leaderboard from', endpoint);

    fetch(endpoint)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((json) => {
        console.log('Leaderboard response:', json);
        const results = Array.isArray(json) ? json : json.results || [];
        setData(results);
      })
      .catch((fetchError) => {
        console.error('Leaderboard fetch error:', fetchError);
        setError(fetchError.message);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const filteredData = useMemo(
    () => data.filter((item) => JSON.stringify(item).toLowerCase().includes(searchTerm.toLowerCase())),
    [data, searchTerm]
  );

  const columns = filteredData.length > 0 ? Object.keys(filteredData[0]) : [];

  const openDetails = (item) => setActiveItem(item);

  return (
    <div className="card mb-4 shadow-sm">
      <div className="card-header d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3">
        <div>
          <h2 className="h4 mb-1">Leaderboard</h2>
          <small className="text-muted">
            REST API endpoint: <code>{endpoint}</code>
          </small>
        </div>
        <button type="button" className="btn btn-secondary" onClick={fetchData}>
          Refresh
        </button>
      </div>
      <div className="card-body">
        <form className="row g-3 mb-4">
          <div className="col-md-8">
            <label htmlFor="leaderboardSearch" className="form-label">
              Filter leaderboard entries
            </label>
            <input
              id="leaderboardSearch"
              type="search"
              className="form-control"
              placeholder="Search leaderboard data"
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
            />
          </div>
        </form>

        {loading ? (
          <div className="text-center py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
          </div>
        ) : error ? (
          <div className="alert alert-danger">{error}</div>
        ) : (
          <div className="table-responsive">
            <table className="table table-striped table-hover table-bordered align-middle mb-0">
              <thead className="table-light">
                <tr>
                  <th scope="col">#</th>
                  {columns.map((column) => (
                    <th scope="col" key={column}>{column}</th>
                  ))}
                  <th scope="col">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.map((item, index) => (
                  <tr key={item.id || index}>
                    <th scope="row">{index + 1}</th>
                    {columns.map((column) => {
                      const value = item[column];
                      const displayValue =
                        value === null || value === undefined
                          ? ''
                          : typeof value === 'object'
                          ? JSON.stringify(value)
                          : value;
                      return <td key={column}>{displayValue}</td>;
                    })}
                    <td>
                      <button
                        type="button"
                        className="btn btn-sm btn-outline-primary"
                        data-bs-toggle="modal"
                        data-bs-target="#leaderboardDetailsModal"
                        onClick={() => openDetails(item)}
                      >
                        View
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
      <div className="card-footer text-muted">
        Showing {filteredData.length} of {data.length} leaderboard records.
      </div>

      <div className="modal fade" id="leaderboardDetailsModal" tabIndex="-1" aria-labelledby="leaderboardDetailsModalLabel" aria-hidden="true">
        <div className="modal-dialog modal-lg modal-dialog-scrollable">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="leaderboardDetailsModalLabel">
                Leaderboard details
              </h5>
              <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close" />
            </div>
            <div className="modal-body">
              {activeItem ? <pre>{JSON.stringify(activeItem, null, 2)}</pre> : <p>No leaderboard item selected.</p>}
            </div>
            <div className="modal-footer">
              <button type="button" className="btn btn-secondary" data-bs-dismiss="modal">
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Leaderboard;
