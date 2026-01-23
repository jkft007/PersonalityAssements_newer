import gradio as gr
import json
import requests
from datetime import datetime
import os
import sys
from pathlib import Path
import platform
from dotenv import load_dotenv
import random

# Questions and answer options
questions = [
    {
        "id": 1,
        "category": "Stress Response",
        "question": "When faced with major stress, what do you typically do?",
        "options": {
            "Narcissistic": "I push harder, prove I can handle it better than others",
            "Obsessive": "I make lists, analyze all options systematically",
            "Depressive": "I feel it's somehow my fault, withdraw to reflect",
            "Paranoid": "I suspect others are working against me",
            "Schizoid": "I retreat into solitude, need space from people",
            "Hysterical": "I become emotional, seek immediate support",
            "Borderline": "My feelings swing wildly, I might act impulsively",
            "Masochistic": "I endure it, others have it worse"
        }
    },
    {
        "id": 2,
        "category": "Self-Worth Source",
        "question": "What makes you feel valuable?",
        "options": {
            "Narcissistic": "Achievement, admiration, being exceptional",
            "Obsessive": "Doing things correctly, being reliable",
            "Depressive": "Helping others, being needed",
            "Paranoid": "Being vigilant, protecting myself/others",
            "Schizoid": "My inner world, autonomy",
            "Hysterical": "Being attractive, emotionally connecting",
            "Borderline": "Varies drastically day-to-day",
            "Masochistic": "Sacrifice, suffering for others"
        }
    },
    {
        "id": 3,
        "category": "Relationship Pattern",
        "question": "Describe your typical relationship dynamic:",
        "options": {
            "Narcissistic": "I need admiration; partners disappoint me",
            "Obsessive": "I'm loyal but critical of imperfection",
            "Depressive": "I give endlessly, fear abandonment",
            "Paranoid": "I'm suspicious, test loyalty constantly",
            "Schizoid": "I prefer distance, intimacy feels intrusive",
            "Hysterical": "Intense, dramatic, quickly attached",
            "Borderline": "Intense love-hate swings, fear of abandonment",
            "Masochistic": "I stay in painful situations too long"
        }
    },
    {
        "id": 4,
        "category": "Anger Expression",
        "question": "When angry, you:",
        "options": {
            "Narcissistic": "Feel insulted, lash out or withdraw coldly",
            "Obsessive": "Suppress it, become more rigid",
            "Depressive": "Turn it inward, feel guilty",
            "Paranoid": "Blame others, see attacks everywhere",
            "Schizoid": "Disconnect emotionally",
            "Hysterical": "Express dramatically, then forget quickly",
            "Borderline": "Rage intensely, then feel shame",
            "Masochistic": "Swallow it, express passive-aggressively"
        }
    },
    {
        "id": 5,
        "category": "Identity Sense",
        "question": "How stable is your sense of self?",
        "options": {
            "Narcissistic": "Grandiose but fragile underneath",
            "Obsessive": "Stable, defined by principles/roles",
            "Depressive": "Stable but fundamentally flawed",
            "Paranoid": "Stable, misunderstood by hostile world",
            "Schizoid": "Stable but detached observer",
            "Hysterical": "Defined by relationships, dramatic",
            "Borderline": "Fragmented, changes with mood/person",
            "Masochistic": "Defined by suffering, victimhood"
        }
    },
    {
        "id": 6,
        "category": "Criticism Response",
        "question": "When someone criticizes you:",
        "options": {
            "Narcissistic": "I feel shattered or enraged, question their competence",
            "Obsessive": "I defend with logic, prove I was right",
            "Depressive": "I agree, always knew I wasn't good enough",
            "Paranoid": "I knew they were against me all along",
            "Schizoid": "I don't care, doesn't penetrate",
            "Hysterical": "I feel devastated, cry, need reassurance immediately",
            "Borderline": "I'm destroyed or you're evil—extreme reaction",
            "Masochistic": "I probably deserve it, apologize excessively"
        }
    },
    {
        "id": 7,
        "category": "Success/Achievement",
        "question": "When you succeed:",
        "options": {
            "Narcissistic": "I deserve it, should have more recognition",
            "Obsessive": "Relief, but worry about next task",
            "Depressive": "It was luck/others' help, feel guilty for pride",
            "Paranoid": "Finally proved them wrong, stay vigilant",
            "Schizoid": "Indifferent, just met requirements",
            "Hysterical": "Excitement, share dramatically with everyone",
            "Borderline": "Brief high, then empty or suspicious of praise",
            "Masochistic": "Uncomfortable, downplay or sabotage it"
        }
    },
    {
        "id": 8,
        "category": "Alone Time",
        "question": "Being alone for extended periods:",
        "options": {
            "Narcissistic": "Boring without audience, feel depleted",
            "Obsessive": "Productive time, organize and plan",
            "Depressive": "Painful but familiar, ruminate",
            "Paranoid": "Safer but lonely, prepare defenses",
            "Schizoid": "Prefer it, recharge, feel authentic",
            "Hysterical": "Unbearable, need stimulation/connection",
            "Borderline": "Terrifying emptiness, might self-harm",
            "Masochistic": "Deserved isolation, martyr myself"
        }
    },
    {
        "id": 9,
        "category": "Dependency",
        "question": "Someone needing you constantly:",
        "options": {
            "Narcissistic": "Flattering at first, then burdensome drain",
            "Obsessive": "Structured help is fine, clinginess irritates",
            "Depressive": "Finally my purpose, give endlessly",
            "Paranoid": "Suspicious of motives, what do they want?",
            "Schizoid": "Suffocating, need escape",
            "Hysterical": "Love it, feel important and connected",
            "Borderline": "Cling back intensely or push away in panic",
            "Masochistic": "Accept it, complain but stay trapped"
        }
    },
    {
        "id": 10,
        "category": "Moral Transgression",
        "question": "If you broke your own moral code:",
        "options": {
            "Narcissistic": "Justified exception, rules for others",
            "Obsessive": "Severe guilt, confess, overcompensate",
            "Depressive": "Proof I'm fundamentally bad, spiral",
            "Paranoid": "It was defensive, they drove me to it",
            "Schizoid": "Detached observation, intellectualize",
            "Hysterical": "Dramatic guilt, seek forgiveness theatrically",
            "Borderline": "Self-loathing, suicidal thoughts or dissociate",
            "Masochistic": "Expected failure, punish myself"
        }
    },
    {
        "id": 11,
        "category": "Fantasy Life",
        "question": "Your recurring daydreams involve:",
        "options": {
            "Narcissistic": "Triumph, admiration, revenge on detractors",
            "Obsessive": "Perfect scenarios, things going exactly right",
            "Depressive": "Being saved, or saving others sacrificially",
            "Paranoid": "Exposure of plots, vindication, survival",
            "Schizoid": "Elaborate inner worlds, no people needed",
            "Hysterical": "Romance, drama, being center of attention",
            "Borderline": "Merging/fusion, or violent destruction",
            "Masochistic": "Suffering nobly, eventual recognition of pain"
        }
    },
    {
        "id": 12,
        "category": "Body Experience",
        "question": "Your relationship with your body:",
        "options": {
            "Narcissistic": "Extension of image, must be perfect/impressive",
            "Obsessive": "Control it, discipline, function over pleasure",
            "Depressive": "Heavy, sluggish, burdensome",
            "Paranoid": "Vigilant to signs, body betrays/warns",
            "Schizoid": "Detached, mechanical housing",
            "Hysterical": "Dramatic symptoms, highly responsive",
            "Borderline": "Volatile—love/hate, self-harm, disconnect",
            "Masochistic": "Endure pain, deny pleasure"
        }
    },
    {
        "id": 13,
        "category": "Change/Transition",
        "question": "Major life changes make you feel:",
        "options": {
            "Narcissistic": "Opportunity to shine or threat to status",
            "Obsessive": "Anxious, need to plan every detail",
            "Depressive": "Loss-focused, mourn what's ending",
            "Paranoid": "Suspicious, threatened, danger lurking",
            "Schizoid": "Indifferent if autonomy preserved",
            "Hysterical": "Excited/terrified, overly dramatic",
            "Borderline": "Panicked, identity-shattering chaos",
            "Masochistic": "Resigned suffering, inevitable hardship"
        }
    },
    {
        "id": 14,
        "category": "Competition",
        "question": "In competitive situations:",
        "options": {
            "Narcissistic": "Must win, cheating if needed, crushing defeat intolerable",
            "Obsessive": "Play by rules perfectly, resent rule-breakers",
            "Depressive": "Don't deserve to win, give up easily",
            "Paranoid": "Everyone cheats, must stay vigilant",
            "Schizoid": "Disinterested, pointless exercise",
            "Hysterical": "Dramatic display, enjoy attention more than winning",
            "Borderline": "All-or-nothing intensity, rage if losing",
            "Masochistic": "Lose nobly, winning feels wrong"
        }
    },
    {
        "id": 15,
        "category": "Authority Figures",
        "question": "Your relationship with authority:",
        "options": {
            "Narcissistic": "Respect only if superior, compete otherwise",
            "Obsessive": "Respect structure, obey rules, secretly resent",
            "Depressive": "Defer completely, seek approval desperately",
            "Paranoid": "Distrust, see hidden agendas, rebellion",
            "Schizoid": "Minimal engagement, comply superficially",
            "Hysterical": "Seductive or defiant, emotionally reactive",
            "Borderline": "Idealize then devalue rapidly",
            "Masochistic": "Submit, secretly resent, provoke punishment"
        }
    },
    {
        "id": 16,
        "category": "Emptiness/Meaning",
        "question": "Sense of inner emptiness:",
        "options": {
            "Narcissistic": "When not admired, brief then refill externally",
            "Obsessive": "Rare, stay busy to avoid",
            "Depressive": "Chronic, life feels meaningless",
            "Paranoid": "Filled with vigilance, no room for emptiness",
            "Schizoid": "Comfortable void, prefer it",
            "Hysterical": "Terrifying, fill with drama/relationships",
            "Borderline": "Pervasive black hole, unbearable",
            "Masochistic": "Filled with suffering, gives purpose"
        }
    },
    {
        "id": 17,
        "category": "Jealousy/Envy",
        "question": "When others have what you want:",
        "options": {
            "Narcissistic": "Intense envy, devalue their achievement",
            "Obsessive": "Work harder, deserve it through effort",
            "Depressive": "They deserve it, I don't",
            "Paranoid": "They stole/cheated their way",
            "Schizoid": "Detached observation, don't really want it",
            "Hysterical": "Dramatic display of feeling left out",
            "Borderline": "Consuming rage or self-destruction",
            "Masochistic": "Expected, martyrdom continues"
        }
    },
    {
        "id": 18,
        "category": "Trust",
        "question": "You trust others:",
        "options": {
            "Narcissistic": "Only when they validate me consistently",
            "Obsessive": "When proven reliable through time",
            "Depressive": "Too much, get hurt repeatedly",
            "Paranoid": "Never fully, always testing",
            "Schizoid": "Don't need to, keep distance",
            "Hysterical": "Immediately and completely, then betrayed",
            "Borderline": "Desperately then not at all, oscillating",
            "Masochistic": "Despite betrayal, stay loyal to pain"
        }
    }
]

