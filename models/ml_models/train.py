import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from sklearn.preprocessing import StandardScaler
import os

# Load the training data
# Assume train_data.npy and train_labels.npy are NumPy arrays saved earlier
train_data = np.load('data/raw/train_data.npy')
train_labels = np.load('data/raw/train_labels.npy')

# Preprocess the data
scaler = StandardScaler()
train_data = scaler.fit_transform(train_data)

# Define the model
model = Sequential([
    Dense(64, input_dim=train_data.shape[1], activation='relu'),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Define callbacks
checkpoint = ModelCheckpoint('saved_models/dev_model.h5', monitor='val_loss', save_best_only=True, mode='min')
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

# Train the model
history = model.fit(
    train_data, train_labels,
    validation_split=0.2,
    epochs=100,
    batch_size=32,
    callbacks=[checkpoint, early_stopping]
)

# Save the scaler for future use
if not os.path.exists('saved_models'):
    os.makedirs('saved_models')
np.save('saved_models/scaler.npy', scaler)

# Save the training history
history_path = 'training_history.npy'
np.save(history_path, history.history)

print('Model training completed and saved to saved_models/dev_model.h5')
print('Scaler saved to saved_models/scaler.npy')
print(f'Training history saved to {history_path}')
