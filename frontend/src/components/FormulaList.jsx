export default function FormulaList({ formulas, selectedId, onSelect }) {
  return (
    <div className="card">
      <h3>Formulas</h3>
      {formulas.length === 0 && <div>No formulas extracted yet.</div>}
      {formulas.map((formula) => (
        <button
          key={formula.id}
          type="button"
          className={`formula-item ${selectedId === formula.id ? "active" : ""}`}
          onClick={() => onSelect(formula.id)}
        >
          <strong>#{formula.order_index}</strong>
          <div>{formula.latex_content || "(empty)"}</div>
        </button>
      ))}
    </div>
  );
}
