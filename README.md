# If it's on this website, it must be real!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/raffertyuy/it-must-be-real-website)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://itmustbereal.streamlit.app/)

Where entertainment meets genuine absurdity. Laugh, cringe, relate—it's all valid here. Remember: If it's on this website, it must be real!

> [!WARNING] **Disclaimer:** This website is intended for entertainment purposes only. My intent here is to teach Python to some of my family members by creating a fun Streamlit app. The content on this website may not accurately represent real-world objects or scenarios. Please do not take the content on this website seriously.

## Features

- 🎭 **Custom Navigation**: Navigate between pages with custom labels using Streamlit's `st.navigation()` API
- 🏠 **Home**: Welcome page with an overview of available categories
- 🍔 **Food**: Master chef quality dishes
- 🎲 **Random**: Anything and everything

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

## Project Structure

```
it-must-be-real-website/
├── .streamlit/          # Streamlit configuration
│   ├── config.toml      # Theme settings
│   └── style.css        # Global styles
├── images/              # Image assets
│   ├── food/           # Food category images
│   └── random/         # Random category images
├── pages/               # Category pages
│   ├── food.py         # Food page content
│   └── random.py       # Random page content
├── streamlit_app.py     # Main app with navigation and home page
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

The app uses Streamlit's `st.navigation()` API to create custom navigation with labeled pages (Home, Food, Random) instead of relying on file-based automatic navigation.

## Contributing

This is a learning project for teaching Python and Streamlit. Feel free to fork and create your own version!

## License

See [LICENSE](LICENSE) file for details.
