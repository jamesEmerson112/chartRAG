# Data Analyzer Frontend

This frontend application is built using Next.js and Tailwind CSS to provide a minimalist, user-friendly interface for uploading and analyzing CSV data. It is designed for non-technical users with a simple, clear layout and intuitive controls.

## Overview

- **Minimalist Design:**
  The homepage focuses on simplicity, featuring a single, prominent upload button as the primary interactive element. Other functionalities, such as asking questions, are available through additional components but are de-emphasized to maintain clarity.

- **File Upload:**
  Users can upload CSV files via the UploadSection component. The uploaded file is sent to a backend service for processing, with feedback displayed directly on the interface.

- **Dynamic Components and Feedback:**
  The application uses React state management to dynamically display components and feedback. For example, once a file is uploaded, a summary is shown to the user. Similarly, users can submit questions through the QuestionSection component, which communicates with the backend to retrieve responses.

- **HTTP Communication:**
  Frontend components interact with the backend using HTTP requests. Endpoints include:
  - **Upload:** `POST http://127.0.0.1:5000/upload`
  - **Ask Question:** `POST http://127.0.0.1:5000/ask`
  - **Process Message:** `POST http://127.0.0.1:5000/process_message` (currently integrated into the code but not prominently displayed)

## Project Structure

```
frontend/
├── app/
│   └── page.js              // Main page rendering the homepage with imported components
├── components/
│   ├── UploadSection.js     // Handles CSV file selection and upload; displays upload summary
│   ├── QuestionSection.js   // Allows users to ask questions about the data; displays answers
│   └── MessageSection.js    // Additional messaging component (currently commented out in page.js)
├── package.json             // Project metadata, scripts, and dependencies
├── tailwind.config.mjs      // Tailwind CSS configuration file for styling
└── README.md                // This documentation file
```

## Setup and Running

1. **Install Dependencies:**
   Navigate to the `frontend` directory and run:
   ```
   npm install
   ```

2. **Development Server:**
   Start the development server with:
   ```
   npm run dev
   ```
   The app will be accessible at [http://localhost:3000](http://localhost:3000).

3. **Tailwind CSS Customization:**
   Tailwind CSS is pre-configured for styling. Customizations can be made by updating the `tailwind.config.mjs` file.

## Frontend-to-Backend Integration

- **Backend Endpoints:**
  The application communicates with a Flask-based backend via HTTP:
  - **Upload CSV:** `POST http://127.0.0.1:5000/upload`
  - **Ask Question:** `POST http://127.0.0.1:5000/ask`
  - **Process Message:** `POST http://127.0.0.1:5000/process_message` (functionality present but secondary)

- **Error Handling & Feedback:**
  The interface validates user inputs (e.g., checking for file selection or empty question fields) and provides real-time alerts and messages based on the responses from the backend.

## Customization and Further Development

- **Components:**
  The UI is modular:
  - **UploadSection.js** handles file uploads and displays summaries.
  - **QuestionSection.js** enables users to ask questions related to the uploaded data.
  - **MessageSection.js** is available for additional messaging functionality and can be integrated as needed.

- **Design Considerations:**
  The design is clean and responsive, ensuring ease-of-use on various devices. Minimalist styling is achieved through Tailwind CSS, with ample room for further customization.

- **Package Information:**
  The project uses Next.js version 15.1.7 and React 19.0.0, reflecting the latest updates in the package configuration (see `package.json`).

For any further modifications, update the respective components in the `frontend/components` directory or adjust the layout in `frontend/app/page.js`. This documentation reflects the current state of the frontend application, providing an overview of its structure, functionality, and setup instructions.
