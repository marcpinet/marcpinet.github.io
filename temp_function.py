def fix_code_blocks_and_spacing(content):
    """Fix code blocks and ensure proper spacing around all elements"""
    
    # First, ensure proper newlines around code blocks
    # Fix missing newline BEFORE opening ```
    content = re.sub(r'([^\n])(\n```)', r'\1\n\n```', content)
    content = re.sub(r'([^\n])(```)', r'\1\n\n```', content)
    
    # Fix missing newline AFTER closing ```
    content = re.sub(r'(```\n?)([^\n])', r'\1\n\2', content)
    content = re.sub(r'(```)([^\n])', r'\1\n\n\2', content)
    
    # Remove extra newlines BEFORE closing ``` (this was the problem!)
    content = re.sub(r'\n+```', '\n```', content)
    
    # Ensure proper spacing around HTML div elements (like alerts)
    content = re.sub(r'([^\n])(<div)', r'\1\n\n\2', content)
    content = re.sub(r'(</div>)([^\n])', r'\1\n\n\2', content)
    
    # Ensure proper spacing around video elements
    content = re.sub(r'([^\n])(<video)', r'\1\n\n\2', content)
    content = re.sub(r'(</video>)([^\n])', r'\1\n\n\2', content)
    
    # Clean up excessive newlines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    # Clean up spaces at the end of lines
    content = re.sub(r' +\n', '\n', content)
    
    return content