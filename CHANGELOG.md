# Changelog

## Version 2.1.0 - December 2024

### 🎉 New Feature: Custom Filename Selection

#### Custom Filename Inputs
- **Filename Text Fields**: Editable fields for both Word and Markdown exports
- **Auto-Generated Suggestions**: Default timestamp-based names pre-filled
- **Real-Time Updates**: Filenames refresh when clearing forms
- **Smart Extension Handling**: Automatically adds `.docx` or `.md` if missing
- **Both Tabs**: Available in "New Assessment" and "Upload Previous" tabs

#### User Experience Improvements
- Clear labels explaining filename customization
- Placeholder text showing example formats
- Info text guiding users on extension handling
- Save location information displayed
- Consistent interface across both tabs

### 🔧 Technical Implementation

#### New Functions
- `generate_suggested_filename(extension)` - Creates timestamp-based filenames
- `update_filename_suggestion()` - Updates both filename fields simultaneously
- Updated `export_to_word()` - Now accepts custom filename parameter
- Updated `export_to_markdown()` - Now accepts custom filename parameter

#### Improvements
- Enhanced export functions with filename validation
- Automatic extension appending if missing
- Path handling for custom filenames
- Better error messages for invalid filenames

### 📚 New Documentation
- `FILENAME_GUIDE.md` - Comprehensive guide to custom filenames
  - Use cases and examples
  - Naming best practices
  - Workflow examples
  - Technical details
  - FAQ section

### 💡 Use Cases Enabled

1. **Clinical Identification**
   ```
   client_john_doe_initial_assessment.docx
   ```

2. **Progress Tracking**
   ```
   therapy_session_01_baseline.docx
   therapy_session_02_3month.docx
   ```

3. **Research Participants**
   ```
   study_2024_participant_037.docx
   ```

4. **Personal Organization**
   ```
   2024_12_18_career_reflection.md
   ```

### 🎨 Interface Updates

**New Assessment Tab**:
- Added Word filename input field
- Added Markdown filename input field
- Updated export button layout
- Added save location information

**Upload Previous Tab**:
- Added Word filename input field
- Added Markdown filename input field
- Consistent with New Assessment layout

### 📊 Benefits

- **Flexibility**: Choose meaningful names instead of timestamps
- **Organization**: Create consistent naming conventions
- **Professionalism**: Client/participant-friendly filenames
- **Tracking**: Easier to identify and compare files
- **Searchability**: Descriptive names improve file discovery

### 🔄 Backward Compatibility

- Default behavior unchanged (uses timestamp if field empty)
- Existing code examples remain valid
- No breaking changes to export functions
- Optional feature - works with or without customization

---

## Version 2.0.0 - December 2024

### 🎉 Major New Features

#### 1. Upload Previous Assessments
- **New Tab**: "📂 Upload Previous Assessment"
- Upload saved JSON files for re-analysis
- Compatible with all previously exported JSON assessments
- Useful for tracking progress over time
- Re-analyze with updated LLM models

#### 2. Export to Word (.docx)
- Professional document formatting
- Complete analysis text included
- Detailed response breakdown
- Timestamp and metadata preserved
- Ready for printing or sharing with professionals

#### 3. Export to Markdown (.md)
- Plain text format for maximum compatibility
- Works with note-taking apps (Obsidian, Notion, etc.)
- Git-friendly for version control
- Easy to read and edit
- Perfect for personal journals

#### 4. Dual Interface Design
- **Tab 1**: New Assessment - Complete fresh assessments
- **Tab 2**: Upload Previous - Re-analyze saved assessments
- Clear separation of workflows
- Consistent export options on both tabs

### 🔧 Technical Improvements

#### Code Enhancements
- Added `load_json_file()` function for file uploads
- Added `export_to_word()` function with python-docx integration
- Added `export_to_markdown()` function for text export
- Improved error handling for file operations
- Auto-installation of python-docx if missing

