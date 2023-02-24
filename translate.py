import os
import requests
from bs4 import BeautifulSoup
from googletrans import Translator

def download_file(url):
    response = requests.get(url)
    filename = os.path.basename(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename

url = 'https://www.classcentral.com' # Replace with the URL of your live website
target_language = 'hi' # Replace 'hi' with your desired language code

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all CSS and JavaScript files and download them
css_links = [link['href'] for link in soup.find_all('link', rel='stylesheet')]
js_links = [script['src'] for script in soup.find_all('script', src=True)]

for link in css_links + js_links:
    if link.startswith('//'):
        link = 'https:' + link
    elif link.startswith('/'):
        link = url + link
    download_file(link)

# Loop through all HTML elements and translate their text content
for element in soup.find_all():
    # Skip elements that don't have any text content or are script or style tags
    if element.name in ['script', 'style'] or not element.string:
        continue
    # Translate text content
    translator = Translator()
    translation = translator.translate(element.string, dest=target_language)
    element.string = translation.text

# Replace links to CSS and JavaScript files with the actual file content
for link in css_links + js_links:
    filename = os.path.basename(link)
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
    css_element = soup.find('link', href=link)
    if css_element is not None:
        css_element['href'] = filename
    js_element = soup.find('script', src=link)
    if js_element is not None:
        js_element['src'] = filename

# Write translated HTML to file
with open('translated.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))