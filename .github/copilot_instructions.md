# GitHub Copilot Instructions for "It Must Be Real" Website

## Project Overview

**IMPORTANT**: Before making any code changes or architectural decisions, always refer to the [README.md](../README.md) file for comprehensive information about:
- What this application is about (satirical entertainment website)
- Complete tech stack and dependencies
- Project structure and file organization
- Architecture patterns and coding conventions
- Key features and navigation structure

This file contains coding guidelines specific to GitHub Copilot assistance for this Streamlit Python application.

---

## Core Principles for AI Assistance

### 1. Critical Thinking & Validation

- **DO NOT automatically agree with all user requests** - Take a step back and evaluate if the request:
  - Aligns with the project's architecture and patterns (see README.md)
  - Follows Streamlit best practices
  - Maintains code consistency across the application
  - Could introduce security issues or anti-patterns
  
- **Always validate before implementing**:
  - Review existing code patterns in similar files
  - Check if the requested change conflicts with established conventions
  - Consider alternative approaches that might be more maintainable
  - Ask clarifying questions if the request is ambiguous or potentially problematic

- **Provide thoughtful pushback** when appropriate:
  - "I notice this approach differs from the pattern used in other pages. Should we keep consistency with X pattern, or is there a reason to deviate?"
  - "This could impact performance/maintainability because X. Would you like to consider Y approach instead?"
  - "Before implementing this, let me verify it aligns with Streamlit's best practices..."

### 2. Research First, Code Second

- **Always review relevant context** before generating code:
  - Read existing page files to understand patterns
  - Check how similar features are implemented elsewhere
  - Verify the current project structure matches expectations
  - Consult README.md for architectural decisions

- **Don't assume - investigate**:
  - Use file search to find similar implementations
  - Check if utilities or helpers already exist
  - Verify file paths and directory structures
  - Look for existing CSS classes or styling patterns

---

## Streamlit-Specific Best Practices

### Application Structure

1. **Page Configuration** (from README.md patterns):
   - `st.set_page_config()` should only be called in `streamlit_app.py` (main entry point)
   - Use `page_title`, `page_icon`, and `layout` parameters consistently
   - Never call `st.set_page_config()` in individual page files in `pages/` directory

2. **Navigation**:
   - This app uses `st.navigation()` API, NOT file-based auto-navigation
   - All pages must be explicitly registered in `streamlit_app.py`
   - Page definitions use `st.Page()` with `title` and `icon` parameters
   - Navigation structure: `[home, food, games, travel, random, ...]`

3. **CSS Loading Pattern**:
   ```python
   # Every page should load global CSS this way
   with open(".streamlit/style.css") as f:
       st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
   ```
   - Always add this at the top of page files after imports
   - Use relative path `.streamlit/style.css` (works from all page locations)

### Code Quality & Patterns

1. **Consistent Page Structure**:
   ```python
   import streamlit as st
   
   # Load global CSS
   with open(".streamlit/style.css") as f:
       st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
   
   # Header with emoji
   st.title("🎲 Page Title")
   
   # Description
   st.write("""...""")
   
   st.divider()
   
   # Main content
   ```

2. **Image Handling**:
   - Images stored in `images/{category}/` directories
   - Use `st.image("images/category/filename.ext")`
   - Always include descriptive captions with `st.caption()`
   - Add subheaders before images for context with `st.subheader()`

3. **Component Usage**:
   - Use `st.button()` with `type="primary"` for main CTAs
   - Use `st.warning()` or `st.info()` for notices/disclaimers
   - Use `st.divider()` to separate content sections
   - Prefer multi-line strings with `"""` for better readability

4. **State Management**:
   - Minimize use of `st.session_state` unless absolutely necessary
   - Keep pages stateless when possible (Streamlit reruns are normal)
   - Use `st.cache_data` or `st.cache_resource` for expensive operations

### Performance Best Practices

1. **Caching**:
   - Cache data loading: `@st.cache_data`
   - Cache resource connections: `@st.cache_resource`
   - Don't cache UI rendering functions

