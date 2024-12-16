import os
import sys
import requests
from bs4 import BeautifulSoup
import html2text
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
from urllib.parse import urlparse

# Load environment variables
load_dotenv()

def get_webpage(url):
    """Fetch webpage content."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        sys.exit(1)

def clean_html(html_content):
    """Clean HTML using BeautifulSoup."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove script and style elements
    for script in soup(["script", "style"]):
        script.decompose()
    
    # Get text
    return str(soup)

def html_to_markdown(html_content):
    """Convert HTML to markdown."""
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_tables = False
    return converter.handle(html_content)

def enhance_markdown_with_gpt(markdown_content, url):
    """Enhance markdown content using GPT-4."""
    client = OpenAI()
    
    prompt = f"""Please improve this markdown content from {url}. 
    Make it more readable and well-formatted while preserving all important information. 
    Remove any unnecessary content like navigation menus, footers, or ads. 
    Ensure proper heading hierarchy and clean formatting.
    
    Content:
    {markdown_content}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a markdown formatting expert. Convert web content to clean, well-structured markdown."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=8192,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return markdown_content

def save_markdown(markdown_content, url):
    """Save markdown content to file."""
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Create filename from URL and timestamp
    domain = urlparse(url).netloc
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"output/{domain}_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filename

def main():
    if len(sys.argv) != 2:
        print("Usage: python web_to_md.py <url>")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"Processing {url}...")
    
    # Get and process webpage
    html_content = get_webpage(url)
    clean_content = clean_html(html_content)
    markdown_content = html_to_markdown(clean_content)
    enhanced_markdown = enhance_markdown_with_gpt(markdown_content, url)
    
    # Save result
    output_file = save_markdown(enhanced_markdown, url)
    print(f"Markdown saved to: {output_file}")

if __name__ == "__main__":
    main() 