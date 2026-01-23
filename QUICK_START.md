# Quick Start Guide

## Get Up and Running in 5 Minutes

### Step 1: Install Dependencies (30 seconds)
```bash
pip install gradio requests
```

### Step 2: Run the Application (10 seconds)
```bash
python personality_assessment_ui.py
```

### Step 3: Open Your Browser
Navigate to: `http://localhost:7860`

### Step 4: Complete the Assessment
1. Answer all 18 questions across the 3 tabs
2. Click "📊 Analyze My Personality"
3. View your results!

### Step 5: Export Your Results (Optional)
- **Default Names**: Auto-generated timestamps like `assessment_results_20241218_143022`
- **Custom Names**: Edit the filename fields before clicking export
  - Example: Change to `my_first_assessment` or `client_john_baseline`
  - Extensions (.docx or .md) added automatically
- Click "📄 Export to Word" for a formatted document
- Click "📝 Export to Markdown" for a text file
- JSON is automatically available in the interface

**Filename Tips**:
```
✅ Good: client_baseline, 2024_assessment, initial_evaluation
❌ Avoid: file*?.docx, assessment@home, my/file
```

---

## 📂 Upload Previous Assessment

### Quick Upload
1. Click the **"📂 Upload Previous Assessment"** tab
2. Upload your saved JSON file
3. Click "🔍 Analyze Uploaded Assessment"
4. View re-analyzed results with current LLM

**Why Upload?**
- Re-analyze with newer/different AI models
- Review past assessments
- Compare results over time

---

## With LLM Analysis (Full Features)

### Option A: Using Anthropic Claude API

1. **Get API Key**: Sign up at https://console.anthropic.com/

2. **Set Environment Variable**:
```bash
export ANTHROPIC_API_KEY="your-key-here"
python personality_assessment_ui.py
```

3. **Or Edit Code** (line ~348):
```python
headers={
    "Content-Type": "application/json",
    "anthropic-version": "2023-06-01",
    "x-api-key": "your-key-here"  # Add this line
}
```

### Option B: Using OpenAI GPT

1. **Install OpenAI**:
```bash
pip install openai
```

2. **Replace the `analyze_with_llm()` function**:
```python
import openai

def analyze_with_llm(responses_json):
    client = openai.OpenAI(api_key="your-key")
    
    prompt = f"""You are a clinical psychologist. Analyze these responses:
    
{responses_json}

Provide:
1. Primary personality type
2. Key characteristics
3. Strengths and challenges
"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Option C: Using Local LLM (Ollama)

1. **Install Ollama**: https://ollama.ai/

2. **Pull a Model**:
```bash
ollama pull llama2
```

3. **Replace the `analyze_with_llm()` function**:
```python
def analyze_with_llm(responses_json):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama2",
            "prompt": f"Analyze: {responses_json}",
            "stream": False
        }
    )
    return response.json()['response']
```

---

## Testing Without API

The application works without an API key! It will use a fallback pattern-matching algorithm that:
- Counts responses by personality type
- Identifies dominant patterns
- Provides confidence levels
- Shows response distribution

---

## Common Issues & Solutions

### Port Already in Use
```bash
# Use different port
demo.launch(server_port=8080)
```

### Can't Access from Other Devices
```bash
# Allow external access
demo.launch(server_name="0.0.0.0", share=False)
```

### Want Public Link
```bash
# Create shareable link (expires in 72 hours)
demo.launch(share=True)
```

### API Rate Limit Errors
```python
# Add retry logic
import time

def analyze_with_llm(responses_json):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = requests.post(...)
            return response.json()
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                return fallback_analysis(responses_json)
```

---

## What You Get

### 1. JSON Output
```json
{
  "timestamp": "2024-12-18T14:30:45",
  "responses": [...]
}
```

### 2. Detailed Analysis
- Primary personality type
- Confidence level
- Pattern analysis
- Key characteristics
- Strengths & challenges
- Therapeutic considerations

### 3. Visual Interface
- Clean, organized question layout
- Easy navigation
- Real-time feedback
- Export capabilities

---

## Next Steps

### For Research
- Review `example_usage.py` for batch processing
- Set up database integration
- Export to CSV/Excel
- Generate visualizations

### For Clinical Use
- Customize questions
- Modify analysis prompt
- Add PDF report generation
- Implement patient tracking

### For Self-Development
- Complete assessment honestly
- Review insights regularly
- Track changes over time
- Share with therapist

---

## File Structure

```
personality_assessment_ui.py  # Main application
README.md                     # Full documentation
example_usage.py             # Code examples
sample_output.json           # Example data structure
QUICK_START.md              # This file
```

---

## Tips for Best Results

1. **Answer Honestly**: No "right" answers
2. **Take Your Time**: Read each option carefully
3. **Don't Overthink**: Go with first instinct
4. **Context Matters**: Consider recent behavior patterns
5. **Review Results**: Reflect on insights provided

---

## Support

- 📚 Full docs: `README.md`
- 💡 Examples: `example_usage.py`
- 🐛 Issues: Check troubleshooting section
- 📊 Sample data: `sample_output.json`

---

**Ready to start? Run:**
```bash
python personality_assessment_ui.py
```

Then open `http://localhost:7860` in your browser!
