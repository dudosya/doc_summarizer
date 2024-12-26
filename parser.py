from bs4 import BeautifulSoup
import requests
import json
import os
from datetime import datetime
import hashlib

base_url = "https://adilet.zan.kz"
filter_url = "/rus/index/docs/dt=2024"

def extract_article_content(doc_url):
    response = requests.get(doc_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Get the title if available
    title = soup.find('h1')
    title_text = title.get_text(strip=True) if title else "No title"
    
    articles = soup.find_all('article')
    all_text = []
    
    for article in articles:
        text_content = article.get_text(strip=True)
        all_text.append(text_content)
        
    return {
        "title": title_text,
        "url": doc_url,
        "content": "\n\n".join(all_text),
        "timestamp": datetime.now().isoformat()
    }

def extract_doc_links(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    post_headers = soup.find_all('h4', class_="post_header")
    
    links = []
    
    for post_header in post_headers:
        link = post_header.find('a')
        if link and 'href' in link.attrs:
            href = link['href']
            if not href.startswith('http'):
                href = base_url + href
            links.append(href)
            
    next_page = soup.find('a', class_="nextpostslink", text = '>')
    next_page_url = None
    if next_page and 'href' in next_page.attrs:
        next_page_url = base_url + next_page['href']
        
    return links, next_page_url

def create_corpus(start_url, num_docs, output_dir="corpus"):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    current_url = start_url
    all_doc_links = []
    corpus = []
    
    # Create a metadata file to keep track of all documents
    metadata_file = os.path.join(output_dir, "metadata.json")
    
    while current_url and len(all_doc_links) < num_docs:
        print(f"Scraping page: {current_url}")
        doc_links, next_page_url = extract_doc_links(current_url)
        all_doc_links.extend(doc_links)
        current_url = next_page_url
    
    for idx, doc_url in enumerate(all_doc_links[:num_docs], start=1):
        print(f"Processing doc {idx}/{num_docs}: {doc_url}")
        try:
            # Extract content and metadata
            doc_data = extract_article_content(doc_url)
            
            # Create a unique filename based on URL
            filename = hashlib.md5(doc_url.encode()).hexdigest()
            
            # Save individual document
            doc_path = os.path.join(output_dir, f"{filename}.json")
            with open(doc_path, 'w', encoding='utf-8') as f:
                json.dump(doc_data, f, ensure_ascii=False, indent=2)
            
            # Add to corpus
            corpus.append(doc_data)
            
            print(f"Saved document {idx} to {doc_path}")
            
        except Exception as e:
            print(f"Error processing doc {idx} at {doc_url}: {e}")
    
    # Save complete corpus metadata
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            "total_documents": len(corpus),
            "creation_date": datetime.now().isoformat(),
            "documents": corpus
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nCorpus creation complete. Total documents: {len(corpus)}")
    print(f"Corpus saved in directory: {output_dir}")
    return corpus

if __name__ == "__main__":
    corpus = create_corpus(base_url + filter_url, 20)