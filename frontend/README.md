# 🎓 Internship Recommender - Frontend

A React frontend application for the Internship Recommender System. This application helps students discover personalized internship opportunities based on their skills and domain using semantic search powered by vector similarity.

## 🚀 Features

- **Student Input Form** - Collect student information including name, skills, and domain
- **Real-time Recommendations** - Get personalized internship recommendations with similarity scores
- **Responsive Design** - Modern, clean UI built with Tailwind CSS
- **Interactive Results** - View detailed internship information including company, domain, required skills, and stipend
- **Error Handling** - Comprehensive error messages and loading states

## 🛠️ Tech Stack

- **React 18** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **Axios** - HTTP client for API calls
- **JavaScript (JSX)** - No TypeScript dependencies

## 📋 Prerequisites

- Node.js 16.x or higher
- npm or yarn package manager
- Backend API running on `http://localhost:8000` (or configured via environment variable)

## 📦 Installation

### 1. Navigate to frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install
```

### 3. Configure environment variables (optional)
Create a `.env` file in the frontend directory:
```env
VITE_API_BASE_URL=http://localhost:8000
```

## 🚀 Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## 🏗️ Build

Build for production:
```bash
npm run build
```

The optimized build will be in the `dist/` directory.

Preview production build:
```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── RecommendationForm.jsx
│   │   └── RecommendationResults.jsx
│   ├── pages/           # Page components
│   │   └── Home.jsx
│   ├── services/        # API services
│   │   └── api.js
│   ├── App.jsx          # Root component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles with Tailwind
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
├── postcss.config.js    # PostCSS configuration
└── package.json         # Dependencies
```

## 🔗 API Integration

The frontend communicates with the backend API:
- **Base URL**: `http://localhost:8000` (configurable via `VITE_API_BASE_URL`)
- **Endpoint**: `POST /recommendations/`
- **Health Check**: `GET /health`

### Request Format
```json
{
  "name": "John Doe",
  "skills": ["Python", "Machine Learning", "TensorFlow"],
  "domain": "Artificial Intelligence"
}
```

### Response Format
```json
{
  "student_id": "ABC12345",
  "student_name": "John Doe",
  "student_skills": ["Python", "Machine Learning", "TensorFlow"],
  "recommendatons": [
    {
      "rank": 1,
      "internship_id": "101",
      "internship_title": "ML Engineer Intern",
      "company": "Tech Corp",
      "domain": "AI/ML",
      "similarity_score": 0.8636,
      "required_skills": ["Python", "TensorFlow", "Deep Learning"],
      "stipend": 30000
    }
  ],
  "total_recommendations": 5
}
```

## 📝 How to Use

1. Enter your name
2. Specify your domain (e.g., Web Development, Data Science, AI/ML)
3. List your skills (comma-separated)
4. Select number of recommendations (1-20)
5. Click "Get Recommendations"
6. View your personalized internship matches with similarity scores

## 🎨 Styling

This project uses **Tailwind CSS** for styling:
- Utility classes for responsive design
- Custom color schemes
- Consistent spacing and typography
- Hover and focus states
- Mobile-first approach

## 🐛 Troubleshooting

### CORS Issues
If you encounter CORS errors, ensure your backend has CORS middleware configured to accept requests from `http://localhost:3000`.

### API Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check `.env` file for correct `VITE_API_BASE_URL`
- Check browser console for detailed error messages

### Build Issues
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📜 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🚀 Deployment

### Vercel
```bash
npm run build
vercel --prod
```

### Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

### Docker
Create a `Dockerfile` and containerize the frontend with a web server like Nginx.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## 📄 License

This project is part of the Internship Recommender System.
