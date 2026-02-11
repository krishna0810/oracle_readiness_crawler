# 🌐 Website Crawler & PDF Generator

A powerful Python tool that crawls websites, analyzes content using AI, and generates professional PDF reports with summaries and buildable project ideas for each module.

## ✨ Features

- 🕷️ **Smart Web Crawling**: Automatically discovers and crawls all internal pages
- 🤖 **AI-Powered Analysis**: Uses Claude AI to generate intelligent summaries
- 📊 **Auto-Organization**: Groups pages into logical modules
- 📋 **Project Identification**: Identifies specific things you can build from the content
- 📄 **Professional PDFs**: Creates beautiful, well-formatted PDF reports
- 🎨 **Rich Formatting**: Tables, sections, colors, and proper typography

## 🚀 Quick Start

### Option 1: Google Colab (Recommended)

Perfect for users who want a no-setup, browser-based solution:

1. **Open the notebook in Google Colab**:
   - Upload `Website_Crawler_PDF_Generator.ipynb` to Google Colab
   - Or click: [Open in Colab](https://colab.research.google.com/)

2. **Configure your settings** (in Step 3):
   ```python
   WEBSITE_URL = "https://your-target-website.com"
   MAX_PAGES = 30
   ANTHROPIC_API_KEY = "your-api-key-here"  # Optional
   ```

3. **Run all cells** (Runtime → Run all)

4. **Download your PDFs** from the `pdfs` folder or use the zip download cell

### Option 2: Python Script

For users who prefer running locally:

1. **Install dependencies**:
   ```bash
   pip install beautifulsoup4 requests reportlab
   ```

2. **Run the script**:
   ```bash
   python website_crawler_pdf_generator.py
   ```

3. **Follow the prompts**:
   - Enter website URL
   - Set maximum pages to crawl
   - (Optional) Enter your Anthropic API key

4. **Find your PDFs** in the `./pdfs` folder

## 📋 Requirements

- Python 3.7+
- Internet connection
- (Optional) Anthropic API key for AI-powered analysis

### Python Packages

```
beautifulsoup4>=4.12.0
requests>=2.31.0
reportlab>=4.0.0
```

## 🔑 Getting an Anthropic API Key (Optional)

While the tool works without an API key (using basic analysis), AI-powered analysis provides much better results.

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new API key
5. Copy and use it in the configuration

**Note**: The free tier includes $5 of credits, which is plenty for analyzing multiple websites.

## 📖 How It Works

### 1. **Web Crawling**
   - Starts from your provided URL
   - Discovers all internal links
   - Respects the same-domain policy
   - Extracts clean content from each page

### 2. **Content Organization**
   - Groups pages by URL structure
   - Creates logical modules (e.g., "Docs", "API", "Tutorials")
   - Maintains page metadata

### 3. **AI Analysis** (with API key)
   - Summarizes each module's content
   - Identifies 3-5 specific buildable projects
   - Extracts key concepts and technologies
   - Provides actionable insights

### 4. **PDF Generation**
   - Creates one PDF per module
   - Beautiful formatting with colors and sections
   - Includes:
     - Module summary
     - Buildable projects list
     - Key concepts
     - Complete page inventory
     - Timestamps and metadata

## 📊 Example Output

For a documentation website, you might get:

```
pdfs/
├── home_analysis.pdf
├── getting_started_analysis.pdf
├── api_reference_analysis.pdf
├── tutorials_analysis.pdf
└── examples_analysis.pdf
```

Each PDF contains:
- **Summary**: 2-3 paragraph overview of the module
- **Buildable Projects**: Specific things you can create
- **Key Concepts**: Important technologies/terms
- **Page List**: All pages with word counts

## 🎯 Use Cases

- **Learning Resources**: Understand documentation structure
- **Project Planning**: Find implementation ideas
- **Content Analysis**: Get overview of large websites
- **Knowledge Mining**: Extract key concepts from documentation
- **Competitive Research**: Analyze competitor documentation
- **Archive Creation**: Save website content in organized PDFs

## ⚙️ Configuration Options

### In Google Colab / Script

```python
# Website to analyze
WEBSITE_URL = "https://example.com"

# Maximum pages to crawl (prevents infinite crawling)
MAX_PAGES = 50  # Recommended: 20-100

# Optional: Enable AI-powered analysis
ANTHROPIC_API_KEY = "sk-ant-..."  # Leave empty for basic analysis
```

### Customization

You can modify the code to:
- Change PDF styling (colors, fonts, layout)
- Adjust content extraction rules
- Add custom analysis logic
- Modify module organization rules
- Change output formats

## 🛡️ Best Practices

1. **Start Small**: Test with `MAX_PAGES=10` first
2. **Respect Websites**: The crawler is polite (0.5s delay) but check robots.txt
3. **Use API Key**: AI analysis is much better than basic analysis
4. **Check Permissions**: Ensure you have the right to crawl the website
5. **Review Output**: PDFs are auto-generated; review for accuracy

## 🚨 Troubleshooting

### "No content extracted"
- Check if the URL is correct and accessible
- Some websites block crawlers
- Try a different website

### "API Error: 401"
- Check your API key is correct
- Ensure you have credits remaining
- Try without AI (basic analysis)

### PDFs look empty
- Website might have dynamic content (JavaScript-heavy)
- Try crawling static documentation sites
- Check if content is behind authentication

### Too many pages
- Reduce `MAX_PAGES` value
- Target specific subdirectories in URL

## 🔍 Advanced Usage

### Crawl Specific Sections

```python
# Instead of root URL, use specific section
WEBSITE_URL = "https://docs.example.com/api"
```

### Custom Module Organization

Edit the `organize_by_modules` method to use different logic:

```python
def organize_by_modules(self, pages_content):
    # Custom logic here
    # Group by content type, topic, etc.
    pass
```

### Export to Other Formats

The code extracts structured data that can be exported to:
- JSON
- Markdown
- HTML
- Database

## 📄 Output Format

### PDF Structure

```
Module Name (Title Page)
├── Generation Date & Source
├── Summary Section
│   └── 2-3 paragraph overview
├── Buildable Projects Section
│   ├── Project 1
│   ├── Project 2
│   └── Project 3-5
├── Key Concepts Section
│   └── Comma-separated list
└── Pages Table (New Page)
    ├── Page #
    ├── Title
    └── Word Count
```

## 🤝 Contributing

Feel free to modify and extend this tool:
- Add new analysis features
- Improve PDF styling
- Support different output formats
- Enhance AI prompts
- Add language support

## 📝 License

This tool is provided as-is for educational and personal use.

## ⚡ Performance

- **Crawling**: ~2 seconds per page (with 0.5s delay)
- **AI Analysis**: ~5-10 seconds per module
- **PDF Generation**: <1 second per module

**Total time for 30 pages, 5 modules**: ~2-3 minutes

## 🎓 Examples

### Python Documentation
```python
WEBSITE_URL = "https://docs.python.org/3/"
MAX_PAGES = 50
```

### React Documentation
```python
WEBSITE_URL = "https://react.dev/"
MAX_PAGES = 40
```

### Your Own Project Docs
```python
WEBSITE_URL = "https://yourproject.readthedocs.io/"
MAX_PAGES = 30
```

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your Python version (3.7+)
3. Ensure all dependencies are installed
4. Try with a simpler website first

## 🎉 Success Tips

1. **Good URLs to start with**:
   - Documentation sites (Read the Docs, GitHub Pages)
   - Static blogs
   - Product documentation

2. **URLs to avoid**:
   - Social media sites
   - E-commerce sites (too many products)
   - Sites requiring login
   - JavaScript-heavy SPAs

3. **Optimal settings**:
   - MAX_PAGES: 20-50 for most sites
   - Use API key for best results
   - Start with subdirectories for large sites

---

**Happy Crawling! 🕷️📄**

For questions or improvements, feel free to modify the code!
