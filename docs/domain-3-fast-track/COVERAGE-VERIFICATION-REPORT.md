# Domain 3 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete; all findings fixed · **Verified:** 2026-09-09 · **Backfilled:** 2026-09-09

This report is the technical verification flagged as outstanding in the
Content Health assessment for Domain 3's condensed layer. This is a
correctness audit against the live files, not new content authoring —
no prose in the Fast Track or Ultra Fast Learn was rewritten to produce
the original audit below; two classes of real coverage gap were found
and documented with exact locations. The hop-1 gap (Finding 1, Kendra
GenAI Index) was fixed first, in a separate change (Part 2, Section 4).
The four hop-2 gaps (Findings 2-5) have since been backfilled into
`ULTRA-FAST-LEARN.md` (2026-09-09), sourced verbatim from the same Fast
Track sections this report cites. See the "Finding 1" and
"Findings 2-5" sections below for both updates.

## The claim under audit

[`docs/DOCUMENTATION_STRUCTURE.md`](../DOCUMENTATION_STRUCTURE.md) states
the guarantee this report checks:

> Every Fast Track guide and Ultra Fast Learn cram sheet carries the same
> coverage guarantee: every testable concept the full domain guide covers
> is retained somewhere in the condensed layer — only narrative
> explanation, extra worked examples, and repetition are cut, not
> exam-relevant content.