2. **Efficient Rendering**:
   - Use `st.container()` and `st.columns()` for layout control
   - Avoid nested loops that call Streamlit functions
   - Minimize reruns by structuring logic efficiently

3. **File Operations**:
   - Always use `with open()` context managers
   - Prefer relative paths for portability
   - Handle file not found errors gracefully

### Security & Safety

1. **Safe HTML Usage**:
   - Only use `unsafe_allow_html=True` when necessary
   - Sanitize any user input before rendering as HTML
   - Prefer Streamlit's native components when possible

2. **Path Safety**:
   - Validate file paths before loading
   - Don't expose system paths to users
   - Use relative paths from project root

3. **Dependencies**:
   - Keep `requirements.txt` minimal and updated
   - Document any new dependencies added
   - Prefer standard library when sufficient

---

## Project-Specific Guidelines

### Content Tone & Style

- This is a **satirical/humorous** entertainment website
- Content should be tongue-in-cheek about things being "real"
- Maintain playful, lighthearted copy with intentionally controversial opinions (e.g., "pineapple on pizza")
- Use emojis liberally in titles and UI elements for visual interest
- Include disclaimers reminding users content is for entertainment only

### Adding New Categories/Pages

When adding a new category page:

1. **Create the page file**: `pages/{category_name}.py`
2. **Follow the standard structure**: Import → CSS loading → Title → Content → Images
3. **Add images**: Create directory `images/{category_name}/` if needed
4. **⚠️ CRITICAL: Register in navigation**: Update `streamlit_app.py` to add the new page:
   - Define the page: `new_page = st.Page("pages/{category_name}.py", title="Title", icon="🎨")`
   - Add to navigation list: `pg = st.navigation([home, food, games, travel, random, new_page])`
   - **The page will NOT appear in the sidebar without this step!**
5. **Update README.md**: Add the new category to the Features, Project Structure, and Architecture sections
6. **Update copilot_instructions.md**: Update the navigation structure and any relevant examples
7. **Use appropriate emoji**: Choose a fitting emoji icon for the category
8. **Add preview on home page**: Consider adding a button or section on the home page to link to the new category

### Image Management

- **Naming**: Use lowercase with underscores (e.g., `sunny_side_up_egg.png`)
- **Organization**: Images must be in appropriate subdirectory under `images/`
- **Formats**: Support `.jpg`, `.png`, `.gif` - choose based on content needs
- **Size**: Optimize images for web viewing (Streamlit will handle responsive sizing)
- **Captions**: Every image should have a humorous/satirical caption

### Styling Approach

- **Global styles**: Add to `.streamlit/style.css` for app-wide changes
- **Theme settings**: Modify `.streamlit/config.toml` for colors, fonts, etc.
- **Inline styles**: Use sparingly, prefer CSS classes
- **Responsive design**: Streamlit handles most responsive behavior, use `layout="wide"` in config

---

## Development Workflow

### Before Writing Code

1. ✅ Read README.md to understand project context
2. ✅ Review existing similar implementations
3. ✅ Check current project structure with file searches
4. ✅ Identify patterns and conventions in use
5. ✅ Consider if changes require README.md updates

### Code Review Checklist

Before suggesting code, verify:

- [ ] Follows established patterns from README.md and existing code
- [ ] Uses consistent imports and structure
- [ ] Includes proper CSS loading for page files
- [ ] Has appropriate error handling
- [ ] Maintains the humorous/satirical tone
- [ ] Doesn't duplicate existing functionality
- [ ] Properly integrates with navigation system
- [ ] Updates README.md if architecture changes

### Testing Suggestions

When suggesting code, remind users to test:

1. **Run the app**: `streamlit run streamlit_app.py`
2. **Check navigation**: Verify all pages are accessible
3. **Test responsive layout**: Resize browser window
4. **Verify images load**: Check correct paths and file existence
5. **Review console**: Look for errors or warnings in terminal
6. **Cross-page consistency**: Ensure styling and behavior is consistent

