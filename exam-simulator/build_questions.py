#!/usr/bin/env python3
"""Parse the markdown mock exams in ../docs into questions.js for the simulator."""
import json, re, pathlib
from explain_structure import structure

DOCS = pathlib.Path(__file__).resolve().parent.parent / "docs"
SOURCES = [("full-length-mock-exam.md", "Full-Length Mock Exam", "## Mock exam questions", "## 4. Answer key"),
           ("mock-exam.md", "Mock Exam B", "## Mock exam questions", "## Answer key and explanations")]
DOMAINS = {1: "Fundamentals of AI and ML", 2: "Fundamentals of Generative AI",
           3: "Applications of Foundation Models", 4: "Guidelines for Responsible AI",
           5: "Security, Compliance, and Governance"}

def squash(s): return re.sub(r"\s+", " ", s).strip()

def parse(fname, label, qmark, amark):
    text = (DOCS / fname).read_text()
    qs = text[text.index(qmark):text.index(amark)]
    ans = text[text.index(amark):]
    ans = ans.split("## After you finish")[0].split("## 5.")[0]
    out = {}
    for m in re.finditer(r"^(\d+)\. (.*?)(?=^\d+\. |\Z)", qs, re.S | re.M):
        n, body = int(m.group(1)), m.group(2)
        parts = re.split(r"^\s*([A-E])\. ", body, flags=re.M)
        stem = squash(parts[0])
        opts = {parts[i]: squash(parts[i + 1]) for i in range(1, len(parts) - 1, 2)}
        if len(opts) < 2: continue
        out[n] = {"q": stem, "options": opts}
    for m in re.finditer(r"^(\d+)\. \*\*(.*?)\*\*(.*?)(?=^\d+\. \*\*|\Z)", ans, re.S | re.M):
        n = int(m.group(1))
        if n not in out: continue
        head, rest = m.group(2), squash(m.group(3))
        letters = re.match(r"([A-E](?:(?:,| and|,? and) ?[A-E])*)", head)
        correct = re.findall(r"[A-E]", letters.group(1))
        dm = re.search(r"Domain (\d)", head + " " + rest)
        out[n]["answer"] = correct
        out[n]["explanation"] = re.sub(r"\s*\(Domain \d\)\s*$", "", squash(head.split("—", 1)[-1] + " " + rest if "—" in head else rest))
        out[n]["domain"] = int(dm.group(1)) if dm else 0
    res = []
    for n in sorted(out):
        q = out[n]
        assert "answer" in q and q["domain"], (fname, n)
        assert all(a in q["options"] for a in q["answer"]), (fname, n)
        q.update(id=f"{fname[:4]}-{n}", source=label,
                 multi=len(q["answer"]) > 1, domainName=DOMAINS[q["domain"]])
        res.append(q)
    return res

allq = [q for s in SOURCES for q in parse(*s)]

def load_extra():
    """Hand-written edge-case questions in extra-questions/domain-N.json (already structured: why / others)."""
    out = []
    for f in sorted((pathlib.Path(__file__).resolve().parent / "extra-questions").glob("domain-*.json")):
        for i, x in enumerate(json.load(open(f)), 1):
            opts, ans = x["options"], x["answer"]
            assert 2 <= len(opts) <= 5 and ans and all(a in opts for a in ans), (f.name, i)
            covered = [l for o in x["others"] for l in o["l"]]
            assert sorted(covered) == sorted(k for k in opts if k not in ans), (f.name, i, "others must cover every wrong option once")
            expl = " ".join(x["why"] + [f"{'/'.join(o['l'])}: {o['t']}" for o in x["others"]])
            out.append(dict(id=f"x{x['domain']}-{i}", q=x["q"], options=opts, answer=ans, explanation=expl,
                            why=x["why"], others=x["others"], domain=x["domain"], domainName=DOMAINS[x["domain"]],
                            source="Edge-case bank", topic=x.get("topic", ""), multi=len(ans) > 1))
    return out
allq += load_extra()
for q in allq:
    if "why" not in q:
        q["why"], q["others"] = structure(q["explanation"], q["answer"], q["options"][q["answer"][0]])
(pathlib.Path(__file__).parent / "questions.js").write_text(
    "window.QUESTIONS = " + json.dumps(allq, indent=1, ensure_ascii=False) + ";\n")
from collections import Counter
print(len(allq), Counter(q["domain"] for q in allq), sum(q["multi"] for q in allq))
