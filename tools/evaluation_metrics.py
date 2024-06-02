from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_metrics(y_true, y_pred):
    """
    Calculate evaluation metrics for binary classification.
    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :return: Dictionary containing evaluation metrics.
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred),
        'recall': recall_score(y_true, y_pred),
        'f1_score': f1_score(y_true, y_pred),
        'roc_auc': roc_auc_score(y_true, y_pred)
    }
    return metrics

def plot_confusion_matrix(y_true, y_pred, labels=None):
    """
    Plot confusion matrix for binary classification.
    :param y_true: True labels.
    :param y_pred: Predicted labels.
    :param labels: List of label names (optional).
    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.show()

def evaluate_model(y_true, y_pred):
    """
    Evaluate the model and print metrics.
    :param y_true: True labels.
    :param y_pred: Predicted labels.
    """
    metrics = calculate_metrics(y_true, y_pred)
    for metric, value in metrics.items():
        print(f'{metric}: {value:.4f}')

    plot_confusion_matrix(y_true, y_pred)

# Example usage
if __name__ == "__main__":
    # Example true and predicted labels
    y_true = [0, 1, 1, 0, 1, 0, 1, 1, 0, 0]
    y_pred = [0, 1, 1, 0, 0, 0, 1, 1, 1, 0]

    # Evaluate model
    evaluate_model(y_true, y_pred)
