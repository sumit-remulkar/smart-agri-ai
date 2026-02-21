import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load dataset
data = pd.read_csv("data/crop_data.csv")

# Encode categorical data
encoder = LabelEncoder()
for column in data.columns:
    data[column] = encoder.fit_transform(data[column])

# Split data
X = data.drop("suitability", axis=1)
y = data["suitability"]

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Prediction function
def predict_suitability(soil, rainfall, temp, crop):
    test_data = pd.DataFrame([[soil, rainfall, temp, crop]],
        columns=["soil", "rainfall", "temp", "crop"])

    for column in test_data.columns:
        test_data[column] = encoder.fit_transform(test_data[column])

    prediction = model.predict(test_data)
    return suitability_map[prediction[0]]

# Suitability label mapping
suitability_map = {
    0: "High",
    1: "Low",
    2: "Medium"
}