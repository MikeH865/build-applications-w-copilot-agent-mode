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
      <div className="card-header d-flex flex-column flex-md-row align-items-md-center justify-content-between gap-3 py-3">
        <div>
          <h2 className="h4 mb-2">Leaderboard</h2>
          <small className="text-muted">
            REST API: <code>{endpoint}</code>
          </small>
        </div>
        <button type="button" className="btn btn-secondary" onClick={fetchData}>
          <i className="bi bi-arrow-clockwise"></i> Refresh
        </button>
      </div>
      <div className="card-body">
        <form className="row g-3 mb-4">
          <div className="col-12">
            <label htmlFor="leaderboardSearch" className="form-label">
              Search Leaderboard
            </label>
            <input
              id="leaderboardSearch"
              type="search"
              className="form-control form-control-lg"
              placeholder="Filter by any field..."
              value={searchTerm}
              onChange={(event) => setSearchTerm(event.target.value)}
            />
          </div>
        </form>

        {loading ? (
          <div className="text-center py-5">
            <div className="spinner-border spinner-border-lg" role="status">
              <span className="visually-hidden">Loading...</span>
            </div>
            <p className="mt-3 text-muted">Loading leaderboard...</p>
          </div>
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            <strong>Error:</strong> {error}
          </div>
        ) : filteredData.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No leaderboard entries found. <button type="button" className="btn btn-sm btn-info" onClick={fetchData}>Retry</button>
          </div>
        ) : (
          <>
            <div className="table-responsive">
              <table className="table table-striped table-hover table-bordered align-middle">
                <thead className="table-light">
                  <tr>
                    <th scope="col" className="text-center" style={{ width: '50px' }}>#</th>
                    {columns.map((column) => (
                      <th scope="col" key={column} className="text-start">
                        {column.charAt(0).toUpperCase() + column.slice(1)}
                      </th>
                    ))}
                    <th scope="col" className="text-center" style={{ width: '100px' }}>
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {filteredData.map((item, index) => (
                    <tr key={item.id || index}>
                      <th scope="row" className="text-center">{index + 1}</th>
                      {columns.map((column) => {
                        const value = item[column];
                        const displayValue =
                          value === null || value === undefined
                            ? '-'
                            : typeof value === 'object'
                            ? JSON.stringify(value)
                            : String(value).length > 50 ? String(value).substring(0, 50) + '...' : value;
                        return <td key={column} className="text-start">{displayValue}</td>;
                      })}
                      <td className="text-center">
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
            <div className="card-footer text-muted text-center py-3">
              Showing <strong>{filteredData.length}</strong> of <strong>{data.length}</strong> leaderboard records
            </div>
          </>
        )}
      </div>

      <div
        className="modal fade"
        id="leaderboardDetailsModal"
        tabIndex="-1"
        aria-labelledby="leaderboardDetailsModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-lg modal-dialog-scrollable">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="leaderboardDetailsModalLabel">
                Leaderboard Entry Details
              </h5>
              <button
                type="button"
                className="btn-close btn-close-white"
                data-bs-dismiss="modal"
                aria-label="Close"
              />
            </div>
            <div className="modal-body">
              {activeItem ? (
                <>
                  <h6 className="mb-3">Leaderboard Information</h6>
                  <pre>{JSON.stringify(activeItem, null, 2)}</pre>
                </>
              ) : (
                <p className="text-muted">No leaderboard entry selected.</p>
              )}
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
