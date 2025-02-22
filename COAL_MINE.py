import serial
import time
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Configure the serial port (adjust the port name for your system)
# For Windows, e.g., 'COM3'; for Linux/Mac, it might be '/dev/ttyACM0' or '/dev/ttyUSB0'
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # Allow time for the serial connection to initialize

# Generate synthetic training data
n_samples = 200
np.random.seed(42)
# Simulated analog sensor readings (range: 0-1023)
flame = np.random.randint(0, 1024, n_samples)
smoke = np.random.randint(0, 1024, n_samples)
humidity = np.random.randint(0, 1024, n_samples)

# Define a hazard condition: for example, hazard=1 if flame > 600 and smoke > 600, or humidity < 300
hazard = (((flame > 600) & (smoke > 600)) | (humidity < 300)).astype(int)

data = pd.DataFrame({
    'flame': flame,
    'smoke': smoke,
    'humidity': humidity,
    'hazard': hazard
})

X = data[['flame', 'smoke', 'humidity']]
y = data['hazard']

# Train logistic regression model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate model accuracy
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print("Model Test Accuracy: {:.2f}%".format(accuracy * 100))
print("Training complete. Now reading sensor data...")

def predict_hazard(sensor_values):
    # sensor_values should be a list: [flame, smoke, humidity]
    X_new = np.array(sensor_values).reshape(1, -1)
    return model.predict(X_new)[0]

try:
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line and not line.startswith("flame"):
            # Expected line format: flame,smoke,humidity
            parts = line.split(',')
            if len(parts) == 3:
                sensor_values = list(map(int, parts))
                hazard_prediction = predict_hazard(sensor_values)
                print("Sensor values:", sensor_values, "Predicted Hazard:", hazard_prediction)
except KeyboardInterrupt:
    print("Stopping data reading...")

ser.close()
