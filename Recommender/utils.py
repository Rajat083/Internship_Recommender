"""
PM Intern Recommender - Utility Functions
========================================

This module contains common utility functions used by both train.py and recommend.py
for data loading, preprocessing, cleaning, and skill processing.
"""

import pandas as pd
import numpy as np
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter


def load_data():
    """Load student and internship datasets"""
    print("Loading datasets...")
    students = pd.read_csv('Recommender/dataset/students.csv')
    internships = pd.read_csv('Recommender/dataset/internships.csv')
    
    print(f"Loaded {len(students)} students and {len(internships)} internships")
    return students, internships


def preprocess_data(students, internships):
    """Preprocess the data by converting skills to lowercase"""
    print("Preprocessing data...")
    
    # Convert skills to lowercase
    students["skills"] = students["skills"].str.lower()
    internships["required_skills"] = internships["required_skills"].str.lower()
    
    # Create dictionaries for skills mapping
    stu_skills = students.set_index('student_id')['skills'].to_dict()
    int_reqs = internships.set_index('internship_id')['required_skills'].to_dict()
    
    return stu_skills, int_reqs


def clean_skills(skills):
    """Clean skills text by removing special characters and normalizing whitespace"""
    skills = re.sub(r'[^a-zA-Z0-9, ]', '', skills)
    skills = re.sub(r'\s+', ' ', skills)
    skills = skills.strip()
    return skills


def process_skills(stu_skills, int_reqs):
    """Process and clean skills, convert to lists"""
    print("Processing and cleaning skills...")
    
    # Clean and split student skills
    for sid, skills in stu_skills.items():
        stu_skills[sid] = clean_skills(skills).split(', ')
    
    # Clean and split internship requirements
    for iid, reqs in int_reqs.items():
        int_reqs[iid] = [clean_skills(req) for req in reqs.split(', ')]
    
    return stu_skills, int_reqs


def process_skills_for_prediction(students, internships):
    """Process skills from loaded datasets for prediction (used in recommend.py)"""
    print("Processing skills for prediction...")
    
    # Create dictionaries for skills mapping
    stu_skills = students.set_index('student_id')['skills'].to_dict()
    int_reqs = internships.set_index('internship_id')['required_skills'].to_dict()
    
    # Clean and split student skills
    for sid, skills in stu_skills.items():
        stu_skills[sid] = clean_skills(skills).split(', ')
    
    # Clean and split internship requirements
    for iid, reqs in int_reqs.items():
        int_reqs[iid] = [clean_skills(req) for req in reqs.split(', ')]
    
    return stu_skills, int_reqs


def analyze_skills(stu_skills, int_reqs):
    """Analyze skill distributions (optional for insights)"""
    print("Analyzing skill distributions...")
    
    # Count all student skills
    all_stu_skills = Counter()
    for skill in stu_skills.values():
        all_stu_skills.update(skill)
    
    # Count all internship requirements
    all_int_reqs = Counter()
    for req in int_reqs.values():
        all_int_reqs.update(req)
    
    print(f"Total unique student skills: {len(all_stu_skills)}")
    print(f"Total unique internship requirements: {len(all_int_reqs)}")
    
    return all_stu_skills, all_int_reqs


def create_vectorizer_and_transform(stu_skills, int_reqs):
    """Create TF-IDF vectorizer and transform skills to vectors"""
    print("Creating TF-IDF vectors...")
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer()
    
    # Prepare skill corpus for students (training data)
    skill_corpus = [' '.join(skills) for skills in stu_skills.values()]
    X = vectorizer.fit_transform(skill_corpus)
    
    # Transform internship requirements using the same vectorizer
    intern_reqs_corpus = [' '.join(reqs) for reqs in int_reqs.values()]
    Y = vectorizer.transform(intern_reqs_corpus)
    
    print(f"Student vectors shape: {X.shape}")
    print(f"Internship vectors shape: {Y.shape}")
    
    return vectorizer, X, Y


def create_student_vectors(stu_skills, vectorizer):
    """Create TF-IDF vectors for students using the trained vectorizer"""
    skill_corpus = [' '.join(skills) for skills in stu_skills.values()]
    X = vectorizer.transform(skill_corpus)
    return X


