# screener.py
# This file talks to OpenAI's AI model.
# It takes a job description and a resume's text, asks the AI to
# compare them, and gets back a score + analysis as structured data.

# Import 'os' so we can read environment variables (like our API key)
import os

# Import 'json' so we can convert the AI's text response into a Python dictionary
import json

# Import a function that loads variables from our .env file
from dotenv import load_dotenv

# Import ChatOpenAI - this is LangChain's way of talking to OpenAI's models
from langchain_openai import ChatOpenAI

# Import a class that represents a message we send to the AI
from langchain_core.messages import HumanMessage


# Load the variables from .env (this reads OPENAI_API_KEY and makes it available)
load_dotenv()


def screen_resume(job_description, resume_text):
    """
    Sends the job description and resume text to OpenAI,
    and asks it to return a JSON object with scoring details.

    Parameters:
        job_description: string - the job description text
        resume_text: string - the extracted text from the resume PDF

    Returns:
        A Python dictionary containing:
        - match_score
        - matched_skills
        - missing_skills
        - skill_gap_summary
        - recommendation
    """

    # Create a connection to OpenAI's chat model
    # model="gpt-3.5-turbo" is a fast, low-cost model - perfect for this project
    # temperature=0 means the AI gives more consistent, less random answers
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    # This is the instruction (prompt) we send to the AI.
    # We are very specific about what format we want back: pure JSON.
    prompt = f"""
You are an expert technical recruiter and resume screener.

Compare the following job description and resume.
Return ONLY a valid JSON object (no extra text, no markdown formatting)
with exactly these keys:

- "match_score": an integer from 0 to 100 representing how well the resume matches the job
- "matched_skills": a list of skills/keywords found in both the job description and resume
- "missing_skills": a list of important skills from the job description that are NOT in the resume
- "skill_gap_summary": a 2-3 sentence summary explaining the candidate's fit
- "recommendation": one of "Strong fit", "Moderate fit", or "Poor fit"

Job Description:
{job_description}

Resume:
{resume_text}
"""

    # Send the prompt to the AI and wait for a response
    # HumanMessage wraps our prompt text as a "message from the user"
    response = llm.invoke([HumanMessage(content=prompt)])

    # response.content contains the AI's text reply
    # We expect it to be a JSON string, so we convert it into a Python dictionary
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError:
        # If the AI didn't return clean JSON, we return an error message
        # instead of crashing the whole app
        result = {
            "match_score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "skill_gap_summary": "Could not parse AI response. Please try again.",
            "recommendation": "Error"
        }

    return result