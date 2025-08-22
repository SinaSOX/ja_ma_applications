# AppFigures Market Analysis Project

A comprehensive analysis project for mobile app market research using AppFigures API data. This project focuses on analyzing app markets in Japan and Malaysia, with specific emphasis on market entry strategies and localization considerations.

## 📊 Project Overview

This project provides tools and analysis for:
- **Data Collection**: Automated fetching of app store data from AppFigures API
- **Market Analysis**: Comparative analysis between Japanese and Malaysian app markets
- **Strategic Insights**: Market entry strategies and localization recommendations
- **Visualization**: Data visualization and reporting capabilities

## 🚀 Features

### Data Collection
- Automated data fetching from AppFigures API
- Support for multiple app categories (Free, Grossing)
- Multi-country data collection (Japan, Malaysia)
- Timestamped data storage with JSON format

### Analysis Capabilities
- **Market Comparison**: Side-by-side analysis of app markets
- **App Characteristics**: Detailed analysis of app features and pricing
- **Developer Analysis**: Insights into top developers and publishers
- **Category Analysis**: Understanding app category distributions

### Reporting
- **Comprehensive Reports**: Detailed market analysis reports
- **Visual Timeline**: Market entry timeline visualization
- **Localization Guide**: Persian language localization considerations
- **Marketing Strategy**: Strategic recommendations for market entry

## 📁 Project Structure

```
HW3Q2/
├── 📊 Data Collection
│   ├── fetch_appfigures_data.py          # Main data fetcher
│   ├── fetch_with_different_params.py    # Parameterized data fetching
│   └── appfigures_data/                  # Raw data storage
│
├── 🔍 Analysis Scripts
│   ├── analyze_data.py                   # Basic data analysis
│   ├── analyze_app_characteristics.py    # App feature analysis
│   ├── analyze_readers.py                # Reader app analysis
│   ├── compare_countries.py              # Country comparison
│   ├── compare_countries_fixed.py        # Enhanced comparison
│   ├── top20_comparison.py               # Top 20 apps analysis
│   └── display_data.py                   # Data visualization
│
├── 📈 Reports
│   ├── comparison_summary.md             # Market comparison summary
│   ├── top20_comparison_report.md        # Top 20 apps report
│   ├── top100_comparison_report.md       # Top 100 apps report
│   ├── iran_market_analysis_report.md    # Iran market analysis
│   ├── marketing_strategy_report.md      # Marketing strategy
│   ├── localization_considerations_report.md # Localization guide
│   └── localization_summary_persian.md   # Persian summary
│
├── 📅 Timeline & Visualization
│   ├── publishing_timeline_gantt.py      # Timeline generator
│   └── iran_market_entry_timeline.png    # Visual timeline
│
└── 📋 Documentation
    ├── README.md                         # This file
    ├── requirements.txt                  # Python dependencies
    └── chr.md                           # Additional documentation
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SinaSOX/ja_ma_applications.git
   cd ja_ma_applications
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (if needed):
   Create a `.env` file with your AppFigures API credentials:
   ```
   RAPIDAPI_KEY=your_api_key_here
   ```

## 📖 Usage

### 1. Data Collection
```bash
# Fetch basic app data
python fetch_appfigures_data.py

# Fetch data with custom parameters
python fetch_with_different_params.py
```

### 2. Analysis
```bash
# Basic data analysis
python analyze_data.py

# Compare markets between countries
python compare_countries.py

# Analyze top 20 apps
python top20_comparison.py

# Analyze app characteristics
python analyze_app_characteristics.py
```

### 3. Visualization
```bash
# Generate timeline visualization
python publishing_timeline_gantt.py

# Display data visualizations
python display_data.py
```

## 📊 Key Findings

### Market Insights
- **Japan**: Strong preference for PDF readers and entertainment apps
- **Malaysia**: Focus on local financial and utility applications
- **Common Apps**: ChatGPT and TikTok are popular across both markets

### Strategic Recommendations
- **Localization**: Essential for market entry success
- **Category Focus**: Different strategies needed for each market
- **Timing**: Optimal entry periods identified for various app categories

## 📈 Reports Generated

1. **Market Comparison Summary** - Core findings and insights
2. **Top 20/100 Comparison Reports** - Detailed app rankings
3. **Iran Market Analysis** - Specific market entry strategy
4. **Marketing Strategy Report** - Comprehensive go-to-market plan
5. **Localization Considerations** - Cultural and linguistic adaptation guide

## 🔧 Technical Details

- **Language**: Python 3.x
- **Data Format**: JSON
- **API**: AppFigures (via RapidAPI)
- **Visualization**: Matplotlib, Plotly
- **Documentation**: Markdown

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is for educational and research purposes.

## 🤝 Contact

For questions or contributions, please open an issue on GitHub.

---

**Note**: This project is designed for market research and analysis purposes. Please ensure compliance with AppFigures API terms of service when using this tool.
