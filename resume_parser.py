# resume_parser.py
# This file is responsible for one job: reading a PDF resume
# and extracting all the text from it as plain text.

# Import the PdfReader class from the PyPDF2 library
# This lets us open and read PDF files
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_file):
    """
    Takes an uploaded PDF file and returns all the text inside it as a string.

    Parameters:
        pdf_file: the uploaded PDF file (comes from Streamlit's file uploader)

    Returns:
        A single string containing all text from every page of the PDF.
    """

    # Create a PdfReader object - this "opens" the PDF so we can read it
    reader = PdfReader(pdf_file)

    # Create an empty string to collect all the text
    full_text = ""

    # Loop through every page in the PDF, one by one
    for page in reader.pages:
        # extract_text() pulls the text out of the current page
        # Sometimes a page might have no text (e.g. it's an image),
        # so we use "or ''" as a backup to avoid errors
        page_text = page.extract_text() or ""

        # Add this page's text to our full_text string
        # We add a newline "\n" so text from different pages doesn't merge together
        full_text += page_text + "\n"

    # .strip() removes any extra blank space at the very start and end
    return full_text.strip()