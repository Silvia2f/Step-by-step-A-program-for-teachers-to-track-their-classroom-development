# Developer’s Guide — Step-by-Step: Child Progress Tracker

This document is intended for developers who want to understand or extend the functionality of this app. It assumes the app is already running and that the user has reviewed the [README](../README.md).


## 1. Overview

Step-by-Step is a lightweight Streamlit app designed for classroom teachers to track children's developmental milestones across key categories. It saves all data to a local CSV and provides simple visualizations like line charts and pie charts.

This guide describes the app’s internal logic, data structure, and areas for future development.


## 2. Final Specs (Implemented Features)

- Logging new entries via sidebar form
- Categories supported: Mobility, Social Emotional, Cognitive, Language, Fine Motor
- Automatically flags regressions if a score is lower than the child’s previous milestone
- Saves entries to `data/test_data.csv`
- Category-level line chart (per child)
- Pie chart for log distribution (per child)
- Pie chart to compare all children in one category


## 3. Install / Deployment 
```bash
pip install -r requirements.txt
```
**To run:**
```bash
streamlit run main.py
```

## 4. Folder Structure

project-folder/

├── main.py

├── data/

.   └── test_data.csv

├── doc/

.   └── Alberti_HCI5840_ReviewDoc_Version1.pdf

.   └── Alberti_HCI5840_ProjectSpecs.pdf

.   └── dev_guide.md

├── requirements.txt

├── README.md

## 4. End User Interaction and Flow Through Code

### User Experience Flow

1. User selects a child or types a new name  
2. Chooses a category and milestone number  
3. Optional note is added  
4. Regression warning appears if applicable  
5. Entry is saved to `test_data.csv`  
6. Below the table, the user can:
   - View line graph (per category)
   - View pie chart (category distribution)
   - View classroom comparison pie chart

### Code Flow
