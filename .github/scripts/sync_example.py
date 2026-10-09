#!/usr/bin/env python3
"""Copy the skill's verbatim template sections into each example project.

Run this after you change a template. Any section check_example_drift.py
would report gets the template's version, and both copies of dashboard.html
get the template file. Sections that already match aren't touched, so a
second run changes nothing.

Placeholders like [Project Name] keep the value the example gave them. One
the example hasn't filled in yet stays in brackets.

CLAUDE.md's Task Sizing gets the template's general rules followed by the
example's own lines, which are printed so you can check them. The example's
own lines are the ones after its last line that looks like a template rule.
So a rule deleted from the end of the template, or reworded past
recognition, still looks like one of the example's own lines. Delete it from
the example by hand.

Then it runs the drift check, which lists anything left to fix by hand, like
a placeholder to fill in or a section the example doesn't have yet.
"""

import difflib
import re
import sys

import check_example_drift as drift

SLOT = re.compile(r'(\[.*?\])')
COMMENT = re.compile(r'^\s*<!--.*-->\s*$')

# How close a line in the example's Task Sizing has to be to one of the
# template's general rules to count as an older wording of that rule.
SAME_RULE = 0.6


def slot_pattern(template_line):
    """Return (pattern, slots) for a template line with [placeholder] slots."""
    parts = SLOT.split(template_line.rstrip())
    pattern = ''.join('(.+?)' if i % 2 else re.escape(part) for i, part in enumerate(parts))
    return re.compile(pattern + r'\Z'), parts[1::2]


def filled_values(template_lines, example_lines):
    """Return {placeholder: value} from example lines that fill in a template line."""
    values = {}
    for template_line in template_lines:
        pattern, slots = slot_pattern(template_line)
        if not slots:
            continue
        for example_line in example_lines:
            match = pattern.match(example_line.rstrip())
            if match:
                for slot, value in zip(slots, match.groups()):
                    values.setdefault(slot, value)
                break
    return values


def fill(line, values):
    return SLOT.sub(lambda match: values.get(match.group(1), match.group(1)), line)


def content_end(lines):
    """Return the index just past the last meaningful line."""
    meaningful = [i for i, line in enumerate(lines) if drift.meaningful([line])]
    return meaningful[-1] + 1 if meaningful else 0


def own_lines(example_lines, rules):
    """Return the example's lines that follow its copy of the general rules."""
    rules = [rule.strip() for rule in rules]
    last_rule = -1
    for i, line in enumerate(example_lines):
        line = line.strip()
        if drift.meaningful([line]) and any(
                difflib.SequenceMatcher(None, line, rule).ratio() >= SAME_RULE for rule in rules):
            last_rule = i
    return example_lines[last_rule + 1:]


def sync_section(copy, text):
    """Return (text, note) with copy's section replaced by the template's.

    note is None when the section already matches or can't be found.
    """
    if not drift.compare(copy.label, copy.template, text, copy.title, copy.prefix):
        return text, None
    template_lines, lines = copy.template.split('\n'), text.split('\n')
    template_span = drift.section_span(template_lines, copy.title)
    span = drift.section_span(lines, copy.title)
    if template_span is None or span is None:
        return text, None

    # Comments in a template are notes for the builder, and examples leave them out.
    new = [line for line in template_lines[template_span[0] + 1:template_span[1]]
           if not COMMENT.match(line)]
    if copy.prefix:
        new = [line for line in new if not drift.PLACEHOLDER_ONLY.match(line.strip())]
    new = new[:content_end(new)]
    start, end = span[0] + 1, span[1]
    old = lines[start:start + content_end(lines[start:end])]

    values = filled_values(drift.meaningful(new), drift.meaningful(old))
    new = [fill(line, values) for line in new]
    note = f'copied "{copy.title}" from the template'
    if copy.prefix:
        kept = own_lines(old, drift.meaningful(new))
        new += kept
        note += f', then kept {len(drift.meaningful(kept))} line(s) of its own:'
        note += ''.join(f'\n    {line}' for line in drift.meaningful(kept))

    lines[start:start + len(old)] = new
    return '\n'.join(lines), note


def sync_example(project):
    claude = project / '.claude'
    template_html = (drift.TEMPLATES / 'dashboard.html').read_bytes()
    for copy in drift.DASHBOARD_COPIES:
        path = claude / copy
        if not path.exists() or path.read_bytes() != template_html:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(template_html)
            print(f'{path.relative_to(drift.ROOT).as_posix()}: copied the template')

    copies, _ = drift.verbatim_copies(project)
    texts = {}
    for copy in copies:
        if copy.path not in texts:
            texts[copy.path] = drift.read(copy.path)
        texts[copy.path], note = sync_section(copy, texts[copy.path])
        if note:
            print(f'{copy.path.relative_to(drift.ROOT).as_posix()}: {note}')

    for path, text in texts.items():
        if text != drift.read(path):
            path.write_text(text, encoding='utf-8', newline='\n')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    for project in sorted(path.parent for path in (drift.ROOT / 'examples').glob('*/.claude')):
        sync_example(project)
    print()
    return drift.main()


if __name__ == '__main__':
    sys.exit(main())
