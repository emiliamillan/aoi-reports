import email
from bs4 import BeautifulSoup

def mht_to_txt(mht_file_path, txt_file_path):
    # Read the MHT file
    with open(mht_file_path, 'rb') as mht_file:
        mht_data = mht_file.read()
    
    # Parse the MHT file using the email library
    msg = email.message_from_bytes(mht_data)
    
    # Extract the HTML part from the MHT file
    html_content = None
    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html_content = part.get_payload(decode=True)
            break
    
    if html_content is None:
        raise ValueError("No HTML content found in MHT file")
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Extract text from the parsed HTML
    text_content = soup.get_text()
    
    # Write the extracted text to a TXT file
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text_content)

# Example usage
mht_to_txt('mht file/copy.mht', 'output.txt')
