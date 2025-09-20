"""
PM Intern Recommender - Training Pipeline
=========================================

This module trains the ML model for the PM Intern Recommender system using:
- TF-IDF vectorization for skill text processing
- k-nearest neighbors for similarity-based recommendations
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import pickle
import re
import os


def clean_skills(skills_text):
    """Clean skills text by removing special characters and normalizing format."""
    if pd.isna(skills_text):
        return ""
    
    # Remove special characters except letters, numbers, commas, and spaces
    cleaned = re.sub(r'[^a-zA-Z0-9, ]', '', str(skills_text))
    
    # Normalize whitespace and convert to lowercase
    cleaned = ' '.join(cleaned.lower().split())
    
    return cleaned


def load_and_preprocess_data():
    """Load and preprocess the student and internship datasets."""
    print("Loading datasets...")
    
    # Load datasets
    students_df = pd.read_csv('Recommender/dataset/students.csv')
    internships_df = pd.read_csv('Recommender/dataset/internships.csv')
    
    print(f"Loaded {len(students_df)} students and {len(internships_df)} internships")
    
    # Clean skills
    print("Cleaning skills data...")
    students_df['skills_cleaned'] = students_df['skills'].apply(clean_skills)
    internships_df['required_skills_cleaned'] = internships_df['required_skills'].apply(clean_skills)
    
    # Remove rows with empty skills
    students_df = students_df[students_df['skills_cleaned'].str.len() > 0]
    internships_df = internships_df[internships_df['required_skills_cleaned'].str.len() > 0]
    
    print(f"After cleaning: {len(students_df)} students and {len(internships_df)} internships")
    
    # Save processed data
    students_df.to_csv('Recommender/dataset/processed_students.csv', index=False)
    internships_df.to_csv('Recommender/dataset/processed_internships.csv', index=False)
    
    return students_df, internships_df


def train_model(students_df, internships_df):
    """Train the TF-IDF vectorizer and k-NN model."""
    print("Training TF-IDF vectorizer...")
    
    # Combine all skills text for vocabulary building
    all_skills = list(students_df['skills_cleaned']) + list(internships_df['required_skills_cleaned'])
    
    # Initialize and fit TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words='english',
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95
    )
    
    vectorizer.fit(all_skills)
    
    # Transform internship skills
    internship_vectors = vectorizer.transform(internships_df['required_skills_cleaned'])
    
    print("Training k-NN model...")
    
    # Initialize and fit k-NN model
    knn_model = NearestNeighbors(
        n_neighbors=min(10, len(internships_df)),
        metric='cosine',
        algorithm='brute'
    )
    
    knn_model.fit(internship_vectors)
    
    # Save models
    print("Saving models...")
    os.makedirs('Recommender/model', exist_ok=True)
    
    with (open('Recommender/model/trained_model.pkl', 'wb')) as f:
        pickle.dump(knn_model, f)
    
    with (open('Recommender/model/vectorizer.pkl', 'wb')) as f:
        pickle.dump(vectorizer, f)
    
    print("Training completed successfully!")
    print(f"Model saved with {len(internships_df)} internships and {len(students_df)} students")


def main():
    """Main training pipeline"""
    try:
        # Load and preprocess data
        students_df, internships_df = load_and_preprocess_data()
        
        # Train model
        train_model(students_df, internships_df)
        
        print("\n Training pipeline completed successfully!")
        print(" Files created:")
        print("   - model/trained_model.pkl")
        print("   - model/vectorizer.pkl")
        print("   - dataset/processed_students.csv")
        print("   - dataset/processed_internships.csv")
        
    except Exception as e:
        print(f" Error during training: {e}")
        raise


if __name__ == "__main__":
    main()
