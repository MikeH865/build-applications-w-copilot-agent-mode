import { useEffect, useMemo, useState } from 'react';

const endpoint = process.env.REACT_APP_CODESPACE_NAME
  ? `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`
  : 'http://localhost:8000/api/activities/';

function Activities() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [activeItem, setActiveItem] = useState(null);

  const fetchData = () => {
    setLoading(true);
    setError(null);
    console.log('Fetching Activities from', endpoint);

    fetch(endpoint)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}`);
        }
        return response.json();
      })
      .then((json) => {
        console.log('Activities response:', json);
        const results = Array.isArray(json) ? json : json.results || [];
        setData(results);
      })
      .catch((fetchError) => {
        console.error('Activities fetch error:', fetchError);
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
          <h2 className="h4 mb-2">Activities</h2>
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
            <label htmlFor="activitiesSearch" className="form-label">
              Search Activities
            </label>
            <input
              id="activitiesSearch"
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
            <p className="mt-3 text-muted">Loading activities...</p>
          </div>
        ) : error ? (
          <div className="alert alert-danger" role="alert">
            <strong>Error:</strong> {error}
          </div>
        ) : filteredData.length === 0 ? (
          <div className="alert alert-info" role="alert">
            No activities found. <button type="button" className="btn btn-sm btn-info" onClick={fetchData}>Retry</button>
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
                          data-bs-target="#activitiesDetailsModal"
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
              Showing <strong>{filteredData.length}</strong> of <strong>{data.length}</strong> activity records
            </div>
          </>
        )}
      </div>

      <div
        className="modal fade"
        id="activitiesDetailsModal"
        tabIndex="-1"
        aria-labelledby="activitiesDetailsModalLabel"
        aria-hidden="true"
      >
        <div className="modal-dialog modal-lg modal-dialog-scrollable">
          <div className="modal-content">
            <div className="modal-header">
              <h5 className="modal-title" id="activitiesDetailsModalLabel">
                Activity Details
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
                  <h6 className="mb-3">Activity Information</h6>
                  <pre>{JSON.stringify(activeItem, null, 2)}</pre>
                </>
              ) : (
                <p className="text-muted">No activity selected.</p>
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

export default Activities;
