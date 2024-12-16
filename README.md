# Web to Markdown Converter

A Python web application that converts web pages to clean markdown format using OpenAI's GPT-4 model.

## Features

- Clean, modern web interface
- Converts any webpage to markdown format
- Uses GPT-4 to enhance and clean up the markdown
- Automatic file download
- Progress indication and error handling

## Setup

1. Create the conda environment:
```bash
conda env create -f environment.yml
```

2. Activate the environment:
```bash
conda activate web-to-md
```

3. Create a `.env` file with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

### Web Interface

1. Start the web server:
```bash
python app.py
```

2. Open your browser and navigate to `http://localhost:8000`
3. Enter a URL and click "Convert to Markdown"
4. The converted markdown file will be downloaded automatically

### Command Line

You can also use the command-line interface:
```bash
python web_to_md.py https://example.com
```

The converted markdown will be saved in the `output` directory. 