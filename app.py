# app.py
# This is the main file - it creates the web interface (UI)
# that users see in their browser, using Streamlit.

# Import streamlit - this builds our web interface
import streamlit as st

# Import our own function to extract text from PDF resumes
from resume_parser import extract_text_from_pdf

# Import our own function that scores resumes using AI
from screener import screen_resume


# Set the title and icon that appear in the browser tab
st.set_page_config(page_title="Resume Screening AI", page_icon="📄", layout="wide")

# Display a big title at the top of the page
st.title("📄 Resume Screening AI")

# Display a short description below the title
st.write("Upload resumes and a job description to get AI-powered candidate scoring.")


# --- SECTION 1: Job Description Input ---
st.header("1. Job Description")

# Create a large text box where the user pastes the job description
job_description = st.text_area(
    "Paste the job description here:",
    height=200,
    placeholder="e.g. We are looking for a Python developer with experience in..."
)


# --- SECTION 2: Resume Upload ---
st.header("2. Upload Resumes")

# Create a file uploader that accepts multiple PDF files
uploaded_files = st.file_uploader(
    "Upload one or more resume PDFs:",
    type=["pdf"],
    accept_multiple_files=True
)


# --- SECTION 3: Screen Button ---
st.header("3. Screen Candidates")

# Create a button - when clicked, the code inside the "if" block runs
if st.button("Screen Resumes"):

    # Check that the user has filled in both the job description and uploaded files
    if not job_description:
        st.warning("Please paste a job description first.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        # This list will store results for every resume
        results = []

        # Show a progress bar so the user knows something is happening
        progress_bar = st.progress(0)

        # Loop through every uploaded resume file
        for i, file in enumerate(uploaded_files):

            # Show a temporary message while processing this file
            with st.spinner(f"Screening {file.name}..."):

                # Step 1: Extract text from the PDF
                resume_text = extract_text_from_pdf(file)

                # Step 2: Send the text to the AI to get a score
                result = screen_resume(job_description, resume_text)

                # Step 3: Add the candidate's name and result to our list
                result["filename"] = file.name
                results.append(result)

            # Update the progress bar (e.g. 1 out of 3 = 33%)
            progress_bar.progress((i + 1) / len(uploaded_files))

        # --- SECTION 4: Display Ranked Results ---
        st.header("4. Results")

        # Sort the results so the highest match_score appears first
        results_sorted = sorted(results, key=lambda x: x["match_score"], reverse=True)

        # Loop through each result and display it
        for rank, result in enumerate(results_sorted, start=1):

            # Create an expandable section for each candidate
            with st.expander(f"#{rank} - {result['filename']} - Score: {result['match_score']}/100"):

                # Show the recommendation (Strong fit / Moderate fit / Poor fit)
                st.subheader(f"Recommendation: {result['recommendation']}")

                # Show the summary explanation
                st.write("**Summary:**", result["skill_gap_summary"])

                # Show matched skills as a comma-separated list
                st.write("**Matched Skills:**", ", ".join(result["matched_skills"]))

                # Show missing skills as a comma-separated list
                st.write("**Missing Skills:**", ", ".join(result["missing_skills"]))
                