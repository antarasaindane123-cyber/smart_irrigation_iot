import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from xgboost import XGBClassifier


def evaluate_models():
  if not pd.io.common.file_exists("irrigation_data.csv"):
    print("[-] Please run sensor_simulator.py first!")
    return

  df = pd.read_csv("irrigation_data.csv")
  df["target"] = (df["fault"] != "none").astype(int)
  df_encoded = pd.get_dummies(df, columns=["crop"])

  features = [
      "soil_moisture",
      "temperature",
      "humidity",
  ] + [c for c in df_encoded.columns if "crop_" in c]
  X = df_encoded[features]
  y = df_encoded["target"]

  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.25, random_state=42, stratify=y
  )

  # Train Random Forest
  rf = RandomForestClassifier(n_estimators=100, random_state=42)
  rf.fit(X_train, y_train)
  print(f"[+] Random Forest Accuracy: {accuracy_score(y_test, rf.predict(X_test)):.3f}")


if __name__ == "__main__":
  evaluate_models()