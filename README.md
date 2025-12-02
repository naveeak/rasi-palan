# Thirukkural Recommender 🕉️

A monolithic web application that analyzes text content or article URLs and recommends the most relevant **Thirukkural** (திருக்குறள்) using semantic similarity powered by local AI embeddings.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.123+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📖 About

Thirukkural is an ancient Tamil text composed by the legendary Tamil poet and philosopher **Thiruvalluvar**. It consists of 1,330 couplets (kurals) organized into 133 chapters, covering ethics, politics, economics, and love.

This application uses **AI-powered semantic search** to find the most contextually relevant Thirukkural for any given text or article, bridging ancient wisdom with modern technology.

## ✨ Features

- 📝 **Text Analysis**: Paste any text to find matching Thirukkural
- 🌐 **URL Analysis**: Submit article URLs for automatic content extraction and analysis
- 🤖 **Local AI**: Uses `sentence-transformers` for embeddings (no API keys required)
- 🎯 **Semantic Search**: Finds kurals based on meaning, not just keywords
- 🌍 **Bilingual Display**: Shows Tamil text, Tamil meaning, English translation, and detailed explanation
- ⚡ **Fast & Efficient**: Pre-computed embeddings for instant results
- 🎨 **Clean UI**: Simple, responsive interface built with vanilla HTML/CSS

## 🚀 Demo

### Text Mode
Simply paste your text and get the most relevant Thirukkural:

```
Input: "Friendship is important for a happy life"
Output: Kural about the value of friendship
```

### URL Mode
Submit any article URL and the app will extract and analyze it:

```
Input: https://www.bbc.com/news/technology
Output: Relevant Thirukkural based on the article's theme
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/naveeak/thirukural-recommender.git
   cd thirukural-recommender
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or if you're on a system-managed Python environment:
   ```bash
   python3 -m pip install --user --break-system-packages -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the app**
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

## 📁 Project Structure

```
thirukural-recommender/
├── main.py                 # FastAPI backend with AI logic
├── requirements.txt        # Python dependencies
├── static/
│   ├── index.html         # Frontend UI
│   └── style.css          # Styling
├── thirukkural.json       # Dataset (auto-downloaded on first run)
├── .gitignore
└── README.md
```

## 🔧 How It Works

1. **Data Loading**: Downloads Thirukkural dataset from GitHub on first run
2. **Embedding Generation**: Uses `sentence-transformers` (all-MiniLM-L6-v2) to create embeddings for all 1,330 kurals
3. **Text Extraction**: For URLs, uses BeautifulSoup to extract main article content
4. **Semantic Search**: Computes cosine similarity between input and all kurals
5. **Result Display**: Returns the most relevant Thirukkural with Tamil text, translation, and meaning

## 🎨 What You'll See

When you analyze text or a URL, the app displays:

1. **Kural Number**: The specific kural number (1-1330)
2. **Tamil Kural**: The two-line couplet in beautiful Tamil script
3. **தமிழ் பொருள் (Tamil Meaning)**: Explanation in Tamil (mk field)
4. **Translation**: English translation of the kural
5. **Meaning**: Detailed English explanation of the context and wisdom

All in a clean, card-based layout with Tamil font support!

## 🧠 Technical Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **Sentence Transformers**: State-of-the-art text embeddings
- **BeautifulSoup4**: HTML parsing and content extraction
- **NumPy**: Numerical computing for similarity calculations

### Frontend
- **HTML5**: Semantic markup
- **Vanilla CSS**: Clean, responsive design
- **Vanilla JavaScript**: Tab switching and API calls

### AI Model
- **Model**: `all-MiniLM-L6-v2`
- **Size**: ~90MB
- **Performance**: Fast inference on CPU
- **Privacy**: Runs completely offline after initial download

## 📊 Dataset

The Thirukkural dataset is sourced from:
- **Repository**: [tk120404/thirukkural](https://github.com/tk120404/thirukkural)
- **Format**: JSON with Tamil text, transliteration, translation, and explanation
- **Kurals**: 1,330 couplets covering all chapters
- **License**: Public domain (ancient text)

## 🙏 Credits & Acknowledgments

### Data Sources
- **Thirukkural JSON Dataset**: [tk120404/thirukkural](https://github.com/tk120404/thirukkural) - Comprehensive JSON dataset of all Thirukkurals
- **Thiruvalluvar**: Ancient Tamil poet and philosopher who authored this timeless work

### Technologies & Libraries
- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **Sentence Transformers**: [https://www.sbert.net/](https://www.sbert.net/)
- **BeautifulSoup4**: [https://www.crummy.com/software/BeautifulSoup/](https://www.crummy.com/software/BeautifulSoup/)
- **Uvicorn**: [https://www.uvicorn.org/](https://www.uvicorn.org/)

### Fonts
- **Inter**: [Google Fonts](https://fonts.google.com/specimen/Inter)
- **Noto Sans Tamil**: [Google Fonts](https://fonts.google.com/specimen/Noto+Sans+Tamil)

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Bug Reports**: Open an issue describing the bug
2. **Feature Requests**: Suggest new features via issues
3. **Code Contributions**: 
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/AmazingFeature`)
   - Commit your changes (`git commit -m 'Add some AmazingFeature'`)
   - Push to the branch (`git push origin feature/AmazingFeature`)
   - Open a Pull Request

## 📝 API Documentation

Once the server is running, access the interactive API docs at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Endpoints

#### `POST /analyze`
Analyze text or URL and get matching Thirukkural

**Request Body:**
```json
{
  "text": "Your text here"
}
```
or
```json
{
  "url": "https://example.com/article"
}
```

**Response:**
```json
{
  "number": 786,
  "line1": "Tamil text line 1",
  "line2": "Tamil text line 2",
  "mk": "Tamil meaning",
  "eng": "English translation",
  "eng_exp": "Detailed explanation"
}
```

## 🌟 Future Enhancements

- [ ] Add chapter-wise browsing
- [ ] Implement search history
- [ ] Support for multiple languages
- [ ] Add more Tamil literary works
- [ ] Mobile app version
- [ ] API rate limiting
- [ ] User authentication
- [ ] Favorites/bookmarking feature

## 📄 License

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2025 Naveen Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Note**: Thirukkural text is in the public domain as an ancient literary work.

## 📧 Contact

- **GitHub**: [@naveeak](https://github.com/naveeak)
- **Repository**: [thirukural-recommender](https://github.com/naveeak/thirukural-recommender)

## 🌏 About Thirukkural

> *"திருக்குறள் உலகப் பொதுமறை"*  
> *"Thirukkural is the universal scripture"*

Thirukkural, written over 2000 years ago, remains one of the most revered works in Tamil literature. Its 1,330 couplets cover:

- **அறத்துப்பால் (Aram)**: Virtue and righteousness (Chapters 1-38)
- **பொருட்பால் (Porul)**: Wealth and governance (Chapters 39-108)
- **காமத்துப்பால் (Inbam)**: Love and pleasure (Chapters 109-133)

This application aims to make this ancient wisdom accessible and relevant to modern contexts.

---

**Made with ❤️ for Tamil literature and AI enthusiasts**
