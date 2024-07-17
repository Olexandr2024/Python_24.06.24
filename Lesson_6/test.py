def clean_html_tags(text):
    in_tag = 0
    result = ''
    i = 0

    while i < len(text):
        if text[i] == '<':
            in_tag += 1
        elif text[i] == '>':
            in_tag -= 1
        elif in_tag == 0:
            result += text[i]
        i += 1


    while '<' in result:
        start = result.find('<')
        end = result.find('>')
        if start != -1 and end != -1:
            result = result[:start] + result[end + 1:]

    return result

# Example usage
html_text = '''
<div id="rcnt" style="clear:both;position:relative;zoom:1">
'''

cleaned_text = clean_html_tags(html_text)
print("Cleared text:")

