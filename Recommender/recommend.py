"""
PM Intern Recommender - CLI Tool
================================

Simple command-line interface for the PM Intern Recommender system.
"""

import argparse
import sys
from utils import (
    load_model, 
    get_student_recommendations, 
    get_new_student_recommendations,
    get_all_students,
    get_all_internships,
    get_model_stats
)


def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("    PM INTERN RECOMMENDER - CLI TOOL")
    print("    Machine Learning Powered Internship Matching")
    print("=" * 60)


def print_recommendations(recommendations, title="Recommendations"):
    """Print recommendations in a formatted way"""
    print(f"\n {title}")
    print("-" * 50)
    
    if not recommendations:
        print(" No recommendations found.")
        return
    
    for rec in recommendations:
        print(f" Rank {rec['rank']}: {rec['company']}")
        if rec['title']:
            print(f"    Title: {rec['title']}")
        print(f"    Match Score: {rec['similarity_score']:.3f}")
        print(f"     Required Skills: {rec['required_skills']}")
        print(f"    Location: {rec['location']}")
        print(f"    Duration: {rec['duration']}")
        if rec['stipend']:
            print(f"    Stipend: {rec['stipend']}")
        print()


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="PM Intern Recommender - ML-powered internship matching system"
    )
    
    parser.add_argument('--student-id', type=int, help='Get recommendations for existing student by ID')
    parser.add_argument('--new-student', type=str, help='New student name for recommendations')
    parser.add_argument('--skills', type=str, help='Student skills (comma-separated, use with --new-student)')
    parser.add_argument('--top-n', type=int, default=5, help='Number of recommendations to return (default: 5)')
    parser.add_argument('--list-students', action='store_true', help='List all students')
    parser.add_argument('--list-internships', action='store_true', help='List all internships')
    parser.add_argument('--stats', action='store_true', help='Show model statistics')
    
    args = parser.parse_args()
    
    # If no arguments provided, show help
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        return
    
    print_banner()
    
    try:
        if args.stats:
            print(" Model Statistics")
            model_data = load_model()
            stats = get_model_stats(model_data)
            print("-" * 30)
            print(f" Students in database: {stats['students_count']}")
            print(f" Internships available: {stats['internships_count']}")
            print(f" Model type: {stats['model_type']}")
            print(f" Model status: Ready")
            
        elif args.student_id:
            print(f" Getting recommendations for Student ID: {args.student_id}")
            model_data = load_model()
            result = get_student_recommendations(args.student_id, args.top_n, model_data)
            print(f"\n Student: {result['student_name']}")
            print(f"  Skills: {', '.join(result['student_skills'])}")
            print_recommendations(result['recommendations'], f"Top {args.top_n} Recommendations")
            
        elif args.new_student:
            if not args.skills:
                print(" Error: --skills is required when using --new-student")
                return
            print(f" Getting recommendations for new student: {args.new_student}")
            model_data = load_model()
            result = get_new_student_recommendations(args.new_student, args.skills, args.top_n, model_data)
            print(f"\n Student: {result['student_name']}")
            print(f"  Skills: {', '.join(result['student_skills'])}")
            print_recommendations(result['recommendations'], f"Top {args.top_n} Recommendations")
            
        elif args.list_students:
            print(" Available Students:")
            model_data = load_model()
            students = get_all_students(10, model_data)
            print("-" * 50)
            for student in students:
                print(f" ID: {student['id']} |  {student['name']}")
                print(f"     Skills: {student['skills'][:60]}{'...' if len(student['skills']) > 60 else ''}")
                print()
                
        elif args.list_internships:
            print(" Available Internships:")
            model_data = load_model()
            internships = get_all_internships(10, model_data)
            print("-" * 50)
            for internship in internships:
                print(f" ID: {internship['id']} |  {internship['company']}")
                if internship['title']:
                    print(f"    Title: {internship['title']}")
                print(f"     Required: {internship['required_skills'][:60]}{'...' if len(internship['required_skills']) > 60 else ''}")
                print(f"    {internship['location']} |  {internship['duration']}")
                if internship['stipend']:
                    print(f"    {internship['stipend']}")
                print()
        else:
            print(" No valid action specified. Use --help for usage information.")
            
    except Exception as e:
        print(f" Error: {e}")
        print(" Try running 'python train.py' first to train the model.")


if __name__ == "__main__":
    main()
