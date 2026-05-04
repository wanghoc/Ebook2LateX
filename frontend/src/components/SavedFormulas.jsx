import { useEffect, useState } from "react";
import { getDocumentFormulas, deleteFormula } from "../services/api";

export default function SavedFormulas({ documentId, onOpen, onClose }) {
  const [loading, setLoading] = useState(false);
  const [formulas, setFormulas] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!documentId) return;
    fetchFormulas();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [documentId]);

  async function fetchFormulas() {
    setLoading(true);
    setError(null);
    try {
      const data = await getDocumentFormulas(documentId);
      // Expecting an array of formulas
      setFormulas(data.formulas ?? data);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || "Failed to load formulas");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="card saved-formulas">
      <div className="saved-header">
        <h3>Saved formulas</h3>
        <div className="controls">
          <button className="secondary" onClick={fetchFormulas} disabled={loading || !documentId}>
            Refresh
          </button>
          <button className="secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>

      {!documentId && <div>Please upload a document first to view saved formulas.</div>}

      {error && <div className="error">{error}</div>}

      {loading && <div>Loading...</div>}

      {!loading && formulas.length === 0 && <div>No saved formulas found for this document.</div>}

      <ul className="saved-list">
        {formulas.map((f) => (
          <li key={f.id} className="saved-item">
            <div className="saved-meta">
              <strong>#{f.id}</strong>
              <span className="confidence">{f.confidence_score != null ? Math.round(f.confidence_score * 100) + "%" : "-"}</span>
            </div>
            <div className="saved-latex">{f.latex_content || "(empty)"}</div>
            <div className="saved-actions">
              <button
                className="secondary"
                onClick={() => {
                  if (onOpen) onOpen(f);
                }}
              >
                Open in editor
              </button>
              <button
                className="danger"
                onClick={async () => {
                  if (!confirm("Delete this formula? This action cannot be undone.")) return;
                  try {
                    await deleteFormula(f.id);
                    // remove from local list
                    setFormulas((cur) => cur.filter((x) => x.id !== f.id));
                  } catch (err) {
                    setError(err.response?.data?.detail || err.message || "Delete failed.");
                  }
                }}
              >
                Delete
              </button>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
