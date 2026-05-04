import { useMemo, useState } from "react";

import FormulaList from "./components/FormulaList";
import MathLiveEditor from "./components/MathLiveEditor";
import PDFUploader from "./components/PDFUploader";
import SavedFormulas from "./components/SavedFormulas";
import { submitDocument, updateFormula, uploadPdf } from "./services/api";

export default function App() {
  const [documentId, setDocumentId] = useState(null);
  const [formulas, setFormulas] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [statusMessage, setStatusMessage] = useState("Ready.");
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [showLowConfidence, setShowLowConfidence] = useState(false);
  const [showSavedView, setShowSavedView] = useState(false);

  const selectedFormula = useMemo(
    () => formulas.find((item) => item.id === selectedId) ?? null,
    [formulas, selectedId]
  );

  const selectedIndex = useMemo(
    () => formulas.findIndex((item) => item.id === selectedId),
    [formulas, selectedId]
  );

  const visibleFormulas = useMemo(
    () =>
      formulas.filter(
        (formula) => showLowConfidence || formula.confidence_score == null || formula.confidence_score >= 0.65
      ),
    [formulas, showLowConfidence]
  );

  const isBusy = uploading || saving;

  const goToFormula = (offset) => {
    if (visibleFormulas.length === 0) {
      return;
    }

    const currentIndex = visibleFormulas.findIndex((item) => item.id === selectedId);
    const safeIndex = currentIndex >= 0 ? currentIndex : 0;
    const nextIndex = (safeIndex + offset + visibleFormulas.length) % visibleFormulas.length;
    setSelectedId(visibleFormulas[nextIndex].id);
  };

  const handleUpload = async (file) => {
    setUploading(true);
    setStatusMessage("Uploading and extracting formulas...");
    try {
      const data = await uploadPdf(file);
      setDocumentId(data.document_id);
      setFormulas(data.formulas);
      setSelectedId(data.formulas[0]?.id ?? null);
      setStatusMessage(
        `Done. Extracted ${data.formula_count} candidates. Low-confidence items are hidden by default.`
      );
    } catch (error) {
      setStatusMessage(error.response?.data?.detail || error.message || "Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const handleLatexChange = (value) => {
    if (!selectedFormula) {
      return;
    }

    // Keep the selected formula in local state in sync with editor input.
    setFormulas((current) =>
      current.map((item) => (item.id === selectedFormula.id ? { ...item, latex_content: value } : item))
    );
  };

  const handleSaveCurrent = async () => {
    if (!selectedFormula) {
      setStatusMessage("Please select a formula first.");
      return;
    }

    setSaving(true);
    setStatusMessage("Saving current formula...");
    try {
      const result = await updateFormula(selectedFormula.id, selectedFormula.latex_content || "\\text{}");
      setFormulas((current) => current.map((item) => (item.id === result.id ? { ...item, ...result } : item)));
      setStatusMessage("Current formula saved to the database.");
    } catch (error) {
      setStatusMessage(error.response?.data?.detail || error.message || "Save failed.");
    } finally {
      setSaving(false);
    }
  };

  const handleSubmit = async () => {
    if (!documentId) {
      setStatusMessage("Please upload a PDF first.");
      return;
    }

    if (formulas.length === 0) {
      setStatusMessage("No formulas were extracted from this PDF.");
      return;
    }

    setSaving(true);
    setStatusMessage("Submitting formulas...");
    try {
      // Send all edited formulas in one API call to mark document as completed.
      const payload = formulas.map((item) => ({
        id: item.id,
        latex_content: item.latex_content || "\\text{}"
      }));
      const result = await submitDocument(documentId, payload);
      setStatusMessage(`Submitted. Updated ${result.updated_count} formulas.`);
    } catch (error) {
      setStatusMessage(error.response?.data?.detail || error.message || "Submit failed.");
    } finally {
      setSaving(false);
    }
  };

  const handleOpenSaved = (formula) => {
    // Ensure formula is present in local list and select it
    setFormulas((current) => {
      const exists = current.find((f) => f.id === formula.id);
      if (exists) return current;
      return [...current, formula];
    });
    setSelectedId(formula.id);
    setShowSavedView(false);
  };

  return (
    <div className="app-shell">
      <main className="container">
        <section className="hero card">
          <div>
            <p className="eyebrow">PDF to LaTeX review flow</p>
            <h1 className="title">Ebook2LateX</h1>
            <p className="lead">
              Upload a PDF, review the extracted formulas, fix any noisy characters, and submit the final LaTeX.
            </p>
          </div>

          <div className="hero-stats">
            <div className="stat">
              <span>Formulas</span>
              <strong>{formulas.length}</strong>
            </div>
            <div className="stat">
              <span>State</span>
              <strong>{uploading ? "Uploading" : saving ? "Saving" : documentId ? "Ready" : "Idle"}</strong>
            </div>
          </div>
        </section>

        <section className="workflow-grid">
          <div className="stack">
            <PDFUploader onUpload={handleUpload} uploading={uploading} />

            <div className="card steps-card">
              <h3>How to use</h3>
              <ol>
                <li>Upload one PDF document.</li>
                <li>Select a formula from the list.</li>
                <li>Edit it in the LaTeX editor.</li>
                <li>Submit when everything looks right.</li>
              </ol>
            </div>
          </div>

          <div className="stack">
            <div className="card editor-toolbar">
              <div>
                <h3>Formula review</h3>
                <p>
                  {visibleFormulas.length > 0
                    ? `Reviewing formula ${visibleFormulas.findIndex((item) => item.id === selectedId) + 1 || 1} of ${visibleFormulas.length}`
                    : "No formulas extracted yet."}
                </p>
              </div>

              <div className="controls">
                <button
                  type="button"
                  className="secondary"
                  onClick={() => setShowSavedView((s) => !s)}
                  disabled={!documentId || isBusy}
                >
                  {showSavedView ? "Hide saved" : "View saved formulas"}
                </button>
                <button
                  type="button"
                  className="secondary"
                  onClick={() => setShowLowConfidence((current) => !current)}
                  disabled={isBusy || formulas.length === 0}
                >
                  {showLowConfidence ? "Hide low confidence" : "Show all candidates"}
                </button>
                <button type="button" className="secondary" onClick={() => goToFormula(-1)} disabled={isBusy || formulas.length === 0}>
                  Previous
                </button>
                <button type="button" className="secondary" onClick={() => goToFormula(1)} disabled={isBusy || formulas.length === 0}>
                  Next
                </button>
              </div>
            </div>

            <div className="grid">
              {showSavedView ? (
                <SavedFormulas documentId={documentId} onOpen={handleOpenSaved} onClose={() => setShowSavedView(false)} />
              ) : (
                <FormulaList formulas={visibleFormulas} selectedId={selectedId} onSelect={setSelectedId} />
              )}
              <div className="editor-column">
                <MathLiveEditor
                  latexValue={selectedFormula?.latex_content || ""}
                  onLatexChange={handleLatexChange}
                  disabled={visibleFormulas.length === 0}
                  onSaveCurrent={handleSaveCurrent}
                  canSaveCurrent={Boolean(selectedFormula)}
                  savingCurrent={saving}
                />

                <div className="controls submit-row">
                  <button className="primary" type="button" onClick={handleSubmit} disabled={saving || visibleFormulas.length === 0}>
                    Submit all formulas
                  </button>
                </div>

                <div className="status">{statusMessage}</div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
