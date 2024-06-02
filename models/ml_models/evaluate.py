import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
import tensorflow as tf
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import seaborn as sns

# Load the saved model
model_path = 'saved_models/dev_model.h5'
model = load_model(model_path)

# Load the test data
# Assume test_data.npy and test_labels.npy are NumPy arrays saved earlier
test_data = np.load('data/raw/test_data.npy')
test_labels = np.load('data/raw/test_labels.npy')

# Make predictions
predictions = model.predict(test_data)
predicted_labels = (predictions > 0.5).astype(int).flatten()

# Calculate evaluation metrics
accuracy = accuracy_score(test_labels, predicted_labels)
precision = precision_score(test_labels, predicted_labels)
recall = recall_score(test_labels, predicted_labels)
f1 = f1_score(test_labels, predicted_labels)
roc_auc = roc_auc_score(test_labels, predictions)

# Print evaluation metrics
print(f'Accuracy: {accuracy:.4f}')
print(f'Precision: {precision:.4f}')
print(f'Recall: {recall:.4f}')
print(f'F1 Score: {f1:.4f}')
print(f'ROC AUC: {roc_auc:.4f}')

# Plot confusion matrix
cm = confusion_matrix(test_labels, predicted_labels)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.show()

# Save evaluation results
with open('evaluation_results.txt', 'w') as f:
    f.write(f'Accuracy: {accuracy:.4f}\n')
    f.write(f'Precision: {precision:.4f}\n')
    f.write(f'Recall: {recall:.4f}\n')
    f.write(f'F1 Score: {f1:.4f}\n')
    f.write(f'ROC AUC: {roc_auc:.4f}\n')

print('Evaluation results saved to evaluation_results.txt')
