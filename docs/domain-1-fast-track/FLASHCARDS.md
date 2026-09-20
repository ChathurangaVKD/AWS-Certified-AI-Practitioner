# Domain 1 Flashcards: Fundamentals of AI and ML

**Flashcard deck** · fast track: [`README.md`](README.md) · ultra fast
learn: [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md) · full guide:
[`docs/domain-1-fundamentals-of-ai-and-ml.md`](../domain-1-fundamentals-of-ai-and-ml.md)

One card per testable concept — front/back only, no prose. A reformat of
this domain's already-verified [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md)
content into active-recall/spaced-repetition format; it introduces no new
facts. Cards are ordered to match `ULTRA-FAST-LEARN.md`'s own section
order, so working through the deck top to bottom reinforces the domain's
structure. For app-based spaced repetition (Anki, Quizlet, etc.), import
[`flashcards.tsv`](flashcards.tsv) — the same 95 cards, same order, no
header row, tab-separated `front\tback`.

## 1. The 8-stage ML development lifecycle

| Front | Back |
|---|---|
| ML lifecycle — stage 1? | Business goal identification (define problem + success metric first). |
| ML lifecycle — stage 2 tools? | Data collection — Amazon S3, AWS Glue, Amazon Kinesis/MSK. |
| ML lifecycle — stage 3 tools? | EDA — SageMaker Data Wrangler, SageMaker Studio, Amazon Athena. |
| ML lifecycle — stage 4 tools? | Data prep/feature engineering — SageMaker Data Wrangler, SageMaker Feature Store. |
| ML lifecycle — stage 5 tools? | Model training — SageMaker Training Jobs, SageMaker JumpStart, Managed Spot Training. |
| ML lifecycle — stage 6 tools? | Hyperparameter tuning/evaluation — SageMaker automatic model tuning, SageMaker Clarify. |
| ML lifecycle — stage 7 tools? | Deployment — SageMaker endpoints (real-time), batch transform, serverless/async inference. |
| ML lifecycle — stage 8 tools? | Monitoring — SageMaker Model Monitor, Amazon CloudWatch. |
| What loops back to step 2 (data collection)? | Drift/degraded accuracy detected in step 8 (monitoring). |
| What loops back to step 4 (feature engineering)? | A failed evaluation in step 6. |
| What does SageMaker Feature Store prevent? | Training/serving skew. |
| SageMaker Autopilot automates which steps, for what data? | Steps 3–6 (EDA through tuning), tabular data only. |
| What rules out SageMaker Autopilot in favor of manual training? | A custom loss function, domain-specific feature engineering, or a novel architecture. |
| Managed Spot Training — cost vs. On-Demand? | Up to ~90% cheaper (uses spare EC2 capacity). |
| Managed Spot Training — interruption notice? | 2-minute interruption notice. |
| What avoids a Spot-interrupted job restarting from 0%? | Periodic checkpointing to S3 (`checkpoint_s3_uri`). |
| Managed Spot Training is best for... | Routine retraining with no fixed deadline. |
| On-Demand training is best for... | A drift-triggered emergency retrain under a strict compliance SLA. |
| Canary deployment — what does it do? | Routes a small % of traffic to the new version, gradually increasing. |
| Blue/green deployment — what does it do? | New version on a separate fleet; cut traffic over all at once, instant rollback. |
| A/B testing — intent? | Deliberately compare two live versions' real-world performance. |
| Shadow deployment — intent? | Validate a new version with zero user-facing risk; predictions never reach users. |
| What does SageMaker Model Registry do? | Catalogs model versions, stores metrics/lineage, gates deployment behind reviewer approval. |
| Model Registry vs. Model Monitor vs. Model Cards? | Registry = version tracking/approval; Model Monitor = post-deployment drift; Model Cards = documentation. |

## 2. The three learning types

