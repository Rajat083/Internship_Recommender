import React from 'react';

function RecommendationResults({ data, error }) {
  if (error) {
    return (
      <div className="max-w-2xl mx-auto mt-8 p-5 bg-red-100 border border-red-400 rounded-lg">
        <h3 className="text-red-800 font-bold mt-0">Error</h3>
        <p className="text-red-800 m-2 mt-2">{error}</p>
      </div>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <div className="max-w-2xl mx-auto mt-8 p-5">
      <h2 className="text-3xl text-gray-800 font-bold mb-2">Recommendations for {data.student_name}</h2>
      <p className="text-gray-600 text-sm mb-5">Total Recommendations: {data.total_recommendations}</p>
      
      <div className="flex flex-col gap-4">
        {data.recommendatons && data.recommendatons.length > 0 ? (
          data.recommendatons.map((rec, index) => (
            <div key={index} className="bg-white border border-gray-300 rounded-lg p-5 shadow-md flex gap-4">
              <div className="bg-blue-600 text-white rounded-full w-12 h-12 flex items-center justify-center text-xl font-bold shrink-0">
                #{rec.rank}
              </div>
              <div className="flex-1">
                <h3 className="m-0 mb-2 text-lg text-gray-800 font-bold">{rec.internship_title}</h3>
                <p className="my-1 text-gray-700"><strong>{rec.company}</strong></p>
                <p className="my-1 text-gray-600 text-sm">Domain: {rec.domain}</p>
                <p className="my-2 text-gray-600 text-sm leading-relaxed">
                  <strong>Required Skills:</strong> {rec.required_skills.join(', ')}
                </p>
                {rec.stipend > 0 && (
                  <p className="my-1 text-green-600 text-sm font-bold">
                    <strong>Stipend:</strong> ₹{rec.stipend.toLocaleString()}
                  </p>
                )}
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <span className="bg-gray-100 px-2 py-1 rounded text-xs font-bold text-blue-600">
                    Similarity Score: {(rec.similarity_score * 100).toFixed(2)}%
                  </span>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className="text-center text-gray-500 py-10 text-base">No recommendations found. Try adjusting your skills or domain.</p>
        )}
      </div>
    </div>
  );
}

export default RecommendationResults;
