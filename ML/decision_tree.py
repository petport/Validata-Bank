import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import cross_val_score

# Load the preprocessed data
df = pd.read_csv("Dataset/processed_loan_approval_dataset.csv")

# The columns are: cibil_score,loan_amount,loan_term,self_employed,loan_status
X = df.drop("loan_status", axis=1)
y = df["loan_status"]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a decision tree classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Test for model overfitting
train_accuracy = clf.score(X_train, y_train)
test_accuracy = clf.score(X_test, y_test)

print(f"\nTrain Accuracy: {train_accuracy}")
print(f"Test Accuracy: {test_accuracy}")

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# k-fold cross-validation

scores = cross_val_score(clf, X, y, cv=5)
print("\nCross-validation scores:", scores)
print("Mean cross-validation score:", scores.mean())


print("\nDecision Tree Model Performance:")
print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"F1 Score: {f1}")

# Get feature importances
feature_importances = clf.feature_importances_
feature_names = X.columns

# Create a DataFrame to display feature importances
feature_df = pd.DataFrame({"Feature": feature_names, "Importance": feature_importances})
feature_df = feature_df.sort_values(by="Importance", ascending=False)

print("\nFeature Importances:")
print(feature_df)

