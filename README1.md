# Psychoanalytic Personality Assessment System

## 📋 Overview

A comprehensive Gradio-based web application for conducting psychoanalytic personality assessments. The system presents 18 carefully designed questions across multiple personality dimensions and uses LLM analysis to provide detailed personality type insights.

## 🎯 Features

### User Interface
- **Two Main Tabs**:
  1. **New Assessment**: Complete 18-question assessment
  2. **Upload Previous**: Re-analyze saved JSON files

- **18 Assessment Questions** organized across 8 personality types:
  - Narcissistic
  - Obsessive
  - Depressive
  - Paranoid
  - Schizoid
  - Hysterical
  - Borderline
  - Masochistic

- **Organized Layout**: Questions grouped in 3 tabs (6 questions each) for easy navigation

- **Question Categories**:
  1. Stress Response
  2. Self-Worth Source
  3. Relationship Pattern
  4. Anger Expression
  5. Identity Sense
  6. Criticism Response
  7. Success/Achievement
  8. Alone Time
  9. Dependency
  10. Moral Transgression
  11. Fantasy Life
  12. Body Experience
  13. Change/Transition
  14. Competition
  15. Authority Figures
  16. Emptiness/Meaning
  17. Jealousy/Envy
  18. Trust

### Analysis Features
- **JSON Output**: Complete structured data of all responses
- **LLM Analysis**: Comprehensive personality assessment using Claude API
- **Fallback Analysis**: Pattern-matching algorithm when API unavailable
- **Upload Previous Results**: Re-analyze saved JSON assessments
- **Export Options**:
  - **Word (.docx)**: Formatted document with full analysis and response details
  - **Markdown (.md)**: Shareable text format with complete results
  - **JSON (.json)**: Structured data for programmatic use
  - **Custom Filenames**: Edit filename before export for personalized naming
  - **Auto-Generated Names**: Default timestamp-based names provided
- **Detailed Results**:
  - Primary personality type identification
  - Confidence level assessment
  - Secondary features
  - Pattern analysis
  - Key characteristics
  - Strengths and challenges
  - Therapeutic considerations

## 🚀 Installation & Setup

### Prerequisites
```bash
pip install gradio requests
```

### Basic Usage
```bash
python personality_assessment_ui.py
```

The application will launch on `http://localhost:7860`

## 🔑 API Configuration

### Option 1: Environment Variable (Recommended)
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
python personality_assessment_ui.py
```

### Option 2: Modify Code Directly
Edit `personality_assessment_ui.py` and add your API key to the headers:

```python
response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
        "x-api-key": "your-api-key-here"  # Add this line
    },
    # ... rest of code
)
```

### Option 3: Using a Different LLM

Replace the `analyze_with_llm()` function with your preferred LLM:

**OpenAI Example:**
```python
import openai

def analyze_with_llm(responses_json):
    client = openai.OpenAI(api_key="your-key")
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a clinical psychologist..."},
            {"role": "user", "content": responses_json}
        ]
    )
    
    return response.choices[0].message.content
```

**Local LLM (Ollama) Example:**
```python
import requests

def analyze_with_llm(responses_json):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": f"Analyze these responses: {responses_json}",
            "stream": False
        }
    )
    
    return response.json()['response']
```

## 📊 JSON Output Format

```json
{
  "timestamp": "2024-12-18T10:30:00.000000",
  "total_questions": 18,
  "responses": [
    {
      "question_id": 1,
      "category": "Stress Response",
      "question": "When faced with major stress...",
      "selected_answer": "I make lists, analyze all options...",
      "selected_type": "Obsessive"
    }
    // ... more responses
  ]
}
```

## 🧠 LLM Analysis Prompt Structure

The system sends a structured prompt to the LLM requesting:

1. **Primary Personality Type** - Dominant pattern identification
2. **Confidence Level** - Assessment reliability (High/Medium/Low)
3. **Secondary Features** - Additional personality patterns
4. **Pattern Analysis** - Question-by-question breakdown
5. **Key Characteristics** - Core traits (5-7 items)
6. **Strengths** - Positive aspects (3-4 items)
7. **Challenges** - Areas of difficulty (3-4 items)
8. **Therapeutic Considerations** - Recommendations
9. **Important Notes** - Caveats and context

## 🔄 Fallback Analysis

When API is unavailable, the system uses a pattern-matching algorithm:
- Counts responses by personality type
- Identifies dominant type (highest count)
- Calculates confidence based on percentage
- Provides distribution of all types
- Lists all questions answered

## 💾 Upload & Export Features

### Uploading Previous Assessments

The system allows you to upload previously saved JSON assessment files for re-analysis:

1. Navigate to the **"📂 Upload Previous Assessment"** tab
2. Click **"Upload JSON Assessment File"** and select your file
3. Click **"🔍 Analyze Uploaded Assessment"**
4. View the re-analyzed results

**Benefits**:
- Re-analyze with updated LLM models
- Review past assessments
- Compare analyses from different time periods
- Share assessments between sessions or practitioners

### Exporting Results

After completing or uploading an assessment, export results in your preferred format:

#### Custom Filenames

**Customize Before Export**:
```
Default: assessment_results_20241218_143022.docx
Custom:  client_john_initial_assessment.docx
```

**Features**:
- Edit filename field before clicking export
- Extensions (.docx/.md) added automatically if missing
- Use descriptive names for better organization
- Supports alphanumeric characters, hyphens, underscores

**Examples**:
```
✅ client_baseline_2024
✅ therapy_session_01
✅ participant_037_initial
✅ 2024_12_18_assessment

