from flask import Flask, request, jsonify, send_file, render_template
from web_to_md import get_webpage, clean_html, html_to_markdown, enhance_markdown_with_gpt, save_markdown
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Process the webpage
        html_content = get_webpage(url)
        clean_content = clean_html(html_content)
        markdown_content = html_to_markdown(clean_content)
        enhanced_markdown = enhance_markdown_with_gpt(markdown_content, url)
        
        # Save the file and get the filename
        output_file = save_markdown(enhanced_markdown, url)
        
        # Return the file path for download
        return jsonify({
            'success': True,
            'file': output_file,
            'message': 'Conversion successful'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True) 