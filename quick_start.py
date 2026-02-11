"""
QUICK START SCRIPT
==================
The simplest way to run the website crawler!

Just edit the settings below and run:
    python quick_start.py
"""

# ============================================
# EDIT THESE SETTINGS
# ============================================

# The website you want to crawl
WEBSITE_URL = "https://docs.python.org"

# How many pages to crawl (start with a small number!)
MAX_PAGES = 20

# Your Anthropic API key (optional - leave empty for basic analysis)
# Get one free at: https://console.anthropic.com/
API_KEY = ""

# ============================================
# NO NEED TO EDIT BELOW THIS LINE
# ============================================

def check_and_install_packages():
    """Check if required packages are installed, if not install them."""
    import subprocess
    import sys
    
    required_packages = ['beautifulsoup4', 'requests', 'reportlab']
    
    print("🔍 Checking dependencies...")
    try:
        import bs4
        import requests
        import reportlab
        print("✅ All dependencies are installed!\n")
    except ImportError:
        print("📦 Installing required packages...\n")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q'] + required_packages)
        print("✅ Installation complete!\n")

# Install packages if needed
check_and_install_packages()

# Import the main crawler script
import os
import sys

# Check if the main script exists
if not os.path.exists('website_crawler_pdf_generator.py'):
    print("❌ Error: website_crawler_pdf_generator.py not found!")
    print("   Make sure both files are in the same directory.")
    sys.exit(1)

# Load and execute the main functions
print("=" * 70)
print("🌐 Website Crawler & PDF Generator - Quick Start")
print("=" * 70)
print(f"\n📍 Target: {WEBSITE_URL}")
print(f"📄 Max Pages: {MAX_PAGES}")
print(f"🤖 AI Analysis: {'Enabled' if API_KEY else 'Disabled (using basic analysis)'}")
print()

# Import the necessary classes from the main script
exec(open('website_crawler_pdf_generator.py').read())

# Run the crawl
crawler = WebsiteCrawler(WEBSITE_URL, max_pages=MAX_PAGES)
pages_content = crawler.crawl()

if not pages_content:
    print("\n❌ No content extracted. Please check:")
    print("   1. Is the URL correct?")
    print("   2. Is the website accessible?")
    print("   3. Does the website allow crawling?")
    sys.exit(1)

print()

# Organize and analyze
analyzer = ContentAnalyzer(api_key=API_KEY if API_KEY else None)
modules = analyzer.organize_by_modules(pages_content)

print(f"📊 Found {len(modules)} modules:")
for module_name, pages in modules.items():
    print(f"   • {module_name}: {len(pages)} pages")

print()

# Generate PDFs
pdf_generator = PDFGenerator()
generated_pdfs = []

print("🔬 Generating PDFs...\n")

for module_name, pages in modules.items():
    print(f"📝 {module_name}... ", end='', flush=True)
    analysis = analyzer.analyze_with_ai(module_name, pages)
    pdf_path = pdf_generator.generate_pdf(module_name, analysis, pages, WEBSITE_URL)
    generated_pdfs.append(pdf_path)
    print("Done!")

print()
print("=" * 70)
print("✨ Success!")
print(f"\n📁 Generated {len(generated_pdfs)} PDF reports in: ./pdfs/")
print("\nYour PDFs:")
for pdf in generated_pdfs:
    print(f"   📄 {os.path.basename(pdf)}")
print("\n" + "=" * 70)
print("\n💡 Tip: Open the PDFs to see summaries and buildable project ideas!")
