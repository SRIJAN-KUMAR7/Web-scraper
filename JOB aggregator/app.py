from flask import Flask, render_template, request, send_file
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

app = Flask(__name__)

def fetch_all_links(base_url, specific_part=''):
    full_url = base_url + specific_part
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all links and join them with the base URL if they are relative
    links = [urljoin(base_url, a['href']) for a in soup.find_all('a', href=True)]
    
    return links

def save_to_excel(links):
    df = pd.DataFrame(links, columns=["Links"])
    file_path = "links.xlsx"
    df.to_excel(file_path, index=False)
    return file_path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    base_url = request.form['base_url']
    specific_part = request.form.get('specific_part', '')

    links = fetch_all_links(base_url, specific_part)
    file_path = save_to_excel(links)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
