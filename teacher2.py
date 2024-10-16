import streamlit as st
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
import os
import hashlib
from io import BytesIO
import sqlite3
from fpdf import FPDF

# SQLite Database setup
conn = sqlite3.connect('teacher_evaluation.db')
c = conn.cursor()

# Create table if it does not exist
c.execute('''CREATE TABLE IF NOT EXISTS evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name TEXT,
                roll_no TEXT,
                class TEXT,
                teacher_name TEXT,
                subject TEXT,
                q1 TEXT, q2 TEXT, q3 TEXT, course_content_comments TEXT,
                q4 TEXT, q5 TEXT, q6 TEXT, student_contribution_comments TEXT,
                q7 TEXT, q8 TEXT, q9 TEXT, q10 TEXT, learning_env_comments TEXT,
                q11 TEXT, q12 TEXT, q13 TEXT, q14 TEXT, learning_resources_comments TEXT,
                q15 TEXT, q16 TEXT, q17 TEXT, quality_delivery_comments TEXT,
                q18 TEXT, q19 TEXT, q20 TEXT, assessment_comments TEXT,
                q21 TEXT, q22 TEXT, q23 TEXT, q24 TEXT,
                tq1 TEXT, tq2 TEXT, tq3 TEXT, tq4 TEXT, tq5 TEXT, tq6 TEXT, tq7 TEXT, tq8 TEXT, tq9 TEXT, tq10 TEXT, tq11 TEXT, tq12 TEXT, tq13 TEXT,
                tq14 TEXT, tq15 TEXT, tq16 TEXT, tq17 TEXT, tq18 TEXT, teacher_eval_comments TEXT
            )''')
conn.commit()

# App Layout
st.title("Teacher Evaluation System")

# User Selection - Student or Admin
user_role = st.radio("Select Role:", ("Student", "Admin"))

# List of teachers and subjects
teachers = [
    "Dr. Muhammad Khurshid", "Dr. Saima Sadaf", "Prof. Dr. Muhammad Farooq Sabar", "Prof. Dr. Saba Irshad",
    "Dr. Moazzam Ali", "Dr. Zeeshan Mutahir", "Dr. Muhammad Shahbaz Aslam", "Dr. Iram Gull",
    "Dr. Beenish Maqsood", "Dr. Fatima Mueece", "Dr. Asma Irshad", "Dr. Naeem Mahmood Ashraf",
    "Dr. Barizah Malik", "Dr. Hafiz Muzammel Rehman", "Mrs. Afshan Iqbal", "Mrs. Sumaira Pervaiz"
]
subjects = [
    "English-I", "English-II", "English-III", "English-IV/International Language",
    "Pakistan Studies", "Islamic Studies/Ethics", "Mathematics-I", "Mathematics-II", "Statistics",
    "Physical Chemistry (General)", "Inorganic Chemistry (General)", "Organic Chemistry (General)", "Analytical Chemistry & Instrumentation",
    "Ecosystem & Environment", "Introduction to Computer", "Social Sciences (Any Subject)", "Biosafety & Bioethics", "Genetic Resources & Conservation",
    "Plant Diversity", "Animal Diversity", "Cell Biology", "Genetics", "Biochemistry-I", "Biochemistry-II", "Microbiology", "Molecular Biology-I", "Molecular Biology-II", "Immunology",
    "Enzymes", "Biochemical Techniques", "Health Biotechnology", "Microbial Biotechnology", "Agriculture Biotechnology", "Food Biotechnology", "Recombinant DNA Technology",
    "Metabolomics, Proteomics, and Genomics", "Environment Biotechnology", "Downstream Technology", "Principles of Biochemical Engineering", "Cell and Tissue Culture",
    "Elements of Biotechnology", "Bioinformatics", "Skills Enhancement"
]

