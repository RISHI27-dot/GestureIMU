# Importing necessary libraries
import pandas as pd
from sklearn import svm
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# Function to read and preprocess accelerometer data from CSV files
def preprocess_data(file_paths):
    data = [pd.read_csv(file, header='infer') for file in file_paths]
    reutrn data

# Function to train SVM model
def train_model(X_train, y_train):
    clf = svm.SVC(kernel='linear')  # Using linear kernel for SVM
    clf.fit(X_train, y_train)
    return clf

# Function to save trained model to file
def save_model(model, file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(model, f)

# Function to load trained model from file
def load_model(file_path):
    with open(file_path, 'rb') as f:
        model = pickle.load(f)
    return model

# Function to identify digit from accelerometer data using trained model
def identify_digit(model, scaler, accelerometer_data):
    # Preprocess accelerometer data
    processed_data = scaler.transform(accelerometer_data)
    # Predict digit using trained model
    digit = model.predict(processed_data)
    return digit

def main(csv_path):
    # Dictionary containing file paths for each digit
    digit_files = {
        '0': [f"{csv_path}/0_{i}.csv" for i in range(50)],
        '2': [f"{csv_path}/2_{i}.csv" for i in range(50)],
        '9': [f"{csv_path}/9_{i}.csv" for i in range(50)]
    }

    # Read and preprocess data for each digit
    data = []
    for digit, files in digit_files.items():
        data = preprocess_data(files)
    
    # Concatenate data for all digits
    X = pd.concat(data.values())
    y = [int(digit) for digit in data.keys() for _ in range(len(data[digit]))]  # Assign label for each digit
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train SVM model
    model = train_model(X_train, y_train)
    
    # Save trained model and scalers to file
    save_model(model, 'svm_model.pkl')
    for digit, scaler in scalers.items():
        save_model(scaler, f'scaler_{digit}.pkl')
    print("Model trained and saved successfully.")

# Entry point of the program
if __name__ == "__main__":
    csv_path = "csv"  # Replace with the path to your CSV files directory
    main(csv_path)

