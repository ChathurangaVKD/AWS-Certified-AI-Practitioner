# Domain 4 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete · **Verified:** 2026-09-09

## What this report is

`docs/DOCUMENTATION_STRUCTURE.md` states a coverage guarantee for every
domain's condensed layer: "every testable concept the full domain guide
covers is retained somewhere in the condensed layer — only narrative
explanation, extra worked examples, and repetition are cut, not
exam-relevant content." For Domain 4 specifically, that guarantee had not
been technically verified — it was flagged as a claim requiring spot-check
against the source material. This report is that spot-check: a
line-by-line comparison of four major sections of
[`docs/domain-4-guidelines-for-responsible-ai.md`](../domain-4-guidelines-for-responsible-ai.md)
(2,250 lines) against
[`docs/domain-4-fast-track/README.md`](README.md) (796 lines) and
[`docs/domain-4-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md)
(158 lines), confirming whether every exam-relevant fact, decision
criterion, AWS service, metric, and concept survives both condensation
hops.

This is a correctness audit, not new content authoring: it documents what
was checked, what verified clean, and where a real gap was found. It does
not itself change `README.md` or `ULTRA-FAST-LEARN.md`.

## Sections spot-checked

| # | Full guide section | Fast Track section | Ultra Fast Learn section |
|---|---|---|---|
| 1 | [§1 Core dimensions of responsible AI](../domain-4-guidelines-for-responsible-ai.md#1-core-dimensions-of-responsible-ai) (line 56) | [§1](README.md#1-core-dimensions-of-responsible-ai) (line 59) | [§1](ULTRA-FAST-LEARN.md#1-dimensions-of-responsible-ai) (line 22) |
| 2 | [§2 Identifying bias and fairness issues](../domain-4-guidelines-for-responsible-ai.md#2-identifying-bias-and-fairness-issues-in-training-data-and-model-outputs) (line 229), incl. the "representativeness vs. demographic fairness bias" worked example (line 406) | [§2](README.md#2-bias-and-fairness) (line 133) | [§2](ULTRA-FAST-LEARN.md#2-common-bias-sources) (line 42), [§3](ULTRA-FAST-LEARN.md#3-fairness-metrics-by-use-case-stage) (line 59) |
| 3 | [§3 AWS tools for responsible AI](../domain-4-guidelines-for-responsible-ai.md#3-aws-tools-for-responsible-ai) (line 544), incl. the Amazon A2I worked example (line 609) and the Clarify/Guardrails layering worked example (line 699) | [§3](README.md#3-aws-tools-for-responsible-ai) (line 244) | [§5](ULTRA-FAST-LEARN.md#5-amazon-sagemaker-clarify-capabilities) (line 107) — Clarify only |
| 4 | [§4 Legal and ethical considerations](../domain-4-guidelines-for-responsible-ai.md#4-legal-and-ethical-considerations) (line 960) | [§4](README.md#4-legal-and-ethical-considerations) (line 362) | *no corresponding section exists* |

## Result: Fast Track (full guide → Fast Track hop)

**Verified clean, with one narrow exception.** For all four sections
above, essentially every exam-relevant fact, decision criterion, AWS
service, metric, and named constraint in the full guide is present in the
Fast Track, condensed to tables and shortened exam tips. Specifically
confirmed:

- The full 8-dimension table, the fast-disambiguation callouts
  ("explainability" vs. "transparency", "fairness" vs. "veracity and
  robustness"), and both Mermaid diagrams (dimension relationships,
  dimension-to-tool mapping) — all retained in Fast Track §1.
- The bias-vs-variance terminology trap, all 6 bias categories (sampling,
  measurement, label/human, historical, exclusion, aggregation), the
  bias-detection-metrics-by-lifecycle-stage table, all three mitigation
  stages (pre-/in-/post-processing), and the full **representativeness
  bias vs. demographic fairness bias** worked example — including why a
  clean Clarify report can still miss a thin/absent deployment
  segment — all retained in Fast Track §2.
- The 5-tool comparison table (Clarify, Model Cards, Guardrails, AI
  Service Cards, A2I), the Guardrails 5-capability table (denied topics,
  content filters, word filters, sensitive information filters,
  contextual grounding checks), the two layering patterns (one model/two
  lifecycle stages vs. two components/two model types), and the
  RAG-native fairness approach (retrieval corpus curation, grounding
  checks, source citation) — all retained in Fast Track §3.
- All four legal/ethical categories (IP, data privacy, toxicity,
  environmental impact) and every named AWS mitigation (IP
  indemnification, Guardrails sensitive information filters, Amazon
  Macie, AWS Customer Carbon Footprint Tool, Well-Architected
  Sustainability Pillar) — all retained in Fast Track §4.

**One item was dropped even at this hop — now fixed.** The full guide's
Amazon A2I worked example (line 661) names three A2I building blocks: a
**worker task template** (the reviewer-facing UI), a **flow definition**
(the activation-condition wiring), and a **private workforce** (via
Amazon Cognito). Fast Track §3's condensed version of the same worked
example (README.md line 299–310) already retained `StartHumanLoop`, the
flow definition, the private-workforce/Cognito/Mechanical-Turk
distinction, and the Model-Monitor drift signal, but never named the
**worker task template** component — a narrow, single-term gap (the
other two A2I building blocks and the routing logic around them were
intact), but a named, testable AWS A2I concept, not narrative. This has
since been backfilled: Fast Track §3 now names the **worker task
template** alongside the flow definition and private workforce,
condensed verbatim from the same full-guide worked example.

## Result: Ultra Fast Learn (Fast Track → Ultra Fast Learn hop)

**Two significant coverage gaps found**, plus a structural gap relative to
sibling domains. `ULTRA-FAST-LEARN.md` is deliberately far more
compressed than the Fast Track (158 lines vs. 796), and its own intro says
it is "bullets and tables only — no prose, no worked examples, no
mini-quizzes" by design — that trim is expected and consistent with the
guarantee (narrative and worked examples are the parts allowed to go).
However, the following are *named AWS tools/capabilities and a whole
category of exam content*, not narrative, and are missing entirely rather
than condensed:

1. **Four of the five AWS responsible-AI tools have no capability detail
   anywhere.** `ULTRA-FAST-LEARN.md` §5 is titled "Amazon SageMaker
   Clarify capabilities" and covers only Clarify. SageMaker Model Cards,
   AI Service Cards, Guardrails for Amazon Bedrock, and Amazon A2I appear
   *only* as one-line "Primary AWS tool" values inside the §1 dimensions
   table (e.g., "Guardrails (denied topics)"). None of the following
   survives anywhere in the file: Guardrails' **word filters** or
   **sensitive information filters** capabilities (2 of its 5 named
   capabilities — only denied topics, content filters, and contextual
   grounding surface, and only as table-cell labels, not as a capability
   list); the Amazon A2I mechanics of `StartHumanLoop`, **flow
   definition**, **worker task template**, **private workforce**, or
   **Mechanical Turk**; and the Model-Card-vs-AI-Service-Card
   self-authored/AWS-authored distinction (the file names both terms once
   each in the dimensions table but never states the distinguishing
   exam tip). Grepping the file for `word filters|sensitive information
   filters|StartHumanLoop|worker task template|private workforce|Mechanical
   Turk|you fill it in` outside this report returns nothing.

2. **The entire "Legal and ethical considerations" category is absent.**
   Neither the table of contents nor any section of
   `ULTRA-FAST-LEARN.md` mentions **intellectual property (IP)
   indemnification**, **GDPR**, **data residency**, **toxicity**, or
   **environmental impact** (the **AWS Customer Carbon Footprint Tool**,
   the **Well-Architected Sustainability Pillar**). This is a full,
   named section in both the full guide (line 960, with its own mini-quiz)
   and the Fast Track (line 362, with its own exam tip and AWS example
   row) — a scored ~14%-of-exam domain with an entire legal/ethical
   category untested by the cram sheet is a genuine, checkable
   regression, not a narrative trim.

3. **Structural gap versus every sibling domain's Ultra Fast Learn.**
   Domains 1, 2, 3, and 5 each close their `ULTRA-FAST-LEARN.md` with a
   "Rapid-fire key terms" section and a "Common exam traps checklist"
   section (see, e.g.,
   [`docs/domain-1-fast-track/ULTRA-FAST-LEARN.md`](../domain-1-fast-track/ULTRA-FAST-LEARN.md#rapid-fire-key-terms)).
   Domain 4's `ULTRA-FAST-LEARN.md` has neither — it jumps from
   "6. Monitoring checklist" straight to "Where each row comes from." Both
   the full guide's glossary (30+ terms) and the Fast Track's own
   "Rapid-fire key terms" (README.md line 568) and "Common exam traps
   checklist" (README.md line 687) sections exist and could be condensed
   the same way the other four domains' cram sheets already are — their
   absence here is inconsistent with the rest of the repository's
   established Ultra Fast Learn format, independent of any single
   dropped fact.

Corroborating evidence: `ULTRA-FAST-LEARN.md`'s own "Where each row comes
from" table (line 142–149) maps its six numbered sections back to Fast
Track §1, §2 (twice), §3, §5, and the monitoring section — it never lists
a source row for Fast Track §4 (Legal and ethical considerations), and its
§5 row cites Fast Track §3 only for the Clarify slice of that section, not
Guardrails, Model Cards, AI Service Cards, or A2I. This is consistent with
those items having been dropped when the cram sheet was condensed, rather
than merged elsewhere under a different heading.

## Recommendation

Backfill `ULTRA-FAST-LEARN.md` with condensed additions (tables/bullets
only, no prose/worked examples, consistent with the file's existing
format), sourced verbatim from Fast Track §3 and §4 (no new facts to
author):

1. Expand §5 into an "AWS tools for responsible AI" section: a short tool
   table (Clarify, Model Cards, AI Service Cards, Guardrails, A2I) with
   the self-authored/AWS-authored exam tip, a Guardrails 5-capability
   table (adding word filters and sensitive information filters), and an
   A2I mechanics bullet list (`StartHumanLoop`, flow definition, worker
   task template, private workforce vs. Mechanical Turk) — keeping the
   existing Clarify-capabilities bullets as a subsection.
2. Add a new "Legal and ethical considerations" section (IP
   indemnification, GDPR/data privacy/data residency, toxicity,
   environmental impact/Carbon Footprint Tool/Sustainability Pillar).
3. Add "Rapid-fire key terms" and "Common exam traps checklist" sections
   matching the format already used in Domains 1, 2, 3, and 5's Ultra Fast
   Learn cram sheets.
4. ~~Separately, add the missing **worker task template** term to Fast
   Track §3's condensed A2I worked-example pattern (README.md line
   299–310), closing the one hop-1 gap this report also found.~~ **Done**
   — Fast Track §3 now names the worker task template alongside the flow
   definition and private workforce.

Each addition should also extend `tests/test_domain_4_ultra_fast_learn.py`
with assertions for the newly-covered terms, so a future edit cannot
silently drop this content again. This backfill is scoped as follow-up
work rather than folded into this report, since `ULTRA-FAST-LEARN.md`'s
stated line count is cross-checked by exact-total assertions in
`tests/test_documentation_structure.py` (per-domain Fast Track totals and
the repository-wide grand total) that must be updated in lockstep with
any line-count change to that file.
