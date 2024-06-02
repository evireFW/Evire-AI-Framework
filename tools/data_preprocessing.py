import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def load_data(file_path):
    """
    Load data from a CSV file.
    :param file_path: Path to the CSV file.
    :return: A pandas DataFrame.
    """
    return pd.read_csv(file_path)

def encode_categorical_data(df, columns):
    """
    Encode categorical features using Label Encoding.
    :param df: Input DataFrame.
    :param columns: List of column names to be encoded.
    :return: DataFrame with encoded categorical features.
    """
    le = LabelEncoder()
    for column in columns:
        df[column] = le.fit_transform(df[column])
    return df

def scale_features(df, columns):
    """
    Scale numerical features using Standard Scaler.
    :param df: Input DataFrame.
    :param columns: List of column names to be scaled.
    :return: DataFrame with scaled numerical features.
    """
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df

def preprocess_transaction_data(df):
    """
    Preprocess transaction data specific to blockchain context.
    :param df: Input DataFrame containing transaction data.
    :return: Preprocessed DataFrame.
    """
    # Example preprocessing steps
    categorical_columns = ['from_address', 'to_address']
    numerical_columns = ['value', 'gas', 'gas_price', 'nonce']

    # Encode categorical data
    df = encode_categorical_data(df, categorical_columns)

    # Scale numerical data
    df = scale_features(df, numerical_columns)

    return df

def preprocess_ai_data(df):
    """
    Preprocess data for AI model training.
    :param df: Input DataFrame containing AI training data.
    :return: Tuple (features, labels)
    """
    # Example: Assuming 'label' is the column we want to predict
    labels = df['label'].values
    features = df.drop(columns=['label']).values

    # Scale features
    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    return features, labels

# Example usage
if __name__ == "__main__":
    # Load data
    transaction_data = load_data('data/raw/transactions.csv')
    ai_data = load_data('data/raw/ai_training_data.csv')

    # Preprocess data
    processed_transaction_data = preprocess_transaction_data(transaction_data)
    features, labels = preprocess_ai_data(ai_data)

    print("Processed Transaction Data:")
    print(processed_transaction_data.head())

    print("\nAI Training Data - Features:")
    print(features[:5])
    print("\nAI Training Data - Labels:")
    print(labels[:5])
