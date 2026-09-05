# AWS Certified AI Practitioner (AIF-C01) — Study Guide Series

A structured, exam-focused document series for the AWS Certified AI
Practitioner (AIF-C01) certification, maintained automatically by
gd-autopilot.

## Exam domains

| # | Domain | Weight | Doc |
|---|--------|--------|-----|
| 1 | Fundamentals of AI and ML | ~20% | `docs/domain-1-fundamentals-of-ai-and-ml.md` |
| 2 | Fundamentals of Generative AI | ~24% | `docs/domain-2-fundamentals-of-generative-ai.md` |
| 3 | Applications of Foundation Models | ~28% | `docs/domain-3-applications-of-foundation-models.md` |
| 4 | Guidelines for Responsible AI | ~14% | `docs/domain-4-guidelines-for-responsible-ai.md` |
| 5 | Security, Compliance, and Governance for AI Solutions | ~14% | `docs/domain-5-security-compliance-governance.md` |

Each domain document covers the exam guide's task statements in depth, with
worked examples and a set of practice questions (with answers and
explanations) at the end.

## Study plan

**Recommended reading order: Domain 1 → Domain 2 → Domain 3 → Domain 4 →
Domain 5.** The domain guides are numbered for a reason — read them in
order rather than jumping straight to the domain that interests you most:

- **Domain 1 (Fundamentals of AI and ML) is foundational.** Its ML
  lifecycle, learning types, and model-evaluation vocabulary reappear —
  renamed or specialized — in every later domain, so it should be read
  first regardless of prior experience.
- **Domains 2 and 3 assume Domain 1 knowledge.** Fundamentals of
  Generative AI and Applications of Foundation Models both build directly
  on Domain 1's concepts and terminology, so reading Domain 1 first avoids
  backfilling gaps mid-domain.
- **Domains 4 and 5 build on Domains 1–3.** Guidelines for Responsible AI
  and Security, Compliance, and Governance apply the model and
  application concepts from the earlier domains to responsible-use and
  governance scenarios.

For a full explanation of why this order matters, plus ready-made
1-week/2-week/4-week study schedules, see
[`docs/exam-preparation-strategy.md`](docs/exam-preparation-strategy.md#3-recommended-reading-order).

For a quicker "where is X explained?" lookup, see
[`docs/master-glossary.md`](docs/master-glossary.md) — the same
cross-domain term set as a compact alphabetical index, with a `[D1, D3]`
-style domain tag and direct links per term.

For "where does this series discuss AWS service X?" specifically, see
[`docs/aws-service-index.md`](docs/aws-service-index.md) — every AWS
service referenced anywhere across the five domain guides, listed
alphabetically and linked to every section/domain that covers it (e.g.,
find every mention of Amazon SageMaker or Amazon Bedrock in one place).

Each domain guide ends with its own "Key terms" section, but those are
scoped to that guide alone. See [`docs/GLOSSARY.md`](docs/GLOSSARY.md) for
a single alphabetical glossary of every key term across all five domains,
each with a brief definition and a backlink to the domain section that
explains it in full.

Domains 1, 2, 3, and 5 each include their own service comparison table,
scoped to that domain. See
[`docs/aws-service-decision-guide.md`](docs/aws-service-decision-guide.md)
for a consolidated quick reference: a decision flow for choosing between
SageMaker, Bedrock, and purpose-built AI services, plus cross-domain
comparison tables for security/compliance/governance services and
encryption/privacy options.

The domain guides above are written to stand alone, but the exam and
real-world practice both draw on them together. See
[`docs/cross-domain-concept-map.md`](docs/cross-domain-concept-map.md) for
a map of how Domain 1 fundamentals (model evaluation, the ML lifecycle,
bias–variance) and Domain 2 fundamentals (model selection, prompt
engineering) flow into Domain 3 foundation-model applications, Domain 4
responsible-AI concerns, and Domain 5 security/governance requirements —
plus how Domain 3 application choices flow into Domain 4 and Domain 5 in
turn.

Ready to rehearse actual exam conditions? This series ships **two separate,
complementary 65-question mock exams** — same structure and domain
weighting, entirely different questions — so you get two independent
rehearsal passes instead of memorizing one fixed set of answers. Take
[`docs/full-length-mock-exam.md`](docs/full-length-mock-exam.md) first: a
65-question, 90-minute mock exam weighted across all five domains in the
same proportions as the real exam (~20%/24%/28%/14%/14%), mixed in
exam-like order rather than grouped by domain, with timing guidance and a
full answer key with explanations. Once you've reviewed those results,
use [`docs/mock-exam.md`](docs/mock-exam.md) — a second, independently
written 65-question mock exam with the same 90-minute timing and domain
weighting but a completely different question set — as your second
rehearsal pass; see below.

## Cross-domain scenario questions

Every domain guide's practice questions are scoped to that one domain, but
the real exam often is not. See
[`docs/cross-domain-scenario-questions.md`](docs/cross-domain-scenario-questions.md)
for 30 scenario questions that each require knowledge from two or more
domains — for example, choosing a Domain 3 customization method that also
satisfies a Domain 5 security requirement — tagged by difficulty
(beginner/intermediate/advanced) like the domain guides' own questions.
Five of them (26–30) go further and require reasoning across three or
more domains at once.

## End-to-end case study

Each domain guide illustrates its concepts with isolated "AWS example"
scenarios, but a real AI system moves through every domain over its
lifetime. See
[`docs/case-study-ai-system-lifecycle.md`](docs/case-study-ai-system-lifecycle.md)
for a single company building one AI system — from a classical ML model,
through evaluating and customizing a foundation model, to addressing bias
and securing/governing the deployed result — across all five domains.

## Second mock exam

Each domain guide's practice questions are domain-siloed (15–20 questions,
one domain at a time), and [`docs/full-length-mock-exam.md`](docs/full-length-mock-exam.md)
above is a first full rehearsal — but taking the same 65 questions twice
teaches you the answer key, not the material. [`docs/mock-exam.md`](docs/mock-exam.md)
is a second, independently written 65-question mock exam: a different
question set with the same structure — mixed across all five domains in
the exam's own weight proportions (13/16/18/9/9 questions for Domains
1–5), a 90-minute timing budget, and a full answer key with explanations
tagged by domain. Use it as your follow-up rehearsal after
`full-length-mock-exam.md`, ideally after you've re-studied whatever
domains you missed the first time.

## Status

This series is generated and kept current by gd-autopilot's own
discovery → design → implementation → review pipeline. See `docs/` for the
individual domain guides as they're written.