# Domain 1 Flashcards: Fundamentals of AI and ML

**Flashcard deck** · fast track: [`docs/domain-1-fast-track/README.md`](README.md) · ultra fast track: [`docs/domain-1-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · **Last verified:** 2026-09-05

A companion active-recall / spaced-repetition deck, not a new source of
material — every card below is a front/back reformat of a fact already
verified in the [Ultra Fast Track](ULTRA-FAST-LEARN.md) cram sheet. Cards
are ordered to match that file's own section order, so studying the deck
top to bottom reinforces the domain's structure. One question or term per
card, one-to-two-line answer, no re-explaining.

For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) directly — it's the same 86 cards, same
order, tab-separated with no header row.

## 1. The 8-stage ML development lifecycle

| Front | Back |
|---|---|
| What are the 8 stages of the ML development lifecycle, in order? | Business goal identification → data collection → EDA → data preparation/feature engineering → model training → hyperparameter tuning/evaluation → deployment → monitoring. |
| A failed hyperparameter tuning/evaluation gate (step 6) loops back to which step? | Step 4 — data preparation / feature engineering. |
| Drift or degraded accuracy detected in monitoring (step 8) loops back to which steps? | Step 2 (data collection) or step 5 (model training). |
| What problem does SageMaker Feature Store solve? | Training/serving skew — it's a centralized, versioned feature repository. |
| What rules out SageMaker Autopilot in favor of manual SageMaker training? | A custom loss function, domain-specific feature engineering, or a novel architecture in the scenario. |
| How much cheaper is Managed Spot Training than On-Demand? | Up to ~90% cheaper (uses spare EC2 capacity). |
| How much interruption notice does Managed Spot Training give before reclaiming capacity? | A 2-minute interruption notice. |
| What happens if a Spot training job is interrupted without checkpointing? | It restarts from 0% — periodic checkpointing to S3 (`checkpoint_s3_uri`) is required to resume. |
| Routine retraining with no fixed deadline vs. a drift-triggered emergency retrain under a strict compliance SLA — Spot or On-Demand? | Routine/no deadline → Managed Spot Training; compliance-SLA emergency retrain → On-Demand. |
| Canary vs. blue/green deployment — what's the difference in intent? | Canary gradually increases traffic to a new version; blue/green cuts all traffic over at once to a separate fleet with instant rollback. |
| A/B testing vs. shadow deployment — what's the difference in intent? | A/B testing deliberately compares two+ live versions' real-world performance; shadow deployment validates a new version with zero user-facing risk. |
| What does SageMaker Model Registry do? | Catalogs trained model versions, stores their evaluation metrics/lineage, and lets a reviewer approve/reject a version before deployment. |
| SageMaker Model Registry vs. Model Monitor vs. Model Cards — what's the difference? | Registry = version catalog + approval gate; Model Monitor = watches a deployed model for drift; Model Cards = documents intended use/limitations. |

## 2. The three learning types

| Front | Back |
|---|---|
| Scenario: no labels, an agent takes actions in an environment for a reward — which learning type? | Reinforcement learning. |
| Scenario: no labels, the model finds structure on its own — which learning type? | Unsupervised learning. |
| Scenario: mostly unlabeled data plus a small labeled subset — which learning type? | Semi-supervised learning. |
| Scenario: a fully labeled target column — which learning type? | Supervised learning. |

## 3. AWS AI/ML services — compact decision table

| Front | Back |
|---|---|
| Scenario: images/video — objects, faces, moderation. | Amazon Rekognition. |
| Scenario: convert speech/audio to text, diarization. | Amazon Transcribe. |
| Scenario: analyze text for sentiment, entities, key phrases, PII. | Amazon Comprehend. |
| Scenario: convert text to lifelike speech. | Amazon Polly. |
| Scenario: translate between languages. | Amazon Translate. |
| Scenario: build a chatbot or voice bot. | Amazon Lex. |
| Scenario: personalized product/content recommendations. | Amazon Personalize. |
| Scenario: forecast demand, inventory, or other time-series values. | Amazon Forecast. |
| Scenario: extract text, forms, and tables from scanned documents. | Amazon Textract. |
| Scenario: real-time fraud-risk scoring. | Amazon Fraud Detector. |
| Scenario: human-in-the-loop labeling to produce training data. | Amazon SageMaker Ground Truth. |
| Scenario: no ML expertise, needs a custom model/algorithm not covered by a purpose-built service. | Amazon SageMaker. |
| Golden rule for choosing between SageMaker and a purpose-built AI service? | A matching purpose-built managed AI service beats SageMaker; SageMaker wins only when a custom model/algorithm or full control is needed. |
| Large pool of real, unlabeled data, minimize labeling cost/time — which labeling approach? | SageMaker Ground Truth (managed human-in-the-loop labeling + active learning). |
| Small dataset (tens–hundreds of records), quick PoC — which labeling approach? | Manual labeling. |
| Data is already labeled but needs prep/feature engineering — which tool? | SageMaker Data Wrangler. |
| Tight labeling budget, iterative train → query → label → retrain loop — which approach? | Active learning (standalone). |
| Labels needed fast/cheap at scale, experts can express rules — which approach? | Weak supervision. |
| Real data is scarce/sensitive/expensive, or a rare class/edge case — which approach? | Synthetic data generation. |

## 4. Classification evaluation metrics

| Front | Back |
|---|---|
| Accuracy — formula and best use case? | (TP+TN)/(TP+TN+FP+FN); use when classes are roughly balanced. |
| Precision — formula and best use case? | TP/(TP+FP); use when false positives are costly. |
| Recall (Sensitivity) — formula and best use case? | TP/(TP+FN); use when false negatives are costly. |
| F1 score — formula and best use case? | 2×(P×R)/(P+R); use for imbalanced classes with no single asymmetric cost. |
| AUC-ROC — what does it measure, and what do 1.0 and 0.5 mean? | Ranking quality across all thresholds (area under the TPR-vs-FPR curve); 1.0 = perfect, 0.5 = random. |
| When do you use RMSE/MAE instead of a classification metric? | When the target is a continuous number (regression), not a category. |
| Fraud detection — class balance, costliest error, and best metric? | Highly imbalanced; missed fraud (false negative) is costliest; Recall. |
| Spam filtering — costliest error and best metric? | Legit email flagged (false positive) is costliest; Precision. |
| Disease screening — costliest error and best metric? | Missed case (false negative) is costliest; Recall. |
| Loan-default prediction — best metric? | F1 (both false-positive and false-negative directions matter). |
| What is the "accuracy paradox"? | On 99% "not fraud" data, a model that always predicts "not fraud" scores 99% accuracy while catching zero fraud. |
| Effect of raising the classification threshold on precision and recall? | Precision goes up, recall goes down (and vice versa when lowered). |

## 5. Bias–variance trade-off

| Front | Back |
|---|---|
| Underfitting (high bias) — symptom and root cause? | Poor on both training and test data; model too simple to capture the pattern. |
| Overfitting (high variance) — symptom and root cause? | Great on training, poor on test/validation; model memorizes training-data noise. |
| Fixes for underfitting? | More complex model, more/better features, train longer, less regularization. |
| Fixes for overfitting? | More data, simpler model, regularization (L1/L2, dropout), cross-validation, early stopping, feature selection, data augmentation, ensembling. |
| Bias–variance trade-off — total error formula? | Total error = Bias² + Variance + irreducible error, minimized at the model-complexity "sweet spot." |
| "Bad on both training and test" vs. "great on training, bad on test" — which is underfitting and which is overfitting? | Bad on both = underfitting/high bias; great on training, bad on test = overfitting/high variance. |

## 6. Ensemble methods

| Front | Back |
|---|---|
| Bagging — training pattern, what it reduces, canonical algorithm? | Parallel, each model on a random bootstrap sample; reduces variance; Random Forest. |
| Boosting — training pattern, what it reduces, canonical algorithm? | Sequential, each stage fixes prior errors; reduces bias; Gradient Boosting/SageMaker XGBoost. |
| Voting — training pattern and what it reduces? | Parallel, different model types on the full dataset, combined by majority/average; cancels out errors from diverse algorithms. |
| How do you fix boosting that's overfitting? | Fewer rounds/early stopping, shallower trees, lower learning rate. |
| Tabular data overfitting vs. image/audio/text data overfitting — different fix? | Tabular → bagging/boosting (tree ensembles); image/audio/text → a deep learning architecture (CNN/transformer) — trees can't learn spatial/sequential structure. |

## Rapid-fire key terms

| Front | Back |
|---|---|
| AI | Systems performing tasks that normally require human intelligence. |
| ML | Systems that learn patterns from data instead of explicit rules. |
| DL | Multi-layer neural networks that learn representations automatically. |
| Parameter | A value learned during training (e.g., a neural network weight). |
| Hyperparameter | A configuration value set before training (e.g., learning rate). |
| Feature engineering | Cleaning, transforming, encoding, and selecting model inputs. |
| SageMaker Feature Store | Centralized, versioned feature repository; prevents training/serving skew. |
| SageMaker Autopilot | Automates data prep, algorithm selection, and tuning for tabular data. |
| Supervised learning | Trains on labeled data; classification or regression. |
| Unsupervised learning | Trains on unlabeled data; clustering or dimensionality reduction. |
| Reinforcement learning | An agent maximizes cumulative reward through trial and error. |
| Confusion matrix | TP/FP/FN/TN table underlying every classification metric. |
| Precision | TP / (TP + FP); few false alarms. |
| Recall | TP / (TP + FN); few missed positives. |
| F1 score | Harmonic mean of precision and recall. |
| AUC-ROC | Ranking quality across all classification thresholds. |
| Underfitting / high bias | Model too simple; poor on both training and test data. |
| Overfitting / high variance | Model too sensitive to training noise; poor generalization. |
| Regularization | L1/L2 penalty or dropout that discourages overly complex models. |
| Bagging | Parallel ensemble on bootstrap samples; reduces variance (Random Forest). |
| Boosting | Sequential ensemble correcting prior errors; reduces bias (Gradient Boosting/XGBoost). |
| Voting | Combines different model types by majority vote or averaged probabilities. |
| SageMaker Ground Truth | Human-in-the-loop data labeling with active learning. |
| SageMaker Model Monitor | Watches a deployed endpoint for data/concept drift. |

## Common exam traps checklist

| Front | Back |
|---|---|
| Unsupervised learning vs. "sounds like prediction" — how do you tell? | No labels/target column → unsupervised, even if the goal sounds like "prediction." |
| Reinforcement learning vs. unsupervised learning — how do you tell them apart? | RL needs an agent + environment + reward; don't conflate "no labels" alone with unsupervised learning. |
| SageMaker Feature Store vs. SageMaker Ground Truth — what's the difference? | Feature Store solves training/serving skew; it is not a labeling tool — that's Ground Truth. |

---

[← Back to the Domain 1 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
