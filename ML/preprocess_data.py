import pandas as pd

# The used dataset is from kaggle
# https://www.kaggle.com/datasets/architsharma01/loan-approval-prediction-dataset?resource=download

# Read the dataset, and declare the first row as the header
df = pd.read_csv("Dataset/loan_approval_dataset.csv", header=0)

# Remove all the spaces from the column names and rows
df.columns = df.columns.str.strip()
for col in df.columns:
    if df[col].dtype != "float64" and df[col].dtype != "int64":
        df[col] = df[col].str.strip()


# To keep it simple and as the specification dictates,
# I will keep only the following columns
# cibil_score, loan_amount, loan_term, self_employed, loan_status

df = df[["cibil_score", "loan_amount", "loan_term", "self_employed", "loan_status"]]

# Are there any missing values?
print(df.isnull().sum())

# Convert self_employed and loan_status to binary
df["self_employed"] = df["self_employed"].apply(lambda x: 1 if x == "Yes" else 0)
df["loan_status"] = df["loan_status"].apply(lambda x: 1 if x == "Approved" else 0)

# Save the processed data
df.to_csv("Dataset/processed_loan_approval_dataset.csv", index=False)

