import importlib
import subprocess
import platform
import sys
import os
from colorama import Fore
import time

# Initialize normalization flag
norm = False

def auto_lib_downloader(libs):
    osnames = platform.system()
    python_executable = sys.executable

    for lib in libs:
        try:
            importlib.import_module(lib)
            print(Fore.GREEN + f"[+] Library '{lib}' has been imported successfully.")
        except ImportError:
            print(Fore.YELLOW + f"[-] Library '{lib}' is not installed.")
            print(Fore.CYAN + f"[/] Downloading library '{lib}'...")

            result = subprocess.run(
                [python_executable, "-m", "pip", "install", lib],
                capture_output=True, text=True
            )

            if result.returncode == 0:
                print(Fore.GREEN + f"[++] Library '{lib}' has been successfully installed and imported.")
            else:
                print(Fore.RED + f"[!!] Failed to install '{lib}'. Error:\n{result.stderr}")

    print(Fore.GREEN + "[++] All libraries have been processed.")

def clear():
    osnames = platform.system()
    subprocess.run(['cls' if osnames == "Windows" else 'clear'], shell=True)

def Import_Lib():
    global socket, threading, colorama

# Download necessary libraries if not already installed
auto_lib_downloader(['colorama', 'pandas', 'scikit-learn', 'matplotlib'])

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt

time.sleep(1)

clear()

# Function to initialize libraries or any other setup if needed
Import_Lib()

# Ask user if they want to normalize data
normalize_data = input(Fore.CYAN + "Do you want to normalize data? (yes/no): ").strip().lower()

# Ask for paths to preprocessing scripts or use defaults if empty
preprocessing_script = input(Fore.CYAN + "Enter the path to the normalization script (default: same directory as this script): ").strip()
if not preprocessing_script:
    preprocessing_script = "I:\\IOT\\HW2\\For Me\\Merge_files.py"  # Default to current directory

non_norm_script = input(Fore.CYAN + "Enter the path to the non-normalization script (default: same directory as this script): ").strip()
if not non_norm_script:
    non_norm_script = "I:\\IOT\\HW2\\For Me\\Merge_files(not normall).py"  # Default to current directory

# Run preprocessing scripts based on user's choice
if normalize_data == "yes":
    subprocess.run(["python", preprocessing_script])  # Run normalization preprocessing script
    norm = True
    print(Fore.GREEN + "Data normalization completed!")
else:
    subprocess.run(["python", non_norm_script])  # Run without normalization preprocessing script
    norm = False
    print(Fore.RED + "Data merged without normalization!")

# Add a delay to ensure preprocessing is completed
# time.sleep(15)  # Wait for 15 seconds before starting the main program

# After preprocessing, continue with the main data processing
# Load the combined Excel file based on the normalization flag
data_file = "I:\\IOT\\HW2\\For Me\\Data\\combined_output_with_power_Normall.xlsx" if norm else "I:\\IOT\\HW2\\For Me\\Data\\combined_output_with_power.xlsx"
data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_file)

# Check if the file exists before loading
if os.path.exists(data_path):
    data = pd.read_excel(data_path)
else:
    print(Fore.RED + f"Error: The file '{data_file}' does not exist at the specified path!")
    sys.exit(1)  # Exit or handle error gracefully

# Load data
data = pd.read_excel(data_path)

# Data preprocessing
# Select the relevant columns
data = data[["Temperature", "Humidity", "Power Consumption (kw)"]]

# Separate features (X) and target variable (y)
X = data[["Temperature", "Humidity"]]
y = data["Power Consumption (kw)"]

# Split the data into training and testing sets (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models to evaluate
models = {
    "Linear Regression": LinearRegression(),
    "Decision Tree": DecisionTreeRegressor(),
    "Neural Network": MLPRegressor(hidden_layer_sizes=(50, 50), max_iter=1000, random_state=42)
}

# Dictionary to store results
results = {}

# Train each model and evaluate
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    # Store evaluation results
    results[name] = {
        "MAE": mae,
        "MSE": mse,
        "R^2 Score": r2,
        "Predictions": y_pred
    }

# Display results and plot graphs
for name, metrics in results.items():
    print(Fore.YELLOW + f"\n{name} Results:")
    print(Fore.GREEN + f"Mean Absolute Error (MAE): {metrics['MAE']}")
    print(Fore.GREEN + f"Mean Squared Error (MSE): {metrics['MSE']}")
    print(Fore.GREEN + f"R^2 Score: {metrics['R^2 Score']}")
    
    # Plot actual vs predicted data
    plt.figure(figsize=(10, 5))
    plt.plot(y_test.values, label="Actual", color="blue")
    plt.plot(metrics["Predictions"], label="Predicted", color="red")
    plt.title(f"{name} - Actual vs Predicted Power Consumption")
    plt.xlabel("Sample")
    plt.ylabel("Power Consumption (kw)")
    plt.legend()
    plt.grid(True)
    plt.show()

print(Fore.CYAN + "\n[++] All processes completed successfully!")
input("Done\nEnter To Exit")