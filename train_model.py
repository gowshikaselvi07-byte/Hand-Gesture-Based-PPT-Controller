import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report


# Load dataset
data = pd.read_csv("landmarks.csv")

X = data.drop("label", axis=1)
y = data["label"]


# Normalize landmarks relative to wrist
def normalize_landmarks(row):
    values = row.values.astype(float)

    # 63 values = 21 landmarks × 3
    landmarks = values.reshape(21, 3)

    # Wrist = landmark 0
    wrist = landmarks[0].copy()

    # Make every landmark relative to wrist
    landmarks = landmarks - wrist

    return landmarks.flatten()


# Apply normalization
X_normalized = X.apply(normalize_landmarks, axis=1)

X_normalized = pd.DataFrame(
    X_normalized.tolist(),
    columns=X.columns
)


# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X_normalized,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Scaling
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


# SVM model
model = SVC(
    kernel="rbf",
    C=10,
    gamma="scale"
)

model.fit(X_train, y_train)


# Test
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy)
print("\nClassification Report:")
print(classification_report(y_test, y_pred))


# Save
joblib.dump(model, "gesture_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("\nModel saved successfully!")
print("Scaler saved successfully!")