def load_trained_model_and_data():
    """Load trained model, vectorizer, and datasets"""
    print("Loading model and data...")
    
    try:
        # Load the trained model
        with open('Recommender/model/trained_model.pkl', 'rb') as f:
            model = pickle.load(f)
        
        # Load the vectorizer
        with open('Recommender/model/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        
        # Load processed datasets
        students = pd.read_csv('Recommender/dataset/processed_students.csv')
        internships = pd.read_csv('Recommender/dataset/processed_internships.csv')
        
        print("Model and data loaded successfully!")
        return model, vectorizer, students, internships
        
    except FileNotFoundError as e:
        print(f"Error: Required files not found. Please run train.py first.")
        print(f"Missing file: {e}")
        return None, None, None, None


def save_model_and_data(model, vectorizer, students, internships):
    """Save trained model, vectorizer, and other necessary data"""
    print("Saving trained model and data...")
    
    # Save the trained model
    with open('Recommender/model/trained_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    # Save the vectorizer
    with open('Recommender/model/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    # Save processed datasets for future use
    students.to_csv('Recommender/dataset/processed_students.csv', index=False)
    internships.to_csv('Recommender/dataset/processed_internships.csv', index=False)
    
    print("Model and data saved successfully!")


def create_recommendations(model, X, students, internships, stu_skills, top_n=5):
    """Create recommendations for all students"""
    print("Generating recommendations...")
    
    # Get predictions for all students
    distances, indices = model.kneighbors(X)
    
    recommendations = {}
    
    # Get original student and internship IDs from the dataframes
    student_ids = list(students['student_id'])
    internship_ids = list(internships['internship_id'])
    
    for i, (dists, idxs) in enumerate(zip(distances, indices)):
        student_id = student_ids[i]
        student_name = students[students['student_id'] == student_id]['student_name'].iloc[0]
        
        # Get top internships for this student
        recommended_internships = []
        for j, (dist, idx) in enumerate(zip(dists[:top_n], idxs[:top_n])):
            internship_id = internship_ids[idx]
            company_name = internships[internships['internship_id'] == internship_id]['company'].iloc[0]
            similarity_score = 1 - dist  # Convert distance to similarity
            required_skills = internships[internships['internship_id'] == internship_id]['required_skills'].iloc[0]
            
            recommended_internships.append({
                'rank': j + 1,
                'internship_id': internship_id,
                'company': company_name,
                'similarity_score': similarity_score,
                'distance': dist,
                'required_skills': required_skills
            })
        
        recommendations[student_id] = {
            'student_name': student_name,
            'student_id': student_id,
            'student_skills': stu_skills[student_id],
            'internships': recommended_internships
        }
    
    print(f"Generated recommendations for {len(recommendations)} students")
    return recommendations


def display_sample_recommendations(recommendations, num_samples=3):
    """Display sample recommendations"""
    print(f"\n{'='*60}")
    print(f"SAMPLE RECOMMENDATIONS ({num_samples} students)")
    print(f"{'='*60}")
    
    for i, (student_id, data) in enumerate(recommendations.items()):
        if i >= num_samples:
            break
        
        print(f"\n=== Recommendations for {data['student_name']} (ID: {student_id}) ===")
        print(f"Student Skills: {', '.join(data['student_skills'])}")
        print("Top 5 recommended internships:")
        
        for internship in data['internships']:
            print(f"  {internship['rank']}. {internship['company']} (ID: {internship['internship_id']})")
            print(f"     Similarity Score: {internship['similarity_score']:.4f}")
            print(f"     Required Skills: {internship['required_skills']}")
            print()


def display_single_recommendation(recommendation):
    """Display recommendation for a single student"""
    print(f"\n{'='*60}")
    print(f"RECOMMENDATION RESULTS")
    print(f"{'='*60}")
    
    print(f"\n=== Recommendations for {recommendation['student_name']} (ID: {recommendation['student_id']}) ===")
    print(f"Student Skills: {', '.join(recommendation['student_skills'])}")
    print("Top recommended internships:")
    
    for internship in recommendation['internships']:
        print(f"  {internship['rank']}. {internship['company']} (ID: {internship['internship_id']})")
        print(f"     Similarity Score: {internship['similarity_score']:.4f}")
        print(f"     Required Skills: {internship['required_skills']}")
        print()