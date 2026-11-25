# Memo to Ritu Deshpande — Service-Request Routing

**Decision:** Proceed with a controlled, human-supervised pilot. Do not switch off the existing vendor bot immediately.

## 1. Model Performance

The initial Linear SVM matched historical queue labels with **96.72% accuracy** on a chronological validation set of 2,135 requests from April–June 2026. Its macro-F1 score was **0.965 (96.50%)**.

- Correct predictions: 2,065
- Incorrect predictions: 70
- Validation accuracy: 96.72%

This exceeds the 90% historical-label agreement target for this validation period. However, it is not the hidden test score and does not guarantee that every recommendation is operationally correct.

The model uses TF-IDF text features and request details to predict the initial routing team.

## 2. Financial Impact

The vendor bot licence costs **₹3.2 lakh per year**, approximately ₹26,667 per month.

The local machine-learning model does not use a paid AI API, so it has no external model-inference API charges. Potential gross licence avoidance is up to ₹3.2 lakh annually, before internal hosting, maintenance, monitoring and human-review costs.

The historical resolution log shows:

- Requests with at least one transfer: 2,696
- Total transfers: 3,902
- Transfer handling cost: ₹11,90,110
- Additional customer-contact cost: ₹7,00,960
- **Combined historical estimated cost: ₹18,91,070**

These costs represent historical operational friction. They are not guaranteed savings from the proposed model because the model predicts the historical initial queue label, not the final resolving team.

Finance should approve a monthly operating-cost estimate before any decision to retire the existing bot.

## 3. Monthly Workload Analysis

The model generated predictions for 2,178 requests from July–September 2026.

| Month | Predicted requests |
|---|---:|
| July 2026 | 736 |
| August 2026 | 741 |
| September 2026 | 701 |
| **Total** | **2,178** |

Repairs is consistently the busiest team, receiving **657 requests (30.17%)** across the three months.

This suggests that Repairs should receive priority when reviewing team capacity. Actual staffing requirements should also consider request complexity and handling time.

## 4. Recommended Next Steps

1. Run the model in shadow mode alongside the current process without automatically transferring requests.
2. Have team leads review errors, especially repair-versus-consumable, warranty-versus-repair and requests containing multiple intents.
3. Track first-team acceptance, transfers, repeat contacts, override rates and monthly operating costs for at least two weeks.
4. Review pilot results with Finance and operational team leads.
5. Retire the existing bot only if the pilot demonstrates safe routing and Finance approves the cost benefits.

## 5. Data Limitation

The supplied timestamps cover **1 April 2025 to 30 June 2026**, representing 15 calendar months, although the accompanying email describes eighteen months.

Confirm whether three months of records are missing before making longer-term capacity or savings claims.

## Final Recommendation

The model has achieved 96.72% agreement with historical routing labels, exceeding the stated 90% target in the validation period. It is suitable for further evaluation through a controlled, human-supervised pilot.

A final decision to replace the existing routing bot should depend on actual pilot performance, operational safety and financial approval.