# Members
- Gwynette D. Galleros
- Mariel Laplap
- Yasser Tomawis
- Johanie Abulkhair
- Arjay Libutan
  
# Adaptive Coding Environment Using User Modeling

A simple adaptive Python coding environment developed for **Elective 1 - Laboratory Activity 2**.

The project demonstrates how information about programmers can be analyzed, represented as a **user model**, and used by a system to provide different forms of coding assistance.

The project uses the **Stack Overflow Annual Developer Survey 2024** as the data source for investigating programming experience, development environment usage, and AI-assisted programming behavior.

---

## About the Project

Different programmers may prefer different kinds of coding assistance.

For example:

- Some programmers frequently use AI tools for debugging and writing code.
- Some programmers prefer less AI assistance.
- Programmers may also differ in the number of years they have been programming.
- Different users may therefore benefit from different features in a coding environment.

This project investigates these differences using the **Stack Overflow Annual Developer Survey 2024**.

The overall process is:

```text
Stack Overflow Survey Dataset
            ↓
Select relevant variables
            ↓
Clean and analyze the data
            ↓
Identify user patterns
            ↓
Create user profiles
            ↓
Represent profiles as user models
            ↓
Apply adaptation rules
            ↓
Adaptive coding prototype
```

The prototype is not intended to be a complete IDE.

Its purpose is to demonstrate how a coding environment can change its available assistance depending on the current user's model.

---

# Dataset

This project uses the:

**Stack Overflow Annual Developer Survey 2024**

The required dataset file is:

```text
survey_results_public.csv
```

The dataset can be downloaded from Kaggle:

**Stack Overflow Annual Developer Survey 2024**

https://www.kaggle.com/datasets/berkayalan/stack-overflow-annual-developer-survey-2024

The raw CSV is not stored in this GitHub repository because its file size exceeds GitHub's normal 100 MB file-size limit.

After downloading the dataset, place it inside:

```text
data/raw/
```

The final path should be:

```text
data/raw/survey_results_public.csv
```

---

# Selected Dataset Columns

The original survey contains many variables.

Only the variables relevant to this project are selected.

| Column | Purpose |
|---|---|
| `ResponseId` | Unique identifier for each survey respondent |
| `YearsCode` | Number of years the respondent has been programming |
| `NEWCollabToolsHaveWorkedWith` | Development environments or editors used |
| `AISelect` | Whether the respondent currently uses AI programming tools |
| `AIToolCurrently Using` | Programming activities where AI is currently used |
| `AISent` | Respondent's attitude toward AI tools |

These variables allow the project to investigate differences in:

- programming experience;
- development environment usage;
- AI-tool usage;
- AI-assisted programming activities; and
- attitudes toward AI tools.

---

# Programming Experience Groups

The `YearsCode` variable is converted into three experience groups for analysis.

| Years of Coding | Experience Group |
|---|---|
| 0–2 years | Early Experience |
| 3–9 years | Mid Experience |
| 10+ years | Long Experience |

These experience groups were created specifically for this project to make comparison between respondents easier.

They are **not official experience classifications from Stack Overflow**.

The labels also describe the **length of programming experience**, not the actual skill level of the programmer.

---

# User Profiles

A **user profile** is a human-readable description of a type of user based on meaningful characteristics or patterns found in the dataset.

For example:

```text
Early-Experience AI-Assisted Programmer

- Has relatively few years of programming experience
- Currently uses AI programming tools
- Uses AI for activities such as debugging or writing code
- Has a favorable attitude toward AI assistance
```

Another possible profile may be:

```text
Long-Experience AI Coding User

- Has many years of programming experience
- Uses AI programming tools
- Uses AI mainly for activities such as writing code or documentation
```

The profiles used in the project should come from patterns found during data analysis rather than being assigned randomly.

A user profile answers the question:

> **What type of user does this represent?**

---

# User Model

A **user model** is the structured representation of the user's characteristics that the application can read and use.

For example, the human-readable profile:

```text
Early-experience programmer who uses AI
for debugging and writing code.
```

may be represented in Python as:

```python
user_model = {
    "experience": "Early Experience",
    "uses_ai": True,
    "ai_preference": "High",
    "ai_debugging": True,
    "ai_writing": True,
    "ai_testing": False,
    "ai_learning": True
}
```

The difference is:

```text
USER PROFILE
Human-readable description
        ↓
USER MODEL
Structured representation in the program
        ↓
ADAPTATION
The application changes its behavior
```

A user model answers the question:

> **How can the system represent this user so that it can decide what assistance to provide?**

---

# Adaptive Behavior

The prototype reads the current user model and changes the coding assistance that is available.

Example adaptation rules:

| User Characteristic | Possible Adaptation |
|---|---|
| Uses AI | Make AI assistance available |
| High AI preference | Show AI tools more prominently |
| Uses AI for debugging | Show **Explain Error** |
| Uses AI for writing code | Show **Suggest Code** |
| Uses AI for testing | Show **Suggest Tests** |
| Uses AI for learning | Show **Explain Code** |
| Uses AI for documentation | Show **Generate Documentation** |


# Requirements

The project requires:

- Python 3
- Pandas
- Matplotlib
- Streamlit

The required Python packages are listed in:

```text
requirements.txt
```

Example:

```text
pandas
matplotlib
streamlit
```

---

# How to Run

## 1. Clone the Repository

```bash
git clone https://github.com/gwyiomi03/Elect1_LabAct2.git
```

Enter the project directory:

```bash
cd Elect1_LabAct2
```

## 2. Check Python

Make sure Python is installed.

On Windows, you can also use:

```bash
py --version
```

---

## 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable, install the packages manually:

```bash
pip install pandas matplotlib streamlit
```

---

# Dataset Setup

## 4. Download the Dataset

Download:

```text
survey_results_public.csv
```

---
## 5. Run the Analysis

Run:

```bash
python src/analyze_data.py
```

The tables and charts are used to identify meaningful differences between programming users.

---

# Running the Prototype

## 6. Start the Streamlit Application

Run:

```bash
streamlit run app.py
```

Streamlit should automatically open the application in your web browser.

If the browser does not open automatically, the terminal will display a local URL similar to:

```text
http://localhost:8501
```

Open that address in your browser.

---

# Technologies Used

- Python
- Pandas
- Matplotlib
- Streamlit
- Stack Overflow Annual Developer Survey 2024
- Git
- GitHub

