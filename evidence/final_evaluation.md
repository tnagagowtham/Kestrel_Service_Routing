# Kestrel Home Service Routing – Model Evaluation

## 1. Model
Algorithm: Linear Support Vector Classifier (LinearSVC)

## 2. Validation Method
Chronological holdout validation:
- Training records: Before 1 April 2026
- Validation period: 1 April – 30 June 2026
- Validation records: 2,135

## 3. Overall Performance
- Accuracy: 96.72%
- Macro-F1: 0.9650
- Correct predictions: 2,065
- Incorrect predictions: 70

## 4. Team-wise Performance
The model achieved F1-scores between 95.07% and 97.90% across the seven service teams.

- Billing: 97.90%
- Repairs: 97.45%
- Installs & Demo: 96.98%
- Product Advice: 96.61%
- Returns & Replacement: 95.98%
- Filters & Consumables: 95.50%
- Warranty Claims: 95.07%

## 5. Conclusion
The LinearSVC model demonstrated strong performance in predicting historical initial service-team assignments. It is suitable for a controlled pilot with employee review of ambiguous or multi-issue requests.

The validation score measures agreement with historical routing labels, not necessarily the correctness of the final resolved team. Further monitoring is recommended before replacing the existing routing process.