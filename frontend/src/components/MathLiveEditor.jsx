import { useEffect, useRef } from "react";
import "mathlive";

export default function MathLiveEditor({ latexValue, onLatexChange }) {
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
    // React state -> MathLive (two-way sync direction 2).
    if ((mathField.value ?? "") !== latexValue) {
      mathField.value = latexValue;
    }
  }, [latexValue]);

  return (
    <div className="card">
      <h3>Bi-directional editor (LaTeX + MathLive)</h3>
      <textarea value={latexValue} onChange={(event) => onLatexChange(event.target.value)} />
      <div style={{ height: 8 }} />
      <math-field ref={mathFieldRef} />
    </div>
  );
}