---

## Communication Guidelines

### Be Helpful But Honest

- **Admit uncertainty**: "I'm not certain about this approach. Let me check existing patterns first."
- **Suggest alternatives**: "This would work, but have you considered X which might be more maintainable?"
- **Explain tradeoffs**: "Option A is simpler but less flexible. Option B is more robust but adds complexity."

### Ask Clarifying Questions

Before implementing ambiguous requests:

- "Should this new page follow the same structure as the Food and Random pages?"
- "Do you want this as a new category, or should it be added to an existing page?"
- "Should I update the home page to include a link to this new content?"
- "Would you like me to update the README.md documentation as well?"

### Provide Context

When suggesting code:

- Explain **why** this approach is recommended
- Note if it differs from existing patterns and why
- Mention any potential gotchas or considerations
- Link to relevant Streamlit documentation when helpful

### Educational Approach

Since this is a **learning project** (per README.md), always:

- Explain Streamlit concepts, don't just provide code
- Point out best practices and anti-patterns
- Suggest resources for learning more
- Encourage experimentation while maintaining code quality

---

## Common Tasks & Patterns

### Adding a New Page

```python
# 1. Create pages/new_category.py
import streamlit as st

with open(".streamlit/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🎨 Category Title")
st.write("""Description here""")
st.divider()
# Content...

# 2. Register in streamlit_app.py
new_category = st.Page("pages/new_category.py", title="Category", icon="🎨")
pg = st.navigation([home, food, games, travel, random, new_category])

# 3. Update README.md to document the new page
# 4. Update copilot_instructions.md navigation structure
```

### Adding Images to a Page

```python
st.subheader("Descriptive humorous title")
st.image("images/category/image_name.jpg")
st.caption("Satirical caption here.")
```

### Creating Interactive Elements

```python
# Button with navigation
if st.button("🚀 Check this out!", type="primary"):
    st.switch_page("pages/target_page.py")

# Info boxes
st.info("ℹ️ Helpful information here")
st.warning("⚠️ Disclaimer or warning")
st.success("✅ Success message")
st.error("❌ Error message")
```

### Working with Columns

```python
col1, col2, col3 = st.columns(3)
with col1:
    st.image("images/category/img1.jpg")
with col2:
    st.image("images/category/img2.jpg")
with col3:
    st.image("images/category/img3.jpg")
```

---

## Troubleshooting Common Issues

### Page Not Showing in Navigation

- ✅ Check that page is registered in `st.navigation()` in `streamlit_app.py`
- ✅ Verify file path is correct in `st.Page()` definition
- ✅ Ensure file exists in `pages/` directory

### CSS Not Loading

- ✅ Verify `.streamlit/style.css` exists
- ✅ Check the relative path from the page file location
- ✅ Ensure `with open()` block is at the top of the page
- ✅ Confirm `unsafe_allow_html=True` is set

### Images Not Displaying

- ✅ Check image path is correct (relative from project root)
- ✅ Verify image file exists in the specified directory
- ✅ Ensure filename matches exactly (case-sensitive on some systems)
- ✅ Test image loads when app is run from project root directory

### Config Errors

- ✅ Never call `st.set_page_config()` in page files, only in `streamlit_app.py`
- ✅ Ensure it's the first Streamlit command in the main file
- ✅ Check `.streamlit/config.toml` for syntax errors

---

## Summary: Key Reminders

1. **Read README.md first** - All architectural decisions are documented there
2. **Question requests** - Don't blindly implement, validate and suggest improvements
3. **Follow patterns** - Maintain consistency with existing code structure
4. **Be thorough** - Research context before generating code
5. **Educate users** - This is a learning project, explain your reasoning
6. **Test suggestions** - Remind users how to verify changes work correctly
7. **Stay humble** - Admit when you need to check something or aren't certain
8. **Keep it fun** - Remember the satirical, humorous nature of this project!

---

*This file should evolve as the project grows. Update it when new patterns emerge or architectural decisions change.*
