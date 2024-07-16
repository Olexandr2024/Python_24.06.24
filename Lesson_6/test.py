import re

def clean_html_tags(text):
    clean = re.compile(r'<.*?>|</.*?>')
    return re.sub(clean, '', text)

# Usage example
html_text = '''
<div id="rcnt" style="clear:both;position:relative;zoom:1">
'''

cleaned_text = clean_html_tags(html_text)
print("Cleansing text: ")
print(cleaned_text)


