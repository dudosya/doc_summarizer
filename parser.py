from bs4 import BeautifulSoup
import requests
from io import BytesIO
import pdfplumber

url = "https://senate.parlam.kz/ru-RU/lawProjects/details/6134"
base_url = "https://senate.parlam.kz"  # Base URL for constructing full links

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract links to PDFs
pdf_links = [base_url + link['href'] for link in soup.find_all('a', title="Скачать")]

# Process each PDF link
for pdf_link in pdf_links:
    pdf_response = requests.get(pdf_link)
    pdf_content = BytesIO(pdf_response.content)
    
    print(f"Processing PDF from {pdf_link}")
    
    try:
        with pdfplumber.open(pdf_content) as pdf:
            for page in pdf.pages:
                # Adjust x_tolerance and y_tolerance to improve text extraction
                text = page.extract_text(x_tolerance=1, y_tolerance=1)
                
                if text and text.strip():  # Ensure the text is not empty
                    print("Text extracted with pdfplumber:")
                    print(text)
                else:
                    print("No valid text extracted on this page. Skipping.")
    except Exception as e:
        print(f"Error processing PDF from {pdf_link}: {e}")
