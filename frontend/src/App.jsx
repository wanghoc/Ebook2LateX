import { useMemo, useState } from "react";

import FormulaList from "./components/FormulaList";
import MathLiveEditor from "./components/MathLiveEditor";
import PDFUploader from "./components/PDFUploader";
import { submitDocument, uploadPdf } from "./services/api";

export default function App() {
  const [documentId, setDocumentId] = useState(null);
  const [formulas, setFormulas] = useState([]);
  const [selectedId, setSelectedId] = useState(null);
  const [statusMessage, setStatusMessage] = useState("Ready.");
  const [uploading, setUploading] = useState(false);
  const [saving, setSaving] = useState(false);

  const selectedFormula = useMemo(
    () => formulas.find((item) => item.id === selectedId) ?? null,
    [formulas, selectedId]
  );

  const handleUpload = async (file) => {
    setUploading(true);
    setStatusMessage("Uploading and extracting formulas...");
    try {
      const data = await uploadPdf(file);
      setDocumentId(data.document_id);
      setFormulas(data.formulas);
      setSelectedId(data.formulas[0]?.id ?? null);
      setStatusMessage(`Done. Extracted ${data.formula_count} formulas.`);
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

  const handleSubmit = async () => {
    if (!documentId) {
      setStatusMessage("Please upload a PDF first.");
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

  return (
    <div className="container">
      <h1 className="title">Ebook2LateX</h1>
      <PDFUploader onUpload={handleUpload} uploading={uploading} />

      <div className="grid">
        <FormulaList formulas={formulas} selectedId={selectedId} onSelect={setSelectedId} />
        <div>
          <MathLiveEditor latexValue={selectedFormula?.latex_content || ""} onLatexChange={handleLatexChange} />
          <div className="controls">
            <button className="primary" type="button" onClick={handleSubmit} disabled={saving}>
              Submit to Database
            </button>
          </div>
          <div className="status">{statusMessage}</div>
        </div>
      </div>
    </div>
  );
}
