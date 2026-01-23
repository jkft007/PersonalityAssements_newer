# Custom Filename Guide

## 📝 Overview

The assessment system now supports custom filenames for Word and Markdown exports, giving you full control over how your files are named and organized.

## ✨ Features

### Automatic Suggested Filenames
- **Default Format**: `assessment_results_YYYYMMDD_HHMMSS.docx` / `.md`
- **Example**: `assessment_results_20241218_143022.docx`
- **Updates**: New timestamp generated each time you clear or refresh

### Custom Naming
- Edit the filename before exporting
- Extension automatically added if missing
- Supports any valid filename characters

## 🎯 Use Cases

### 1. Participant/Client Identification

**Default**:
```
assessment_results_20241218_143022.docx
```

**Custom**:
```
client_john_doe_initial_assessment
→ Saved as: client_john_doe_initial_assessment.docx
```

**Workflow**:
1. Complete assessment
2. Edit filename: `client_john_doe_initial_assessment`
3. Click Export to Word
4. File downloads as: `client_john_doe_initial_assessment.docx`

---

### 2. Progress Tracking

**Initial Assessment**:
```
therapy_session_01_baseline.docx
```

**Follow-up Sessions**:
```
therapy_session_02_3month.docx
therapy_session_03_6month.docx
therapy_session_04_9month.docx
```

**Benefits**:
- Clear chronological order
- Easy to compare across sessions
- Professional organization

---

### 3. Research Participants

**Naming Convention**:
```
study_XYZ_participant_001.docx
study_XYZ_participant_002.docx
study_XYZ_participant_003.docx
```

**Batch Processing**:
```python
# Generate sequential filenames
for i in range(1, 51):
    filename = f"study_XYZ_participant_{i:03d}"
    # Complete assessment
    # Export with custom filename
```

---

### 4. Personal Journal

**Dates and Themes**:
```
2024_12_18_holiday_stress_assessment.md
2024_06_15_career_transition_reflection.md
2024_03_22_relationship_patterns.md
```

**Benefits**:
- Searchable by date or theme
- Easy to find in note-taking apps
- Chronological sorting

---

### 5. Family/Group Assessments

**Family Members**:
```
smith_family_mother_assessment.docx
smith_family_father_assessment.docx
smith_family_teen_assessment.docx
```

**Team/Group**:
```
team_alpha_member_alice.docx
team_alpha_member_bob.docx
team_alpha_member_charlie.docx
```

---

## 📋 Naming Best Practices

### DO ✅

**Use descriptive names**:
```
✅ initial_assessment_2024
✅ client_A_baseline
✅ depression_screening_june
```

**Use underscores or hyphens**:
```
✅ my_assessment_file.docx
✅ my-assessment-file.docx
```

**Include dates when relevant**:
```
✅ assessment_2024_12_18.docx
✅ 20241218_assessment.docx
```

**Use lowercase for consistency**:
```
✅ client_report.docx
```

### DON'T ❌

**Avoid special characters**:
```
❌ assessment@#$%.docx
❌ client/report.docx
❌ file*name?.docx
```

**Don't worry about extensions**:
```
✅ my_file → Saves as: my_file.docx
✅ my_file.docx → Saves as: my_file.docx
✅ my_file.txt → Saves as: my_file.txt.docx
```

**Avoid very long names**:
```
❌ this_is_an_extremely_long_filename_that_describes_every_detail_about_the_assessment_including_date_time_person_location_and_purpose.docx
✅ detailed_assessment_20241218.docx
```

---

## 🔄 Workflow Examples

### Example 1: Clinical Practice Workflow

```
1. Client arrives for session
2. Complete assessment together
3. Edit filename:
   Input: jones_sarah_session_12
4. Click "Export to Word"
5. Download: jones_sarah_session_12.docx
6. Share with client
7. Also export to Markdown:
   Input: jones_sarah_session_12
8. Download: jones_sarah_session_12.md
9. Add to clinical notes
```

### Example 2: Research Data Collection

```
1. Participant completes assessment
2. Generate ID-based filename:
   Input: study_2024_p037
3. Export to Word for participant
4. Export to JSON for database
5. Store in organized folder:
   /research/study_2024/participant_037/
```

