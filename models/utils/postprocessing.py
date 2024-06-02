import numpy as np
import json

def interpret_predictions(predictions, threshold=0.5):
    """
    Interpret the raw predictions of the model.
    
    :param predictions: A numpy array of raw predictions (probabilities).
    :param threshold: Threshold for converting probabilities to binary labels.
    :return: A list of interpreted labels (e.g., 0 or 1).
    """
    return (predictions > threshold).astype(int).flatten()

def save_predictions(predictions, output_file='predictions.json'):
    """
    Save the predictions to a JSON file.
    
    :param predictions: A list or numpy array of predictions.
    :param output_file: Path to the output file.
    """
    with open(output_file, 'w') as f:
        json.dump(predictions.tolist(), f)
    print(f'Predictions saved to {output_file}')

def generate_summary(predictions):
    """
    Generate a summary of the predictions.
    
    :param predictions: A list or numpy array of predictions.
    :return: A dictionary containing the summary.
    """
    total = len(predictions)
    positive = np.sum(predictions)
    negative = total - positive
    summary = {
        'total': total,
        'positive': positive,
        'negative': negative,
        'positive_percentage': positive / total * 100,
        'negative_percentage': negative / total * 100
    }
    return summary

def print_summary(summary):
    """
    Print the summary of the predictions.
    
    :param summary: A dictionary containing the summary.
    """
    print("Summary of Predictions:")
    print(f"Total: {summary['total']}")
    print(f"Positive: {summary['positive']} ({summary['positive_percentage']:.2f}%)")
    print(f"Negative: {summary['negative']} ({summary['negative_percentage']:.2f}%)")

# Example usage
if __name__ == "__main__":
    # Load predictions (assuming they are stored in a numpy array)
    predictions = np.load('data/predictions.npy')
    
    # Interpret predictions
    interpreted_predictions = interpret_predictions(predictions)
    
    # Save interpreted predictions
    save_predictions(interpreted_predictions)
    
    # Generate and print summary
    summary = generate_summary(interpreted_predictions)
    print_summary(summary)