def call_claude_api(prompt):
    """
    Call Claude API with the given prompt
    """

    try:
        # Prepare the analysis prompt


        # Call Claude API
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
                "x-api-key": f"{os.getenv('ANTHROPIC_API_KEY')}"
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 2000,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['content'][0]['text']
        else:
            return f"API Error: {response.status_code}\n\nUsing fallback analysis...\n\n{fallback_analysis(responses_json)}"
            
    except Exception as e:
        return f"Error calling API: {str(e)}\n\nUsing fallback analysis...\n\n{fallback_analysis(responses_json)}"

def analyze_with_llm(responses_json):
    """
    Analyze responses using Claude API
    """

    # Prepare the analysis prompt
    prompt = f"""You are a clinical psychologist specializing in psychoanalytic personality assessment. 

Analyze the following assessment responses and provide a comprehensive personality type analysis:

{responses_json}

Based on these responses, please provide:

1. **Primary Personality Type**: Identify the dominant personality organization (Narcissistic, Obsessive, Depressive, Paranoid, Schizoid, Hysterical, Borderline, or Masochistic)

2. **Confidence Level**: Rate your confidence in this assessment (High/Medium/Low) and explain why

3. **Secondary Features**: Identify any secondary personality patterns present

4. **Pattern Analysis**: 
   - Which questions were most indicative of the primary type?
   - Are there any conflicting patterns?
   - Level of personality organization (Neurotic, Borderline, or Psychotic level)

5. **Key Characteristics**: List 5-7 core characteristics of this personality type as evidenced by their responses

6. **Strengths**: Identify 3-4 potential strengths associated with this personality structure

7. **Challenges**: Identify 3-4 common challenges or vulnerabilities

8. **Therapeutic Considerations**: Brief recommendations for therapeutic approach or self-awareness areas

9. **Important Notes**: Any caveats, mixed presentations, or important contextual information

Format your response in clear sections with markdown formatting."""

    return call_claude_api(prompt)

