import React, { useState } from 'react';
import './App.css';
import './output.css';
import FileUpload from './components/FileUpload';
import SummaryDisplay from './components/SummaryDisplay';

function App() {
  const [summary, setSummary] = useState(null);
  return (
    <div className='min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8'>
      <div className='max-w-md mx-auto text-center mb-12'>
        <h1 className='text-3xl font-extrabold text-gray-900'>
          Document Summarizer
        </h1>
        <p className='mt-2 text-sm text-gray-600'>
          Upload a document and receive a summary!
        </p>
      </div>
      <FileUpload onSummaryReceived={setSummary} />
      <SummaryDisplay summary={summary} />
    </div>
  );
}

export default App;