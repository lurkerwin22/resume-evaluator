
# Resume Evaluator System

## Overview
An AI-powered web application that evaluates and ranks resumes against job descriptions using Google Gemini. Built with Flask and CrewAI.

## Features
- 📄 Multi-file upload (PDF/TXT)
- 🎯 Custom job description input
- 🧠 AI evaluation with scoring breakdown
- 📊 Candidate ranking by compatibility
- 📱 Responsive interface

## Quick Start

### Prerequisites
- Python 3.10+
- Google API key

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/resume-evaluator.git
cd resume-evaluator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install flask crewai langchain-community PyPDF2 python-dotenv
```

### Configuration
1. Create `.env` file:
```bash
echo "GOOGLE_API_KEY=your_api_key_here" > .env
```

### Running the Application
```bash
python app.py
```
Access at: `http://localhost:5000`

## Usage Guide
1. **Upload Page** (`/`)
   - Select multiple resumes (PDF/TXT)
   - Paste job description text
   - Click "Evaluate All"

2. **Results Page** (`/evaluate`)
   - View ranked candidates by score (10-point scale)
   - See detailed evaluation breakdown
   - Return to upload page

## Technical Details

### Scoring Criteria
```python
# Defined in evaluator.py
Core Technical Skills: 4 points   # (.NET, C#, SQL)
Supporting Tech Stack: 2 points   # (ReactJS, JS, NodeJS)
Soft Skills: 2 points             # (Agile, Teamwork)
Language & Education: 2 points    # (French, English, Degree)
```

### File Processing
- PDFs parsed with PyPDFLoader
- Text split using Langchain's RecursiveCharacterTextSplitter
- Candidate name extraction with regex patterns

### Project Structure
```
.
├── app.py                # Flask application
├── evaluator.py          # AI evaluation logic
├── templates/
│   ├── index.html        # Upload interface
│   └── results.html      # Results display
├── uploads/              # Resume storage
└── requirements.txt      # Dependencies
```

## Customization
Modify these files for adjustments:
- `evaluator.py`: Change scoring weights or criteria
- `results.html`: Update results display styling
- `index.html`: Alter upload form layout

## Troubleshooting
| Issue | Solution |
|-------|----------|
| API errors | Verify GOOGLE_API_KEY in .env |
| PDF parsing fails | Convert to TXT or ensure text is selectable |
| No candidate name | Filename used as fallback (e.g. "John_Doe.pdf") |

## Dependencies
| Package | Version |
|---------|---------|
| Flask | >=3.0.2 |
| crewai | >=0.28.8 |
| langchain-community | >=0.2.1 |
| PyPDF2 | >=3.0.1 |
| python-dotenv | >=1.0.1 |

## License
MIT License - See [LICENSE](LICENSE) for details.
```

This Markdown file includes:
1. Proper section headers with `##`
2. Code blocks wrapped in triple backticks (```)
3. Tables for troubleshooting and dependencies
4. Clear formatting for commands and file structure
5. Consistent bullet points and numbering
6. All special characters properly escaped

To use:
1. Replace placeholder values (yourusername, your_api_key_here)
2. Save as `README.md`
3. Add to your project root directory

The formatting will render correctly on GitHub and other Markdown viewers.