❌ file*.docx (special characters)
❌ my/file (slashes)
❌ test@home (@ symbol)
```

See **FILENAME_GUIDE.md** for comprehensive naming strategies.

#### Word Document (.docx)
- **Professionally formatted** document ready for printing
- Includes complete analysis text
- Detailed response breakdown by question
- Timestamp and metadata preserved
- **Use for**: Sharing with therapists, archiving, printing

#### Markdown (.md)
- **Plain text format** for maximum compatibility
- Easy to read and edit
- Works with note-taking apps (Obsidian, Notion, etc.)
- Version control friendly (Git)
- **Use for**: Personal journals, documentation, web publishing

#### JSON (.json)
- **Structured data format** for programmatic use
- Includes all metadata and timestamps
- Can be re-uploaded for analysis
- **Use for**: Data analysis, comparison, archiving

### Export Workflow Example

```
Complete Assessment
      ↓
  Get Analysis
      ↓
  ┌─────────┬─────────┬─────────┐
  ↓         ↓         ↓         ↓
Export    Export    Export    Share
to Word   to MD     JSON      Results
  ↓         ↓         ↓
Print     Journal   Re-upload
Share     Archive   Later
```

### Best Practices

1. **Always save JSON**: Keep the JSON file as your master copy
2. **Date stamping**: Files automatically include timestamps in filenames
3. **Organized storage**: Create folders for different assessment periods
4. **Multiple formats**: Export to both Word (for sharing) and JSON (for archiving)
5. **Regular backups**: Keep copies of assessment files in multiple locations

## 💡 Usage Examples

### Example 1: Research Study
```python
# Run assessment
# Export JSON data
# Batch analyze multiple participants
# Compare personality distributions
```

### Example 2: Clinical Practice
```python
# Client completes assessment
# Review JSON + LLM analysis
# Discuss results in session
# Track changes over time
```

### Example 3: Self-Development
```python
# Complete assessment honestly
# Review personality insights
# Identify growth areas
# Re-assess after 6 months
```

## 🎨 Customization

### Adding Questions
```python
questions.append({
    "id": 19,
    "category": "Your Category",
    "question": "Your question?",
    "options": {
        "Narcissistic": "Response for this type",
        "Obsessive": "Response for this type",
        # ... all 8 types
    }
})
```

### Modifying Analysis Prompt
Edit the `prompt` variable in `analyze_with_llm()` to change:
- Analysis depth
- Output format
- Specific focus areas
- Language/tone

### Styling
Gradio themes can be customized:
```python
with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
    # or gr.themes.Glass(), Base(), Soft(), etc.
```

## 📈 Advanced Features

### Saving Results to Database
```python
import sqlite3

def save_to_db(assessment_data, analysis):
    conn = sqlite3.connect('assessments.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO assessments (timestamp, data, analysis)
        VALUES (?, ?, ?)
    ''', (assessment_data['timestamp'], 
          json.dumps(assessment_data), 
          analysis))
    
    conn.commit()
    conn.close()
```

### Exporting to PDF
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def export_to_pdf(analysis, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    # Add analysis content
    c.drawString(100, 750, "Personality Assessment Results")
    # ... format analysis
    c.save()
```

### Email Results
```python
import smtplib
from email.mime.text import MIMEText

def email_results(to_address, analysis):
    msg = MIMEText(analysis)
    msg['Subject'] = 'Your Personality Assessment Results'
    msg['From'] = 'your@email.com'
    msg['To'] = to_address
    
    # Send via SMTP
    # ... smtp code
```

## ⚠️ Important Notes

- **Not a Diagnostic Tool**: This assessment is for educational/research purposes
- **Privacy**: No data is stored unless you implement it
- **Professional Use**: Should complement, not replace, clinical judgment
- **API Costs**: Claude API calls incur charges based on usage
- **Rate Limits**: Be aware of API rate limits for production use

## 🔧 Troubleshooting

### Issue: Gradio won't launch
```bash
# Check port availability
lsof -i :7860

# Use different port
demo.launch(server_port=8080)
```

### Issue: API errors
```python
# Enable detailed error logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Issue: Memory errors with large batches
```python
# Process in smaller chunks
# Implement pagination
# Clear old responses
```

## 📚 Theoretical Background

Based on psychoanalytic personality organization theory:
- **Neurotic level**: Integrated identity, mature defenses
- **Borderline level**: Identity diffusion, primitive defenses  
- **Psychotic level**: Reality testing impairment

The assessment evaluates:
- Defense mechanisms
- Object relations
- Identity integration
- Affective patterns
- Interpersonal style

## 🤝 Contributing

To extend the system:
1. Add new question categories
2. Implement additional personality types
3. Enhance analysis algorithms
4. Add visualization features
5. Create reporting templates

## 📄 License

[Specify your license here]

## 📞 Support

For issues or questions:
- Review the troubleshooting section
- Check Gradio documentation: https://gradio.app/docs
- Anthropic API docs: https://docs.anthropic.com

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Author**: [Your Name]
