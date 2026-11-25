# Kestrel Variant B — Submission Form

## 1. What did you build, and what business outcome does it move? State the number and the money.

I built a local, no-paid-API service-request routing prototype using a Linear Support Vector Machine (Linear SVM) to predict the historical `team_label` routing queue.

The project includes:
- A reproducible model training and evaluation script.
- A Flask JSON prediction API.
- A browser-based interface for submitting service requests.
- A prediction file for 2,178 recent requests.

The model achieved **96.72% validation accuracy** on 2,135 chronologically later requests.

The existing vendor bot licence costs **₹3.2 lakh per year**, approximately ₹26,667 per month. This is the gross licence cost potentially avoided, not guaranteed net savings. Internal hosting, maintenance, monitoring and human-review costs require Finance approval.

## 2. What score do you expect predictions.csv to get on the hidden outcomes, on which metric, and why that metric? Say how you estimated it.

My expected accuracy is approximately **96.7%**, with a macro-F1 score of approximately **0.965** as a secondary metric.

Accuracy is the primary metric because the assignment asks for at least 90% agreement with historical routing labels.

I estimated this using chronological validation:
- Training data: records before 1 April 2026.
- Validation data: 2,135 requests from April–June 2026.
- Validation accuracy: 96.72%.
- Macro-F1: 96.50%.

This is an estimate based on one validation period, not a guaranteed hidden-test result. Actual hidden outcomes may differ.

## 3. How do you know it works? Sample size, how you checked, error rate, and the kind of case it gets wrong.

The model was evaluated on 2,135 chronologically later CRM requests.

Results:
- Correct predictions: 2,065.
- Incorrect predictions: 70.
- Accuracy: 96.72%.
- Error rate: 3.28%.
- Macro-F1: 0.965.

The confusion matrix and classification report were used to examine errors. Ambiguous requests can be difficult to classify, especially repair-versus-consumable, warranty-versus-repair, and requests containing multiple issues.

I also manually tested six representative requests through the application. Five were routed to the expected team. One leaking-water-purifier request was incorrectly routed to Filters & Consumables instead of Repairs. This small manual sample is not a substitute for statistical validation.

The Flask application was run locally. The interface and prediction endpoint should receive a final smoke test before demonstration, including checking that the displayed request details match the submitted form values.

## 4. Did you change, narrow, or push back on the client's ask? What, when, and why?

I narrowed the immediate decision from switching off the existing bot to conducting a supervised shadow-mode pilot.

Although the model exceeds the 90% historical-label agreement target in the validation period, reproducing the bot's initial queue is not the same as reducing transfers or identifying the final resolving team.

The resolution log shows:
- 2,696 requests with at least one transfer.
- 3,902 total transfers.

The supplied timestamps span 15 calendar months (1 April 2025–30 June 2026), rather than the eighteen months mentioned in the email. These points need operational confirmation before making a retirement decision.

## 5. What is wrong with what you are handing us? Be specific: bugs, shortcuts, things you know are off.

The project has the following limitations:

- The validation estimate is based on one chronological split and may not represent future data or seasonal changes.
- The classifier learns historical bot labels, including historical routing mistakes.
- Explanation terms represent model signals, not causal explanations.
- The prototype is not a production deployment.
- It has no CRM integration, authentication, audit trail, role permissions, production monitoring or automated retraining.
- New or unexpected product metadata categories require further testing.
- Ambiguous and multi-issue requests may still be misclassified.

A security and operational review is required before production use.

## 6. What did you deliberately leave out, and why that rather than something else?

I did not use a paid LLM or external AI API because a local supervised text-classification model is sufficient for this labelled routing task and avoids per-request model API charges.

I also left out production CRM integration and automatic queue write-back. The project can be demonstrated through a local API and browser interface, while a human-supervised pilot provides a safer way to evaluate its recommendations.

Customer and operational data are excluded from the public repository in accordance with the supplied data-handling policy.

## 7. Anything you built or found that nobody asked for?

I analysed historical routing transfers and estimated the associated operational friction using the policy rates:

- 3,902 transfers × ₹305 = ₹11,90,110.
- 2,696 transfer-affected requests × ₹260 = ₹7,00,960.
- Combined historical estimated cost = **₹18,91,070**.

This is historical cost, not claimed savings.

I also identified the mismatch between the email's eighteen-month description and the 15-month timestamp range in the supplied export.

## 8. What did you use AI for? Which tools and models, where they helped, where they wasted your time, what you threw away. Link your three-minute screen recording here.

I used ChatGPT (GPT-6) as a coding and analysis assistant to plan the workflow, draft and troubleshoot Python and Flask code, interpret model evaluation results, and prepare project documentation.

The implementation uses:
- Python for programming.
- Pandas for data processing.
- Scikit-learn for TF-IDF feature extraction and Linear SVM classification.
- Flask for the local prediction API.
- HTML, CSS and JavaScript for the browser interface.

The deployed prototype does not call ChatGPT, an LLM or any paid AI API. The final approach uses a local TF-IDF and LinearSVC model.

The assistance was most useful for project scaffolding, debugging and interpreting validation errors. Experimental alternatives, including a rule-based correction approach that reduced validation performance, were not retained.

Model API cost: **₹0**. Local development, hosting and maintenance costs are not included.

**Three-minute screen recording:** https://drive.google.com/file/d/1D8A4lO6DHP6y5DVRuBigYSitgH_yo1ac/view?usp=sharing

## 9. Your Public Google Drive Link

https://drive.google.com/drive/folders/1KLOU8ZciVjPoha1x5eVKI0lxy9XI6Cga?usp=sharing

Use this link for the screen recording or other approved submission materials. Do not share restricted customer or operational data publicly.

## 10. Someone picks this up on Monday and you are unreachable. The three things they need to know.

1. Keep the original Kestrel data private. Do not publish the `data/` folder, trained model or restricted prediction records.
2. In the configured local project environment, run `python train_model.py` and then `python app.py`. The browser interface is available at `http://127.0.0.1:5000`; the prediction endpoint is `POST /api/predict`.
3. Do not enable unattended routing until the shadow pilot, error review and Finance run-cost approval are complete.

## 11. Honest hours spent

18 - 22

## 12. GitHub Repository Link

https://github.com/tnagagowtham/Kestrel_Service_Routing