# Student Section
if user_role == "Student":
    # Student Information
    st.header("Student Information")
    student_name = st.text_input("Enter your name:")
    student_roll_no = st.text_input("Enter your Departmental Roll Number:")
    student_class = st.text_input("Enter your class:")
    st.write("Note: Your name will not be mentioned in the evaluation form.")

    # Select Teacher Name and Subject
    teacher_name = st.selectbox("Select the teacher's name:", teachers)
    subject = st.selectbox("Select the subject:", subjects)

    # Fill Course Evaluation Form (Proforma - 1)
    st.header("Student Course Evaluation Questionnaire")
    st.subheader("Course Content and Organization")
    q1 = st.radio("1. The course objectives were clear", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q2 = st.radio("2. The Course workload was manageable", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q3 = st.radio("3. The Course was well organized (e.g. timely access to materials, notification of changes, etc.)", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    course_content_comments = st.text_area("Comments (Course Content and Organization):")

    st.subheader("Student Contribution")
    q4 = st.radio("5. Approximate level of your own attendance during the whole Course", ("<20%", "21-40%", "41-60%", "61-80%", ">81%"))
    q5 = st.radio("6. I participated actively in the Course", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q6 = st.radio("7. I think I have made progress in this Course", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    student_contribution_comments = st.text_area("Comments (Student Contribution):")

    st.subheader("Learning Environment and Teaching Methods")
    q7 = st.radio("9. I think the Course was well structured to achieve the learning outcomes", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q8 = st.radio("10. The learning and teaching methods encouraged participation.", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q9 = st.radio("11. The overall environment in the class was conducive to learning.", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q10 = st.radio("12. Classrooms were satisfactory", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    learning_env_comments = st.text_area("Comments (Learning Environment and Teaching Methods):")

    st.subheader("Learning Resources")
    q11 = st.radio("14. Learning materials (Lesson Plans, Course Notes etc.) were relevant and useful.", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q12 = st.radio("15. Recommended reading Books etc. were relevant and appropriate", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q13 = st.radio("16. The provision of learning resources in the library was adequate and appropriate", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q14 = st.radio("17. The provision of learning resources on the Web was adequate and appropriate (if relevant)", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    learning_resources_comments = st.text_area("Comments (Learning Resources):")

    st.subheader("Quality of Delivery")
    q15 = st.radio("19. The Course stimulated my interest and thought on the subject area", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q16 = st.radio("20. The pace of the Course was appropriate", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q17 = st.radio("21. Ideas and concepts were presented clearly", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    quality_delivery_comments = st.text_area("Comments (Quality of Delivery):")

    st.subheader("Assessment")
    q18 = st.radio("23. The method of assessment was reasonable", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q19 = st.radio("24. Feedback on assessment was timely", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q20 = st.radio("25. Feedback on assessment was helpful", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    assessment_comments = st.text_area("Comments (Assessment):")

    st.subheader("Additional Core Questions")
    q21 = st.radio("27. I understood the lectures", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q22 = st.radio("28. The material was well organized and presented", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q23 = st.radio("29. The instructor was responsive to student needs and problems", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))
    q24 = st.radio("30. Had the instructor been regular throughout the course?", ("Strongly Agree", "Agree", "Uncertain", "Disagree", "Strongly Disagree"))

    # Teacher Evaluation Form
    st.header("Teacher Evaluation Form")

    st.subheader("Instructor Evaluation")
    tq1 = st.radio("1. The Instructor is prepared for each class", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq2 = st.radio("2. The Instructor demonstrates knowledge of the subject", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq3 = st.radio("3. The Instructor has completed the whole course", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq4 = st.radio("4. The Instructor provides additional material apart from the textbook", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq5 = st.radio("5. The Instructor gives citations regarding current situations with reference to Pakistani context", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq6 = st.radio("6. The Instructor communicates the subject matter effectively", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq7 = st.radio("7. The Instructor shows respect towards students and encourages class participation", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq8 = st.radio("8. The Instructor maintains an environment that is conducive to learning", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq9 = st.radio("9. The Instructor arrives on time", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq10 = st.radio("10. The Instructor leaves on time", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq11 = st.radio("11. The Instructor is fair in examination", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq12 = st.radio("12. The Instructor returns the graded scripts etc. in a reasonable amount of time", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq13 = st.radio("13. The Instructor was available during the specified office hours and for after class consultations", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))

    st.subheader("Course Evaluation")
    tq14 = st.radio("15. The Subject matter presented in the course has increased your knowledge of the subject", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq15 = st.radio("16. The syllabus clearly states course objectives requirements, procedures and grading criteria", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq16 = st.radio("17. The course integrates theoretical course concepts with real-world applications", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq17 = st.radio("18. The assignments and exams covered the materials presented in the course", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))
    tq18 = st.radio("19. The course material is modern and updated", ("A: Strongly Agree", "B: Agree", "C: Uncertain", "D: Disagree", "E: Strongly Disagree"))

    teacher_eval_comments = st.text_area("Comments (Instructor and Course):")

    # Submit Evaluation
    if st.button("Submit Evaluation"):
        evaluation_data = (
            student_name,
            student_roll_no,
            student_class,
            teacher_name,
            subject,
            q1, q2, q3, course_content_comments,
            q4, q5, q6, student_contribution_comments,
            q7, q8, q9, q10, learning_env_comments,
            q11, q12, q13, q14, learning_resources_comments,
            q15, q16, q17, quality_delivery_comments,
            q18, q19, q20, assessment_comments,
            q21, q22, q23, q24,
            tq1, tq2, tq3, tq4, tq5, tq6, tq7, tq8, tq9, tq10, tq11, tq12, tq13,
            tq14, tq15, tq16, tq17, tq18, teacher_eval_comments
        )
        # Save evaluation data to SQLite
        c.execute('''INSERT INTO evaluations (
                        student_name, roll_no, class, teacher_name, subject,
                        q1, q2, q3, course_content_comments,
                        q4, q5, q6, student_contribution_comments,
                        q7, q8, q9, q10, learning_env_comments,
                        q11, q12, q13, q14, learning_resources_comments,
                        q15, q16, q17, quality_delivery_comments,
                        q18, q19, q20, assessment_comments,
                        q21, q22, q23, q24,
                        tq1, tq2, tq3, tq4, tq5, tq6, tq7, tq8, tq9, tq10, tq11, tq12, tq13,
                        tq14, tq15, tq16, tq17, tq18, teacher_eval_comments
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  evaluation_data)
        conn.commit()
        st.success("Thank you for your feedback!")

# Admin Section
elif user_role == "Admin":
    admin_password = st.text_input("Enter Admin Password:", type="password")
    if st.button("Login"):
        if admin_password == 'sbbpu123':
            st.success("Login successful!")

            # Display Evaluations
            c.execute("SELECT * FROM evaluations")
            evaluations = c.fetchall()
            columns = [
                "ID", "Student Name", "Roll No", "Class", "Teacher Name", "Subject",
                "Q1", "Q2", "Q3", "Course Content Comments",
                "Q4", "Q5", "Q6", "Student Contribution Comments",
                "Q7", "Q8", "Q9", "Q10", "Learning Environment Comments",
                "Q11", "Q12", "Q13", "Q14", "Learning Resources Comments",
                "Q15", "Q16", "Q17", "Quality Delivery Comments",
                "Q18", "Q19", "Q20", "Assessment Comments",
                "Q21", "Q22", "Q23", "Q24",
                "TQ1", "TQ2", "TQ3", "TQ4", "TQ5", "TQ6", "TQ7", "TQ8", "TQ9", "TQ10", "TQ11", "TQ12", "TQ13",
                "TQ14", "TQ15", "TQ16", "TQ17", "TQ18", "Teacher Evaluation Comments"
            ]
            evaluations_df = pd.DataFrame(evaluations, columns=columns)
            if not evaluations_df.empty:
                st.dataframe(evaluations_df)

                # Generate and Display Graphs for Course Evaluation
                st.header("Course Evaluation Graphs")
                course_groups = evaluations_df.groupby('Subject')
                for course, data in course_groups:
                    st.subheader(f"Course: {course}")
                    fig, ax = plt.subplots()
                    data['Q1'].value_counts().plot(kind='bar', ax=ax, title=f"Responses for Q1: {course}")
                    st.pyplot(fig)

                # Generate and Display Graphs for Teacher Evaluation
                st.header("Teacher Evaluation Graphs")
                teacher_groups = evaluations_df.groupby('Teacher Name')
                for teacher, data in teacher_groups:
                    st.subheader(f"Teacher: {teacher}")
                    fig, ax = plt.subplots()
                    data['TQ1'].value_counts().plot(kind='bar', ax=ax, title=f"Responses for TQ1: {teacher}")
                    st.pyplot(fig)

                # Count table for evaluations
                st.header("Teacher Evaluation Count Summary")
                teacher_count_summary = evaluations_df['Teacher Name'].value_counts().reset_index()
                teacher_count_summary.columns = ['Teacher Name', 'Number of Evaluations']
                st.table(teacher_count_summary)

                # Detailed response count per teacher
                st.header("Response Summary for Each Teacher")
                response_summary = evaluations_df.groupby(['Teacher Name']).agg(lambda x: x.value_counts().to_dict()).reset_index()
                for index, row in response_summary.iterrows():
                    st.subheader(f"Teacher: {row['Teacher Name']}")
                    st.write({col: row[col] for col in evaluations_df.columns if col not in ['ID', 'Student Name', 'Roll No', 'Class', 'Teacher Name', 'Subject']})

                # Download Evaluations as Excel
                def to_excel(df):
                    output = BytesIO()
                    writer = pd.ExcelWriter(output, engine='xlsxwriter')
                    df.to_excel(writer, index=False, sheet_name='Evaluations')
                    writer.close()
                    processed_data = output.getvalue()
                    return processed_data

                excel_data = to_excel(evaluations_df)
                st.download_button(
                    label="Download Evaluations as Excel",
                    data=excel_data,
                    file_name='teacher_evaluations.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )

                # Download Graphs as PDF
                if st.button("Download Full Report as PDF"):
                    try:
                        pdf = FPDF()
                        pdf.set_auto_page_break(auto=True, margin=15)
                        pdf.add_page()
                        pdf.set_font("Arial", size=12)
                        pdf.cell(200, 10, txt="Teacher Evaluation Report", ln=True, align='C')

                        # Add course graphs
                        for course, data in course_groups:
                            pdf.add_page()
                            pdf.cell(200, 10, txt=f"Course: {course}", ln=True, align='L')
                            
                            # Generate graph as image in memory
                            fig, ax = plt.subplots()
                            data['Q1'].value_counts().plot(kind='bar', ax=ax, title=f"Responses for Q1: {course}")
                            img_data = BytesIO()
                            plt.savefig(img_data, format='png')
                            img_data.seek(0)

                            pdf.image(img_data, x=10, y=20, w=180)
                            plt.close(fig)

                        # Add teacher graphs
                        for teacher, data in teacher_groups:
                            pdf.add_page()
                            pdf.cell(200, 10, txt=f"Teacher: {teacher}", ln=True, align='L')
                            
                            # Generate graph as image in memory
                            fig, ax = plt.subplots()
                            data['TQ1'].value_counts().plot(kind='bar', ax=ax, title=f"Responses for TQ1: {teacher}")
                            img_data = BytesIO()
                            plt.savefig(img_data, format='png')
                            img_data.seek(0)

                            pdf.image(img_data, x=10, y=20, w=180)
                            plt.close(fig)

                        # Add count table
                        pdf.add_page()
                        pdf.cell(200, 10, txt="Teacher Evaluation Count Summary", ln=True, align='L')
                        for index, row in teacher_count_summary.iterrows():
                            pdf.cell(200, 10, txt=f"{row['Teacher Name']}: {row['Number of Evaluations']} evaluations", ln=True, align='L')

                        pdf_output = BytesIO()
                        pdf.output(pdf_output)
                        pdf_output.seek(0)
                        st.download_button(
                            label="Download Full Report as PDF",
                            data=pdf_output,
                            file_name="teacher_evaluation_report.pdf",
                            mime="application/pdf"
                        )
                    except Exception as e:
                        st.error(f"An error occurred while generating the PDF: {e}")
            else:
                st.warning("No evaluations found.")
        else:
            st.error("Invalid password. Please try again.")
