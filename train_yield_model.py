import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv("data/crop_data.csv")

# Features & Target
X = data.drop("yield", axis=1)
y = data["yield"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestRegressor()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "yield_model.pkl")

print("Yield Model trained & saved ✅")