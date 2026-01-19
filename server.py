#!/usr/bin/env python3
"""
Flask Backend for MD File Processor
Handles file uploads and processing for Markdown conversion
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import zipfile
from pathlib import Path
import sys

# Import our conversion modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md_to_confluence import convert_md_to_confluence
from mermaid_to_png import extract_mermaid_diagrams, convert_mermaid_to_png, check_mermaid_cli

app = Flask(__name__)
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = tempfile.gettempdir()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


@app.route('/')
def home():
    """Serve the home page"""
    return send_file('index.html')


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'mermaid_cli_available': check_mermaid_cli()
    })


@app.route('/convert/confluence', methods=['POST'])
def convert_to_confluence():
    """Convert MD file to Confluence-compatible format"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.md'):
            return jsonify({'error': 'File must be a .md file'}), 400
        
        # Read file content
        content = file.read().decode('utf-8')
        
        # Convert content
        converted_content = convert_md_to_confluence(content)
        
        # Generate output filename
        original_name = Path(file.filename).stem
        output_filename = f"{original_name}-Confluence.txt"
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            delete=False,
            suffix='.txt',
            encoding='utf-8'
        )
        temp_file.write(converted_content)
        temp_file.close()
        
        # Send file
        return send_file(
            temp_file.name,
            as_attachment=True,
            download_name=output_filename,
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/convert/mermaid', methods=['POST'])
def convert_mermaid():
    """Extract Mermaid diagrams and convert to PNG"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.md'):
            return jsonify({'error': 'File must be a .md file'}), 400
        
        # Check if mermaid-cli is available
        if not check_mermaid_cli():
            return jsonify({
                'error': 'mermaid-cli (mmdc) is not installed. Install it using: npm install -g @mermaid-js/mermaid-cli'
            }), 500
        
        # Read file content
        content = file.read().decode('utf-8')
        
        # Extract diagrams
        diagrams = extract_mermaid_diagrams(content)
        
        if not diagrams:
            return jsonify({'error': 'No Mermaid diagrams found in file'}), 400
        
        # Create temporary directory for output
        temp_dir = tempfile.mkdtemp()
        base_name = Path(file.filename).stem
        
        # Convert each diagram
        output_files = []
        for diagram_num, diagram_code in diagrams:
            output_filename = f"{base_name}_diagram_{diagram_num}.png"
            output_path = os.path.join(temp_dir, output_filename)
            
            if convert_mermaid_to_png(diagram_code, output_path):
                output_files.append(output_path)
        
        if not output_files:
            return jsonify({'error': 'Failed to convert any diagrams'}), 500
        
        # If single file, return it directly
        if len(output_files) == 1:
            return send_file(
                output_files[0],
                as_attachment=True,
                download_name=os.path.basename(output_files[0]),
                mimetype='image/png'
            )
        
        # If multiple files, create a zip
        zip_path = os.path.join(temp_dir, f"{base_name}_diagrams.zip")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in output_files:
                zipf.write(file_path, os.path.basename(file_path))
        
        return send_file(
            zip_path,
            as_attachment=True,
            download_name=f"{base_name}_diagrams.zip",
            mimetype='application/zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("🚀 MD File Processor Server")
    print("=" * 60)
    print(f"Server running at: http://localhost:5001")
    print(f"Mermaid CLI available: {check_mermaid_cli()}")
    print("=" * 60)
    print("\nPress Ctrl+C to stop the server")
    print()

    app.run(debug=True, host='0.0.0.0', port=5001)
