"use client";

import { useState, useRef, useEffect } from "react";

/**
 * UploadSection component allows users to upload a CSV file
 * and displays a summary of the uploaded data.
 *
 * @param {string} summary - The summary of the uploaded file.
 * @param {function} setSummary - Function to update the summary state.
 */
export default function UploadSection({ summary, setSummary }) {
  const [file, setFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [details, setDetails] = useState(null);
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

    setIsUploading(true);
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
    } finally {
      setIsUploading(false);
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

  useEffect(() => {
    if (summary && !details) {
      const timer = setTimeout(async () => {
        try {
          const detailsResponse = await fetch("http://127.0.0.1:5000/details");
          if (detailsResponse.ok) {
            const detailsData = await detailsResponse.json();
            setDetails(detailsData);
          } else {
            console.error("Failed to fetch details");
          }
        } catch (error) {
          console.error("Error fetching details:", error);
        }
      }, 3000);
      return () => clearTimeout(timer);
    }
  }, [summary, details]);

  return (
    <div className="flex items-center space-x-4">
      <input
        type="file"
        accept=".csv"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
      />
      {!summary && (
        <>
          <button
            onClick={handleButtonClick}
            className="ml-2 px-4 py-2 bg-blue-600 hover:bg-blue-800 text-white rounded transform transition duration-250 hover:scale-95"
          >
            Upload
          </button>
        </>
      )}
      {isUploading && (
        <div className="ml-4 w-6 h-6 border-4 border-blue-600 border-t-transparent border-l-transparent rounded-full animate-spin"></div>
      )}
      {summary && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">Summary:</h3>
          <p className="whitespace-pre-wrap">{summary}</p>
        </div>
      )}
      {details && (
        <div className="mt-4">
          <h3 className="text-lg font-semibold">Graph:</h3>
          <div dangerouslySetInnerHTML={{ __html: details.graph_html }} />
          <h3 className="text-lg font-semibold mt-4">Data Table:</h3>
          <div dangerouslySetInnerHTML={{ __html: details.table }} />
        </div>
      )}
    </div>
  );
}
