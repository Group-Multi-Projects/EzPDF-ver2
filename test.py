from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
# Open the HTML file and read its contents
html_file_path = 'media/files/giayxacnhan.html'
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Translate the text content
translator = GoogleTranslator(source='auto', target='en')

# Replace the original text with the translated text in the HTML structure
new_html_file_path = 'media/files/giayxacnhan.html'
start_time = time.time()
for element in soup.find_all(text=True):
    if element.strip():
        try:
            translated_text = translator.translate(element)
            if translated_text:
                element.replace_with(translated_text)
        except Exception as e:
            print(f"Error translating element: {element}\n{e}")

# Save the modified HTML back to the file
with open(new_html_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))
time.sleep(1)
end_time = time.time()
duration = end_time - start_time
print(f"Translation and saving completed in {duration:.2f} seconds")