def fallback_analysis(responses_json):
    """
    Simple fallback analysis when API is not available
    """
    data = json.loads(responses_json)
    
    # Count responses by type
    type_counts = {}
    for response in data['responses']:
        ptype = response['selected_type']
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
    
    # Find dominant type
    dominant_type = max(type_counts.items(), key=lambda x: x[1])
    
    # Calculate percentage
    total = len(data['responses'])
    percentage = (dominant_type[1] / total) * 100
    
    analysis = f"""## Personality Assessment Results

**Assessment Date**: {data['timestamp']}

### Primary Personality Type: {dominant_type[0]}
**Confidence**: {'High' if percentage > 60 else 'Medium' if percentage > 40 else 'Low'}  
**Indicator Strength**: {dominant_type[1]}/{total} responses ({percentage:.1f}%)

### Response Distribution:
"""
    
    for ptype, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
        pct = (count / total) * 100
        analysis += f"- **{ptype}**: {count} responses ({pct:.1f}%)\n"
    
    analysis += f"""

### Analysis Summary:
Based on {total} assessment questions, the dominant personality pattern is **{dominant_type[0]}**.

**Note**: This is a simplified analysis. For complete psychological insights including therapeutic recommendations, pattern analysis, and detailed characteristics, an API key is required to enable full LLM analysis.

### Questions Answered:
"""
    
    for response in data['responses']:
        analysis += f"\n- **Q{response['question_id']}** ({response['category']}): {response['selected_type']}"
    
    return analysis

