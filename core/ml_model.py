import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

MODEL_PATH = "models/crop_model.pkl"

def train_or_load_model():

    df = pd.read_csv("data/crop_data.csv")

    X = df.drop("label", axis=1)
    y = df["label"]

    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    if not os.path.exists(MODEL_PATH):

        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42
        )

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Save accuracy
        y_pred = model.predict(X_test)
        accuracy = model.score(X, y_encoded)

        joblib.dump((model, le, accuracy), MODEL_PATH)

    else:
        model, le, accuracy = joblib.load(MODEL_PATH)

    return model, le, accuracy


def predict_crop(input_data):
    model, le, accuracy = train_or_load_model()

    prediction = model.predict([input_data])
    probs = model.predict_proba([input_data])

    confidence = max(probs[0]) * 100
    crop = le.inverse_transform(prediction)[0]

    return crop, confidence, accuracy