# If it's on this website, it must be real!

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/raffertyuy/it-must-be-real-website)
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blank-app-template.streamlit.app/)

This is a fun multipage Streamlit app featuring AI-generated images across different categories!

> [!WARNING] **Disclaimer:** This website is intended for entertainment purposes only. My intent here is to teach Python to some of my family members by creating a fun Streamlit app. The images on this website are AI generated and may not accurately represent real-world objects or scenarios. Please do not take the content on this website seriously.

## Features

- 🎭 **Multipage App**: Navigate between different categories using the sidebar
- 🍔 **Food**: Impossible AI-generated dishes
- 🎲 **Random**: AI-generated anything and everything

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
streamlit run Home.py
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
│   ├── 1_🍔_Food.py
│   └── 2_🎲_Random.py
├── Home.py              # Main home page
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## Contributing

This is a learning project for teaching Python and Streamlit. Feel free to fork and create your own version!

## License

See [LICENSE](LICENSE) file for details.
