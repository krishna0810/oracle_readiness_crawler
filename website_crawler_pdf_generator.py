"""
Website Crawler & PDF Generator
================================
This script crawls a website, analyzes content using Claude AI,
and generates PDFs with summaries and buildable project ideas.

Perfect for running in Google Colab!
"""

import os
import re
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from datetime import datetime
import time

# PDF generation
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY


class WebsiteCrawler:
    """Crawls a website and extracts content from all internal pages."""
    
    def __init__(self, base_url, max_pages=50):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.pages_content = []
        self.domain = urlparse(base_url).netloc
        
    def is_valid_url(self, url):
        """Check if URL is valid and belongs to the same domain."""
        parsed = urlparse(url)
        return bool(parsed.netloc) and parsed.netloc == self.domain
    
    def get_all_links(self, url, soup):
        """Extract all internal links from a page."""
        links = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            
            # Remove fragments and query parameters for deduplication
            clean_url = full_url.split('#')[0].split('?')[0]
            
            if self.is_valid_url(clean_url) and clean_url not in self.visited_urls:
                links.add(clean_url)
        return links
    
    def extract_content(self, soup, url):
        """Extract meaningful content from a page."""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get page title
        title = soup.find('title')
        title = title.get_text().strip() if title else "Untitled"
        
        # Get main content
        main_content = soup.find('main') or soup.find('article') or soup.find('body')
        
        if main_content:
            # Extract text
            text = main_content.get_text(separator='\n', strip=True)
            # Clean up whitespace
            text = re.sub(r'\n\s*\n', '\n\n', text)
            
            # Extract headings for structure
            headings = []
            for heading in main_content.find_all(['h1', 'h2', 'h3']):
                headings.append({
                    'level': heading.name,
                    'text': heading.get_text().strip()
                })
            
            return {
                'url': url,
                'title': title,
                'content': text[:5000],  # Limit content length
                'headings': headings,
                'word_count': len(text.split())
            }
        
        return None
    
    def crawl(self):
        """Crawl the website starting from base_url."""
        print(f"🕷️  Starting crawl of {self.base_url}")
        print(f"   Maximum pages: {self.max_pages}\n")
        
        urls_to_visit = {self.base_url}
        
        while urls_to_visit and len(self.visited_urls) < self.max_pages:
            url = urls_to_visit.pop()
            
            if url in self.visited_urls:
                continue
            
            try:
                print(f"📄 Crawling ({len(self.visited_urls) + 1}/{self.max_pages}): {url}")
                
                response = requests.get(url, timeout=10, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract content
                content = self.extract_content(soup, url)
                if content:
                    self.pages_content.append(content)
                
                # Mark as visited
                self.visited_urls.add(url)
                
                # Get new links
                new_links = self.get_all_links(url, soup)
                urls_to_visit.update(new_links)
                
                # Be polite - don't hammer the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"   ⚠️  Error: {str(e)}")
                self.visited_urls.add(url)
        
        print(f"\n✅ Crawl complete! Visited {len(self.visited_urls)} pages")
        return self.pages_content


class ContentAnalyzer:
    """Analyzes content using Claude AI to generate summaries and project ideas."""
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get('ANTHROPIC_API_KEY')
        if not self.api_key:
            print("⚠️  Warning: No Anthropic API key provided. Using basic analysis.")
            self.use_ai = False
        else:
            self.use_ai = True
    
    def organize_by_modules(self, pages_content):
        """Organize pages into logical modules based on URL structure and content."""
        modules = defaultdict(list)
        
        for page in pages_content:
            # Determine module from URL path
            parsed = urlparse(page['url'])
            path_parts = [p for p in parsed.path.split('/') if p]
            
            if not path_parts:
                module_name = "Home"
            else:
                module_name = path_parts[0].replace('-', ' ').replace('_', ' ').title()
            
            modules[module_name].append(page)
        
        return dict(modules)
    
    def analyze_with_ai(self, module_name, pages):
        """Use Claude AI to analyze content and generate insights."""
        if not self.use_ai:
            return self._basic_analysis(module_name, pages)
        
        try:
            # Prepare content for analysis
            content_summary = f"Module: {module_name}\n\n"
            for i, page in enumerate(pages[:10], 1):  # Limit to 10 pages
                content_summary += f"Page {i}: {page['title']}\n"
                content_summary += f"URL: {page['url']}\n"
                content_summary += f"Content preview: {page['content'][:500]}...\n\n"
            
            # Call Claude API
            response = requests.post(
                'https://api.anthropic.com/v1/messages',
                headers={
                    'Content-Type': 'application/json',
                    'x-api-key': self.api_key,
                    'anthropic-version': '2023-06-01'
                },
                json={
                    'model': 'claude-sonnet-4-20250514',
                    'max_tokens': 2000,
                    'messages': [{
                        'role': 'user',
                        'content': f"""Analyze this website module and provide:

1. A concise summary (2-3 paragraphs) of what this module covers
2. 3-5 specific things that could be built or projects that could be created based on this content
3. Key technologies or concepts mentioned

Module content:
{content_summary}

Format your response as JSON with keys: summary, buildable_projects (array), key_concepts (array)"""
                    }]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content_text = result['content'][0]['text']
                
                # Try to parse JSON from response
                try:
                    # Remove markdown code blocks if present
                    content_text = re.sub(r'```json\s*|\s*```', '', content_text).strip()
                    analysis = json.loads(content_text)
                    return analysis
                except json.JSONDecodeError:
                    # If not JSON, parse manually
                    return {
                        'summary': content_text,
                        'buildable_projects': [],
                        'key_concepts': []
                    }
            else:
                print(f"   ⚠️  API Error: {response.status_code}")
                return self._basic_analysis(module_name, pages)
                
        except Exception as e:
            print(f"   ⚠️  AI Analysis Error: {str(e)}")
            return self._basic_analysis(module_name, pages)
    
    def _basic_analysis(self, module_name, pages):
        """Fallback basic analysis without AI."""
        total_words = sum(p['word_count'] for p in pages)
        
        # Extract common keywords
        all_text = ' '.join([p['content'] for p in pages])
        words = re.findall(r'\b[a-z]{4,}\b', all_text.lower())
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1
        
        common_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'summary': f"This module '{module_name}' contains {len(pages)} pages with approximately {total_words} words. "
                      f"The content covers topics related to {', '.join([w[0] for w in common_words[:5]])}.",
            'buildable_projects': [
                f"Project based on {pages[0]['title']}" if pages else "Documentation website",
                f"Tutorial application for {module_name}",
                f"Reference implementation"
            ],
            'key_concepts': [w[0] for w in common_words[:5]]
        }


class PDFGenerator:
    """Generates professional PDFs with summaries and project ideas."""
    
    def __init__(self, output_dir='./pdfs'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Create custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=colors.HexColor('#1e40af'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        self.styles.add(ParagraphStyle(
            name='ModuleName',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#059669'),
            spaceBefore=20,
            spaceAfter=12
        ))
        
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#dc2626'),
            spaceBefore=12,
            spaceAfter=6
        ))
    
    def generate_pdf(self, module_name, analysis, pages, base_url):
        """Generate a PDF for a specific module."""
        # Create filename
        filename = f"{module_name.lower().replace(' ', '_')}_analysis.pdf"
        filepath = os.path.join(self.output_dir, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(filepath, pagesize=letter,
                              topMargin=0.75*inch, bottomMargin=0.75*inch)
        
        story = []
        
        # Title Page
        story.append(Paragraph(f"Module: {module_name}", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2*inch))
        story.append(Paragraph(f"Analysis Report", self.styles['Heading2']))
        story.append(Spacer(1, 0.1*inch))
        story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", 
                             self.styles['Normal']))
        story.append(Paragraph(f"Source: {base_url}", self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Summary Section
        story.append(Paragraph("📋 Summary", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.1*inch))
        
        summary_text = analysis.get('summary', 'No summary available.')
        story.append(Paragraph(summary_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Buildable Projects Section
        story.append(Paragraph("🚀 Things You Can Build", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.1*inch))
        
        projects = analysis.get('buildable_projects', [])
        if projects:
            for i, project in enumerate(projects, 1):
                story.append(Paragraph(f"{i}. {project}", self.styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph("No specific projects identified.", self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Key Concepts Section
        story.append(Paragraph("💡 Key Concepts", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.1*inch))
        
        concepts = analysis.get('key_concepts', [])
        if concepts:
            concepts_text = ", ".join(concepts)
            story.append(Paragraph(concepts_text, self.styles['Normal']))
        else:
            story.append(Paragraph("No key concepts identified.", self.styles['Normal']))
        
        story.append(Spacer(1, 0.3*inch))
        
        # Pages Overview
        story.append(PageBreak())
        story.append(Paragraph("📚 Pages in This Module", self.styles['SectionHeading']))
        story.append(Spacer(1, 0.2*inch))
        
        # Create table of pages
        table_data = [['#', 'Page Title', 'URL']]
        for i, page in enumerate(pages, 1):
            table_data.append([
                str(i),
                Paragraph(page['title'][:50], self.styles['Normal']),
                Paragraph(page['url'], self.styles['Normal'])
            ])
        
        if len(table_data) > 1:
            t = Table(table_data, colWidths=[0.5*inch, 3*inch, 3*inch])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(t)
        
        # Build PDF
        doc.build(story)
        print(f"   ✅ Generated: {filename}")
        return filepath


def main():
    """Main function to run the complete workflow."""
    print("=" * 70)
    print("🌐 Website Crawler & PDF Generator")
    print("=" * 70)
    print()
    
    # Get user input
    url = input("Enter the website URL to crawl: ").strip()
    if not url.startswith('http'):
        url = 'https://' + url
    
    max_pages_input = input("Maximum pages to crawl (default 50): ").strip()
    max_pages = int(max_pages_input) if max_pages_input else 50
    
    api_key_input = input("Enter your Anthropic API key (or press Enter to skip AI analysis): ").strip()
    
    print()
    
    # Step 1: Crawl the website
    crawler = WebsiteCrawler(url, max_pages=max_pages)
    pages_content = crawler.crawl()
    
    if not pages_content:
        print("❌ No content extracted. Please check the URL and try again.")
        return
    
    print()
    
    # Step 2: Organize content into modules
    analyzer = ContentAnalyzer(api_key=api_key_input if api_key_input else None)
    modules = analyzer.organize_by_modules(pages_content)
    
    print(f"📊 Organized into {len(modules)} modules:")
    for module_name, pages in modules.items():
        print(f"   • {module_name}: {len(pages)} pages")
    print()
    
    # Step 3: Analyze each module and generate PDFs
    pdf_generator = PDFGenerator()
    generated_pdfs = []
    
    print("🔬 Analyzing modules and generating PDFs...\n")
    
    for module_name, pages in modules.items():
        print(f"📝 Processing module: {module_name}")
        
        # Analyze content
        analysis = analyzer.analyze_with_ai(module_name, pages)
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(module_name, analysis, pages, url)
        generated_pdfs.append(pdf_path)
        
        print()
    
    # Summary
    print("=" * 70)
    print("✨ All done!")
    print(f"Generated {len(generated_pdfs)} PDF reports in: {pdf_generator.output_dir}")
    print()
    print("PDF files created:")
    for pdf in generated_pdfs:
        print(f"   📄 {os.path.basename(pdf)}")
    print("=" * 70)


if __name__ == "__main__":
    # Check and install dependencies
    try:
        import bs4
        import reportlab
    except ImportError:
        print("📦 Installing required packages...")
        import subprocess
        subprocess.check_call(['pip', 'install', '-q', 'beautifulsoup4', 'requests', 'reportlab'])
        print("✅ Packages installed!\n")
    
    main()
