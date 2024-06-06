import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split

# Download historical data for ETH
eth_data = yf.download('ETH-USD', start='2020-01-01', end='2024-06-05')

# Save the data to a CSV file
eth_data.to_csv('eth_data.csv')

# Read the data from the CSV file
data = pd.read_csv('eth_data.csv')

# Select only the "Close" column for prediction
data = data[['Close']]

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# Create datasets for training and testing
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_data_len]
test_data = scaled_data[train_data_len:]

# Create the training data
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 100
X_evire, y_evire = create_dataset(train_data, time_step)

# Split the data into training and validation sets
X_train_evire, X_val_evire, y_train_evire, y_val_evire = train_test_split(X_evire, y_evire, test_size=0.2, random_state=42)

# Reshape for compatibility with LSTM [samples, time steps, features]
X_train_evire = X_train_evire.reshape(X_train_evire.shape[0], X_train_evire.shape[1], 1)
X_val_evire = X_val_evire.reshape(X_val_evire.shape[0], X_val_evire.shape[1], 1)
X_test_evire, y_test_evire = create_dataset(test_data, time_step)
X_test_evire = X_test_evire.reshape(X_test_evire.shape[0], X_test_evire.shape[1], 1)

# Build the LSTM model
model_evire = Sequential()
model_evire.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model_evire.add(LSTM(50, return_sequences=False))
model_evire.add(Dense(25))
model_evire.add(Dense(1))

# Compile the model
model_evire.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model_evire.fit(X_train_evire, y_train_evire, validation_data=(X_val_evire, y_val_evire), batch_size=1, epochs=50)

# Make predictions on the test dataset
predictions_evire = model_evire.predict(X_test_evire)
predictions_evire = scaler.inverse_transform(predictions_evire)

# Calculate the root mean square error
rmse_evire = np.sqrt(np.mean((predictions_evire - y_test_evire.reshape(-1, 1))**2))
print(f'RMSE: {rmse_evire}')

# Prediction for the next 30 days
last_100_days_evire = data[-100:].values
last_100_days_scaled_evire = scaler.transform(last_100_days_evire)

X_input_evire = last_100_days_scaled_evire.reshape(1, -1)
X_input_evire = X_input_evire.reshape((1, 100, 1))

future_predictions_evire = []
for i in range(30):
    pred_evire = model_evire.predict(X_input_evire, verbose=0)
    future_predictions_evire.append(pred_evire[0, 0])
    # Prepare X_input_evire for the next prediction
    X_input_evire = np.append(X_input_evire[:, 1:, :], np.reshape(pred_evire, (1, 1, 1)), axis=1)

# Reverse the predictions
future_predictions_evire = scaler.inverse_transform(np.array(future_predictions_evire).reshape(-1, 1))

# Print the predictions
print("EVIRE ETH Price Predictions No Sentiment")
last_date = pd.to_datetime(data.index[-1])
prediction_dates = [last_date + pd.DateOffset(days=i) for i in range(1, 31)]
for date, price in zip(prediction_dates, future_predictions_evire):
    print(f"{date.date()}: {price[0]}")