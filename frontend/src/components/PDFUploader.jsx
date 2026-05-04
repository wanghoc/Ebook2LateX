export default function PDFUploader({ onUpload, uploading }) {
  const handleChange = async (event) => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    await onUpload(file);
    event.target.value = "";
  };

  return (
    <div className="card upload-card">
      <p className="eyebrow">Step 1</p>
      <h3>Upload a PDF</h3>
      <p className="muted">Choose one PDF file. The app will extract likely formulas automatically.</p>
      <label className={`upload-button ${uploading ? "disabled" : ""}`}>
        <input type="file" accept=".pdf,application/pdf" onChange={handleChange} disabled={uploading} />
        <span>{uploading ? "Processing..." : "Choose PDF file"}</span>
      </label>
    </div>
  );
}