def create_buttons_attributes(questions, input_responses=None):
    """
    Create question buttons 
    """
    buttons = {}

    if (questions is not None) and (len(questions) > 0):
        for question in questions:
            responses = list(question['options'].values())
            random.shuffle(responses)

            if input_responses:
                response = next((r for r in input_responses if r["question_id"] == question['id']), None)
            else:
                response = None
    
            buttons[question['id']] = {
                        "choices": responses,
                        "label": "Select your response:",
                        "interactive": True,
                        "value": response["selected_answer"] if response else None
            }            
    
    return buttons

def load_json_file(file):
    """
    Load and analyze a previously saved JSON assessment file
    """
    try:
        if file is None:
            return "⚠️ Please upload a JSON file.", "", *([None] * len(questions))
        
                # Handle different file types
        if isinstance(file, bytes):
            content = file
        else:
            content = file.read()

        if isinstance(content, bytes):
            content = content.decode('utf-8')
        
        # Parse JSON
        assessment_data = json.loads(content)
        
        # Validate structure
        if 'responses' not in assessment_data:
            return "⚠️ Invalid JSON format. Missing 'responses' field.", "", *([None] * len(questions))
        
        # Generate JSON output for display
        json_output = json.dumps(assessment_data, indent=2)
        
        # Get LLM analysis
        #analysis = analyze_with_llm(json_output)

        buttons = create_buttons_attributes(questions, assessment_data['responses'])
        # Extract button values in order of question IDs
        button_values = [buttons[q['id']]['value'] for q in questions]
        
        return json_output, *button_values
        
    except json.JSONDecodeError:
        return "⚠️ Invalid JSON file. Please upload a valid JSON assessment file.", "", *([None] * len(questions))
    except Exception as e:
        return f"⚠️ Error loading file: {str(e)}", "", *([None] * len(questions))

