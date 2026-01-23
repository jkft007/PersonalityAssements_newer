# Custom Filename Feature - Implementation Summary

## ✨ What's New

You can now **customize the filename** before exporting Word or Markdown documents!

### Before (v2.0)
```
Click "Export to Word" → Downloads as: assessment_results_20241218_143022.docx
```
❌ No control over filename

### After (v2.1)
```
Edit filename field: "client_john_initial"
Click "Export to Word" → Downloads as: client_john_initial.docx
```
✅ Full control over filename

---

## 🎯 Quick Usage

### Step-by-Step

1. **Complete an assessment** (or upload a previous one)
2. **Look for the filename fields** above the export buttons:
   ```
   Word Filename (optional)
   ┌─────────────────────────────────┐
   │ assessment_results_20241218...  │  ← Edit this!
   └─────────────────────────────────┘
   ```
3. **Click in the field** and edit the name:
   ```
   ┌─────────────────────────────────┐
   │ my_custom_filename              │
   └─────────────────────────────────┘
   ```
4. **Click the export button**
5. **File downloads** with your custom name: `my_custom_filename.docx`

### Key Points

- **Extensions automatic**: Type `myfile` → saves as `myfile.docx`
- **Default provided**: Pre-filled with timestamp if you don't edit
- **Both formats**: Works for Word AND Markdown exports
- **Both tabs**: Available in New Assessment AND Upload Previous

---

## 💼 Real-World Examples

### Clinical Use
```
Before: assessment_results_20241218_143022.docx
After:  jones_sarah_session_12.docx
```

### Research Use
```
Before: assessment_results_20241218_143022.docx
After:  study_2024_participant_037.docx
```

### Personal Use
```
Before: assessment_results_20241218_143022.md
After:  2024_12_holiday_reflection.md
```

---

## 🔧 Technical Implementation

### New Functions Added

1. **`generate_suggested_filename(extension)`**
   - Creates default timestamp-based filenames
   - Called when page loads or resets
   - Format: `assessment_results_YYYYMMDD_HHMMSS.ext`

2. **`update_filename_suggestion()`**
   - Updates both Word and Markdown fields
   - Returns fresh timestamps

3. **Enhanced Export Functions**
   - `export_to_word(analysis, json, custom_filename)`
   - `export_to_markdown(analysis, json, custom_filename)`
   - Now accept optional custom filename parameter
   - Validates and processes filename
   - Adds extension if missing

### Smart Filename Processing

The system automatically:
- **Trims whitespace**: `" file "` → `"file"`
- **Adds extensions**: `"file"` → `"file.docx"`
- **Preserves extensions**: `"file.docx"` → `"file.docx"`
- **Handles paths**: Ensures proper save location

---

## 📱 Interface Changes

### New Assessment Tab

**Added**:
- Word filename text input
- Markdown filename text input
- Save location information
- Enhanced layout with two columns

**Before**:
```
[Export to Word button]
[Export to Markdown button]
```

**After**:
```
Word Filename (optional)          Markdown Filename (optional)
[Text input with suggestion]      [Text input with suggestion]
[Export to Word button]           [Export to Markdown button]
```

### Upload Previous Tab

**Same updates** as New Assessment tab for consistency

---

## 📚 Documentation Added

### 1. FILENAME_GUIDE.md (2,000+ words)
Complete guide including:
- ✅ Use cases and scenarios
- ✅ Naming best practices
- ✅ Technical details
- ✅ Do's and Don'ts
- ✅ Workflow examples
- ✅ FAQ section

### 2. INTERFACE_GUIDE.md (Visual reference)
ASCII art diagrams showing:
- ✅ Interface layout
- ✅ Before/after comparisons
- ✅ Interactive behavior
- ✅ Usage scenarios

### 3. Updated Existing Docs
- ✅ README.md - Added custom filename section
- ✅ QUICK_START.md - Added filename tips
- ✅ CHANGELOG.md - Version 2.1.0 details

---

## 🎓 Usage Tips

### Tip 1: Descriptive Names
```
✅ client_baseline_2024
✅ therapy_session_01
✅ participant_037

❌ file1
❌ test
❌ untitled
```

### Tip 2: Consistent Conventions
Pick a pattern and stick with it:
```
Option A: client_NAME_TYPE
  - client_jones_initial
  - client_jones_followup
  - client_jones_final

Option B: YYYY_MM_DD_description
  - 2024_12_18_baseline
  - 2024_03_18_progress
  - 2024_06_18_final
```

