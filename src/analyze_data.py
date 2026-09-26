from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


# PATHS
ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = ROOT / "data" / "processed" / "selected_clean.csv"

TABLE_DIR = ROOT / "outputs" / "tables"
CHART_DIR = ROOT / "outputs" / "charts"

TABLE_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)


# LOAD DATA
df = pd.read_csv(DATA_FILE)

experience_order = [
    "Early Experience",
    "Mid Experience",
    "Long Experience"
]


# ANALYSIS 1: MISSING VALUES
original_columns = [
    "ResponseId",
    "YearsCode",
    "NEWCollabToolsHaveWorkedWith",
    "AISelect",
    "AIToolCurrently Using",
    "AISent"
]

missing = pd.DataFrame({
    "MissingCount":
        df[original_columns].isna().sum(),

    "MissingPercent":
        df[original_columns].isna().mean() * 100
})

missing["MissingPercent"] = (
    missing["MissingPercent"].round(2)
)

missing.to_csv(
    TABLE_DIR / "missing_values.csv"
)

print("\nMISSING VALUES")
print(missing)


# ANALYSIS 2:EXPERIENCE DISTRIBUTION
experience_counts = (
    df["ExperienceGroup"]
    .value_counts()
    .reindex(experience_order)
)

experience_counts.to_csv(
    TABLE_DIR / "experience_distribution.csv",
    header=["Count"]
)

print("\nEXPERIENCE DISTRIBUTION")
print(experience_counts)


# ANALYSIS 3: AI USAGE BY EXPERIENCE
ai_data = df.dropna(
    subset=[
        "ExperienceGroup",
        "AISelect"
    ]
)

ai_usage = pd.crosstab(
    ai_data["ExperienceGroup"],
    ai_data["AISelect"],
    normalize="index"
) * 100

ai_usage = (
    ai_usage
    .reindex(experience_order)
    .round(2)
)

ai_usage.to_csv(
    TABLE_DIR / "ai_usage_by_experience.csv"
)

print("\nAI USAGE BY EXPERIENCE (%)")
print(ai_usage)


# CHART
if "Yes" in ai_usage.columns:

    current_ai = ai_usage["Yes"]

    ax = current_ai.plot(
        kind="bar"
    )

    ax.set_title(
        "Current AI Usage by Programming Experience"
    )

    ax.set_xlabel(
        "Experience Group"
    )

    ax.set_ylabel(
        "Respondents Using AI (%)"
    )

    plt.xticks(
        rotation=0
    )

    plt.tight_layout()

    plt.savefig(
        CHART_DIR / "ai_usage_by_experience.png",
        dpi=200
    )

    plt.close()



# ANALYSIS 4: AI SENTIMENT BY EXPERIENCE
sentiment_data = df.dropna(
    subset=[
        "ExperienceGroup",
        "AISent"
    ]
)

sentiment = pd.crosstab(
    sentiment_data["ExperienceGroup"],
    sentiment_data["AISent"],
    normalize="index"
) * 100

sentiment = (
    sentiment
    .reindex(experience_order)
    .round(2)
)

sentiment.to_csv(
    TABLE_DIR / "ai_sentiment_by_experience.csv"
)

print("\nAI SENTIMENT BY EXPERIENCE (%)")
print(sentiment)


# ANALYSIS 5: HOW CURRENT AI USERS USE AI
ai_users = df[
    (df["AISelect"] == "Yes")
    &
    (df["ExperienceGroup"].notna())
].copy()


task_columns = [
    "AI_Debugging",
    "AI_WritingCode",
    "AI_Testing",
    "AI_LearningCodebase",
    "AI_Documentation"
]

task_percent = (
    ai_users
    .groupby("ExperienceGroup")[task_columns]
    .mean()
    * 100
)

task_percent = (
    task_percent
    .reindex(experience_order)
    .round(2)
)

task_percent.to_csv(
    TABLE_DIR / "ai_tasks_by_experience.csv"
)

print("\nAI ACTIVITIES BY EXPERIENCE (%)")
print(task_percent)


# CHART
ax = task_percent.plot(
    kind="bar"
)

ax.set_title(
    "AI-Assisted Programming Activities"
)

ax.set_xlabel(
    "Experience Group"
)

ax.set_ylabel(
    "Current AI Users (%)"
)

plt.xticks(
    rotation=0
)

plt.legend(
    title="AI Activity"
)

plt.tight_layout()

plt.savefig(
    CHART_DIR / "ai_tasks_by_experience.png",
    dpi=200
)

plt.close()


# ANALYSIS 6:
# DEVELOPMENT ENVIRONMENT USE
ide_data = df.dropna(
    subset=[
        "ExperienceGroup",
        "NEWCollabToolsHaveWorkedWith"
    ]
).copy()


ide_flags = (
    ide_data["NEWCollabToolsHaveWorkedWith"]
    .str.get_dummies(sep=";")
)

ide_flags["ExperienceGroup"] = (
    ide_data["ExperienceGroup"].values
)

ide_percent = (
    ide_flags
    .groupby("ExperienceGroup")
    .mean(numeric_only=True)
    * 100
)

ide_percent = (
    ide_percent
    .reindex(experience_order)
)


# Pick the 10 most commonly used environments
top_10 = (
    ide_percent
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .index
)

top_ide_percent = (
    ide_percent[top_10]
    .round(2)
)

top_ide_percent.to_csv(
    TABLE_DIR / "top_ides_by_experience.csv"
)

print("\nTOP DEVELOPMENT ENVIRONMENTS (%)")
print(top_ide_percent)


print("\nAnalysis complete.")
print("Tables:", TABLE_DIR)
print("Charts:", CHART_DIR)