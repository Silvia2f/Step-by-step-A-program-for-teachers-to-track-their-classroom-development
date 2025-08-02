# Step-by-Step: Child Progress Tracker
A Streamlit app to help teachers track developmental milestones for each child in their classroom. You can log entries by category (like Mobility or Language, Social Emotional Development, and Fine Motor), and visualize the child’s growth over time using simple graphs. All data is stored in a local CSV file.

# Installation
- use pip to install the required third party packages: `pip install -r requirements.txt`

# Usage
- Open a terminal and navigate to the project folder
- Run the app with: `streamlit run main.py`

Make sure your folder includes this:

```
project-folder/

├── main.py
├── data
│   └── test_data.csv
├── doc
│   ├── Alberti_HCI5840_ReviewDoc_Version1.pdf
│   ├── Alberti_HCI5840_ProjectSpecs.pdf
│   └── dev_guide.md
├── requirements.txt
└── README.md
```

The test_data.csv file already includes sample logs for three children so you can test it right away.

# How to Use It
- Select a child from the dropdown at the top (or enter a new name)
- Choose a category and enter a milestone number
- Optionally write a note
- If the number is lower than a previous one, a warning will appear (for regressions)
- Click “Add Log Entry” to save
- Expand the sections below the table to:
  - View a line chart by category
  - View a pie chart of all logged categories
  - Compare all children by one category (via sidebar)

# Known Issues
- Entries cannot be edited or deleted once saved
- Duplicate entries are not prevented or flagged
- No filters or search for past entries
- Graphs only update when manually re-expanded or on rerun
- App only supports one local CSV file (no database or multi-user support)
- No backups or versioning of the CSV file

# Acknowledgments
This project was created for HCI 584 (Summer 2025). The project's specs and early planning files are available in `doc/Alberti_HCI5840_ProjectSpecs.pdf`.

For more technical details, see the [Developer’s Guide](doc/dev_guide.md).

