import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

# Load the saved model
model_path = 'saved_models/dev_model.h5'
model = load_model(model_path)

# Load the saved scaler
scaler_path = 'saved_models/scaler.npy'
scaler = StandardScaler()
scaler.mean_, scaler.scale_ = np.load(scaler_path)

# Function to make predictions
def predict(new_data):
    # Preprocess the new data
    new_data = scaler.transform(new_data)
    
    # Make predictions
    predictions = model.predict(new_data)
    return predictions

# Example usage
if __name__ == "__main__":
    # Load new data to predict (assuming it's stored in a NumPy array)
    new_data = np.load('data/processed/new_data.npy')
    
    # Make predictions
    predictions = predict(new_data)
    
    # Output predictions
    print("Predictions:", predictions)
