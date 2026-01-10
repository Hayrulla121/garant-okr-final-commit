# OKR Performance Tracker

A comprehensive web-based application for tracking and managing Objectives and Key Results (OKRs) across departments. Built with Streamlit, this tool provides an intuitive interface for setting goals, monitoring performance, and visualizing progress.

![OKR Performance Tracker](https://img.shields.io/badge/version-5.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red)

## Features

### 🎯 Core Functionality

- **Multi-Department Management**: Organize OKRs across multiple departments
- **Flexible Key Results**: Support for three metric types:
  - ↑ Higher is Better (revenue, satisfaction, etc.)
  - ↓ Lower is Better (bugs, costs, response time, etc.)
  - 📊 Qualitative (A/B/C/D/E letter grades)
- **Smart Scoring System**: Automatic calculation of scores on a 3.0-5.0 scale
- **Weighted Objectives**: Assign custom weights to objectives for department-level scoring
- **Real-time Updates**: Instant recalculation and visualization of performance

### 📊 Visualization

- **Interactive Gauges**: Beautiful semi-circular gauges showing performance levels
- **Color-Coded Performance**: Visual indicators (Red → Orange → Light Green → Green → Dark Green)
- **Grid & Full View**: Switch between compact grid view and detailed full view
- **Performance Breakdown**: Detailed view of all KRs, scores, and thresholds

### 🌍 Internationalization

- **Multi-Language Support**: English, Russian, and Uzbek
- **Easy Language Switching**: Toggle between languages with a single click
- **Fully Translated UI**: All labels, buttons, and messages in your preferred language

### 💾 Data Management

- **Auto-Save**: Automatic saving to JSON file
- **Excel Export**: Export all data to formatted Excel files with color coding
- **Data Persistence**: All changes are saved and loaded automatically
- **Demo Data**: Quick demo loading for testing and exploration

### 🎨 User Interface

- **Modern Design**: Clean, professional interface with gradient headers
- **Collapsible Sidebar**: Toggle sidebar visibility for more screen space
- **Responsive Layout**: Works well on different screen sizes
- **Hover Tooltips**: Descriptive tooltips on KRs for additional context

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the repository**
   ```bash
   cd /path/to/okr
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install required packages**
   ```bash
   pip install streamlit pandas openpyxl
   ```

## Usage

### Starting the Application

Run the following command in your terminal:

```bash
streamlit run okr.py
```

The application will open automatically in your default web browser at `http://localhost:8501`

### Basic Workflow

#### 1. Create a Department

- Click "➕ Create New Department" in the sidebar
- Enter the department name
- Click "✅ Create"

#### 2. Add an Objective

- Select a department from the sidebar
- Click "➕ Create New Objective"
- Enter the objective name and weight (%)
- Add Key Results (see below)
- Click "✅ Create Objective"

#### 3. Add Key Results

When creating an objective, add one or more Key Results:

- **KR Name**: Descriptive name (e.g., "Customer Satisfaction")
- **Description**: Hover tooltip to explain what this KR measures
- **Type**: Choose metric type:
  - ↑ Higher is better
  - ↓ Lower is better
  - 📊 Qualitative (A/B/C/D/E)
- **Unit**: Unit of measurement (%, $, count, etc.)
- **Thresholds**: Define 5 performance levels:
  - Below: Minimum acceptable
  - Meets: Meets expectations
  - Good: Good performance
  - Very Good: Very good performance
  - Exceptional: Exceptional/Perfect performance

#### 4. Update Actual Values

- In the main view, find your objectives
- Enter actual values in the input fields
- Scores update automatically
- Changes are saved automatically

#### 5. Monitor Performance

- View individual KR scores
- See objective averages
- Check department-weighted scores
- Use gauges for quick visual assessment

### View Modes

Toggle between two view modes:

- **Grid View**: Compact cards showing objectives with gauges
- **Full View**: Detailed breakdown showing all KRs, thresholds, and scores

### Exporting Data

Click "Export Excel" to download a formatted Excel file with:
- Color-coded performance levels
- All departments, objectives, and key results
- Scores and actual values
- Professional formatting with borders and alignment

## Understanding the Scoring System

The application uses a sophisticated scoring algorithm. For a detailed explanation, see the `LOGIC_EXPLANATION.txt` file.

### Quick Summary

**Score Scale**: 3.0 (worst) to 5.0 (best)

| Score Range | Performance Level | Color |
|-------------|-------------------|-------|
| 5.00 | Exceptional | Dark Green |
| 4.75 - 4.99 | Very Good | Green |
| 4.50 - 4.74 | Good | Light Green |
| 4.25 - 4.49 | Meets Expectations | Orange |
| 3.00 - 4.24 | Below Expectations | Red |

**Score Calculation**:
1. Each KR is scored based on actual value vs. thresholds
2. Objective score = Average of all KR scores
3. Department score = Weighted average of objective scores

## File Structure

```
okr/
├── okr.py                    # Main application file
├── okr_data.json            # Data storage (auto-generated)
├── README.md                # This file
├── LOGIC_EXPLANATION.txt    # Detailed scoring logic explanation
└── .venv/                   # Virtual environment (if created)
```

## Data Storage

All data is stored in `okr_data.json` with the following structure:

```json
{
  "departments": [
    {
      "id": "unique-id",
      "name": "Department Name",
      "objectives": [
        {
          "id": "unique-id",
          "name": "Objective Name",
          "weight": 20,
          "key_results": [
            {
              "id": "unique-id",
              "name": "KR Name",
              "metric_type": "higher_better",
              "unit": "%",
              "description": "Description text",
              "weight": 0,
              "thresholds": {
                "below": 0.0,
                "meets": 60.0,
                "good": 75.0,
                "very_good": 90.0,
                "exceptional": 100.0
              },
              "actual": 85.0
            }
          ]
        }
      ]
    }
  ],
  "language": "en"
}
```

## Tips & Best Practices

### Setting Thresholds

- **Be Realistic**: Set achievable but challenging thresholds
- **Use Historical Data**: Base thresholds on past performance
- **Align with Strategy**: Ensure thresholds support business goals
- **Review Regularly**: Adjust thresholds as your organization evolves

### Managing Weights

- **Prioritize**: Assign higher weights to more strategic objectives
- **Balance**: Ensure weights reflect true priorities
- **Sum to 100%**: Try to make weights sum to 100% (app normalizes if not)

### Higher vs. Lower is Better

- **Higher is Better**: Use for metrics where increase = improvement
  - Revenue, profit, satisfaction, quality scores, completion rates
- **Lower is Better**: Use for metrics where decrease = improvement
  - Costs, bugs, response time, error rates, complaints

### Qualitative Metrics

- Use for subjective assessments that can't be measured numerically
- Examples: Design quality, communication effectiveness, leadership
- Define clear criteria for each grade (A/B/C/D/E) beforehand

## Troubleshooting

### Application Won't Start

```bash
# Check if Streamlit is installed
pip list | grep streamlit

# Reinstall if necessary
pip install --upgrade streamlit
```

### Data Not Saving

- Check file permissions in the application directory
- Ensure `okr_data.json` is not open in another program
- Check browser console for JavaScript errors

### Scores Look Wrong

- Verify threshold values are in the correct order
- For "Lower is Better", exceptional should be smallest
- For "Higher is Better", exceptional should be largest
- Check the `LOGIC_EXPLANATION.txt` file for calculation details

### Language Not Changing

- Click the language selector (flags at top right)
- Wait for automatic page reload
- Check if `okr_data.json` has write permissions

## Advanced Features

### Keyboard Shortcuts

- **Tab**: Navigate between input fields
- **Enter**: Submit forms
- **Esc**: Close modals (browser default)

### Batch Operations

To update multiple values:
1. Switch to Full View mode
2. All KRs are visible with input fields
3. Update values in sequence
4. Each change auto-saves

### Custom Styling

The app uses predefined color themes in the `THEME` dictionary. To customize:
1. Open `okr.py`
2. Find the `THEME` dictionary (around line 268)
3. Modify color values
4. Restart the application

## Performance

- **Fast Loading**: Optimized for quick startup
- **Efficient Rendering**: Only re-renders changed components
- **Automatic Caching**: Streamlit caches static content
- **Minimal Data**: Lightweight JSON storage

## Browser Compatibility

Tested and working on:
- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Opera (latest)

## Contributing

This is a self-contained application. To modify:

1. Make changes to `okr.py`
2. Test thoroughly
3. Update this README if you add features
4. Consider backing up `okr_data.json` before major changes

## Version History

**v5.0** (Current)
- Fixed JSON parsing issues with NaN values
- Fixed empty label warnings in language selector
- Fixed float conversion errors for None values
- Removed hover tooltip from toggle sidebar button
- Stable release with all core features

**Previous versions**
- v4: Added weighted scoring system
- v3: Added multi-language support
- v2: Added Excel export
- v1: Initial release

## License

This is a proprietary application. All rights reserved.

## Support

For issues or questions:
1. Check `LOGIC_EXPLANATION.txt` for scoring questions
2. Review this README for usage guidance
3. Check the troubleshooting section above

## Quick Start Example

Here's a complete example to get you started:

1. **Start the app**: `streamlit run okr.py`
2. **Create IT Department**
3. **Add Objective**: "Improve Code Quality" (weight: 40%)
4. **Add KR1**:
   - Name: "Code Delivered on Time"
   - Type: Higher is Better
   - Unit: %
   - Thresholds: 0, 60, 75, 90, 100
   - Actual: 85%
5. **Add KR2**:
   - Name: "Bug Count"
   - Type: Lower is Better
   - Unit: bugs
   - Thresholds: 20, 10, 5, 2, 0
   - Actual: 3 bugs
6. **View Results**: See automatic scoring and gauges!

---

