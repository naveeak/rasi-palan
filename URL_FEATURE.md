# Thirukkural Matcher - URL Feature Update

## Summary
I've successfully updated your Thirukkural Matcher application to accept article URLs in addition to direct text input.

## Changes Made

### 1. Backend Updates (`main.py`)
- **New dependency**: Added `beautifulsoup4` for HTML parsing
- **Updated model**: Modified `AnalysisRequest` to accept both `text` and `url` fields (both optional)
- **New function**: `extract_text_from_url()` - Fetches and extracts main content from web pages
  - Uses intelligent parsing to find article content
  - Removes navigation, scripts, styles, headers, and footers
  - Fallback to paragraph extraction if article tags aren't found
  - Returns clean, extracted text for analysis
- **Enhanced endpoint**: `/analyze` now validates and processes both text and URL inputs

### 2. Frontend Updates (`static/index.html`)
- **Tab interface**: Added tabs to switch between "Text" and "Article URL" modes
- **URL input**: New input field specifically for article URLs
- **Updated JavaScript**:
  - `switchTab()`: Manages tab switching between text and URL modes
  - `analyzeUrl()`: Handles URL-based analysis
  - `performAnalysis()`: Unified function for both text and URL processing
  - Better error handling for API responses

### 3. Style Updates (`static/style.css`)
- **Tab styling**: Clean, modern tab buttons with active states
- **URL input styling**: Consistent styling with the textarea
- **Responsive design**: Tabs work well on different screen sizes

### 4. Dependencies (`requirements.txt`)
- Added `beautifulsoup4` for web scraping

## How to Use

### Text Mode (Original)
1. Open http://localhost:8000
2. The "Text" tab is selected by default
3. Paste your article or text
4. Click "Find Matching Kural"

### URL Mode (New)
1. Open http://localhost:8000
2. Click the "Article URL" tab
3. Enter a news article URL (e.g., from BBC, CNN, Medium, etc.)
4. Click "Find Matching Kural"
5. The app will fetch the article, extract the text, and find the matching Kural

## Technical Details

### URL Extraction Logic
The `extract_text_from_url()` function:
1. Sends a GET request with proper user-agent headers
2. Parses HTML with BeautifulSoup
3. Removes noise (scripts, styles, navigation)
4. Looks for semantic article containers (`<article>`, `<main>`, divs with "content" class)
5. Falls back to all `<p>` tags if no article structure is found
6. Cleans and validates the extracted text (minimum 50 characters)
7. Returns the text for semantic analysis

## Server Status
✅ Server is running on http://localhost:8000
✅ Model loaded successfully
✅ Embeddings generated for all 1330 Kurals
✅ Ready to process both text and URLs

## Next Steps
You can now test the application by:
1. Opening http://localhost:8000 in your browser
2. Trying both text input and URL input modes
3. Testing with various news articles or blog posts