Domain 3 (Applications of Foundation Models) is the exam's
**highest-weight domain (~28%)** and its full guide is the longest at
**6,957 lines**, condensed into a **2,909-line, three-part Fast Track**
([`README.md`](README.md),
[`part-1-application-design-and-customization.md`](part-1-application-design-and-customization.md),
[`part-2-inference-and-multimodal.md`](part-2-inference-and-multimodal.md),
[`part-3-deployment-and-troubleshooting.md`](part-3-deployment-and-troubleshooting.md))
plus [`ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md). That size and weight
is why this domain gets extra scrutiny rather than the single spot-check
pass other domains received.

## Sections spot-checked

Full traceability was checked hop by hop (full guide → Fast Track → Ultra
Fast Learn) for the full guide's major sections and worked examples,
concentrating on the sections with the highest concept density and the
sections adjacent to a part boundary (Part 1/Part 2 split), where a gap
is most likely to hide:

- **Section 3: Retrieval Augmented Generation (RAG) and Amazon Bedrock
  Knowledge Bases**, including the [vector store decision
  guide](../domain-3-applications-of-foundation-models.md#vector-store-decision-guide-opensearch-vs-aurora-pgvector-vs-amazon-kendra)
  and its two worked examples (compliance-document Q&A;
  [Kendra's GenAI Index as a Bedrock Knowledge Base data
  source](../domain-3-applications-of-foundation-models.md#worked-example-building-a-product-knowledge-assistant-using-kendras-genai-index-as-a-bedrock-knowledge-base-data-source))
- **Section 4: Fine-tuning vs. continued pre-training vs. RAG vs. prompt
  engineering**, including [fine-tuning efficiency
  techniques](../domain-3-applications-of-foundation-models.md#fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-vs-instruction-tuning)
  (full fine-tuning/LoRA/QLoRA/instruction tuning),
  [RLHF](../domain-3-applications-of-foundation-models.md#reinforcement-learning-from-human-feedback-rlhf-aligning-fine-tuned-models-to-human-preferences),
  and [dataset
  curation](../domain-3-applications-of-foundation-models.md#curating-a-fine-tuning-dataset-size-thresholds-a-quality-checklist-and-synthetic-vs-real-data)
- **Section 5: Amazon Bedrock features**, including the [Guardrails
  rule-type decision
  tree](../domain-3-applications-of-foundation-models.md#guardrails-rule-type-decision-tree-matching-the-use-case-to-the-right-filter)
  and the [on-demand vs. provisioned throughput vs. batch decision
  guide](../domain-3-applications-of-foundation-models.md#choosing-among-on-demand-provisioned-throughput-and-batch-inference-a-decision-guide)
- **Section 6: Vector databases and embeddings for search and
  retrieval**, including [retrieval quality metrics (NDCG, MAP,
  Recall@k,
  MRR)](../domain-3-applications-of-foundation-models.md#retrieval-quality-metrics-ndcg-map-recallk-and-mrr-a-selection-decision-guide)
- **Section 8 onward** (AWS infrastructure, auto-scaling, inference
  failure triage, resilience patterns, RAG troubleshooting) — spot-checked
  for AWS service names and numeric thresholds against Part 3

## Method

For each section: extract the exam-relevant facts named in the full
guide (AWS service names, decision criteria, numeric thresholds, named
metrics/benchmarks, and the specific terms an exam distractor would
hinge on), then grep each fact through the Fast Track part that the
[README's own section-origin
table](README.md#where-each-section-comes-from) claims covers it, then
through Ultra Fast Learn. A fact that resolves at both hops is clean. A
fact missing at the Fast Track hop is a **hop-1 gap** (more serious — the
Fast Track is supposed to be the complete condensation). A fact present
in the Fast Track but missing from Ultra Fast Learn is a **hop-2 gap**
(expected to some degree, since Ultra Fast Learn is a further, lossier
condensation — but only acceptable if what's cut is genuinely
non-exam-relevant repetition, not a distinct testable concept).

## Finding 1 (hop-1 gap): Kendra GenAI Index as a Bedrock Knowledge Base data source — fixed

**Update: fixed.** Part 2, Section 4 now states the reuse-over-duplicate
decision rule with a resolving link to the full guide's worked example
(see [Part 2, Section
4](part-2-inference-and-multimodal.md#4-vector-databases-and-embeddings-choosing-a-backend),
subsection "Reuse before you provision: an existing Kendra GenAI
Index"). The description below is the original audit that found the gap
and is retained for the record; the `grep -c` result it quotes for Part
2 reflects the state **before** that fix and is no longer current — Part
2 now contains multiple "Kendra GenAI Index" mentions.

**Severity: real gap, not narrative trimming (at the time of the
original audit).** The full guide devotes a
dedicated, ~200-line worked example
([lines 1208–1405](../domain-3-applications-of-foundation-models.md#worked-example-building-a-product-knowledge-assistant-using-kendras-genai-index-as-a-bedrock-knowledge-base-data-source))
to a specific, exam-called-out distinction: a **Kendra GenAI Index** is an
index *type* (alongside classic Enterprise/Developer Edition indexes)
that **Amazon Bedrock Knowledge Bases** and **Amazon Q Business** can plug
into directly as a retriever — so when a scenario mentions an *existing*
Kendra deployment or Kendra GenAI Index alongside a request for
FM-grounded chat, the exam-tested answer is to point a Knowledge Base at
that index rather than standing up a second OpenSearch/Aurora vector
store over the same content. The full guide states explicitly: "that
distinction matters for the exam."

This concept is entirely absent from both Fast Track parts:

```
$ grep -c "GenAI Index" docs/domain-3-fast-track/part-1-application-design-and-customization.md
0
$ grep -c "GenAI Index" docs/domain-3-fast-track/part-2-inference-and-multimodal.md
0
```

Tracing why: [Part 1, Section 4 (RAG and Amazon Bedrock Knowledge
Bases)](part-1-application-design-and-customization.md#4-rag-and-amazon-bedrock-knowledge-bases)
explicitly defers "the vector store selection guide" to Part 2 ("vector
database/embedding depth is Part 2 scope"). But [Part 2, Section 4
(Vector databases and embeddings: choosing a
backend)](part-2-inference-and-multimodal.md#4-vector-databases-and-embeddings-choosing-a-backend)
links back only to the full guide's **Section 6** (a separate,
general-purpose vector-database section), never to **Section 3's own**
vector store decision guide where the Kendra GenAI Index worked example
actually lives. The concept falls through the gap between where Part 1
says it will be covered and where Part 2 actually draws from — it is not
a case of "extra worked example" trimming, since the underlying decision
fact (reuse an existing Kendra GenAI Index instead of provisioning a
second vector store) does not appear anywhere in either part, in any
form (table row, bullet, or exam tip).

**This is confirmed as exam-relevant, not just full-guide narrative**,
because it independently survived all the way through to
**Ultra Fast Learn**, which was evidently condensed with at least partial
reference back to the full guide rather than only from the Fast Track:

```
$ grep -n "Kendra GenAI Index" docs/domain-3-fast-track/ULTRA-FAST-LEARN.md
117:  can also reuse an existing **Kendra GenAI Index** as its retriever —
332:- [ ] Reuse an existing **Kendra GenAI Index** as a Knowledge Base's
```

At the time of the original audit, a reader who only read Part 1 and
Part 2 (as the Fast Track's own reading-order instructions direct) would
never have encountered this concept at all, while a reader who skipped
straight to the Ultra Fast Learn cram sheet would — an inversion of the
intended layering, and a real, independently-confirmable gap in the Fast
Track's own coverage claim, not a stale test artifact. That inversion is
now closed by the Part 2 fix noted above.

By contrast, the *other* worked example in the same full-guide subsection
(compliance-document Q&A: OpenSearch vs. Aurora + pgvector vs. Kendra
from a blank slate) **is not** a gap — every decision criterion it
demonstrates (hybrid/scale → OpenSearch, existing Aurora + a team that
can operate an embeddings pipeline → pgvector, zero embeddings
infrastructure → Kendra) is already captured in Part 2's vector-database
decision table and flowchart. That one is exactly the "extra worked
example" trimming the coverage guarantee permits.

## Findings 2–5 (hop-2 gaps): dropped entirely from Ultra Fast Learn — now backfilled

**Update, 2026-09-09: all four backfilled.** These four were originally
found dropped entirely from Ultra Fast Learn despite being clean at hop 1
(full guide → Fast Track — each fully present in Part 1 or Part 2). They
have now been backfilled into `ULTRA-FAST-LEARN.md`'s customization
section (Section 1, for #2–#4) and evaluation section (Section 5, for
#5), sourced verbatim from the same Fast Track subsections cited below —
no new facts were authored to close these gaps.

| # | Topic | Full guide → Fast Track (hop 1) | Fast Track → Ultra Fast Learn (hop 2) |
|---|---|---|---|
| 2 | **Fine-tuning efficiency techniques** — LoRA, QLoRA, instruction tuning, the GPU-memory/training-time/quality decision flowchart, and the merged-vs-unmerged serving-latency table | Clean — full explanation in [Part 1, Section 6](part-1-application-design-and-customization.md#6-fine-tuning-efficiency-techniques-full-fine-tuning-vs-lora-vs-qlora-vs-instruction-tuning) | **Fixed** — Ultra Fast Learn's customization section (Section 1) now carries a LoRA/QLoRA/instruction-tuning comparison table, the decision-order bullets standing in for the flowchart, and the merged-vs-unmerged serving-latency bullet |
| 3 | **RLHF** — the three-stage SFT → reward model → PPO process, and when it applies vs. plain SFT or RAG | Clean — full explanation in [Part 1, Section 7](part-1-application-design-and-customization.md#7-rlhf-aligning-fine-tuned-models-to-human-preferences) | **Fixed** — "RLHF," "reward model," "SFT," and "PPO" now appear in Ultra Fast Learn's Section 1, with the three-stage process and the SFT-vs-RLHF-vs-RAG applicability bullets |
| 4 | **Fine-tuning dataset curation** — minimum labeled-example thresholds by technique/model scale, the data-quality checklist (diversity, edge-case coverage, label correctness, class balance), synthetic-vs-real trade-offs, catastrophic forgetting, overfitting, early stopping, inter-annotator agreement | Clean — full explanation in [Part 1, Section 8](part-1-application-design-and-customization.md#8-curating-a-fine-tuning-dataset) | **Fixed** — Ultra Fast Learn's Section 1 now carries the minimum-examples table, the data-quality checklist, the synthetic-vs-real trade-off, and all of catastrophic forgetting/overfitting/early stopping/inter-annotator agreement |
| 5 | **Retrieval quality metrics** — NDCG, MAP, Recall@k, and MRR, and the decision tree for picking among them | Clean — full explanation in [Part 2, Section 8](part-2-inference-and-multimodal.md#8-retrieval-quality-metrics) | **Fixed** — Ultra Fast Learn's evaluation section (Section 5) now carries the NDCG/MAP/Recall@k/MRR comparison table and decision-order bullets standing in for the decision tree |

These four were a materially larger hop-2 gap than any other domain's
report had found (three topics for Domain 1, four for Domain 4 — but
Domain 4's four hop-2 topics were narrower single distinctions; here,
three of the four were entire multi-page subsections with their own
decision flowcharts and comparison tables, dropped as a whole unit).
Given Domain 3 is the highest-weight domain, closing this gap removed a
materially higher chance than other domains' remaining gaps posed of an
exam-taker relying solely on the last-minute Ultra Fast Learn cram sheet
encountering a question on fine-tuning efficiency technique selection,
RLHF, dataset sizing, or retrieval-metric selection with zero cram-sheet
coverage.

## What's confirmed clean

Beyond the sections above, spot-checks of AWS service names and numeric
thresholds found no gaps in:

- The customization decision framework (RAG vs. prompt engineering vs.
  fine-tuning vs. continued pre-training) — full coverage at both hops.
- Amazon Bedrock features: Guardrails' five rule types, Agents vs. Prompt
  Flows vs. prompt chaining, and the on-demand/provisioned-throughput/
  batch decision guide — full coverage at both hops (Ultra Fast Learn
  Section 3).
- AWS infrastructure: Trainium/Inferentia, SageMaker JumpStart,
  auto-scaling's five knobs and cooldown-tuning table, and the four
  inference-failure/RAG-troubleshooting scenario sets — full coverage at
  both hops (Ultra Fast Learn Sections 6 and 8), including Part 3's
  resilience-pattern vocabulary (circuit breaker, jitter, flapping).
- Evaluation benchmarks other than the four retrieval-ranking metrics
  above (MMLU, ARC, HumanEval, GSM8K, BERTScore, perplexity, toxicity) —
  full coverage at both hops (as, now, are the four retrieval-ranking
  metrics themselves — see the "Findings 2–5" update above).

## Recommendation

1. ~~Fix the hop-1 gap (Finding 1)~~ — **done**, in Part 2, Section 4,
   which now states the reuse-over-duplicate decision rule Ultra Fast
   Learn already captured independently.
2. ~~Backfill the four hop-2 gaps (Findings 2–5) into Ultra Fast
   Learn~~ — **done, 2026-09-09**, following the same compact
   bullet/table style already used for the customization trade-off table
   and RAG failure-mode triage.
3. Both fixes are kept accurate by the accompanying test suite
   (`tests/test_domain_3_coverage_verification_report.py` plus
   `tests/test_domain_3_fast_track_kendra_genai_index_reuse_gap.py` for
   Finding 1), which fails loudly if either regresses so the report can
   be updated to match, rather than silently going stale.
