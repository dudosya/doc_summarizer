from bs4 import BeautifulSoup
import requests

base_url = "https://adilet.zan.kz"
filter_url = "/rus/index/docs/dt=2024"

def extract_article_content(doc_url):
    response = requests.get(doc_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = soup.find_all('article')
    
    all_text = []
    
    for article in articles:
        text_content = article.get_text(strip=False)
        all_text.append(text_content)
        
    return "\n\n".join(all_text)


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


def scrape_n_docs(start_url, num_docs):
    current_url = start_url
    all_doc_links = []
    
    while current_url and len(all_doc_links) < num_docs:
        print(f"Scraping page: {current_url}")
        doc_links, next_page_url = extract_doc_links(current_url)
        all_doc_links.extend(doc_links)
        current_url = next_page_url
        
    
        
    for idx, doc_url in enumerate(all_doc_links, start=1):
        print(f"Processing doc {idx}/{num_docs}: {doc_url}")
        try:
            article_content = extract_article_content(doc_url)
            print(f"Document {idx} content: \n")
            print(article_content)
            print("\n" + "="*80 + "\n")
        except Exception as e:
            print(f"Error processing doc {idx} at {doc_url}: {e}")
            

scrape_n_docs(base_url + filter_url, 25)