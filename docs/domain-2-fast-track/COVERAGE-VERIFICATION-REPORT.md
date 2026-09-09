# Domain 2 Fast Track / Ultra Fast Learn: coverage verification report

**Status:** technical verification complete · **Verified:** 2026-09-09

## What this report is

`docs/DOCUMENTATION_STRUCTURE.md` states a coverage guarantee for every
domain's condensed layer: "every testable concept the full domain guide
covers is retained somewhere in the condensed layer — only narrative
explanation, extra worked examples, and repetition are cut, not
exam-relevant content." For Domain 2 specifically, that guarantee had not
been technically verified — it was flagged as a claim requiring spot-check
against the source material. This report is that spot-check: a
line-by-line comparison of five major sections of
[`docs/domain-2-fundamentals-of-generative-ai.md`](../domain-2-fundamentals-of-generative-ai.md)
(2,213 lines) against
[`docs/domain-2-fast-track/README.md`](README.md) (851 lines) and
[`docs/domain-2-fast-track/ULTRA-FAST-LEARN.md`](ULTRA-FAST-LEARN.md)
(284 lines), confirming whether every exam-relevant fact, decision
criterion, AWS service, metric, and concept survives both condensation
hops.

This is a correctness audit, not new content authoring: it documents what
was checked, what verified clean, and where a real gap was found. It does
not itself change `README.md` or `ULTRA-FAST-LEARN.md`.

## Sections spot-checked

