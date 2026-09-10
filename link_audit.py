import re, os, sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))

TARGET_FILES = [
    "README.md",
    "docs/aws-service-index.md",
    "docs/aws-service-decision-guide.md",
    "docs/cross-domain-concept-map.md",
    "docs/cross-domain-scenario-questions.md",
    "docs/case-study-ai-system-lifecycle.md",
    "docs/exam-preparation-strategy.md",
    "docs/GLOSSARY.md",
    "docs/master-glossary.md",
    "docs/study-progress-tracker.md",
    "docs/mock-exam.md",
    "docs/full-length-mock-exam.md",
]

def slugify(heading):
    s = heading.strip().lower()
    s = re.sub(r'`', '', s)
    s = re.sub(r'\*\*', '', s)
    s = re.sub(r'\*', '', s)
    s = re.sub(r'[^\w\s\-]', '', s)
    s = re.sub(r'\s+', '-', s.strip())
    return s

def get_headings(path):
    headings = []
    if not os.path.exists(path):
        return headings
    with open(path, encoding='utf-8') as fh:
        in_code = False
        for line in fh:
            if line.strip().startswith('```'):
                in_code = not in_code
                continue
            if in_code:
                continue
            m = re.match(r'^(#{1,6})\s+(.*)$', line)
            if m:
                headings.append(m.group(2).strip())
    return headings

heading_cache = {}
def get_slugs(path):
    if path not in heading_cache:
        headings = get_headings(path)
        slugs = defaultdict(int)
        result = []
        for h in headings:
            base = slugify(h)
            n = slugs[base]
            slug = base if n == 0 else f"{base}-{n}"
            slugs[base] += 1
            result.append(slug)
        heading_cache[path] = (headings, result)
    return heading_cache[path]

link_pattern = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')

issues = []

for rel in TARGET_FILES:
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        issues.append((rel, 0, "FILE MISSING", rel))
        continue
    with open(path, encoding='utf-8') as fh:
        lines = fh.readlines()
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        for m in link_pattern.finditer(line):
            text, target = m.group(1), m.group(2).strip()
            if target.startswith('http://') or target.startswith('https://') or target.startswith('mailto:'):
                continue
            if '#' in target:
                fpath, anchor = target.split('#', 1)
            else:
                fpath, anchor = target, None
            if fpath == '':
                target_file = path
                target_rel = rel
            else:
                target_file = os.path.normpath(os.path.join(os.path.dirname(path), fpath))
                target_rel = os.path.relpath(target_file, ROOT)
                if not os.path.exists(target_file):
                    issues.append((rel, i, f"BROKEN PATH: [{text}]({target})", target_rel))
                    continue
            if anchor:
                _, slugs = get_slugs(target_file)
                if anchor not in slugs:
                    issues.append((rel, i, f"BROKEN ANCHOR: [{text}]({target}) -> anchor '#{anchor}' not found in {target_rel}", target_rel))

for rel, line, msg, tf in issues:
    print(f"{rel}:{line}: {msg}")
print(f"\nTotal issues: {len(issues)}")