| Front | Back |
|---|---|
| Supervised learning — data & distinguisher? | Labeled data; predicts a known target (classification or regression). |
| Unsupervised learning — data & distinguisher? | Unlabeled data; finds structure, no target column (clustering/dim. reduction). |
| Reinforcement learning — distinguisher? | An agent takes actions in an environment to maximize cumulative reward. |
| Semi-supervised learning — when used? | Small labeled + large unlabeled pool, when labeling is expensive. |
| No labels, agent + environment + reward → which learning type? | Reinforcement learning. |
| No labels, finds structure on its own → which learning type? | Unsupervised learning. |

## 3. AWS AI/ML services

| Front | Back |
|---|---|
| Scenario: no ML expertise, needs a custom model/algorithm → ? | Amazon SageMaker (ML platform). |
| Scenario: images/video — objects, faces, moderation → ? | Amazon Rekognition (computer vision). |
| Scenario: speech/audio to text, diarization → ? | Amazon Transcribe (speech-to-text). |
| Scenario: analyze text sentiment/entities/key phrases/PII → ? | Amazon Comprehend (NLP). |
| Scenario: convert text to lifelike speech → ? | Amazon Polly (text-to-speech). |
| Scenario: translate between languages → ? | Amazon Translate (machine translation). |
| Scenario: build a chatbot or voice bot → ? | Amazon Lex (conversational AI). |
| Scenario: personalized product/content recommendations → ? | Amazon Personalize (recommendations). |
| Scenario: forecast demand/inventory/time-series → ? | Amazon Forecast (forecasting). |
| Scenario: extract text/forms/tables from scanned documents → ? | Amazon Textract (document extraction). |
| Scenario: real-time fraud-risk scoring → ? | Amazon Fraud Detector (fraud detection). |
| Scenario: human-in-the-loop labeling to produce training data → ? | Amazon SageMaker Ground Truth (data labeling). |
| Golden rule: SageMaker vs. purpose-built AI service? | Purpose-built service wins if it matches the task; SageMaker wins only for a custom model/algorithm or full control. |
| SageMaker Ground Truth — exam-correct when? | Large pool of real, unlabeled data; minimize labeling cost/time. |
| Manual labeling — exam-correct when? | Small dataset (tens–hundreds of records), quick PoC. |
| SageMaker Data Wrangler (labeling context) — exam-correct when? | Data already labeled but needs prep/feature engineering, not labels. |
| Active learning (standalone) — exam-correct when? | Tight labeling budget, iterative train → query → label → retrain loop. |
| Weak supervision — exam-correct when? | Labels needed fast/cheap at scale; experts can express rules. |
| Synthetic data generation — exam-correct when? | Real data scarce/sensitive/expensive, or a rare class/edge case. |

## 4. Classification evaluation metrics

| Front | Back |
|---|---|
| Accuracy — formula & best use? | (TP+TN)/(TP+TN+FP+FN); use when classes are roughly balanced. |
| Precision — formula & best use? | TP/(TP+FP); use when false positives are costly. |
| Recall — formula & best use? | TP/(TP+FN); use when false negatives are costly. |
| F1 score — formula & best use? | 2×(P×R)/(P+R); use for imbalanced classes, no single asymmetric cost. |
| AUC-ROC — meaning of 1.0 and 0.5? | Ranking quality across all thresholds; 1.0 = perfect, 0.5 = random. |
| RMSE/MAE — when to use? | Regression error size, when the target is a continuous number, not a category. |
| Fraud detection — which metric? | Recall (missed fraud/FN is costliest). |
| Spam filtering — which metric? | Precision (legit email flagged/FP is costliest). |
| Disease screening — which metric? | Recall (missed case/FN is costliest). |
| Loan-default prediction — which metric? | F1 (both FP and FN matter). |
| General product classifier (balanced) — which metric? | Accuracy. |
| What is the accuracy paradox? | On 99% "not fraud" data, always predicting "not fraud" scores 99% accuracy while catching zero fraud. |
| Effect of raising the classification threshold? | Precision goes up, recall goes down. |

## 5. Bias–variance trade-off

| Front | Back |
|---|---|
| Underfitting (high bias) — symptom? | Poor on both training and test data. |
| Overfitting (high variance) — symptom? | Great on training, poor on test/validation. |
| Underfitting — fixes? | More complex model, more/better features, train longer, less regularization. |
| Overfitting — fixes? | More data, simpler model, regularization, cross-validation, early stopping, feature selection, data augmentation, ensembling. |
| Bias–variance trade-off — total error formula? | Bias² + Variance + irreducible error, minimized at the model-complexity sweet spot. |

