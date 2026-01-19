import React, { useState } from 'react';

function RecommendationForm({ onSubmit, isLoading }) {
  const [name, setName] = useState('');
  const [skills, setSkills] = useState('');
  const [domain, setDomain] = useState('');
  const [topK, setTopK] = useState(5);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (!name || !skills || !domain) {
      alert('Please fill in all fields');
      return;
    }

    const skillsArray = skills.split(',').map((s) => s.trim());
    
    onSubmit(
      {
        name,
        skills: skillsArray,
        domain,
      },
      topK
    );
  };

  return (
    <form onSubmit={handleSubmit} className="max-w-md mx-auto p-6 bg-gray-100 rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Get Internship Recommendations</h2>
      
      <div className="mb-4 flex flex-col">
        <label htmlFor="name" className="mb-2 font-bold text-gray-700">Student Name</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your name"
          className="px-3 py-2 border border-gray-300 rounded-md text-sm font-sans focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          disabled={isLoading}
        />
      </div>

      <div className="mb-4 flex flex-col">
        <label htmlFor="domain" className="mb-2 font-bold text-gray-700">Domain</label>
        <input
          id="domain"
          type="text"
          value={domain}
          onChange={(e) => setDomain(e.target.value)}
          placeholder="e.g., Web Development, Data Science"
          className="px-3 py-2 border border-gray-300 rounded-md text-sm font-sans focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          disabled={isLoading}
        />
      </div>

      <div className="mb-4 flex flex-col">
        <label htmlFor="skills" className="mb-2 font-bold text-gray-700">Skills (comma-separated)</label>
        <input
          id="skills"
          type="text"
          value={skills}
          onChange={(e) => setSkills(e.target.value)}
          placeholder="e.g., React, Python, SQL"
          className="px-3 py-2 border border-gray-300 rounded-md text-sm font-sans focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          disabled={isLoading}
        />
      </div>

      <div className="mb-6 flex flex-col">
        <label htmlFor="topK" className="mb-2 font-bold text-gray-700">Number of Recommendations</label>
        <input
          id="topK"
          type="number"
          min="1"
          max="20"
          value={topK}
          onChange={(e) => setTopK(Number(e.target.value))}
          className="px-3 py-2 border border-gray-300 rounded-md text-sm font-sans focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-300 disabled:cursor-not-allowed"
          disabled={isLoading}
        />
      </div>

      <button 
        type="submit" 
        className="w-full px-5 py-3 bg-blue-600 text-white border-none rounded-md text-base font-bold cursor-pointer transition-opacity hover:opacity-90 disabled:opacity-60 disabled:cursor-not-allowed"
        disabled={isLoading}
      >
        {isLoading ? 'Loading...' : 'Get Recommendations'}
      </button>
    </form>
  );
}

export default RecommendationForm;
