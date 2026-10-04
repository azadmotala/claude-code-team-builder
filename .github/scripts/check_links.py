#!/usr/bin/env python3
"""Check relative links and #anchors in every markdown file in the repo.

External links (http, https, mailto) are skipped: they fail for reasons
that have nothing to do with this repo. Links inside code blocks and
inline code are skipped too, since the templates are full of placeholder
paths.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

MD_LINK = re.compile(r'!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+"[^"]*")?\s*\)')
HTML_LINK = re.compile(r'\b(?:href|src)="([^"]+)"')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
HTML_ANCHOR = re.compile(r'\b(?:id|name)="([^"]+)"')
FENCE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE = re.compile(r'`[^`\n]*`')


def markdown_files():
    for path in sorted(ROOT.rglob('*.md')):
        if '.git' not in path.relative_to(ROOT).parts:
            yield path


def prose_lines(path):
    """Yield (line number, text) for lines outside fenced code blocks."""
    fence = None
    text = path.read_text(encoding='utf-8')
    for number, line in enumerate(text.splitlines(), start=1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker
            elif marker == fence:
                fence = None
            continue
        if fence is None:
            yield number, line


def slugify(heading):
    """Turn a heading into the anchor GitHub generates for it."""
    text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', heading)
    text = text.strip().lower()
    text = re.sub(r'[^\w\- ]', '', text)
    return text.replace(' ', '-')


_anchor_cache = {}


def anchors(path):
    if path not in _anchor_cache:
        found, seen = set(), {}
        for _, line in prose_lines(path):
            match = HEADING.match(line)
            if match:
                slug = slugify(match.group(2))
                count = seen.get(slug, 0)
                seen[slug] = count + 1
                found.add(slug if count == 0 else f'{slug}-{count}')
            found.update(HTML_ANCHOR.findall(line))
        _anchor_cache[path] = found
    return _anchor_cache[path]


def is_external(target):
    return '://' in target or target.startswith(('mailto:', 'tel:', '//'))


def check(path):
    problems = []
    for number, line in prose_lines(path):
        line = INLINE_CODE.sub('', line)
        targets = MD_LINK.findall(line) + HTML_LINK.findall(line)
        for target in targets:
            if is_external(target) or '[' in target:
                continue
            location, _, fragment = target.partition('#')
            location = location.split('?', 1)[0]

            if location.startswith('/'):
                resolved = ROOT / location.lstrip('/')
            elif location:
                resolved = path.parent / location
            else:
                resolved = path

            where = f'{path.relative_to(ROOT).as_posix()}:{number}'
            if not resolved.exists():
                problems.append(f'{where}: {target} -> file not found')
                continue
            if fragment and resolved.suffix == '.md' and fragment.lower() not in anchors(resolved):
                problems.append(f'{where}: {target} -> no heading with anchor #{fragment}')
    return problems


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    files = list(markdown_files())
    problems = [problem for path in files for problem in check(path)]
    for problem in problems:
        print(problem)
    print(f'Checked {len(files)} markdown files: {len(problems)} broken link(s).')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