## 6. Ensemble methods

| Front | Back |
|---|---|
| Bagging — pattern & reduces? | Parallel, random bootstrap samples; reduces variance (Random Forest). |
| Boosting — pattern & reduces? | Sequential, each stage fixes prior errors; reduces bias (Gradient Boosting/XGBoost). |
| Voting — pattern & reduces? | Parallel, different model types, majority/average; cancels errors from diverse algorithms. |
| How to fix boosting when it overfits? | Fewer rounds/early stopping, shallower trees, lower learning rate. |
| Image/audio/text overfitting — right fix? | A deep learning architecture (CNN/transformer) or matching purpose-built AWS service, not a tree ensemble. |

## Rapid-fire key terms

| Front | Back |
|---|---|
| AI — definition? | Systems performing tasks that normally require human intelligence. |
| ML — definition? | Systems that learn patterns from data instead of explicit rules. |
| DL — definition? | Multi-layer neural networks that learn representations automatically. |
| Parameter — definition? | A value learned during training (e.g., a neural network weight). |
| Hyperparameter — definition? | A configuration value set before training (e.g., learning rate). |
| Feature engineering — definition? | Cleaning, transforming, encoding, and selecting model inputs. |
| Confusion matrix — definition? | TP/FP/FN/TN table underlying every classification metric. |
| Regularization — definition? | L1/L2 penalty or dropout that discourages overly complex models. |
| SageMaker Model Monitor — definition? | Watches a deployed endpoint for data/concept drift. |

## Commonly confused pairs & numeric traps

| Front | Back |
|---|---|
| Confused pair: overfitting vs. underfitting? | Poor on both train & test = underfitting/high bias; great on train, poor on test = overfitting/high variance. |
| Confused pair: bagging vs. boosting? | Parallel/bootstrap = bagging (reduces variance); sequential/corrective = boosting (reduces bias). |
| Confused pair: SageMaker vs. purpose-built AI service? | Custom/novel model needed → SageMaker; standard task already covered → purpose-built service. |
| Confused pair: parameter vs. hyperparameter? | Learned automatically during training = parameter; configured by a human beforehand = hyperparameter. |
| Confused pair: unsupervised learning vs. reinforcement learning? | Agent + environment + reward = RL; unlabeled structure-finding only = unsupervised. |
| Confused pair: Amazon Textract vs. Amazon Comprehend? | Extracting layout/structure from a document = Textract; analyzing meaning of plain text = Comprehend. |
| Confused pair: SageMaker Ground Truth vs. SageMaker Data Wrangler? | Data unlabeled, needs labels = Ground Truth; already labeled, needs cleaning/prep = Data Wrangler. |
| Confused pair: precision vs. recall? | False positive costlier = precision; false negative costlier = recall. |
| Confused pair: SageMaker Model Registry vs. Model Monitor? | Approve/track a version before deployment = Model Registry; watch a deployed model for drift = Model Monitor. |
| Confused pair: canary/blue-green vs. A/B testing vs. shadow deployment? | Safe rollout = canary/blue-green; deliberate comparison = A/B testing; zero user-facing risk = shadow deployment. |
| Confused pair: statistical bias (Domain 1) vs. fairness bias (Domain 4)? | Model fit quality = statistical bias; unfair outcomes across groups = fairness bias (Domain 4). |
| Numeric trap: Spot Training without checkpointing restarts from what %? | 0% progress — not from where it left off. |
| Numeric trap: fixed-deadline/compliance-SLA retrain uses which training mode? | On-Demand, not Managed Spot Training. |
| Numeric trap: raising the classification threshold does what? | Precision up, recall down — not both in the same direction. |

---

[← Back to the Domain 1 fast track](README.md) · [Ultra Fast Learn →](ULTRA-FAST-LEARN.md) · [Interactive cheat sheet →](CHEAT-SHEET.md)