### Tip 3: Avoid Special Characters
```
✅ my_file_name.docx
✅ my-file-name.docx
✅ MyFileName.docx

❌ my/file.docx (slash)
❌ file*.docx (asterisk)
❌ file?.docx (question mark)
```

### Tip 4: Include Context
```
✅ smith_family_mother_intake.docx
✅ study_depression_2024_p042.docx
✅ 2024_Q4_self_assessment.docx
```

---

## 🔄 Migration Notes

### From Version 2.0 to 2.1

**No Breaking Changes**:
- Default behavior unchanged
- Empty filename = auto timestamp
- All existing code works

**New Capability**:
- Optional filename customization
- Backward compatible
- Progressive enhancement

**User Experience**:
- Fields pre-filled with suggestions
- Edit anytime before export
- Clear button resets to new timestamp

---

## ❓ FAQ

**Q: Do I have to customize the filename?**
A: No! Leave it as the default timestamp if you prefer.

**Q: What if I forget to add .docx or .md?**
A: The system adds it automatically based on export type.

**Q: Can I use the same name for Word and Markdown?**
A: Yes! Different extensions mean no conflict.

**Q: Will my custom name be saved for next time?**
A: No, fields reset to fresh timestamps after clear/reset.

**Q: Where do the files save?**
A: Files save to `/mnt/user-data/outputs/` and download through your browser.

**Q: What characters are allowed?**
A: Letters, numbers, hyphens, underscores. Avoid special characters like */?\:@

**Q: How long can the filename be?**
A: Up to 255 characters, but keep it under 100 for best compatibility.

**Q: Can I specify a different folder?**
A: Files go to outputs folder and then to your browser's download location.

---

## 🚀 Next Steps

### For Users

1. **Try it out**: Complete an assessment and customize the filename
2. **Develop a convention**: Decide on your naming pattern
3. **Organize files**: Keep exported files in organized folders
4. **Read guides**: Check FILENAME_GUIDE.md for detailed strategies

### For Developers

1. **Review code**: Check updated export functions
2. **Test edge cases**: Try various filename inputs
3. **Extend functionality**: Add more export formats
4. **Improve validation**: Add stricter filename checking

---

## 📊 Feature Comparison

| Feature | v1.0 | v2.0 | v2.1 |
|---------|------|------|------|
| JSON Export | ✅ | ✅ | ✅ |
| Word Export | ❌ | ✅ | ✅ |
| Markdown Export | ❌ | ✅ | ✅ |
| Upload Previous | ❌ | ✅ | ✅ |
| Auto Filenames | ❌ | ✅ | ✅ |
| Custom Filenames | ❌ | ❌ | ✅ |

---

## 🎉 Summary

### What Changed
- ✅ Added filename input fields (Word & Markdown)
- ✅ Auto-generated suggested filenames
- ✅ Smart extension handling
- ✅ Available on both tabs
- ✅ Comprehensive documentation

### Why It Matters
- 🎯 Better organization
- 📁 Professional naming
- 🔍 Easier to find files
- 💼 Clinical/research ready
- 🌟 User-friendly

### How to Use
1. Complete/upload assessment
2. Edit filename field (optional)
3. Click export button
4. Download with custom name

---

## 📦 Files Updated

### Code Files
- ✅ `personality_assessment_ui.py` - Main application

### Documentation Files
- ✅ `FILENAME_GUIDE.md` - Comprehensive guide (NEW)
- ✅ `INTERFACE_GUIDE.md` - Visual reference (NEW)
- ✅ `CHANGELOG.md` - Version 2.1.0 added
- ✅ `README.md` - Custom filename section added
- ✅ `QUICK_START.md` - Filename tips added

### Test Files
- ✅ All existing test files still compatible

---

## 🏁 Conclusion

The custom filename feature gives you full control over how your assessment files are named, making it easier to organize, find, and manage your exports. Whether you're a clinician tracking clients, a researcher managing participants, or an individual doing personal growth work, this feature provides the flexibility you need.

**Get Started**: Launch the app and try customizing a filename today!

```bash
python personality_assessment_ui.py
```

---

**Version**: 2.1.0  
**Release Date**: December 2024  
**Feature**: Custom Filename Selection
