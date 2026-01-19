import React, { useState } from 'react';
import RecommendationForm from '../components/RecommendationForm.jsx';
import RecommendationResults from '../components/RecommendationResults.jsx';
import { getRecommendations } from '../services/api.js';

function Home() {
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFormSubmit = async (studentDetails, topK) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const recommendations = await getRecommendations(studentDetails, topK);
      setResults(recommendations);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      console.error('Error in handleFormSubmit:', errorMessage);
      setError(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  const year = new Date().getFullYear();

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <header className="bg-blue-600 text-white py-10 px-5 text-center shadow-md">
        <h1 className="text-4xl font-bold mb-3">🎓 Internship Recommender</h1>
        <p className="text-lg opacity-90">
          Discover the perfect internship opportunities based on your skills and domain
        </p>
      </header>

      <main className="flex-1 py-10 px-5">
        <RecommendationForm onSubmit={handleFormSubmit} isLoading={isLoading} />
        <RecommendationResults data={results} error={error} />
      </main>

      <footer className="bg-gray-100 text-gray-700 text-center py-5 border-t border-gray-300 mt-auto">
        <p>&copy; {year} Internship Recommender System. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
