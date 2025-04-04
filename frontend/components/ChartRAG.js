import React from 'react';
import UploadSection from './UploadSection';

const ChartRAG = ({ summary, setSummary }) => {
  return (
<div className="min-h-[75vh] min-w-[75vw] bg-white/80 shadow-md rounded-lg p-6 mb-4 flex flex-col justify-center items-center">
      <h1 className="text-5xl font-bold mb-4 text-center">ChartRAG</h1>
<p className="text-lg mb-8 text-center bg-white px-4 py-2">
        Upload a csv file and our ai will summarise for you
      </p>
      <div className="flex flex-col items-center">
        <UploadSection summary={summary} setSummary={setSummary} />
        {/* Additional sections e.g. QuestionSection and MessageSection can be added here */}
      </div>
    </div>
  );
};

export default ChartRAG;