def export_to_word(analysis_text, json_data, custom_filename=None, save_location=None):
    """
    Export assessment results to Word document and return as downloadable file
    """
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        import tempfile
        
        doc = Document()
        
        # Add title
        title = doc.add_heading('Psychoanalytic Personality Assessment Results', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Add timestamp
        if json_data:
            try:
                data = json.loads(json_data)
                timestamp = data.get('timestamp', datetime.now().isoformat())
                date_para = doc.add_paragraph(f'Assessment Date: {timestamp}')
                date_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            except:
                pass
        
        doc.add_paragraph()
        
        # Add analysis section
        doc.add_heading('Analysis', level=1)
        
        # Parse and add analysis text (simple approach - split by lines)
        for line in analysis_text.split('\n'):
            if line.strip():
                if line.startswith('##'):
                    doc.add_heading(line.replace('#', '').strip(), level=1)
                elif line.startswith('###'):
                    doc.add_heading(line.replace('#', '').strip(), level=2)
                elif line.startswith('**') and line.endswith('**'):
                    p = doc.add_paragraph()
                    run = p.add_run(line.replace('**', ''))
                    run.bold = True
                elif line.startswith('- '):
                    doc.add_paragraph(line[2:], style='List Bullet')
                else:
                    doc.add_paragraph(line)
        
        # Add response details if JSON available
        if json_data:
            try:
                data = json.loads(json_data)
                doc.add_page_break()
                doc.add_heading('Detailed Response Data', level=1)
                
                for response in data['responses']:
                    p = doc.add_paragraph()
                    p.add_run(f"Question {response['question_id']}: ").bold = True
                    p.add_run(f"{response['category']}\n")
                    p.add_run(f"Selected Type: ").bold = True
                    p.add_run(f"{response['selected_type']}\n")
                    if 'selected_answer' in response:
                        p.add_run(f"Answer: ").bold = True
                        p.add_run(f"{response['selected_answer']}\n")
                    doc.add_paragraph()
            except:
                pass
        
        # Determine filename
        if custom_filename and custom_filename.strip():
            # Use custom filename, ensure .docx extension
            filename = custom_filename.strip()
            if not filename.endswith('.docx'):
                filename += '.docx'
        else:
            # Use default timestamp filename
            filename = f"assessment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        
        # Create temporary file for download
        temp_file = tempfile.NamedTemporaryFile(suffix='.docx', delete=False)
        doc.save(temp_file.name)
        temp_file.close()
        
        return temp_file.name
        
    except ImportError:
        # Fallback: install python-docx
        os.system("pip install python-docx --break-system-packages -q")
        return export_to_word(analysis_text, json_data, custom_filename, save_location)
    except Exception as e:
        return f"Error creating Word document: {str(e)}"

def export_to_markdown(analysis_text, json_data, custom_filename=None, save_location=None):
    """
    Export assessment results to Markdown file and return as downloadable file
    """
    try:
        import tempfile
        
        markdown_content = f"""# Psychoanalytic Personality Assessment Results

"""
        
        # Add timestamp
        if json_data:
            try:
                data = json.loads(json_data)
                timestamp = data.get('timestamp', datetime.now().isoformat())
                markdown_content += f"**Assessment Date**: {timestamp}\n\n"
            except:
                pass
        
        markdown_content += "---\n\n"
        
        # Add analysis
        markdown_content += "## Analysis\n\n"
        markdown_content += analysis_text + "\n\n"
        
        # Add response details if JSON available
        if json_data:
            try:
                data = json.loads(json_data)
                markdown_content += "---\n\n"
                markdown_content += "## Detailed Response Data\n\n"
                
                for response in data['responses']:
                    markdown_content += f"### Question {response['question_id']}: {response['category']}\n\n"
                    markdown_content += f"**Selected Type**: {response['selected_type']}\n\n"
                    if 'selected_answer' in response:
                        markdown_content += f"**Answer**: {response['selected_answer']}\n\n"
                    markdown_content += "---\n\n"
            except:
                pass
        
        # Determine filename
        if custom_filename and custom_filename.strip():
            # Use custom filename, ensure .md extension
            filename = custom_filename.strip()
            if not filename.endswith('.md'):
                filename += '.md'
        else:
            # Use default timestamp filename
            filename = f"assessment_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        # Create temporary file for download
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False)
        temp_file.write(markdown_content)
        temp_file.close()
        
        return temp_file.name
        
    except Exception as e:
        return f"Error creating Markdown file: {str(e)}"

