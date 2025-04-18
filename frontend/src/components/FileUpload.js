import React, { useState } from "react";
import axios from "axios";

const FileUpload = ({ onSummaryReceived }) => {
    //holds uploaded file but is initially empty
    //const [value, setValue] = useState(initialValue)
    // value = current state
    // setValue = function to change the value 
    // initial value = what value is initialy set to
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    //error message that may occur is initally empty
    const [error, setError] = useState(null);
    const [method, setMethod] = useState('hybrid');
    const [maxLength, setMaxLength] = useState(150);
    const [minLength, setMinLength] = useState(50);
    const [ratio, setRatio] = useState(0.3);

    const handleFileChange = (e) => {
        //get the first file that was uploaded
        setFile(e.target.files[0]);
        setError(null);
    };

    const handleSubmit = async (e) => {
        //default behavior would be to refresh the page which is unwanted
        e.preventDefault();
        //check if a file has been selected and return an error if not 
        if (!file) {
            setError("Please select a file!");
            return;
        }
        //new form data object to prepare the form to be uploaded
        const formData = new FormData();
        formData.append('file', file);
        formData.append('method', method);
        formData.append('max_length', maxLength);
        formData.append('min_length', minLength);
        formData.append('ratio', ratio);

        setLoading(true);


        //utilize post request that send data to a server
        //send a file to the server so that some action can be done on it (summarize document)
        try {
            //make HTTP post request to backend API
            const response = await axios.post(
                //URL of the API stored in the env variable
                //formdata contains body of request - uploaded file
                `${process.env.REACT_APP_API_URL}/summarize`,
                formData,
                {
                    //ensure correct formatting
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            );
            onSummaryReceived(response.data);
        } catch (err) {
            setError('Error summarizing document, please try again');
            console.error(err)
        } finally {
            setLoading(false);
        }
    };
    return (
        <div className="max-w-d mx-auto p-4 bg-white rounded shadow-md">
            <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label className="">
                        Select document to summarize
                    </label>
                    <input
                        type="file"
                        onChange={handleFileChange}
                        className="w-full text-sm text-gray-500
                                    file:mr-4 file:py-2 file:px-4
                                    file:rounded-md file:border-0
                                    file:text-sm file:font-semibold
                                    file:bg-blue-50 file:text-blue-700
                                    hover:file:bg-blue-50"
                        accept=".pdf,.docx,.txt"
                    />
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Summarization Method
                    </label>
                    <select
                        //method is synced to the previously defined react hook of method
                        //whenever user selects option handler udpates the method state
                        //drop down value is stored in e.target.value ("abstractive")
                        value={method}
                        onChange={(e) => setMethod(e.target.value)}
                        className="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300
                                   focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm
                                   rounded-md"
                    >
                        <option value="extractive">Extractive (selects key sentences)</option>
                        <option value="abstractive">Abstractive (generates new text)</option>
                        <option value="hybrid">Hybrid (combination)</option>
                    </select>
                </div>
                
                {(method === "abstractive" || method === "hybrid") && (
                    <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Min Length
                            </label>
                            <input
                                type="number"
                                min="10"
                                max="100"
                                value={minLength}
                                onChange={(e) => setMinLength(parseInt(e.target.value))}
                                className="mt-1 block w-full pl-3 pr-3 py-2 text-base border-gray-300
                                           focus:outline-none focus:ring-blue-500 focus-border-blue-500 sm:text-sm
                                           rounded-md"
                            />
                        </div>
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Max Length
                            </label>
                            <input
                                type="number"
                                min="50"
                                max="500"
                                value={maxLength}
                                onChange={(e) => setMaxLength(parseInt(e.target.value))}
                                className="mt-1 block w-full pl-3 pr-3 py-2 text-base border-gray-300
                                           focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm
                                           rounded-md"   
                            />
                        </div>
                    </div>
                )
                }
                {(method === "extractive" || method === "hybrid") && (
                    <div className="mb-4">
                        <label className="block text-sm font-medium text-gray-700 mb-2">
                            Sentence Ratio ({(ratio * 100).toFixed(0)}%)
                        </label>
                        <input
                            type="range"
                            min="0.1"
                            max="0.5"
                            step="0.05"
                            value={ratio}
                            onChange={(e) => setRatio(parseFloat(e.target.value))}
                            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                        />
                    </div>
                )}
                
                {error && (
                    <div className="mb-4 text-red-500 text-sm">{error}</div>
                )}
                <button
                    type="submit"
                    disabled={loading}
                    className={ `w-full py-2 px-4 border border-transparent rounded-md
                                shadow-sm text-sm font-medium text-white bg-blue-600
                                hover:bg-blue-700 focus:outline-none focus:ring-2
                                focus:ring-offset-2 focus:ring-blue-500 ${
                                    loading ? 'opacity-50 cursor-not-allowed' : ''
                                }`} 
                        >
                    {loading ? 'Summarizing...' : 'Summarize document'}
                </button>
            </form>
        </div>
    );
};

export default FileUpload;