### Example 3: Personal Growth Tracking

```
Month 1:
  Filename: personal_growth_2024_01_baseline.md
  
Month 3:
  Filename: personal_growth_2024_03_progress.md
  
Month 6:
  Filename: personal_growth_2024_06_milestone.md
  
Result: Clear progression timeline
```

---

## 🎨 Advanced Naming Strategies

### Date-First Strategy
**Format**: `YYYYMMDD_description`
```
20241218_initial_assessment.docx
20240615_followup_session.docx
20240322_quarterly_review.docx
```
**Benefit**: Perfect chronological sorting

### Category-First Strategy
**Format**: `category_subcategory_identifier`
```
clinical_intake_doe_john.docx
clinical_progress_doe_john.docx
clinical_discharge_doe_john.docx
```
**Benefit**: Group by type first

### Hierarchical Strategy
**Format**: `project_phase_item`
```
therapy_assessment_baseline.docx
therapy_assessment_midpoint.docx
therapy_assessment_final.docx
```
**Benefit**: Clear project structure

---

## 💡 Tips & Tricks

### Tip 1: Use Consistent Patterns
Pick one naming convention and stick with it:
```
✅ All files use: assessment_YYYY_MM_DD.docx
❌ Mixed: assessment_2024.docx, 12-18-assessment.docx
```

### Tip 2: Include Version Numbers
For revised assessments:
```
assessment_v1.docx
assessment_v2.docx
assessment_final.docx
```

### Tip 3: Use Meaningful Abbreviations
```
init → initial
fu → followup
qtr → quarterly
yrly → yearly
```

### Tip 4: Pre-plan Your Naming
Create a naming guide before starting:
```
Project: Depression Study 2024
Format: ds2024_pXXX_sYY
  ds2024 = Depression Study 2024
  pXXX = Participant number (001-999)
  sYY = Session number (01-99)
  
Example: ds2024_p042_s03.docx
```

---

## 🔧 Technical Details

### Filename Processing

The system automatically:
1. **Trims whitespace**: `" filename "` → `"filename"`
2. **Adds extensions**: `"file"` → `"file.docx"`
3. **Preserves extensions**: `"file.docx"` → `"file.docx"`
4. **Handles paths**: Saves to `/mnt/user-data/outputs/`

### Valid Characters

**Supported**:
- Letters: `a-z`, `A-Z`
- Numbers: `0-9`
- Underscore: `_`
- Hyphen: `-`
- Period: `.` (for extensions)
- Space: ` ` (converted to underscore in some systems)

**Avoid**:
- Slashes: `/` `\`
- Special characters: `* ? " < > | : @`

### Length Limits
- **Recommended**: Under 100 characters
- **Maximum**: 255 characters (system dependent)

---

## ❓ FAQ

**Q: What if I leave the filename empty?**
A: The system uses the default timestamp format automatically.

**Q: Can I use spaces in filenames?**
A: Yes, but underscores are recommended for better compatibility.

**Q: What happens if I don't include the extension?**
A: The system adds `.docx` or `.md` automatically based on export type.

**Q: Can I specify a custom save location?**
A: Files are saved to the outputs directory and downloaded through your browser's download location.

**Q: Will my custom filename be remembered?**
A: No, the filename field resets to a new timestamp after each clear/refresh.

**Q: Can I use the same filename for both Word and Markdown?**
A: Yes! Different extensions mean no conflicts: `file.docx` and `file.md`

**Q: What if my filename is invalid?**
A: The system will display an error. Use only alphanumeric characters, hyphens, and underscores.

---

## 📚 Related Documentation

- **README.md** - Complete system documentation
- **FEATURE_GUIDE.md** - Comprehensive feature walkthroughs
- **QUICK_START.md** - Quick setup and usage guide
- **CHANGELOG.md** - Version history and updates

---

## 🎓 Learning Path

1. **Beginner**: Use default filenames, understand the timestamp format
2. **Intermediate**: Customize with descriptive names for personal use
3. **Advanced**: Implement consistent naming conventions for projects
4. **Expert**: Create automated naming schemes for research/clinical work

---

**Version**: 2.1.0  
**Last Updated**: December 2024  
**Feature**: Custom Filename Selection
