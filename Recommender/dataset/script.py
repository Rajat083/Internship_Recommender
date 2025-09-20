import pandas as pd
import random

# --- Define skill taxonomy ---
domains = {
    "Web Development": [
        "javascript", "html", "css", "react", "angular", "vue", "next.js",
        "nodejs", "express", "django", "flask", "spring", "sql", "mongodb", "postgresql"
    ],
    "Machine Learning / AI": [
        "machine learning", "data science", "deep learning", "nlp", "computer vision",
        "gen ai", "agentic ai", "mlops", "pytorch", "tensorflow", "scikit-learn"
    ],
    "DevOps / Cloud": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "terraform",
        "ci/cd", "infrastructure as code", "ansible"
    ],
    "Data / Analytics": [
        "sql", "excel", "powerbi", "tableau", "hadoop", "spark", "airflow", "kafka", "etl", "snowflake"
    ],
    "Mobile Development": [
        "android", "ios", "flutter", "react native", "swift", "kotlin", "firebase", "dart"
    ],
    "Design": [
        "figma", "adobe xd", "photoshop", "illustrator", "ui/ux design", "graphic design", "interaction design", "canva"
    ],
    "Business / Marketing": [
        "seo", "content writing", "digital marketing", "market research",
        "google analytics", "hubspot", "mailchimp", "social media strategy"
    ],
    "Finance / Management": [
        "financial modeling", "accounting", "ms excel", "risk analysis", "tally", "quickbooks", "business analysis"
    ]
}

companies = [
    "Mitchell, Stewart and Morris", "Hansen, Harding and Graham", "Robertson-Logan",
    "Guerrero LLC", "Harris and Sons", "Kumar & Patel", "Singh Technologies",
    "GlobalSoft", "NextGen Systems", "Bright Future Ltd.", "Skyline Corp", "DataWorks Inc."
]

# --- Internship generation ---
def generate_internship(n=2000):
    data = []
    for i in range(1, n+1):
        domain = random.choice(list(domains.keys()))
        skills = random.sample(domains[domain], k=random.randint(3, 6))
        title = f"{random.choice(skills).title()} Intern"
        company = random.choice(companies)
        stipend = random.choice([0, 5000, 10000, 15000, 20000, 25000])
        data.append([i, title, company, stipend, ", ".join(skills), domain])
    return pd.DataFrame(data, columns=["internship_id", "internship_title", "company", "stipend", "required_skills", "domain"])

# --- Student generation ---
def generate_student(n=1000):
    data = []
    for i in range(1, n+1):
        domain = random.choice(list(domains.keys()))
        skills = random.sample(domains[domain], k=random.randint(3, 6))
        name = f"Student_{i}"
        data.append([i, name, ", ".join(skills), domain])
    return pd.DataFrame(data, columns=["student_id", "student_name", "skills", "primary_domain"])

# --- Generate datasets ---
internships_df = generate_internship(2000)
students_df = generate_student(1000)

# --- Save CSVs ---
internships_df.to_csv("Recommender/dataset/internships.csv", index=False)
students_df.to_csv("Recommender/dataset/students.csv", index=False)

print("✅ Files generated: internships.csv, students.csv")
