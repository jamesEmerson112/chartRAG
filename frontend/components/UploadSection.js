"use client";

import { useState, useRef } from "react";

/**
 * UploadSection component allows users to upload a CSV file
 * and displays a summary of the uploaded data.
 *
 * @param {string} summary - The summary of the uploaded file.
 * @param {function} setSummary - Function to update the summary state.
 */
export default function UploadSection({ summary, setSummary }) {
  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  /**
   * Handles the file input change event.
   * Automatically uploads the selected file.
   *
   * @param {object} e - The event object.
   */
  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      handleUpload(selectedFile);
    }
  };

  /**
   * Handles the upload process.
   *
   * @param {File} selectedFile - The file to upload.
   */
  const handleUpload = async (selectedFile) => {
    const uploadFile = selectedFile || file;
    if (!uploadFile) {
      alert("Please select a file first.");
      return;
    }
    const formData = new FormData();
    formData.append("datafile", uploadFile);

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
        alert(data.error || 'Error uploading file.');
      }
    } catch (error) {
      console.error("Error:", error);
      alert('An error occurred while uploading the file.');
    }
  };

  /**
   * Handles the button click event.
   * Triggers the hidden file input.
   */
  const handleButtonClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="flex items-center space-x-4">
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        onClick={handleButtonClick}
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
