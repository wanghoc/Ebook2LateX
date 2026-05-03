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
    <div className="card">
      <h3>Upload PDF</h3>
      <input type="file" accept=".pdf,application/pdf" onChange={handleChange} disabled={uploading} />
    </div>
  );
}
