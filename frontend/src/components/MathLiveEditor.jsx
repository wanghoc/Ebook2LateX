import { useEffect, useRef } from "react";
import "mathlive";

export default function MathLiveEditor({
  latexValue,
  onLatexChange,
  disabled = false,
  onSaveCurrent,
  canSaveCurrent = false,
  savingCurrent = false
}) {
  const mathFieldRef = useRef(null);

  useEffect(() => {
    const mathField = mathFieldRef.current;
    if (!mathField) {
      return undefined;
    }

    // MathLive -> React state (two-way sync direction 1).
    const handleInput = () => {
      onLatexChange(mathField.value ?? "");
    };

    mathField.addEventListener("input", handleInput);
    return () => {
      mathField.removeEventListener("input", handleInput);
    };
  }, [onLatexChange]);

  useEffect(() => {
    const mathField = mathFieldRef.current;
    if (!mathField) {
      return;
    }
    mathField.disabled = disabled;
    // React state -> MathLive (two-way sync direction 2).
    if ((mathField.value ?? "") !== latexValue) {
      mathField.value = latexValue;
    }
  }, [disabled, latexValue]);

  return (
    <div className="card editor-card">
      <div className="card-header">
        <div>
          <p className="eyebrow">Step 3</p>
          <h3>Edit LaTeX</h3>
        </div>
        <span className="badge">MathLive</span>
      </div>
      <p className="muted">Use the editor below to clean the current candidate. The raw LaTeX updates automatically.</p>
      <math-field ref={mathFieldRef} className={disabled ? "is-disabled" : ""} />
      <div className="latex-preview">
        <span>LaTeX</span>
        <code>{latexValue || "(empty)"}</code>
      </div>
      <div className="controls save-row">
        <button type="button" className="secondary" onClick={onSaveCurrent} disabled={!canSaveCurrent || savingCurrent || disabled}>
          {savingCurrent ? "Saving..." : "Save this formula"}
        </button>
      </div>
    </div>
  );
}
