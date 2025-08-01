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

<img width="454" height="961" alt="Code Flow" src="https://github.com/user-attachments/assets/7b6de86d-10b4-43c2-a0da-8d59fde92eac" />

### Data (CSV Columns)

- `Child` (string): Name of the child  
- `Category` (string): Developmental domain  
- `Milestone` (int): Logged value  
- `Note` (string): Optional comment  
- `parsed_date` (datetime.date): Parsed at entry time  
- `Flag` (string): Empty or `"regression"`

## 5. Known Issues

- There is currently no way to edit or delete entries  
- No filtering or search for past entries  
- Duplicate entries are not being managed  
- CSV is overwritten every save; no backups  

## 6. Future Work

- Add edit and delete tools  
- Implement CSV versioning or database storage  
- Enable filtering logs by date, category, or flag etc.  
- Allow exporting charts as PNG or PDF
  
