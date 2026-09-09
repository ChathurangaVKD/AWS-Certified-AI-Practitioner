# Domain 1 Ultra Fast Track: Fundamentals of AI and ML

**Ultra-condensed cram sheet** · fast track: [`docs/domain-1-fast-track/README.md`](README.md) (743 lines) · full guide: [`docs/domain-1-fundamentals-of-ai-and-ml.md`](../domain-1-fundamentals-of-ai-and-ml.md) (2,030 lines) · **Last verified:** 2026-09-05

Bullets and tables only — no prose, no worked examples, no mini-quizzes.
For the last 15-20 minutes before the exam, once the [fast track
guide](README.md) (or the full guide's own [Quick-reference cheat
sheet](../domain-1-fundamentals-of-ai-and-ml.md#quick-reference-cheat-sheet))
is already familiar and you just need the highest-yield tables refreshed
one more time. Every row below links back to the fast track section it's
drawn from.

## Table of contents

- [1. The 8-stage ML development lifecycle](#1-the-8-stage-ml-development-lifecycle)
- [2. The three learning types](#2-the-three-learning-types)
- [3. AWS AI/ML services — compact decision table](#3-aws-aiml-services-compact-decision-table)
- [4. Classification evaluation metrics](#4-classification-evaluation-metrics)
- [5. Bias–variance trade-off](#5-biasvariance-trade-off)
- [6. Ensemble methods](#6-ensemble-methods)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Common exam traps checklist](#common-exam-traps-checklist)
- [Where each row comes from](#where-each-row-comes-from)

---

## 1. The 8-stage ML development lifecycle

| # | Stage | Key AWS tools | Loop-back trigger |
|---|---|---|---|
| 1 | Business goal identification | (define problem + success metric first — no tooling) | — |
| 2 | Data collection | Amazon S3, AWS Glue, Amazon Kinesis / MSK | Drift/degraded accuracy detected in step 8 |
| 3 | Exploratory data analysis (EDA) | SageMaker Data Wrangler, SageMaker Studio, Amazon Athena | — |
| 4 | Data preparation / feature engineering | SageMaker Data Wrangler, **SageMaker Feature Store** | Failed evaluation in step 6 |
| 5 | Model training | SageMaker Training Jobs, SageMaker JumpStart, Managed Spot Training | Degraded accuracy detected in step 8 |
| 6 | Hyperparameter tuning / evaluation | SageMaker automatic model tuning, SageMaker Clarify | **Decision gate:** pass → step 7; fail → step 4 |
| 7 | Deployment | SageMaker endpoints (real-time), batch transform, serverless/async inference | — |
| 8 | Monitoring | SageMaker Model Monitor, Amazon CloudWatch | — |

- **Order to memorize:** collect → explore (EDA) → prepare/feature-engineer → train → evaluate/tune → deploy → monitor.
- **It's a loop, not a waterfall** — a failed evaluation (step 6) goes back to step 4; drift/degraded accuracy (step 8) goes back to step 2 or step 5.
- **SageMaker Feature Store** exists specifically to prevent **training/serving skew**.
- **SageMaker Autopilot** automates steps 3–6 for tabular data (fast baseline, no custom loss function/feature engineering, no novel architecture) — a **custom loss function**, **domain-specific feature engineering**, or a **novel architecture** in the scenario rules Autopilot out in favor of manual SageMaker training.

**Managed Spot Training vs. On-Demand training** (step 5's other cost lever):

| | Managed Spot Training | On-Demand training |
|---|---|---|
| **Cost** | Up to ~90% cheaper (spare EC2 capacity) | Full price, no discount |
| **Risk** | Reclaimed with a 2-minute interruption notice | Never interrupted |
| **Requires** | Periodic **checkpointing** to S3 (`checkpoint_s3_uri`) — without it, an interruption restarts the job from **0%** | No special handling |
| **Billing** | Only actual compute seconds consumed | Billed for the full run |
| **Best for** | Routine retraining, no fixed deadline | Drift-triggered emergency retrain under a strict compliance SLA |

**Production deployment strategies** (distinguish by **intent**, not mechanics):

| Pattern | What it does | Intent |
|---|---|---|
| **Canary** | Route a small % of traffic to the new version, gradually increasing | Safely roll out one new version, gradually |
| **Blue/green** | New version on a separate fleet, cut traffic over all at once, instant rollback | Safely roll out one new version, all at once |
| **A/B testing** | Split live traffic between two+ versions deliberately | **Compare** two versions' real-world performance |
| **Shadow deployment** | Send a copy of live traffic to the new version; its predictions never reach users | **Validate** a new version with zero user-facing risk |

- **SageMaker Model Registry** — catalogs trained model versions, stores each version's evaluation metrics/lineage, lets a reviewer **approve/reject** before deployment. Flow: train → register ("Pending manual approval") → reviewer approves → deployment pipeline rolls the approved version out via canary/blue-green. Not Model Monitor (watches an already-deployed model for drift); not Model Cards (documents intended use/limitations).

## 2. The three learning types

| Type | Data | Distinguisher | AWS SageMaker examples |
|---|---|---|---|
| **Supervised** | Labeled | Predicts a known target — classification or regression | Linear Learner, XGBoost, k-NN |
| **Unsupervised** | Unlabeled | Finds structure with no target column — clustering or dimensionality reduction | k-means, PCA, Random Cut Forest |
| **Reinforcement (RL)** | None (trial-and-error) | **Agent** takes **actions** in an **environment** to maximize cumulative **reward** | Amazon SageMaker RL, AWS DeepRacer |
| Semi-supervised *(lower emphasis)* | Small labeled + large unlabeled pool | Labeling is expensive, so most data stays unlabeled | — |

**If–then lookup:**

- No labels, agent + environment + reward → **reinforcement learning**
- No labels, finds structure on its own → **unsupervised learning**
- Mostly unlabeled + a small labeled subset → **semi-supervised learning**
- Fully labeled target column → **supervised learning**

## 3. AWS AI/ML services — compact decision table

| If the scenario says... | Use... | Category |
|---|---|---|
| "no ML expertise, needs a custom model/algorithm not covered below" | **Amazon SageMaker** | ML platform |
| "images/video: objects, faces, moderation" | **Amazon Rekognition** | Computer vision |
| "convert speech/audio to text, diarization" | **Amazon Transcribe** | Speech-to-text |
| "analyze text: sentiment, entities, key phrases, PII" | **Amazon Comprehend** | NLP |
| "convert text to lifelike speech" | **Amazon Polly** | Text-to-speech |
| "translate between languages" | **Amazon Translate** | Machine translation |
| "build a chatbot or voice bot" | **Amazon Lex** | Conversational AI |
| "personalized product/content recommendations" | **Amazon Personalize** | Recommendations |
| "forecast demand, inventory, or other time-series values" | **Amazon Forecast** | Forecasting |
| "extract text, forms, and tables from scanned documents" | **Amazon Textract** | Document extraction |
| "real-time fraud-risk scoring" | **Amazon Fraud Detector** | Fraud detection |
| "human-in-the-loop labeling to produce training data" | **Amazon SageMaker Ground Truth** | Data labeling |

**Ground Truth vs. alternatives** (deciding factor = the named constraint):

| Approach | What it does | Exam-correct when... |
|---|---|---|
| **SageMaker Ground Truth** | Managed human-in-the-loop labeling + built-in active learning | Large pool of **real, unlabeled** data, minimize labeling cost/time |
| **Manual labeling** | People label every record by hand | Small dataset (tens–hundreds of records), quick PoC |
| **SageMaker Data Wrangler** | Cleans/transforms/joins **already-labeled** data | Data is labeled but needs prep/feature engineering, not labels |
| **Active learning (standalone)** | Baseline model picks the *next* most-informative unlabeled examples to label | Tight **labeling budget**, iterative train → query → label → retrain loop |
| **Weak supervision** | Combines noisy rules/heuristics into probabilistic labels, little manual labeling | Labels needed fast/cheap at scale; experts can express **rules** |
| **Synthetic data generation** | Manufactures artificial labeled examples | Real data **scarce**/sensitive/expensive, or a rare class/edge case |

- **Golden rule:** if a purpose-built managed AI service matches the described task, it beats **Amazon SageMaker** — SageMaker wins only when the use case needs a **custom** model/algorithm or full control.

## 4. Classification evaluation metrics

| Metric | Formula | Answers | Use when |
|---|---|---|---|
| **Accuracy** | (TP + TN) / (TP + TN + FP + FN) | Overall % correct | Classes are **roughly balanced** |
| **Precision** | TP / (TP + FP) | Of flagged-positive, how much was real? | **False positives** are costly (e.g., blocking a legit transaction) |
| **Recall (Sensitivity)** | TP / (TP + FN) | Of actual positives, how many were caught? | **False negatives** are costly (e.g., missed fraud/disease) |
| **F1 score** | 2 × (P × R) / (P + R) | Balanced precision/recall | **Imbalanced classes**, no single asymmetric cost |
| **AUC-ROC** | Area under TPR-vs-FPR curve | Ranking quality across all thresholds | Compare models independent of one fixed threshold (1.0 = perfect, 0.5 = random) |
| **RMSE / MAE** | Avg. distance between predicted & actual numbers | Regression error size | Target is a **continuous number**, not a category |

**Scenario → metric table:**

| Use case | Class balance | Costliest error | Metric |
|---|---|---|---|
| Fraud detection | Highly imbalanced | Missed fraud (FN) | **Recall** |
| Spam filtering | Imbalanced | Legit email flagged (FP) | **Precision** |
| Disease screening | Imbalanced | Missed case (FN) | **Recall** |
| Loan-default prediction | Imbalanced | Both directions matter | **F1** |
| General product classifier | Roughly balanced | No single asymmetric cost | **Accuracy** |
| House-price prediction | N/A (regression) | N/A | **RMSE / MAE** |

- **Accuracy paradox:** 99% "not fraud" data → a model that always predicts "not fraud" scores 99% accuracy while catching zero fraud.
- Raising the classification threshold → **precision up, recall down** (and vice versa).

## 5. Bias–variance trade-off

| | Underfitting (high bias) | Overfitting (high variance) |
|---|---|---|
| **Symptom** | Poor on **both** training and test data | Great on training, poor on test/validation |
| **Root cause** | Model too simple to capture the pattern | Model memorizes training-data noise |
| **Fixes** | More complex model, more/better features, train longer, less regularization | More data, simpler model, regularization (L1/L2, dropout), cross-validation, early stopping, feature selection, data augmentation, **ensembling** |

- **Bias–variance trade-off:** reducing one typically increases the other; total error = Bias² + Variance + irreducible error, minimized at the "sweet spot" model complexity.
- "Bad on both sets" → **underfitting/high bias**. "Great on training, bad on test" → **overfitting/high variance**.

## 6. Ensemble methods

| Method | Base models | Training pattern | Primarily reduces | Canonical algorithm |
|---|---|---|---|---|
| **Bagging** (bootstrap aggregating) | Same model, many instances | Parallel, each on a random bootstrap sample | **Variance** | Random Forest |
| **Boosting** | Same model, many instances | Sequential — each stage fixes prior errors | **Bias** (also handles weak learners) | Gradient Boosting / SageMaker XGBoost |
| **Voting** | Different model types | Parallel, same full dataset, combine by majority/average | Errors from **diverse** algorithms canceling out | Logistic regression + decision tree + k-NN, etc. |

- Ensembles are the go-to fix for overfitting on **structured/tabular** data beyond "more data" or "add regularization."
- Boosting overfits if left unchecked — fix with fewer rounds/early stopping, shallower trees, lower learning rate.
- **Exam trap:** the same overfitting symptom on **image/audio/text** data is not fixed by a tree ensemble — decision trees can't learn spatial/sequential structure. Reach for a **deep learning architecture** (CNN/transformer) or the matching purpose-built AWS AI service instead.

---

## Rapid-fire key terms

- **AI** — systems performing tasks that normally require human intelligence.
- **ML** — systems that learn patterns from data instead of explicit rules.
- **DL** — multi-layer neural networks that learn representations automatically.
- **Parameter** — a value learned during training (e.g., a neural network weight).
- **Hyperparameter** — a configuration value set before training (e.g., learning rate).
- **Feature engineering** — cleaning, transforming, encoding, and selecting model inputs.
- **SageMaker Feature Store** — centralized, versioned feature repository; prevents training/serving skew.
- **SageMaker Autopilot** — automates data prep, algorithm selection, and tuning for tabular data.
- **Supervised learning** — trains on labeled data; classification or regression.
- **Unsupervised learning** — trains on unlabeled data; clustering or dimensionality reduction.
- **Reinforcement learning** — an agent maximizes cumulative reward through trial and error.
- **Confusion matrix** — TP/FP/FN/TN table underlying every classification metric.
- **Precision** — TP / (TP + FP); few false alarms.
- **Recall** — TP / (TP + FN); few missed positives.
- **F1 score** — harmonic mean of precision and recall.
- **AUC-ROC** — ranking quality across all classification thresholds.
- **Underfitting / high bias** — model too simple; poor on both training and test data.
- **Overfitting / high variance** — model too sensitive to training noise; poor generalization.
- **Regularization** — L1/L2 penalty or dropout that discourages overly complex models.
- **Bagging** — parallel ensemble on bootstrap samples; reduces variance (Random Forest).
- **Boosting** — sequential ensemble correcting prior errors; reduces bias (Gradient Boosting/XGBoost).
- **Voting** — combines different model types by majority vote or averaged probabilities.
- **SageMaker Ground Truth** — human-in-the-loop data labeling with active learning.
- **SageMaker Model Monitor** — watches a deployed endpoint for data/concept drift.

## Common exam traps checklist

- [ ] "No ML expertise + standard task (vision/speech/text/forecast/rec)" → the **purpose-built service**, not SageMaker.
- [ ] SageMaker is correct only when a **custom** model/algorithm or full control is explicitly needed.
- [ ] **No labels/target column** → **unsupervised**, even if the goal sounds like "prediction."
- [ ] RL needs **agent + environment + reward** — don't conflate it with "no labels = unsupervised."
- [ ] **Accuracy is misleading on imbalanced data** — look for precision, recall, F1, or AUC-ROC.
- [ ] Raising the threshold → precision up, recall down (not both up or both down).
- [ ] A **failed** evaluation gate (step 6) loops back to **feature engineering** (step 4), not to business goal identification or straight to deployment.
- [ ] "Great on training, bad on test" = **overfitting**; "bad on both" = **underfitting** — don't swap them.
- [ ] Tabular overfitting → **bagging/boosting**; image/audio/text overfitting → a **deep learning architecture**, not more trees.
- [ ] **Feature Store** solves training/serving skew — it is not a labeling tool (that's Ground Truth).
- [ ] **Managed Spot Training** without **checkpointing** restarts an interrupted job from **0%**, not from where it left off.
- [ ] A **fixed-deadline/compliance-SLA** retrain uses **On-Demand**, not Spot — Spot is for routine retraining with no fixed deadline.
- [ ] Gradual traffic shift with automatic rollback → **canary**; instant all-at-once cutover → **blue/green**; deliberately comparing two live versions → **A/B testing**; zero user-facing risk validation → **shadow deployment**.
- [ ] **SageMaker Model Registry** tracks model versions and requires reviewer **approval** before deployment — it is not Model Monitor (drift) or Model Cards (documentation).
- [ ] Among labeling/data-prep options, match the **named constraint**: labeling *budget* → active learning; *expressible rules* → weak supervision; *scarce/rare* data → synthetic data; large genuinely unlabeled pool → Ground Truth; already labeled → Data Wrangler.

---

## Where each row comes from

| This cram sheet | Fast track section |
|---|---|
| 1. The 8-stage lifecycle | [Section 2](README.md#2-the-ml-development-lifecycle) |
| Managed Spot Training vs. On-Demand | [Section 2](README.md#2-the-ml-development-lifecycle) |
| Production deployment strategies & Model Registry | [Section 2](README.md#2-the-ml-development-lifecycle) |
| 2. The three learning types | [Section 3](README.md#3-three-learning-types) |
| 3. AWS services decision table | [Section 5](README.md#5-aws-managed-aiml-services) |
| Ground Truth vs. alternatives | [Section 5](README.md#5-aws-managed-aiml-services) |
| 4. Classification evaluation metrics | [Section 6](README.md#6-model-evaluation-basics) |
| 5. Bias–variance trade-off | [Section 7](README.md#7-biasvariance-trade-off-and-ensemble-methods) |
| 6. Ensemble methods | [Section 7](README.md#7-biasvariance-trade-off-and-ensemble-methods) |
| Rapid-fire key terms | [Rapid-fire key terms](README.md#rapid-fire-key-terms) |

For the full tables, decision flowcharts, condensed worked example, and
rapid self-check this cram sheet intentionally omits, go back to the
[Domain 1 fast track](README.md) or the [full Domain 1
guide](../domain-1-fundamentals-of-ai-and-ml.md) for the underlying
explanations, worked examples, mini-quizzes, and 24 practice questions.
For material spanning multiple domains, see
[`docs/cross-domain-concept-map.md`](../cross-domain-concept-map.md).

[← Back to the Domain 1 fast track](README.md) · [Full Domain 1 guide →](../domain-1-fundamentals-of-ai-and-ml.md)
