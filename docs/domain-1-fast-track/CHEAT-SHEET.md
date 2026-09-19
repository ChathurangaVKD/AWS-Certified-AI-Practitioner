# Domain 1 Cheat Sheet: Fundamentals of AI and ML

**Interactive quick-scan cheat sheet** · companion to the [Fast Track guide](README.md) and the [Ultra Fast Track cram sheet](ULTRA-FAST-LEARN.md) · full guide: [`docs/domain-1-fundamentals-of-ai-and-ml.md`](../domain-1-fundamentals-of-ai-and-ml.md)

Built for a 2-3 minute skim right before the exam — jump straight to the
topic you're weakest on, expand only that section, and tick off the
self-check checklist at the end. Every fact here already lives in the
[Fast Track](README.md) and [Ultra Fast Track](ULTRA-FAST-LEARN.md); this
is a reformat for scannability, not new content.

## Table of contents

- [1. The 8-stage ML development lifecycle](#1-the-8-stage-ml-development-lifecycle)
- [2. The three learning types](#2-the-three-learning-types)
- [3. AWS AI/ML services — compact decision table](#3-aws-aiml-services-compact-decision-table)
- [4. Classification evaluation metrics](#4-classification-evaluation-metrics)
- [5. Bias–variance trade-off](#5-biasvariance-trade-off)
- [6. Ensemble methods](#6-ensemble-methods)
- [Commonly confused pairs](#commonly-confused-pairs)
- [Rapid-fire key terms](#rapid-fire-key-terms)
- [Self-check checklist](#self-check-checklist)

---

### 1. The 8-stage ML development lifecycle

<details>
<summary>8-stage lifecycle table · Spot vs. On-Demand · deployment strategies · Model Registry — tap to expand</summary>

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
- **SageMaker Autopilot** automates steps 3–6 for tabular data — a **custom loss function**, **domain-specific feature engineering**, or a **novel architecture** rules it out in favor of manual SageMaker training.

**Managed Spot Training vs. On-Demand training:**

| | Managed Spot Training | On-Demand training |
|---|---|---|
| **Cost** | Up to **~90% cheaper** (spare EC2 capacity) | Full price, no discount |
| **Risk** | Reclaimed with a **2-minute interruption notice** | Never interrupted |
| **Requires** | Periodic **checkpointing** to S3 — without it, an interruption restarts the job from **0%** | No special handling |
| **Best for** | Routine retraining, no fixed deadline | Drift-triggered emergency retrain under a strict compliance SLA |

**Production deployment strategies (distinguish by intent, not mechanics):**

| Pattern | What it does | Intent |
|---|---|---|
| **Canary** | Route a small % of traffic to the new version, gradually increasing | Safely roll out one new version, **gradually** |
| **Blue/green** | New version on a separate fleet, cut traffic over **all at once**, instant rollback | Safely roll out one new version, **all at once** |
| **A/B testing** | Split live traffic between two+ versions deliberately | **Compare** two versions' real-world performance |
| **Shadow deployment** | Send a copy of live traffic to the new version; predictions never reach users | **Validate** with **zero** user-facing risk |

- **SageMaker Model Registry** — catalogs trained model versions, stores evaluation metrics/lineage, lets a reviewer **approve/reject** before deployment. Not Model Monitor (drift) or Model Cards (documentation).

</details>

### 2. The three learning types

<details>
<summary>Supervised vs. unsupervised vs. reinforcement vs. semi-supervised — tap to expand</summary>

| Type | Data | Distinguisher | AWS SageMaker examples |
|---|---|---|---|
| **Supervised** | Labeled | Predicts a known target — classification or regression | Linear Learner, XGBoost, k-NN |
| **Unsupervised** | Unlabeled | Finds structure with **no target column** | k-means, PCA, Random Cut Forest |
| **Reinforcement (RL)** | None (trial-and-error) | **Agent** takes **actions** in an **environment** to maximize cumulative **reward** | Amazon SageMaker RL, AWS DeepRacer |
| Semi-supervised | Small labeled + large unlabeled pool | Labeling is expensive, most data stays unlabeled | — |

**If–then lookup:**

- No labels, agent + environment + reward → **reinforcement learning**
- No labels, finds structure on its own → **unsupervised learning**
- Mostly unlabeled + a small labeled subset → **semi-supervised learning**
- Fully labeled target column → **supervised learning**

</details>

### 3. AWS AI/ML services — compact decision table

<details>
<summary>Purpose-built AI services keyword table · Ground Truth vs. alternatives — tap to expand</summary>

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

**Ground Truth vs. alternatives (deciding factor = the named constraint):**

| Approach | Exam-correct when... |
|---|---|
| **SageMaker Ground Truth** | Large pool of **real, unlabeled** data, minimize labeling cost/time |
| **Manual labeling** | Small dataset (tens–hundreds of records), quick PoC |
| **SageMaker Data Wrangler** | Data is **already labeled** but needs prep/feature engineering |
| **Active learning (standalone)** | Tight **labeling budget**, iterative train → query → label → retrain loop |
| **Weak supervision** | Labels needed fast/cheap at scale; experts can express **rules** |
| **Synthetic data generation** | Real data **scarce**/sensitive/expensive, or a rare class/edge case |

- **Golden rule:** a purpose-built managed AI service beats **Amazon SageMaker** whenever it matches the described task — SageMaker wins only for a **custom** model/algorithm or full control.

</details>

### 4. Classification evaluation metrics

<details>
<summary>Precision, recall, F1, AUC-ROC, RMSE/MAE, scenario → metric table — tap to expand</summary>

| Metric | Formula | Use when |
|---|---|---|
| **Accuracy** | (TP + TN) / (TP + TN + FP + FN) | Classes are **roughly balanced** |
| **Precision** | TP / (TP + FP) | **False positives** are costly |
| **Recall (Sensitivity)** | TP / (TP + FN) | **False negatives** are costly |
| **F1 score** | 2 × (P × R) / (P + R) | **Imbalanced classes**, no single asymmetric cost |
| **AUC-ROC** | Area under TPR-vs-FPR curve | Compare models across all thresholds (**1.0** = perfect, **0.5** = random) |
| **RMSE / MAE** | Avg. distance between predicted & actual numbers | Target is a **continuous number** |

**Scenario → metric:**

| Use case | Costliest error | Metric |
|---|---|---|
| Fraud detection | Missed fraud (FN) | **Recall** |
| Spam filtering | Legit email flagged (FP) | **Precision** |
| Disease screening | Missed case (FN) | **Recall** |
| Loan-default prediction | Both directions matter | **F1** |
| General product classifier | No single asymmetric cost | **Accuracy** |
| House-price prediction | N/A (regression) | **RMSE / MAE** |

- **Accuracy paradox:** **99%** "not fraud" data → a model that always predicts "not fraud" scores **99% accuracy** while catching zero fraud.
- Raising the classification threshold → **precision up, recall down** (and vice versa).

</details>

### 5. Bias–variance trade-off

<details>
<summary>Underfitting vs. overfitting symptoms and fixes — tap to expand</summary>

| | Underfitting (high bias) | Overfitting (high variance) |
|---|---|---|
| **Symptom** | Poor on **both** training and test data | Great on training, poor on test/validation |
| **Root cause** | Model too simple | Model memorizes training-data noise |
| **Fixes** | More complex model, more/better features, train longer, less regularization | More data, simpler model, regularization (L1/L2, dropout), cross-validation, early stopping, **ensembling** |

- **Total error = Bias² + Variance + irreducible error**, minimized at the "sweet spot" model complexity.
- "Bad on both sets" → **underfitting/high bias**. "Great on training, bad on test" → **overfitting/high variance**.

</details>

### 6. Ensemble methods

<details>
<summary>Bagging vs. boosting vs. voting — tap to expand</summary>

| Method | Training pattern | Primarily reduces | Canonical algorithm |
|---|---|---|---|
| **Bagging** (bootstrap aggregating) | Parallel, each on a random bootstrap sample | **Variance** | Random Forest |
| **Boosting** | Sequential — each stage fixes prior errors | **Bias** | Gradient Boosting / SageMaker XGBoost |
| **Voting** | Parallel, different model types, combine by majority/average | Errors from **diverse** algorithms canceling out | Logistic regression + decision tree + k-NN |

- Ensembles are the go-to fix for overfitting on **structured/tabular** data.
- **Exam trap:** the same overfitting symptom on **image/audio/text** data is not fixed by a tree ensemble — reach for a **deep learning architecture** (CNN/transformer) instead.

</details>

---

### Commonly confused pairs

<details>
<summary>8 pairs the exam loves to swap — tap to expand</summary>

| Pair | How to tell them apart |
|---|---|
| **Precision** vs. **Recall** | Precision = cost of false positives; **Recall** = cost of false negatives (missed cases) |
| **Underfitting** vs. **Overfitting** | Underfitting = bad on **both** sets; Overfitting = great on train, **bad on test** |
| **Bagging** vs. **Boosting** | Bagging = parallel, reduces **variance**; Boosting = sequential, reduces **bias** |
| **Canary** vs. **Blue/green** | Canary = **gradual** traffic shift; Blue/green = **all-at-once** cutover |
| **A/B testing** vs. **Shadow deployment** | A/B = live traffic **compared**; Shadow = live traffic copied with **zero** user-facing risk |
| **SageMaker Model Registry** vs. **Model Monitor** vs. **Model Cards** | Registry = version **approval gate**; Monitor = watches **deployed** drift; Cards = **documentation** |
| **Managed Spot Training** vs. **On-Demand** | Spot = up to **~90% cheaper**, needs checkpointing; On-Demand = full price, never interrupted |
| **Unsupervised learning** vs. **Reinforcement learning** | Unsupervised = finds structure alone; RL = **agent + environment + reward** |

</details>

### Rapid-fire key terms

<details>
<summary>24 key terms — tap to expand</summary>

| Term | Definition |
|---|---|
| **AI** | Systems performing tasks that normally require human intelligence |
| **ML** | Systems that learn patterns from data instead of explicit rules |
| **DL** | Multi-layer neural networks that learn representations automatically |
| **Parameter** | A value learned during training (e.g., a neural network weight) |
| **Hyperparameter** | A configuration value set **before** training (e.g., learning rate) |
| **Feature engineering** | Cleaning, transforming, encoding, and selecting model inputs |
| **SageMaker Feature Store** | Centralized, versioned feature repository; prevents **training/serving skew** |
| **SageMaker Autopilot** | Automates data prep, algorithm selection, and tuning for **tabular** data |
| **Supervised learning** | Trains on labeled data; classification or regression |
| **Unsupervised learning** | Trains on unlabeled data; clustering or dimensionality reduction |
| **Reinforcement learning** | An agent maximizes cumulative reward through trial and error |
| **Confusion matrix** | TP/FP/FN/TN table underlying every classification metric |
| **Precision** | TP / (TP + FP); few false alarms |
| **Recall** | TP / (TP + FN); few missed positives |
| **F1 score** | Harmonic mean of precision and recall |
| **AUC-ROC** | Ranking quality across all classification thresholds |
| **Underfitting / high bias** | Model too simple; poor on both training and test data |
| **Overfitting / high variance** | Model too sensitive to training noise |
| **Regularization** | L1/L2 penalty or dropout that discourages overly complex models |
| **Bagging** | Parallel ensemble on bootstrap samples; reduces **variance** (Random Forest) |
| **Boosting** | Sequential ensemble correcting prior errors; reduces **bias** (Gradient Boosting/XGBoost) |
| **Voting** | Combines different model types by majority vote or averaged probabilities |
| **SageMaker Ground Truth** | Human-in-the-loop data labeling with active learning |
| **SageMaker Model Monitor** | Watches a deployed endpoint for data/concept drift |

</details>

---

## Self-check checklist

Tick each fact you can already state cold — anything unchecked is what to
re-read in the [Fast Track](README.md) or [Ultra Fast
Track](ULTRA-FAST-LEARN.md) before the exam.

- [ ] "No ML expertise + standard task (vision/speech/text/forecast/rec)" → the **purpose-built service**, not SageMaker.
- [ ] SageMaker is correct only when a **custom** model/algorithm or full control is explicitly needed.
- [ ] **No labels/target column** → **unsupervised**, even if the goal sounds like "prediction."
- [ ] RL needs **agent + environment + reward** — don't conflate it with "no labels = unsupervised."
- [ ] **Accuracy is misleading on imbalanced data** — look for precision, recall, F1, or AUC-ROC.
- [ ] Raising the threshold → **precision up, recall down** (not both up or both down).
- [ ] A **failed** evaluation gate (step 6) loops back to **feature engineering** (step 4), not to business goal identification or straight to deployment.
- [ ] "Great on training, bad on test" = **overfitting**; "bad on both" = **underfitting** — don't swap them.
- [ ] Tabular overfitting → **bagging/boosting**; image/audio/text overfitting → a **deep learning architecture**, not more trees.
- [ ] **Feature Store** solves training/serving skew — it is not a labeling tool (that's Ground Truth).
- [ ] **Managed Spot Training** without **checkpointing** restarts an interrupted job from **0%**, not from where it left off.
- [ ] A **fixed-deadline/compliance-SLA** retrain uses **On-Demand**, not Spot.
- [ ] Gradual traffic shift with rollback → **canary**; instant all-at-once cutover → **blue/green**; deliberately comparing two live versions → **A/B testing**; zero user-facing risk validation → **shadow deployment**.
- [ ] **SageMaker Model Registry** tracks model versions and requires reviewer **approval** before deployment — it is not Model Monitor (drift) or Model Cards (documentation).
- [ ] Among labeling/data-prep options, match the **named constraint**: labeling *budget* → active learning; *expressible rules* → weak supervision; *scarce/rare* data → synthetic data; large genuinely unlabeled pool → Ground Truth; already labeled → Data Wrangler.

---

For the full explanations, worked examples, mini-quizzes, and 24 practice
questions this cheat sheet intentionally omits, go back to the [Domain 1
fast track](README.md), the [Ultra Fast Track](ULTRA-FAST-LEARN.md), or
the [full Domain 1 guide](../domain-1-fundamentals-of-ai-and-ml.md).

[← Back to the Domain 1 fast track](README.md) · [Ultra Fast Track →](ULTRA-FAST-LEARN.md)
