import React from 'react';

const SummaryDisplay = ({ summary }) => {
    if (!summary) return null;
    return (
        <div className='max-w-md mx-auto mt-6 p-4 bg-white rounded shadow-md'>
            <h2 className='text-cl font-semibold mb-4'>Summary</h2>
            <div className='mb-4'>
                <h3>Original Document: {summary.filename}</h3>
            </div>
            <div className='border-t pt-4'>
                <p className='text-gray-800 whitespace-pre-wrap'>{summary.summary}</p>
            </div>
        </div>
    );
};

export default SummaryDisplay;