#### UI Improvements
- Organized layout with two main tabs
- File upload component with .json filter
- Download buttons for Word and Markdown exports
- File output components for easy download
- Clear visual separation between new and upload workflows

#### Documentation Updates
- Updated README.md with upload/export sections
- Enhanced QUICK_START.md with new feature guides
- Added FEATURE_GUIDE.md with comprehensive walkthroughs
- Created example_usage.py examples for uploads/exports
- Added test JSON files for demonstration

### 📚 New Files

#### Documentation
- `FEATURE_GUIDE.md` - Comprehensive feature demonstrations
- `CHANGELOG.md` - This file, documenting changes

#### Test Data
- `test_upload_schizoid.json` - Example Schizoid personality assessment
- `test_upload_borderline.json` - Example Borderline personality assessment

#### Code Examples
- Updated `example_usage.py` with 3 new examples:
  - Example 10: Upload and Re-analyze
  - Example 11: Export to Multiple Formats
  - Example 12: Batch Upload and Compare

### 🐛 Bug Fixes
- Fixed Gradio 6.0 theme parameter warning
- Improved JSON validation on upload
- Enhanced error messages for invalid uploads
- Better file path handling for exports

### 💡 Use Cases Enabled

1. **Clinical Practice**
   - Track client progress over time
   - Share formatted reports with clients
   - Maintain organized assessment records

2. **Research**
   - Collect data in JSON format
   - Batch process multiple assessments
   - Export results for analysis

3. **Self-Development**
   - Monitor personal growth
   - Keep journal entries in Markdown
   - Re-analyze with improved models

4. **Education**
   - Demonstrate personality theory
   - Compare different personality types
   - Create teaching materials

### 🔄 Migration Guide

#### From Version 1.0
1. No breaking changes - all v1.0 JSON files compatible
2. New features are additions, not replacements
3. Original assessment workflow unchanged
4. Simply use new export buttons after analysis

#### JSON Format
- Format remains unchanged from v1.0
- All previous JSON files can be uploaded
- Timestamp format preserved
- Response structure identical

### ⚙️ Dependencies

#### New Dependencies
- `python-docx` - For Word document generation
  - Auto-installs on first use if missing
  - Can be manually installed: `pip install python-docx`

#### Existing Dependencies (Unchanged)
- `gradio >= 6.0`
- `requests`
- Python 3.8+

### 📊 Performance

- File upload: ~instant for typical JSON files (<100KB)
- Word export: ~1-2 seconds for full assessment
- Markdown export: ~instant
- No impact on analysis performance

### 🔒 Security & Privacy

- All file operations are local
- No data transmitted during export
- JSON files contain no personal identifiers by default
- Users responsible for secure storage of exported files

### 🚀 Future Roadmap

#### Planned Features (v2.1)
- [ ] PDF export option
- [ ] Side-by-side comparison view
- [ ] Timeline visualization
- [ ] Email delivery integration

#### Under Consideration (v3.0)
- [ ] Database backend option
- [ ] Multi-user support
- [ ] API endpoints
- [ ] Mobile app version

### 📝 Notes

- **Backward Compatible**: All v1.0 features remain unchanged
- **No Breaking Changes**: Existing workflows continue to work
- **Optional Features**: Upload and export are optional enhancements
- **Progressive Enhancement**: Works with or without API key

### 🙏 Credits

- Built with Gradio 6.0
- Uses python-docx for Word generation
- Anthropic Claude API for analysis
- Community feedback and suggestions

---

## Version 1.0.0 - Initial Release

### Features
- 18-question psychoanalytic assessment
- 8 personality type classifications
- Claude API integration
- Fallback pattern-matching analysis
- JSON output format
- Web-based Gradio interface
- Real-time analysis
- Comprehensive results display

---

**For detailed usage instructions, see:**
- README.md - Complete documentation
- QUICK_START.md - Quick setup guide
- FEATURE_GUIDE.md - Feature demonstrations
- example_usage.py - Code examples
