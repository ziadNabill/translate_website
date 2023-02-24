import requests
from bs4 import BeautifulSoup
from googletrans import Translator

def translate_text(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text


# scraping the website using beaytifulSoup library
url = 'https://www.classcentral.com/' # Replace with the URL of your live website
target_language = 'hi' # replace 'hi' with your desired language code

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find all HTML elements that contain text content
elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'a', 'li', 'td'])

# Loop through all elements and translate their content
for element in elements:
    # Check if the element contains any child elements
    if element.find():
        continue
    # Translate the text content
    translator = Translator()
    translation = translator.translate(element.text, dest=target_language)
    translated_text = translation.text
    # Replace the original text content with the translated text content
    element.string.replace_with(translated_text)

# Write the translated HTML content to a file
with open('translated.html', 'w', encoding='utf-8') as file:
    file.write(soup.prettify())
