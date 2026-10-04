#!/usr/bin/env python3
"""Check relative links and #anchors in every markdown and HTML file in the repo.

Markdown is checked for inline links, reference-style links and their
definitions, and HTML href/src attributes. HTML files are checked for
href/src attributes.

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
REF_DEFINITION = re.compile(r'^\s{0,3}\[([^\]]+)\]:\s*<?([^\s>]+)>?')
REF_USE = re.compile(r'!?\[([^\]]+)\]\[([^\]]*)\]')
HTML_LINK = re.compile(r'\b(?:href|src)="([^"]+)"')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
HTML_ANCHOR = re.compile(r'\b(?:id|name)="([^"]+)"')
FENCE = re.compile(r'^\s*(```|~~~)')
INLINE_CODE = re.compile(r'`[^`\n]*`')


def doc_files():
    for pattern in ('*.md', '*.html'):
        for path in sorted(ROOT.rglob(pattern)):
            if '.git' not in path.relative_to(ROOT).parts:
                yield path


def lines_to_check(path):
    """Yield (line number, text) to scan. In markdown, skip fenced code blocks."""
    text = path.read_text(encoding='utf-8')
    if path.suffix != '.md':
        yield from enumerate(text.splitlines(), start=1)
        return
    fence = None
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
        for _, line in lines_to_check(path):
            match = HEADING.match(line) if path.suffix == '.md' else None
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


def check_target(path, where, target):
    """Return a problem string if a relative target doesn't resolve, else None."""
    if is_external(target) or '[' in target:
        return None
    location, _, fragment = target.partition('#')
    location = location.split('?', 1)[0]

    if location.startswith('/'):
        resolved = ROOT / location.lstrip('/')
    elif location:
        resolved = path.parent / location
    else:
        resolved = path

    if not resolved.exists():
        return f'{where}: {target} -> file not found'
    if fragment and resolved.suffix in ('.md', '.html') and fragment.lower() not in anchors(resolved):
        return f'{where}: {target} -> no anchor #{fragment}'
    return None


def check(path):
    problems = []
    lines = list(lines_to_check(path))
    is_markdown = path.suffix == '.md'

    definitions = {}
    if is_markdown:
        for number, line in lines:
            match = REF_DEFINITION.match(line)
            if match:
                definitions[match.group(1).lower()] = (number, match.group(2))

    for number, line in lines:
        where = f'{path.relative_to(ROOT).as_posix()}:{number}'
        if is_markdown:
            line = INLINE_CODE.sub('', line)
            targets = MD_LINK.findall(line) + HTML_LINK.findall(line)
            for text, label in REF_USE.findall(line):
                if (label or text).lower() not in definitions:
                    problems.append(f'{where}: [{text}][{label}] -> no definition for [{label or text}]')
        else:
            targets = HTML_LINK.findall(line)
        for target in targets:
            problem = check_target(path, where, target)
            if problem:
                problems.append(problem)

    for number, target in definitions.values():
        problem = check_target(path, f'{path.relative_to(ROOT).as_posix()}:{number}', target)
        if problem:
            problems.append(problem)
    return problems


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    files = list(doc_files())
    problems = [problem for path in files for problem in check(path)]
    for problem in problems:
        print(problem)
    print(f'Checked {len(files)} markdown and HTML files: {len(problems)} broken link(s).')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
