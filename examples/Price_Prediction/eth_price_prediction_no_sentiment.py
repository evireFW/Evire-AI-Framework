import yfinance as yf
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.model_selection import train_test_split


# Download historical data for ETH
eth_data = yf.download('ETH-USD', start='2020-01-01', end='2024-05-25')

# We save the data to a file CSV
eth_data.to_csv('eth_data.csv')

# We read the data from the file CSV
data = pd.read_csv('eth_data.csv')

# We select only the "Close" column for prediction
data = data[['Close']]

# Normalize the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data)

# We create datasets for training and testing
train_data_len = int(len(scaled_data) * 0.8)
train_data = scaled_data[:train_data_len]
test_data = scaled_data[train_data_len:]

# We create the training data
def create_dataset(data, time_step=1):
    X, Y = [], []
    for i in range(len(data) - time_step):
        X.append(data[i:(i + time_step), 0])
        Y.append(data[i + time_step, 0])
    return np.array(X), np.array(Y)

time_step = 100
X, y = create_dataset(train_data, time_step)

# We split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Reshape for compatibility with LSTM [samples, time steps, features]
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_val = X_val.reshape(X_val.shape[0], X_val.shape[1], 1)
X_test, y_test = create_dataset(test_data, time_step)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

# We build the LSTM model
model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(time_step, 1)))
model.add(LSTM(50, return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# We train the model
model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=1, epochs=50)

# We make predictions on the test data set
predictions = model.predict(X_test)
predictions = scaler.inverse_transform(predictions)

# We calculate the root mean square error
rmse = np.sqrt(np.mean((predictions - y_test.reshape(-1, 1))**2))
print(f'RMSE: {rmse}')

# Prediction for the next 30 days
last_100_days = data[-100:].values
last_100_days_scaled = scaler.transform(last_100_days)

X_input = last_100_days_scaled.reshape(1, -1)
X_input = X_input.reshape((1, 100, 1))

future_predictions = []
for i in range(30):
    pred = model.predict(X_input, verbose=0)
    future_predictions.append(pred[0, 0])
    # Prepare X_input for the next prediction
    X_input = np.append(X_input[:, 1:, :], np.reshape(pred, (1, 1, 1)), axis=1)

# We reverse the predictions
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))
print(future_predictions)