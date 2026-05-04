export default function FormulaList({ formulas, selectedId, onSelect }) {
  return (
    <div className="card formula-list-card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Step 2</p>
          <h3>Extracted formulas</h3>
        </div>
        <span className="badge">{formulas.length}</span>
      </div>
      {formulas.length === 0 && <div>No high-confidence formulas yet.</div>}
      {formulas.map((formula) => (
        <button
          key={formula.id}
          type="button"
          className={`formula-item ${selectedId === formula.id ? "active" : ""}`}
          onClick={() => onSelect(formula.id)}
        >
          <div className="formula-item-top">
            <strong>Formula {formula.order_index}</strong>
            <span>{Math.round((formula.confidence_score ?? 0) * 100)}%</span>
          </div>
          <div className="formula-preview">{formula.latex_content || "(empty candidate)"}</div>
        </button>
      ))}
    </div>
  );
}
