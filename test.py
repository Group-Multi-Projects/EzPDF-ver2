from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# Open the HTML file and read its contents
html_file_path = 'media/files/giayxacnhan.html'
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Translate the text content
translator = GoogleTranslator(source='auto', target='vi')

# Function to translate text
def translate_text(element):
    try:
        translated_text = translator.translate(element)
        if translated_text:
            return element, translated_text
    except Exception as e:
        print(f"Error translating element: {element}\n{e}")
    return element, None

# Record the start time
start_time = time.time()

# Use ThreadPoolExecutor to translate elements concurrently
with ThreadPoolExecutor() as executor:
    futures = {executor.submit(translate_text, element): element for element in soup.find_all(text=True) if element.strip()}
    for future in as_completed(futures):
        element, translated_text = future.result()
        if translated_text:
            element.replace_with(translated_text)

# Save the modified HTML back to the file
with open(html_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

# Record the end time
end_time = time.time()

# Calculate and print the duration
duration = end_time - start_time
print(f"Translation and saving completed in {duration:.2f} seconds")
