"use client";
import React, { useState } from 'react';
import ChartRAG from '../components/ChartRAG';

export default function Home() {
  const [summary, setSummary] = useState('');

  return (
    <div className="min-h-screen flex flex-col justify-center items-center bg-gradient-to-b from-blue-400 to-blue-50">
      <ChartRAG summary={summary} setSummary={setSummary} />
    </div>
  );
}
