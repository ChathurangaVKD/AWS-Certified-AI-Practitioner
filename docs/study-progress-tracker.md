# Study Progress Tracker

This series gives you **259 total self-assessment items** to practice
with: 129 domain-scoped [practice questions](exam-preparation-strategy.md#1-exam-format-and-time-management)
(spread across the five domain guides), 35 embedded
[mini-quizzes](exam-preparation-strategy.md#mini-quizzes-formative-checks-while-you-study),
30 [cross-domain scenario questions](cross-domain-scenario-questions.md),
and two independent 65-question mock exams
([`full-length-mock-exam.md`](full-length-mock-exam.md) and
[`mock-exam.md`](mock-exam.md)). What none of those pages give you is a
single place to *log* your scores across multiple attempts and notice
which domains or topics keep coming up short — this page is that place.

Copy the table in [Section 1](#1-attempt-log-template) into your own notes
(a spreadsheet, a local Markdown file, or directly into a copy of this
file) and add one row every time you finish a practice-question set, a
mini-quiz pass, a cross-domain scenario set, or a mock exam. The table
ships empty — column headers only — because your scores are the whole
point; there is nothing to pre-fill.

## 1. Attempt log template

| Attempt # | Assessment / question set | Date | # Correct | # Total | % Score | Domain breakdown (if available) | Time spent | Weak-area notes |
|---|---|---|---|---|---|---|---|---|

*(Add one row per attempt below the header — the table intentionally ships
with no rows yet.)*

**How to fill this in:**

- **Attempt #** — a running count (1, 2, 3, …) *per assessment*, not
  across all assessments — e.g., your second attempt at the Domain 3
  practice questions and your first attempt at `mock-exam.md` are both
  "Attempt 1" for their own row.
- **Assessment / question set** — name it specifically enough to compare
  attempts later: "Domain 3 practice questions," "Domain 1 mini-quizzes,"
  "Cross-domain scenario questions 1–25," or "`full-length-mock-exam.md`."
- **Date** — when you took it, so you can see how scores change over time
  (see [Section 4](#4-interpreting-score-trends-across-attempts)).
- **# Correct / # Total** — your raw count, e.g. `11 / 13` for a Domain 1
  practice-question pass.
- **% Score** — `# Correct ÷ # Total`, so you can compare sets of
  different sizes on the same scale. For a mock exam, also compare this
  against the exam's own **700/1000 passing bar** (roughly **54/65 ≈ 83%**
  as a rough proxy per the [exam prep guide](exam-preparation-strategy.md#1-exam-format-and-time-management) —
  the real scoring scale is nonlinear, so treat this as a directional
  signal, not an exact conversion).
- **Domain breakdown (if available)** — only the two mock exams and the
  cross-domain scenario questions are mixed across domains; fill this in
  using their own scoring worksheets (e.g. the [score-band remediation
  table](full-length-mock-exam.md#score-band-remediation-by-domain)'s
  per-domain worksheet). Leave it blank for a single-domain practice-question
  or mini-quiz attempt — the whole row is already one domain.
- **Time spent** — wall-clock minutes. Comparing this against the
  [exam's pacing guidance](exam-preparation-strategy.md#1-exam-format-and-time-management)
  (~1.4 minutes/question average) tells you whether a low score came from
  a knowledge gap or from rushing.
- **Weak-area notes** — the specific topic(s) behind your wrong answers,
  not just "Domain 3." Write down the concept (e.g. "confused RAG with
  fine-tuning," "missed the CloudTrail vs. Config distinction") so it's
  searchable across attempts.

## 2. Example: turning a recurring weak area into targeted study

The point of logging more than one attempt is to catch a weak area that
keeps recurring, then act on it — instead of re-reading a whole domain
guide (1,300–5,500+ lines) every time a score dips.

**Worked scenario (illustrative only — no scores from this scenario belong
in your own log):** suppose your first attempt at the Domain 3 practice
questions logs a weak-area note that you kept picking fine-tuning in
scenarios where RAG was the better fit, with a % Score below roughly 75%.
You retake the same practice questions later and log a second row: the
% Score is still below 75%, and the weak-area note this time is the same
fine-tuning-vs-RAG confusion plus a missed Bedrock Guardrails question.

**The rule to apply:** if a domain's score stays below roughly 75%
(a conservative stand-in for the exam's 700/1000 passing bar) across
**two consecutive attempts** on the same assessment, stop retaking it cold
and go re-read the specific sections most likely to be behind the gap
before your next attempt. For the scenario above, the recurring theme is
the customization decision and a Bedrock feature — both covered in
Domain 3:

- Re-read [Domain 3, §4 — Fine-tuning vs. continued pre-training vs. RAG vs. prompt engineering](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering),
  which walks through the exact prompt-engineering → RAG → fine-tuning →
  continued-pre-training decision spectrum the wrong answers above confused.
- Re-read [Domain 3, §5 — Amazon Bedrock features](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features),
  which covers Guardrails alongside Agents, Knowledge Bases, and
  provisioned throughput.
- Then retake the Domain 3 practice questions untimed, reviewing every
  explanation, before moving on to a mock exam.

This mirrors the [full-length mock exam's score-band remediation
table](full-length-mock-exam.md#score-band-remediation-by-domain) and the
[exam prep guide's topic-based review quick reference](exam-preparation-strategy.md#6-topic-based-review-quick-reference):
both point a low score at specific sections rather than "re-read
everything." Use whichever of the two matches your situation — the
score-band table if a whole mock-exam domain is weak, the topic-based
reference if you can already name the narrower concept.

## 3. Quick reference: where to go after two low scores in a domain

| Domain | If scores stay low after two attempts, go to |
|---|---|
| 1 — Fundamentals of AI and ML | [Domain 1 score-band remediation](full-length-mock-exam.md#score-band-remediation-by-domain) |
| 2 — Fundamentals of Generative AI | [Domain 2 score-band remediation](full-length-mock-exam.md#score-band-remediation-by-domain) |
| 3 — Applications of Foundation Models | [Domain 3 score-band remediation](full-length-mock-exam.md#score-band-remediation-by-domain), or directly [§4](domain-3-applications-of-foundation-models.md#4-fine-tuning-vs-continued-pre-training-vs-rag-vs-prompt-engineering) / [§5](domain-3-applications-of-foundation-models.md#5-amazon-bedrock-features) as in the worked example above |
| 4 — Guidelines for Responsible AI | [Domain 4 score-band remediation](full-length-mock-exam.md#score-band-remediation-by-domain) |
| 5 — Security, Compliance, and Governance | [Domain 5 score-band remediation](full-length-mock-exam.md#score-band-remediation-by-domain) |
| Any domain, once you know the specific topic | [Exam prep guide, §6 — Topic-based review quick reference](exam-preparation-strategy.md#6-topic-based-review-quick-reference) |

## 4. Interpreting score trends across attempts

A single score tells you where you stand today; logging every attempt in
[Section 1](#1-attempt-log-template) lets you read the *trend*, which is a
better signal of exam readiness than any one number:

- **Rising and converging** — each retake of the same assessment scores
  higher than the last, and the gap between attempts shrinks. This is the
  strongest available signal that a weak area has actually closed, not
  just that you memorized that attempt's specific questions.
- **Flat or recurring** — the same domain or topic scores low across two
  or more attempts with no improvement. Don't retake the same set a third
  time expecting a different result — follow [Section 2](#2-example-turning-a-recurring-weak-area-into-targeted-study)'s
  rule and go re-read the targeted sections first.
- **High variance between attempts** — a domain swings widely (e.g. 90%
  then 60% then 85%) rather than trending in either direction. This
  usually signals inconsistent pacing or guessing rather than a knowledge
  gap; cross-check the **Time spent** column — rushed attempts often
  correlate with the low scores in a variance pattern like this.
- **Strong on domain practice questions, weak on mock exams** — this
  points at the cross-domain and scenario-blending skill the [mock
  exams](full-length-mock-exam.md) and
  [cross-domain scenario questions](cross-domain-scenario-questions.md)
  test, not at any single domain's content. Work through the scenario
  questions specifically rather than re-reading a domain guide again.
- **Close to but under the 700/1000 passing bar on a mock exam** — per the
  [exam prep guide's study plans](exam-preparation-strategy.md#5-study-plans),
  retake the *other* mock exam next (if you scored `full-length-mock-exam.md`,
  take `mock-exam.md` next, and vice versa) rather than immediately
  retaking the same one — a fresh, previously-unseen question set is a
  more honest readiness check than a set you've already reviewed the
  answer key for.
