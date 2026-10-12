"""
data_pipeline.py - Smart Campus Analytics (Data Engineering Module)
Author: Data Engineer
Responsibility: Integrates disparate campus sources (Academics, Attendance, LMS, 
                Engagement, Placement, Skills, Feedback) into a unified Student 360 table.
"""

import os
import pandas as pd
import numpy as np

CSV_FILENAME = "student_360_profile.csv"

def load_and_clean_data(file_path: str = None) -> pd.DataFrame:
    """
    Loads raw multi-source student records, cleanses missing entries,
    and returns a standardized master DataFrame.
    """
    if file_path is None or not os.path.exists(file_path):
        # Look in current directory or script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, CSV_FILENAME)
        
    if not os.path.exists(file_path):
        # Fallback to local root search
        if os.path.exists(CSV_FILENAME):
            file_path = CSV_FILENAME
        else:
            raise FileNotFoundError(f"Master student profile CSV not found at {file_path}")

    df = pd.read_csv(file_path)

    # 1. Type Enforcement & Missing Value Imputation
    numeric_cols = [
        'cgpa', 'backlogs', 'midterm_score', 'attendance_rate', 
        'lab_attendance', 'lms_logins', 'assignment_completion_rate', 
        'forum_posts', 'event_participation', 'hackathons_participated',
        'aptitude_score', 'coding_score', 'mock_interview_score',
        'technical_skills', 'soft_skills', 'faculty_rating', 'satisfaction_score'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # 2. String Normalization
    string_cols = ['name', 'department', 'year', 'gender', 'student_id']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    # 3. Validation Rules
    df['attendance_rate'] = df['attendance_rate'].clip(0, 100)
    df['assignment_completion_rate'] = df['assignment_completion_rate'].clip(0, 100)
    df['cgpa'] = df['cgpa'].clip(0.0, 10.0)

    return df

if __name__ == "__main__":
    df = load_and_clean_data()
    print(f"Data Pipeline Check: Successfully loaded {len(df)} student records with {len(df.columns)} features.")
    print("Columns:", list(df.columns))
