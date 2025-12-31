# If it's on this website, it must be real!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/raffertyuy/it-must-be-real-website)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://itmustbereal.streamlit.app/)

Where entertainment meets genuine absurdity. Laugh, cringe, relate—it's all valid here. Remember: If it's on this website, it must be real!

> [!WARNING] **Disclaimer:** This website is intended for entertainment purposes only. My intent here is to teach Python to some of my family members by creating a fun Streamlit app. The content on this website may not accurately represent real-world objects or scenarios. Please do not take the content on this website seriously.

## Features

- 🎭 **Custom Navigation**: Navigate between pages with custom labels using Streamlit's `st.navigation()` API
- 🏠 **Home**: Welcome page with an overview of available categories
- 🍔 **Food**: Master chef quality dishes
- � **Games**: Real gaming experiences
- ✈️ **Travel**: Authentic travel destinations
- �🎲 **Random**: Anything and everything

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone this repository

   ```bash
   git clone https://github.com/raffertyuy/it-must-be-real-website.git
   cd it-must-be-real-website
   ```

2. Install Streamlit and other requirements

   ```bash
   pip install streamlit
   pip install -r requirements.txt
   ```

### Running the App

Run the Streamlit app with:

```bash
streamlit run streamlit_app.py
```

The app will open in your default browser at `http://localhost:8501`

## Tech Stack

- **Python 3.8+**: Core programming language
- **Streamlit**: Web framework for building the interactive app
- **Streamlit Navigation API**: Custom navigation using `st.navigation()` for labeled pages

## Project Structure

```
it-must-be-real-website/
├── .streamlit/          # Streamlit configuration
│   ├── config.toml      # Theme settings
│   └── style.css        # Global styles
├── images/              # Image assets
│   ├── food/           # Food category images
│   ├── games/          # Games category images
│   ├── travel/         # Travel category images
│   └── random/         # Random category images
├── pages/               # Category pages
│   ├── food.py         # Food page content
│   ├── games.py        # Games page content
│   ├── travel.py       # Travel page content
│   └── random.py       # Random page content
├── streamlit_app.py     # Main app with navigation and home page
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Architecture & Patterns

- **Main Entry Point**: `streamlit_app.py` contains the navigation setup and home page
- **Page Structure**: Each category page is a separate Python file in the `pages/` directory
- **Navigation**: Uses Streamlit's `st.navigation()` API to create custom navigation with labeled pages (Home, Food, Games, Travel, Random) instead of relying on file-based automatic navigation
- **Styling**: Global CSS is loaded from `.streamlit/style.css` in each page using `st.markdown()` with `unsafe_allow_html=True`
- **Page Configuration**: Set using `st.set_page_config()` in the main file with wide layout and custom page title/icon
- **Content Pattern**: Each page follows a consistent structure:
  1. Load global CSS
  2. Display title with emoji icon
  3. Show descriptive content
  4. Display images with captions and subheaders

### Key Coding Conventions

- **Images**: Stored in `images/` with category-specific subdirectories
- **Page Files**: Named descriptively (e.g., `food.py`, `games.py`, `travel.py`, `random.py`) and placed in `pages/` directory
- **Navigation Icons**: Each page uses emoji icons for visual identification (🍔 Food, 🎮 Games, ✈️ Travel, 🎲 Random)
- **Humor Tone**: Content maintains a satirical, tongue-in-cheek tone about "real" things

## Contributing

This is a learning project for teaching Python and Streamlit. Feel free to fork and create your own version!

## License

See [LICENSE](LICENSE) file for details.
