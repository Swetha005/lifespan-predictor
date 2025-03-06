import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv(r"C:\Users\sweth\Desktop\Lifespan Prediction\Sleep_health_and_lifestyle_dataset.csv")

# Handle missing values
df.fillna(df.mode().iloc[0], inplace=True)  # Fill missing categorical values with mode
df.fillna(df.median(numeric_only=True), inplace=True)  # Fill missing numerical values with median

# Define categorical columns
categorical_columns = ['Gender', 'Occupation', 'BMI Category', 'Blood Pressure', 'Sleep Disorder']

# Create LabelEncoders for categorical columns
encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df[col] = df[col].astype(str)  # Ensure all values are string before encoding
    df[col] = le.fit_transform(df[col])  # Fit & transform data
    encoders[col] = le  # Store encoder for later use

# Ensure all categories are recognized before encoding
if 'Yes' not in encoders['Sleep Disorder'].classes_:
    encoders['Sleep Disorder'].classes_ = np.append(encoders['Sleep Disorder'].classes_, 'Yes')
if 'No' not in encoders['Sleep Disorder'].classes_:
    encoders['Sleep Disorder'].classes_ = np.append(encoders['Sleep Disorder'].classes_, 'No')

# Save all encoders
joblib.dump(encoders, "label_encoders.pkl")

# Generate Synthetic Lifespan Data
def generate_lifespan(row):
    base_lifespan = np.random.randint(60, 90)
    
    # Adjust lifespan based on features
    if row['Quality of Sleep'] >= 7 and row['Physical Activity Level'] >= 7:
        base_lifespan += np.random.randint(3, 8)
    if row['Stress Level'] >= 7:
        base_lifespan -= np.random.randint(3, 6)

    # Ensure valid categorical encoding before checking conditions
    if row['BMI Category'] in encoders['BMI Category'].transform(['Overweight', 'Obese']).tolist():
        base_lifespan -= np.random.randint(5, 10)
    if row['Sleep Disorder'] == encoders['Sleep Disorder'].transform(['Yes'])[0]:
        base_lifespan -= np.random.randint(2, 5)

    return max(base_lifespan, 50)

# Apply the function to generate lifespan data
df['Lifespan'] = df.apply(generate_lifespan, axis=1)

# Define features (X) and target (y)
X = df.drop(columns=['Lifespan'])
y = df['Lifespan']

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale numerical features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# Save model and scaler
joblib.dump(model, "lifespan_model.pkl")
joblib.dump(scaler, "scaler.pkl")

print("✅ Model training complete! Model, Scaler, and Encoders saved successfully.")
