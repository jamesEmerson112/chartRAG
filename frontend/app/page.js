"use client";

// Import required React hooks and components
import { useState } from "react";
import UploadSection from "../components/UploadSection";
import QuestionSection from "../components/QuestionSection";
import MessageSection from "../components/MessageSection";

// Main component: Home page for ChartRAG application
export default function Home() {
  // State variables for file, summary, question, and answer
  const [file, setFile] = useState(null);
  const [summary, setSummary] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  // State variables for message handling
  const [userMessage, setUserMessage] = useState("");
  const [backendResponse, setBackendResponse] = useState("");

  // Handler for file input change event. Sets the selected file.
  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  // Handler for uploading a file to the server.
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
        // Update summary with the response from server
        setSummary(data.summary || "File uploaded successfully.");
      } else {
        const data = await response.json();
        // Show error if file upload fails
        alert(data.error || "Error uploading file.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while uploading the file.");
    }
  };

  // Handler to submit a question to the backend.
  const handleAsk = async () => {
    if (!question) {
      alert("Please enter a question.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });
      if (response.ok) {
        const data = await response.json();
        // Update answer state with the response from server
        setAnswer(data.answer || "No answer received.");
      } else {
        const data = await response.json();
        alert(data.error || "Error getting answer.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while asking the question.");
    }
  };

  // Handler to send a user message to the backend for processing.
  const handleSendMessage = async () => {
    if (!userMessage) {
      alert("Please enter a message.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:5000/process_message", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: userMessage }),
      });
      if (response.ok) {
        const data = await response.json();
        // Update backend response state with the received message.
        setBackendResponse(data.message || "No response received.");
      } else {
        const data = await response.json();
        alert(data.error || "Error processing message.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("An error occurred while sending the message.");
    }
  };

  // Render the home page component with a title, an info box, and an upload section container without extra background.
  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-b from-green-100 to-white">
      <div className="bg-white shadow-md rounded-lg p-6">
          <h1 className="text-5xl font-bold mb-4 text-center">ChartRAG</h1>
        <p className="text-lg mb-8 text-center">
          Upload a csv file and our ai will summarise for you
        </p>
        <div className="flex flex-col items-center">
        <UploadSection summary={summary} setSummary={setSummary} />
        {/* QuestionSection and MessageSection can be added as needed */}
      </div>
      </div>

    </div>
  );
}
