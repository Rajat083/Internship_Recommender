import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getRecommendations = async (studentDetails, topK = 5) => {
  try {
    console.log('API Base URL:', API_BASE_URL);
    console.log('Request payload:', { studentDetails, topK });
    
    const response = await apiClient.post('/recommendations/', studentDetails, {
      params: { top_k: topK },
    });
    
    console.log('Response received:', response.data);
    return response.data;
  } catch (error) {
    const errorMessage = axios.isAxiosError?.(error)
      ? `API Error: ${error.response?.status} - ${JSON.stringify(error.response?.data) || error.message}`
      : `Failed to fetch recommendations: ${error instanceof Error ? error.message : String(error)}`;
    
    console.error('Detailed error:', errorMessage);
    throw new Error(errorMessage);
  }
};

export const healthCheck = async () => {
  try {
    const response = await apiClient.get('/health');
    return response.data;
  } catch (error) {
    const errorMessage = axios.isAxiosError?.(error)
      ? `Health check failed: ${error.response?.status} - ${error.message}`
      : `Health check failed: ${error instanceof Error ? error.message : String(error)}`;
    
    console.error(errorMessage);
    throw new Error(errorMessage);
  }
};
