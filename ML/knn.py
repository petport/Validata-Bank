import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load the preprocessed data
df = pd.read_csv("Dataset/processed_loan_approval_dataset.csv")

# The columns are: cibil_score,loan_amount,loan_term,self_employed,loan_status
X = df.drop("loan_status", axis=1)
y = df["loan_status"]

feature_importances_dict = {
    "cibil_score": 0,
    "loan_amount": 0,
    "self_employed": 0,
    "loan_term": 0
}

for i in range(1, 10):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a KNN classifier
    clf = KNeighborsClassifier(n_neighbors=3)
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Evaluate the model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    print("\nKNN Model Performance:")
    print(f"Accuracy: {accuracy}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1 Score: {f1}")

    # Calculate the feature importance
    feature_importances = []

    for col in X.columns:
        # Randomly shuffle the column
        X_test_shuffled = X_test.copy()
        X_test_shuffled[col] = X_test_shuffled[col].sample(frac=1).values

        # Calculate the distance between the shuffled data and the original data
        shuffled_distances = clf.kneighbors(X_test_shuffled, n_neighbors=3, return_distance=True)[0]
        original_distances = clf.kneighbors(X_test, n_neighbors=3, return_distance=True)[0]

        # Calculate the feature importance
        importance = (original_distances - shuffled_distances).mean()
        feature_importances.append(importance)

    # Create a DataFrame to display feature importances
    feature_df = pd.DataFrame({"Feature": X.columns, "Importance": feature_importances})
    feature_df = feature_df.sort_values(by="Importance", ascending=False)

    print("\nFeature Importances:")
    print(feature_df)


    # Save the feature importances in the correct place
    for idx, row in feature_df.iterrows():
        feature_importances_dict[row["Feature"]] += row["Importance"]


# Calculate the average feature importancies
avg_feature_importances = {k: v / 10 for k, v in feature_importances_dict.items()}

print("\nAverage Feature Importances:")
print(avg_feature_importances)