// frontend/components/UploadSection.js

"use client";

import { useState } from "react";

/**
 * UploadSection component allows users to upload a CSV file
 * and displays a summary of the uploaded data.
 *
 * @param {string} summary - The summary of the uploaded file.
 * @param {function} setSummary - Function to update the summary state.
 */
export default function UploadSection({ summary, setSummary }) {
  const [file, setFile] = useState(null);

  /**
   * Handles the file input change event.
   * Sets the selected file to the state.
   *
   * @param {object} e - The event object.
   */
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  /**
   * Handles the upload button click event.
   * Uploads the selected file to the server and updates the summary.
   */
  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("datafile", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });
      if (response.ok) {
        const data = await response.json();
        setSummary(data.summary || "File uploaded successfully.");
      } else {
        const data = await response.json();
        alert(data.error || "Error uploading file.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  return (
    <div className="mb-8 bg-background text-foreground">
      <p className="text-lg mb-8 text-center">
        Upload a csv file and our ai will summarise for you
      </p>
      <input type="file" accept=".csv" onChange={handleFileChange} />
      <button
        onClick={handleUpload}
        className="ml-2 px-4 py-2 bg-blue-500 text-white rounded"
      >
        Upload Data
      </button>
      {summary && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">Summary:</h3>
          <p className="whitespace-pre-wrap">{summary}</p>
        </div>
      )}
    </div>
  );
}
