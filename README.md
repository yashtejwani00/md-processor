# MD File Processor - Web Application

A complete web application for processing Markdown files with drag-and-drop interface.

## 📦 Files Created

All files are located in: `/home/claude/md-processor/`

```
md-processor/
├── server.py                 # Flask backend
├── md_to_confluence.py       # Confluence converter
├── mermaid_to_png.py         # Mermaid PNG converter
├── index.html                # Frontend web page
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
cd /home/claude/md-processor
pip install -r requirements.txt
```

### 2. Install Mermaid CLI (Optional - for PNG conversion)

```bash
npm install -g @mermaid-js/mermaid-cli
```

### 3. Start the Server

```bash
python server.py
```

You should see:
```
============================================================
🚀 MD File Processor Server
============================================================
Server running at: http://localhost:5000
Mermaid CLI available: True
============================================================
```

### 4. Open the Web Interface

Open `index.html` in your browser:
```bash
# Option 1: Open directly
open index.html   # Mac
xdg-open index.html   # Linux
start index.html   # Windows

# Option 2: Navigate in browser
file:///home/claude/md-processor/index.html
```

## 📖 Usage

1. **Drag & Drop** your `.md` file onto the upload area
2. Choose an action:
   - **📋 Reformat File**: Converts to Confluence-compatible Markdown
   - **🎨 Mermaid to PNG**: Extracts and converts Mermaid diagrams
3. File will automatically download to your browser

## ✨ Features

### Reformat File (Confluence Converter)
- Converts Markdown to Confluence-compatible format
- Preserves headers, code blocks, tables, lists
- Output: `.txt` file ready to paste into Confluence

### Mermaid to PNG
- Extracts all Mermaid diagrams from MD file
- Converts each to PNG image with transparent background
- **Single diagram**: Downloads as `.png`
- **Multiple diagrams**: Downloads as `.zip` with all images

## 🔧 Troubleshooting

### "Server not running" error
```bash
# Make sure server is running
python server.py
```

### "mermaid-cli not installed" warning
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Verify installation
mmdc --version
```

### CORS errors
```bash
# Install Flask-CORS
pip install flask-cors
```

### Port 5000 already in use
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>
```

## 📝 Command Line Usage

You can also use the scripts directly from command line:

### Confluence Converter
```bash
python md_to_confluence.py document.md
# Creates: document-Confluence.txt
```

### Mermaid to PNG
```bash
python mermaid_to_png.py document.md
# Creates: ./mermaid_images/document_diagram_1.png
```

## 🛠️ API Endpoints

- `GET /health` - Server health check
- `POST /convert/confluence` - Convert MD to Confluence format
- `POST /convert/mermaid` - Extract Mermaid diagrams to PNG

## 📋 Requirements

- Python 3.7+
- Flask & Flask-CORS
- Node.js (for mermaid-cli)
- Modern web browser

## 🔒 Security

- Server runs on localhost only
- 16MB max file upload size
- Only accepts `.md` files

## 💡 Tips

- Server must be running before opening the web interface
- Check browser console (F12) for detailed error messages
- Multiple diagrams are automatically zipped for download

---

## 🚀 Deployment

### Deploy to Render

1. **Create a new Web Service** on [Render](https://render.com)
2. **Connect your GitHub repository**
3. **Configure the service:**
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt && npm install -g @mermaid-js/mermaid-cli`
   - Start Command: `gunicorn server:app`
4. **Add environment variables** (optional):
   - `PYTHON_VERSION`: `3.11.0`
5. **Deploy!** Your app will be available at `https://your-app.onrender.com`

### Deploy to Railway

1. **Create a new project** on [Railway](https://railway.app)
2. **Deploy from GitHub repo**
3. Railway will automatically detect the Procfile and deploy
4. **Add Node.js buildpack** for mermaid-cli:
   - Go to Settings → Add Buildpack
   - Add: `heroku/nodejs`
5. Your app will be live at the generated Railway URL

### Deploy to Heroku

1. **Install Heroku CLI** and login:
   ```bash
   heroku login
   ```

2. **Create a new Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Add Node.js buildpack** (for mermaid-cli):
   ```bash
   heroku buildpacks:add --index 1 heroku/nodejs
   heroku buildpacks:add --index 2 heroku/python
   ```

4. **Create package.json** for Node.js dependencies:
   ```bash
   echo '{"dependencies": {"@mermaid-js/mermaid-cli": "^10.6.1"}}' > package.json
   ```

5. **Deploy:**
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push heroku main
   ```

6. **Open your app:**
   ```bash
   heroku open
   ```

### Important Notes for Deployment

- The app uses Node.js (mermaid-cli) and Python, so both buildpacks/environments are needed
- Ensure `PORT` environment variable is used (already configured in Procfile)
- File uploads are stored in `/tmp` which is ephemeral - files are automatically cleaned up
- Increase timeout if processing large files (configured to 120s in Procfile)

---

**Made with ❤️ for easy Markdown processing**