def generate_suggested_filename(extension='docx'):
    """
    Generate a suggested filename with timestamp
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    return f"assessment_results_{timestamp}.{extension}"

def update_filename_suggestion():
    """
    Update both filename suggestions when called
    """
    word_suggestion = generate_suggested_filename('docx')
    md_suggestion = generate_suggested_filename('md')
    return word_suggestion, md_suggestion

def get_default_save_location():
    """
    Get OS-specific default save location
    """
    system = platform.system()
    home = str(Path.home())
    
    if system == "Windows":
        # Try Documents folder first, fall back to Desktop
        documents = os.path.join(home, "Documents")
        desktop = os.path.join(home, "Desktop")
        downloads = os.path.join(home, "Downloads")
        
        if os.path.exists(documents):
            return documents
        elif os.path.exists(desktop):
            return desktop
        elif os.path.exists(downloads):
            return downloads
        else:
            return home
            
    elif system == "Darwin":  # macOS
        documents = os.path.join(home, "Documents")
        downloads = os.path.join(home, "Downloads")
        
        if os.path.exists(documents):
            return documents
        elif os.path.exists(downloads):
            return downloads
        else:
            return home
            
    else:  # Linux and others
        documents = os.path.join(home, "Documents")
        downloads = os.path.join(home, "Downloads")
        
        if os.path.exists(documents):
            return documents
        elif os.path.exists(downloads):
            return downloads
        else:
            return home

def get_save_location_suggestions():
    """
    Get a list of suggested save locations based on OS
    """
    system = platform.system()
    home = str(Path.home())
    suggestions = []
    
    # Common locations across platforms
    common_paths = [
        os.path.join(home, "Documents"),
        os.path.join(home, "Downloads"),
        os.path.join(home, "Desktop"),
    ]
    
    # Add existing paths
    for path in common_paths:
        if os.path.exists(path):
            suggestions.append(path)
    
    # Add home directory
    suggestions.append(home)
    
    # Add current directory for containers/servers
    suggestions.append("/mnt/user-data/outputs")
    
    return suggestions

def validate_save_location(path):
    """
    Validate if a path is writable
    Returns: (is_valid, error_message, normalized_path)
    """
    if not path or not path.strip():
        return False, "Path cannot be empty", None
    
    path = path.strip()
    
    # Expand user home directory
    path = os.path.expanduser(path)
    
    # Convert to absolute path
    path = os.path.abspath(path)
    
    # Check if path exists
    if not os.path.exists(path):
        return False, f"Path does not exist: {path}", None
    
    # Check if it's a directory
    if not os.path.isdir(path):
        return False, f"Path is not a directory: {path}", None
    
    # Check if writable
    if not os.access(path, os.W_OK):
        return False, f"Path is not writable: {path}", None
    
    return True, "", path

def create_full_filepath(directory, filename):
    """
    Combine directory and filename, ensuring proper path
    """
    if not directory or not directory.strip():
        directory = "/mnt/user-data/outputs"
    
    # Validate and normalize directory
    is_valid, error, normalized_dir = validate_save_location(directory)
    if not is_valid:
        # Fall back to default output location
        normalized_dir = "/mnt/user-data/outputs"
    
    # Ensure filename has proper extension
    if not filename.endswith('.docx') and not filename.endswith('.md'):
        # Extension will be added by export functions
        pass
    
    return os.path.join(normalized_dir, filename)

def process_assessment(*args):
    """
    Process all responses and generate analysis
    """
    # Collect all responses
    responses = []
    args_list = list(args)
    for i, answer in enumerate(args):
        if answer:  # Only include answered questions
            q = questions[i]
            # Find which type was selected
            selected_type = None
            for ptype, text in q['options'].items():
                if text == answer:
                    selected_type = ptype
                    break
            
            responses.append({
                "question_id": q['id'],
                "category": q['category'],
                "question": q['question'],
                "selected_answer": answer,
                "selected_type": selected_type
            })
    
    # Check if all questions answered
    if len(responses) < len(questions):
        return "⚠️ Please answer all questions before submitting.", ""
    
    # Create JSON structure
    assessment_data = {
        "timestamp": datetime.now().isoformat(),
        "total_questions": len(questions),
        "responses": responses
    }
    
    json_output = json.dumps(assessment_data, indent=2)
    
    # Get LLM analysis
    analysis = analyze_with_llm(json_output)
    
    return analysis, json_output

def process_export_to_word_with_LLM(analysis_text, json_data, custom_filename, save_location):
    """
    Process export to Word with LLM analysis
    """
    filepath = create_full_filepath(save_location, custom_filename)
    prompt = """re-write the following analysis text as a professional report formated so it can be written to a file that is a Word document:\n\n""" + analysis_text

    result = call_claude_api(prompt)

    return result

# Create Gradio interface
with gr.Blocks(title="Psychoanalytic Personality Assessment") as demo:

    
    gr.Markdown("""
    # 🧠 Psychoanalytic Personality Assessment
    
    This comprehensive assessment uses psychoanalytic theory to identify personality patterns. 
    Answer all 18 questions honestly based on how you typically think, feel, and behave.
    
    **Instructions**: For each question, select the response that best describes you.
    """)
    
    with gr.Tabs():
        # Tab 1: Assessment
        with gr.Tab("📝 Assessment"):
            # Store radio button components
            buttons = create_buttons_attributes(questions)
            radio_buttons = []
            
            with gr.Tabs():
                # Create tabs for better organization (6 questions per tab)
                for tab_num in range(3):
                    with gr.Tab(f"Questions {tab_num*6 + 1}-{min((tab_num+1)*6, 18)}"):
                        start_idx = tab_num * 6
                        end_idx = min((tab_num + 1) * 6, len(questions))
                        
                        for q in questions[start_idx:end_idx]:
                            with gr.Group():
                                gr.Markdown(f"### Question {q['id']}: {q['category']}")
                                gr.Markdown(f"**{q['question']}**")
                                
                                responses = list(q['options'].values())
                                # Shuffle responses to avoid bias
                                responses = list(q['options'].values())
                                random.shuffle(responses)

                                # Create radio button with all options
                                radio = gr.Radio(
                                    choices=buttons[q['id']]['choices'],
                                    label=buttons[q['id']]['label'],
                                    interactive=buttons[q['id']]['interactive'],
                                    value=buttons[q['id']]['value']
                                )
                                radio_buttons.append(radio)
            
            gr.Markdown("---")
            
            with gr.Row():
                submit_btn = gr.Button("📊 Analyze My Personality", variant="primary", size="lg")
                clear_btn = gr.Button("🔄 Clear All Responses", size="lg")
            
            gr.Markdown("---")
            
            # Results section
            gr.Markdown("## 📋 Assessment Results")
            
            with gr.Row():
                with gr.Column(scale=2):
                    analysis_output = gr.Markdown(label="Personality Analysis")
                with gr.Column(scale=1):
                    json_output = gr.Code(label="Response Data (JSON)", language="json")
            
           
            
            # Button actions for new assessment
        
        # Tab 2: Upload Previous Results
        with gr.Tab("📂 Upload Previous Assessment"):
            gr.Markdown("""
            ## Upload and Analyze Previous Results
            
            Upload a previously saved JSON assessment file to re-analyze the results or view them again.
            """)
            
            with gr.Row():
                json_file_upload = gr.File(
                    label="Upload previously saved Assessment",
                    file_types=[".json"],
                    type="binary"
                )

                json_file_upload.change(
                    fn=load_json_file,
                    inputs=[json_file_upload],
                    outputs=[json_output, *radio_buttons]
            )
            """      
            with gr.Row():
                analyze_upload_btn = gr.Button("🔍 Analyze Uploaded Assessment", variant="primary", size="lg")
                clear_upload_btn = gr.Button("🔄 Clear", size="lg")

            gr.Markdown("---")
            gr.Markdown("## 📋 Analysis Results")
            
            with gr.Row():
                with gr.Column(scale=2):
                    uploaded_analysis_output = gr.Markdown(label="Personality Analysis")
                with gr.Column(scale=1):
                    uploaded_json_output = gr.Code(label="Response Data (JSON)", language="json")
            
            # Export buttons for uploaded file
            gr.Markdown("### 💾 Export Results")
            
            # Save location selector
            with gr.Row():
                upload_save_location_input = gr.Textbox(
                    label="📁 Save Location",
                    placeholder=get_default_save_location(),
                    value=get_default_save_location(),
                    info=f"Default: {get_default_save_location()} | Click to edit path"
                )
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("**Common Locations:**")
                    location_suggestions = get_save_location_suggestions()
                    for loc in location_suggestions[:4]:  # Show top 4
                        gr.Markdown(f"• `{loc}`")
            
            with gr.Row():
                with gr.Column():
                    upload_word_filename_input = gr.Textbox(
                        label="Word Filename (optional)",
                        placeholder="assessment_results_20241218_143022.docx",
                        value=generate_suggested_filename('docx'),
                        info="Filename only (no path). Extension .docx added automatically."
                    )
                    upload_export_word_btn = gr.Button("📄 Export to Word (.docx)", size="lg")
                with gr.Column():
                    upload_md_filename_input = gr.Textbox(
                        label="Markdown Filename (optional)",
                        placeholder="assessment_results_20241218_143022.md",
                        value=generate_suggested_filename('md'),
                        info="Filename only (no path). Extension .md added automatically."
                    )
                    upload_export_md_btn = gr.Button("📝 Export to Markdown (.md)", size="lg")
            
            gr.Markdown("**💡 Tip**: Files save to the location above. Default is your Documents folder.")
            
            with gr.Row():
                upload_word_file_output = gr.File(label="Word Document")
                upload_md_file_output = gr.File(label="Markdown Document")
            """
            """
            # Button actions for uploaded file
            analyze_upload_btn.click(
                fn=load_json_file,
                inputs=[json_file_upload],
                outputs=[uploaded_analysis_output, uploaded_json_output, *radio_buttons]
            )
            
            clear_upload_btn.click(
                fn=lambda: [None, "", "", get_default_save_location(), generate_suggested_filename('docx'), generate_suggested_filename('md'), None, None],
                inputs=None,
                outputs=[json_file_upload, uploaded_analysis_output, uploaded_json_output, 
                        upload_save_location_input, upload_word_filename_input, upload_md_filename_input,
                        upload_word_file_output, upload_md_file_output]
            )
            
            upload_export_word_btn.click(
                fn=export_to_word,
                inputs=[uploaded_analysis_output, uploaded_json_output, upload_word_filename_input, upload_save_location_input],
                outputs=[upload_word_file_output]
            )
            
            upload_export_md_btn.click(
                fn=export_to_markdown,
                inputs=[uploaded_analysis_output, uploaded_json_output, upload_md_filename_input, upload_save_location_input],
                outputs=[upload_md_file_output]
            )
            """
    
        with gr.Tab("📝 Save results"):
             # Export buttons
            gr.Markdown("### 💾 Save Results")
            
            # Save location selector
            with gr.Row():
                save_location_input = gr.Textbox(
                    label="📁 Save Location",
                    placeholder=get_default_save_location(),
                    value=get_default_save_location(),
                    info=f"Default: {get_default_save_location()} | Click to edit path"
                )
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("**Common Locations:**")
                    location_suggestions = get_save_location_suggestions()
                    for loc in location_suggestions[:4]:  # Show top 4
                        gr.Markdown(f"• `{loc}`")
                
            with gr.Row():
                with gr.Column():
                    word_filename_input = gr.Textbox(
                        label="Word Filename (optional)",
                        placeholder="assessment_results_20241218_143022.docx",
                        value=generate_suggested_filename('docx'),
                        info="Filename only (no path). Extension .docx added automatically."
                    )
                    export_word_btn = gr.Button("📄 Export to Word (.docx)", size="lg")
                with gr.Column():
                    md_filename_input = gr.Textbox(
                        label="Markdown Filename (optional)",
                        placeholder="assessment_results_20241218_143022.md",
                        value=generate_suggested_filename('md'),
                        info="Filename only (no path). Extension .md added automatically."
                    )
                    export_md_btn = gr.Button("📝 Export to Markdown (.md)", size="lg")
            
            gr.Markdown("**💡 Tip**: Files save to the location above. Default is your Documents folder.")
            
            with gr.Row():
                word_file_output = gr.File(label="Word Document")
                md_file_output = gr.File(label="Markdown Document")

                        
                export_word_btn.click(
                    fn=process_export_to_word_with_LLM,
                    inputs=[analysis_output, json_output, word_filename_input, save_location_input],
                    outputs=[word_file_output]
                )
                
                export_md_btn.click(
                    fn=export_to_markdown,
                    inputs=[analysis_output, json_output, md_filename_input, save_location_input],
                    outputs=[md_file_output]
            )
    
                submit_btn.click(
                fn=process_assessment,
                inputs=radio_buttons,
                outputs=[analysis_output, json_output]
            )
            
            clear_btn.click(
                fn=lambda: [None] * len(questions) + ["", "", get_default_save_location(), generate_suggested_filename('docx'), generate_suggested_filename('md'), None, None],
                inputs=None,
                outputs=radio_buttons + [analysis_output, json_output, save_location_input, word_filename_input, md_filename_input, word_file_output, md_file_output]
            )
            
    gr.Markdown("""
    ---
    ### 📌 Important Notes:
    - This assessment is for educational and self-reflection purposes only
    - Results should not replace professional psychological evaluation
    - All personality types have strengths and challenges
    - Most people show mixed patterns across different types
    
    ### 💾 Data Management & File Saving:
    - **Save Location**: Choose where to save files (Documents, Downloads, Desktop, or custom path)
    - **OS-Specific Defaults**: Automatically detects your operating system and suggests appropriate folders
    - **Custom Paths**: Edit the save location field to use any writable directory on your system
    - **Filename Customization**: Edit filename fields before exporting for personalized names
    - **Default Naming**: Auto-generated names include timestamp for easy organization
    - **JSON Upload**: Previously saved JSON files can be re-analyzed anytime
    - **Multiple Formats**: Export to Word (.docx) for professional use or Markdown (.md) for notes
    - **Browser Download**: Files are also available through your browser's download mechanism
    
    ### 📁 Save Location Tips:
    - **Windows**: Default is `C:\\Users\\YourName\\Documents`
    - **macOS**: Default is `/Users/YourName/Documents`
    - **Linux**: Default is `/home/username/Documents`
    - **Custom**: Edit the path field to save anywhere you have write permissions
    - **Validation**: System checks if location is writable before saving
    
    ### 🔧 API Configuration:
    To enable full LLM analysis with Claude, set your API key in the environment or modify the code.
    Without API access, a simplified pattern-matching analysis will be used.
    """)

if __name__ == "__main__":
    load_dotenv()
    #demo.launch(server_name="127.0.0.1", server_port=7860, share=True, allowed_paths=list(get_default_save_location()))
    demo.launch()
