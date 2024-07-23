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
html_text = """
<ul class="menu" role="tree">
    <li class="python-meta current_item selectedcurrent_branch selected">
        <a href="/" title="The Python Programming Language" class="current_item selectedcurrent_branch selected">Python</a>
    </li>
    <li class="psf-meta ">
        <a href="https://www.python.org/psf/" title="The Python Software Foundation" >PSF</a>
    </li>
    <li class="docs-meta ">
        <a href="https://docs.python.org" title="Python Documentation" >Docs</a>
    </li>
    <li class="pypi-meta ">
        <a href="https://pypi.org/" title="Python Package Index" >PyPI</a>
    </li>
    <li class="jobs-meta ">
        <a href="/jobs/" title="Python Job Board" >Jobs</a>
    </li>
    <li class="shop-meta ">
        <a href="/community-landing/"  >Community</a>
    </li>
</ul>
"""

cleaned_text = clean_html_tags(html_text)
print("Cleared text:")