| # | Full guide section | Fast Track section | Ultra Fast Learn section |
|---|---|---|---|
| 1 | [§1 Generative AI core concepts](../domain-2-fundamentals-of-generative-ai.md#1-generative-ai-core-concepts) (line 52), incl. the "Choosing an embedding model" decision tree (line 215) | [§1](README.md#1-transformer-architecture-and-core-concepts) (line 69) | [§1](ULTRA-FAST-LEARN.md#1-transformer-mechanics) (line 28) |
| 2 | [§2 LLM lifecycle basics](../domain-2-fundamentals-of-generative-ai.md#2-llm-lifecycle-basics) (line 300) | [§2](README.md#2-foundation-model-and-llm-lifecycle) (line 148) | *no corresponding section exists* |
| 3 | [§3 Advantages and disadvantages of generative AI](../domain-2-fundamentals-of-generative-ai.md#3-advantages-and-disadvantages-of-generative-ai) (line 442) | [§3](README.md#3-advantages-and-disadvantages-of-generative-ai) (line 204) | [§6 Common GenAI risks](ULTRA-FAST-LEARN.md#6-common-genai-risks) (line 149) — disadvantages only |
| 4 | [§4 Business use cases for generative AI](../domain-2-fundamentals-of-generative-ai.md#4-business-use-cases-for-generative-ai) (line 541) | [§4](README.md#4-business-use-cases) (line 237) | *no corresponding section exists* |
| 5 | [§5 AWS generative AI services](../domain-2-fundamentals-of-generative-ai.md#5-aws-generative-ai-services-and-capabilities) (line 626), [§6 Prompt engineering fundamentals](../domain-2-fundamentals-of-generative-ai.md#6-prompt-engineering-fundamentals) (line 743), and [§7 Foundation model selection criteria](../domain-2-fundamentals-of-generative-ai.md#7-foundation-model-selection-criteria) (line 988), incl. the Nova variant comparison (line 1038) | [§5](README.md#5-aws-generative-ai-services-and-capabilities) (line 279), [§6](README.md#6-prompt-engineering-fundamentals) (line 330), [§7](README.md#7-foundation-model-selection-criteria) (line 435) | [§7](ULTRA-FAST-LEARN.md#7-aws-service-use-case-table) (line 167), [§3](ULTRA-FAST-LEARN.md#3-prompt-engineering-techniques) (line 81), [§4](ULTRA-FAST-LEARN.md#4-inference-parameters) (line 103), [§2](ULTRA-FAST-LEARN.md#2-foundation-model-selection-criteria) (line 52) |

## Result: Fast Track (full guide → Fast Track hop)

**Verified clean — no gaps found.** For all five rows above, every
exam-relevant fact, decision criterion, AWS service, metric, and named
constraint in the full guide is present in the Fast Track, condensed to
tables and shortened exam tips but with no testable content dropped.
Specifically confirmed:

- The core-vocabulary set (token, embedding, vector, vector database,
  prompt, FM, LLM, multimodal model), the transformer pipeline diagram,
  the self-attention "it" → "cat" worked weight example, and the full
  "Choosing an embedding model" decision tree (general-purpose →
  domain-specific → fine-tuned, with cost/latency/accuracy notes at each
  branch) — all retained in Fast Track §1.
- The full 6-stage FM/LLM lifecycle (scope → select → adapt & customize →
  evaluate → deploy & integrate → monitor), all four adaptation options
  under stage 3 (prompt engineering, RAG, fine-tuning, continued
  pre-training) each mapped to its AWS service, the iterative loop-back
  note, and the RAG-vs-fine-tuning-vs-full-pretraining exam tip — all
  retained in Fast Track §2.
- All four advantages (**Adaptability**, **Responsiveness**, Simplicity/
  creativity, Scalability) and all five disadvantages (hallucination,
  interpretability, inaccuracy, nondeterminism, cost/compute intensity),
  plus the hallucination-vs.-inaccuracy exam-tip distinction — all
  retained in Fast Track §3.
- All five named business use cases (**Content creation**, summarization,
  chatbots, code generation, search) plus the "other exam-relevant use
  cases" list (translation, personalization, data augmentation,
  text-to-image/video) — all retained in Fast Track §4.
- Every Amazon Bedrock capability (Knowledge Bases, Agents, Guardrails,
  Model Evaluation, Titan, Nova, Provisioned Throughput), both Amazon Q
  variants, SageMaker JumpStart, and PartyRock; all four prompting
  techniques plus fine-tuning as contrast, prompt template, and prompt
  injection; all five inference parameters and the temperature/top-p/
  top-k interaction table; all six foundation-model selection criteria and
  the full seven-variant Nova comparison table — all retained in Fast
  Track §5–§7.

## Result: Ultra Fast Learn (Fast Track → Ultra Fast Learn hop)

**Four coverage gaps found.** `ULTRA-FAST-LEARN.md` is deliberately far
more compressed than the Fast Track (284 lines vs. 851), and its own intro
says it is "bullets and tables only — no prose, no worked examples, no
mini-quizzes" by design — that trim is expected and consistent with the
guarantee (narrative and worked examples are the parts allowed to go).
However, four items that are *named lifecycle stages, decision criteria,
and use cases*, not narrative, are missing entirely rather than condensed:

1. **The foundation model/LLM lifecycle is entirely absent.** Neither the
   table of contents (line 13–24) nor any section of
   `ULTRA-FAST-LEARN.md` names the 6-stage lifecycle from the full guide's
   §2 and the Fast Track's §2. "Continued pre-training" — a named AWS
   capability (**Amazon Bedrock continued pre-training**) and a distinct
   customization option from fine-tuning — does not appear anywhere in the
   file. Neither does "Scope the use case," "Deploy and integrate," or the
   "Monitor" stage with its CloudWatch/Guardrails tooling. Grepping the
   file for `continued pre-training|Scope the use case` outside this
   report returns nothing.

2. **The "Choosing an embedding model" decision tree is entirely absent.**
   The full guide (line 215–254) and the Fast Track (line 131–146) both
   carry the three-question decision tree (general-purpose sufficient? →
   domain specialized? → fine-tuning justified?) with a cost/latency/
   accuracy note at each branch. `ULTRA-FAST-LEARN.md` §1 (Transformer
   mechanics) covers tokenization, embeddings, and vectors as
   *definitions* but never states the *decision criterion* for choosing
   between a general-purpose, domain-specific, or fine-tuned embedding
   model — a genuine cost/accuracy trade-off the exam tests, not just
   vocabulary.

3. **The four advantages of generative AI are entirely absent.**
   `ULTRA-FAST-LEARN.md` §6 ("Common GenAI risks," line 149) covers only
   the *disadvantages* side of the full guide's §3 (hallucination,
   interpretability, inaccuracy, nondeterminism, cost/compute) — it
   carries no equivalent table or bullet list for **Adaptability**,
   **Responsiveness**, Simplicity/creativity, or Scalability, even though
   these are exam-testable (the full guide's own mini-quiz asks which
   advantage a scenario illustrates) and both other tiers retain them in
   full.

4. **The business use cases section is entirely absent.** Neither the
   table of contents nor any section of `ULTRA-FAST-LEARN.md` names
   content creation, summarization, chatbots, code generation, or search
   as a use-case category, nor the "other exam-relevant use cases" list
   (translation, personalization, data augmentation, text-to-image/video).
   The only surviving trace is the single term "semantic search" inside
   the unrelated "Rapid-fire key terms" glossary (line 208) — the
   use-case-to-AWS-service mapping itself (e.g., code generation → Amazon
   Q Developer) is gone.

Corroborating evidence: `ULTRA-FAST-LEARN.md`'s own "Where each row comes
from" table (line 265–276) maps its seven numbered sections back to full
guide §1, §3, §5, §6, §7, and the cost/latency subsection and comparison
table — it never lists a source row for full guide §2 (LLM lifecycle) or
§4 (business use cases), and never mentions the "Choosing an embedding
model" subsection or the advantages half of §3. This is consistent with
those four items having been dropped when the file was condensed, rather
than merged elsewhere under a different heading.

## Recommendation

Backfill `ULTRA-FAST-LEARN.md` with four condensed additions (tables/
bullets only, no prose/worked examples, consistent with the file's
existing format), sourced verbatim from Fast Track §1, §2, §3, and §4 (no
new facts to author):

1. A "Foundation model/LLM lifecycle" table (the 6 stages, the 4
   adaptation options under stage 3, and each stage's AWS service),
   likely as a new numbered section alongside the existing 7.
2. A "Choosing an embedding model" mini decision table (general-purpose /
   domain-specific / fine-tuned, with the deciding question and
   cost/accuracy note for each), folded into §1 (Transformer mechanics)
   next to the existing embedding/vector definitions.
3. An "Advantages of generative AI" table (adaptability, responsiveness,
   simplicity/creativity, scalability), added next to or merged into §6
   (renaming it to cover both sides, matching the full guide's and Fast
   Track's "Advantages and disadvantages" framing).
4. A "Business use cases" table (content creation, summarization,
   chatbots, code generation, search, plus the secondary use-case list),
   likely as a new numbered section.

Each addition should also extend the "Common exam traps checklist" and
"Rapid-fire key terms" in `ULTRA-FAST-LEARN.md` with the newly-covered
terms, and the "Where each row comes from" table with the new sections'
source rows, so a future edit cannot silently drop this content again.
This backfill is scoped as follow-up work rather than folded into this
report, since `ULTRA-FAST-LEARN.md`'s stated line count is cross-checked
by exact-total assertions in `tests/test_documentation_structure.py`
(per-domain Fast Track totals and the repository-wide grand total) that
must be updated in lockstep with any line-count change to that file.
