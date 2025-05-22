from bs4 import BeautifulSoup
import requests
import html
import re
from urllib.parse import urlparse


def clean_text_for_json(text):
    """
    Clean text to ensure it's JSON-compatible, handling special characters that break JSON

    Args:
        text: Raw text from the webpage

    Returns:
        Cleaned and sanitized text that won't break JSON
    """
    if not text:
        return ""

    # Replace problematic characters
    text = text.replace('\n', ' ').replace('\t', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    text = html.unescape(text.strip())

    # Handle JSON-breaking characters
    text = text.replace('\\', '\\\\')  # Escape backslashes first
    text = text.replace('"', '\\"')  # Escape double quotes
    text = text.replace('\b', '\\b')  # Escape backspace
    text = text.replace('\f', '\\f')  # Escape form feed
    text = text.replace('\n', '\\n')  # Escape newline
    text = text.replace('\r', '\\r')  # Escape carriage return
    text = text.replace('\t', '\\t')  # Escape tab

    # Remove control characters that break JSON
    text = re.sub(r'[\x00-\x1F\x7F]', '', text)

    return text


# You can modify your original scraper code to use this function:
# Just replace your existing clean_text function call with clean_text_for_json

# Example usage in your original code:
url = "https://prodigyinfotech.dev/"
response = requests.get(url)
my_soup = BeautifulSoup(response.text, "html.parser")

# Extract domain
domain = urlparse(url).netloc

# Use the improved cleaning function
formatted_output = [f"Domain: {domain}"]

# Extract titles
for t in my_soup.find_all(['h1', 'h2']):
    cleaned_title = clean_text_for_json(t.text)  # Use the new function here
    if cleaned_title:
        formatted_output.append(f"Title: {cleaned_title}")

# Extract paragraphs
for p in my_soup.find_all('p'):
    cleaned_para = clean_text_for_json(p.text)  # Use the new function here
    if cleaned_para and len(cleaned_para) > 20:  # Skip very short/malformed ones
        formatted_output.append(f"Paragraph: {cleaned_para}")

# Extract email addresses - make sure they're clean for JSON too
emails = set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", my_soup.text))
for email in emails:
    cleaned_email = clean_text_for_json(email)  # Clean emails as well
    formatted_output.append(f"Email: {cleaned_email}")

# Combine
final_string = "\n".join(formatted_output)

# If you're writing to JSON, use json.dumps with the cleaned text
import json

json_output = json.dumps({"scraped_data": final_string})  # This should now be valid JSON

with open("testing.txt", "w") as file:
    file.write(final_string)

# If you want to output directly as JSON
with open("testing.json", "w") as file:
    json.dump({"scraped_data": final_string}, file)

# Output
print(final_string)