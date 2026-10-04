#!/usr/bin/env python3
"""Check that each example project still matches the skill's templates.

SKILL.md (Phase 4, "copy structural sections verbatim") lists the template
sections every generated project must copy word for word. The projects in
examples/ are reference output, so those sections in them must match the
templates, and their dashboard.html must be an exact copy of the template.

Square-bracket placeholders in a template line, like [Project Name], match
any text. Blank lines, horizontal rules and HTML comments are ignored.
"""

import difflib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / 'skill' / 'references' / 'templates'

# Keep in step with the verbatim-sections table in skill/SKILL.md.
AGENT_SECTIONS = {
    'orchestrator': ['Task Sizing Rules', 'State Management', 'State Summarization',
                     'Execution Loop', 'Self-Healing Pipeline', 'Handoff Protocol'],
    'problem-solver': ['Self-Healing Workflow', 'Handoff Protocol'],
}
OTHER_AGENT_SECTIONS = ['Handoff Protocol']
SKILL_SECTIONS = {
    'run': ['Execution Loop'],
    'dashboard': ['How the dashboard works', 'Important'],
}
# CLAUDE.md keeps the template's general rules first, then adds its own.
CLAUDE_MD_PREFIX_SECTIONS = ['Task Sizing']

FENCE = re.compile(r'^\s*(```|~~~)')
HEADING = re.compile(r'^(#{1,6})\s+(.*?)\s*$')
NAME = re.compile(r'^name:\s*(.+?)\s*$', re.MULTILINE)
PLACEHOLDER = re.compile(r'\\\[.*?\\\]')
PLACEHOLDER_ONLY = re.compile(r'^- \[.*\]$')


def read(path):
    return path.read_text(encoding='utf-8').replace('\r\n', '\n')


def template_blocks(path):
    """Return {name: text} for each ```markdown block in a template file.

    A block runs to the last closing fence before the next ```markdown
    opener, so fenced examples nested inside a block stay part of it.
    """
    lines = read(path).split('\n')
    starts = [i for i, line in enumerate(lines) if line.strip() == '```markdown']
    blocks = {}
    for n, start in enumerate(starts):
        stop = starts[n + 1] if n + 1 < len(starts) else len(lines)
        end = max(i for i in range(start + 1, stop) if lines[i].strip() == '```')
        text = '\n'.join(lines[start + 1:end])
        match = NAME.search(text)
        blocks[match.group(1) if match else path.stem] = text
    return blocks


def section(text, title):
    """Return the lines under the first heading that starts with title.

    The section runs to the next heading at the same or a higher level.
    Headings inside fenced code don't count.
    """
    lines = text.split('\n')
    fence, level, body = None, None, None
    for line in lines:
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            fence = marker if fence is None else (None if marker == fence else fence)
        heading = HEADING.match(line) if fence is None and not match else None
        if body is not None:
            if heading and len(heading.group(1)) <= level:
                break
            body.append(line)
        elif heading and heading.group(2).lower().startswith(title.lower()):
            level, body = len(heading.group(1)), []
    return body


def meaningful(lines):
    kept = []
    for line in lines:
        line = line.rstrip()
        if not line.strip() or line.strip() == '---':
            continue
        if line.strip().startswith('<!--') and line.strip().endswith('-->'):
            continue
        kept.append(line)
    return kept


def line_pattern(template_line):
    return re.compile(PLACEHOLDER.sub('.+?', re.escape(template_line)) + r'\Z')


def lines_match(template_lines, example_lines):
    return len(template_lines) == len(example_lines) and all(
        line_pattern(t).match(e) for t, e in zip(template_lines, example_lines))


def compare(label, template_text, example_text, title, prefix=False):
    template = section(template_text, title)
    if template is None:
        return [f'{label}: template has no "{title}" section']
    example = section(example_text, title)
    if example is None:
        return [f'{label}: missing the "{title}" section']

    template, example = meaningful(template), meaningful(example)
    if prefix:
        template = [line for line in template if not PLACEHOLDER_ONLY.match(line.strip())]
        example = example[:len(template)]
    if lines_match(template, example):
        return []

    diff = difflib.unified_diff(template, example, 'template', 'example', lineterm='', n=1)
    return [f'{label}: "{title}" differs from the template\n    ' + '\n    '.join(diff)]


def check_example(project):
    claude = project / '.claude'
    name = project.relative_to(ROOT).as_posix()
    problems = []

    template_html = read(TEMPLATES / 'dashboard.html')
    example_html = claude / 'workspace' / 'dashboard.html'
    if not example_html.exists():
        problems.append(f'{name}: no .claude/workspace/dashboard.html')
    elif read(example_html) != template_html:
        problems.append(f'{name}: dashboard.html is not an exact copy of the template')

    agent_templates = template_blocks(TEMPLATES / 'agents.md')
    for agent_file in sorted((claude / 'agents').glob('*/AGENT.md')):
        agent = agent_file.parent.name
        label = f'{name} agent {agent}'
        if agent not in agent_templates:
            problems.append(f'{label}: no template with name: {agent} in agents.md')
            continue
        for title in AGENT_SECTIONS.get(agent, OTHER_AGENT_SECTIONS):
            problems += compare(label, agent_templates[agent], read(agent_file), title)

    skill_templates = template_blocks(TEMPLATES / 'skills.md')
    for skill, titles in SKILL_SECTIONS.items():
        skill_file = claude / 'skills' / skill / 'SKILL.md'
        label = f'{name} skill /{skill}'
        if not skill_file.exists():
            problems.append(f'{label}: missing (it is always generated)')
            continue
        for title in titles:
            problems += compare(label, skill_templates[skill], read(skill_file), title)

    claude_md_template = next(iter(template_blocks(TEMPLATES / 'claude-md.md').values()))
    for title in CLAUDE_MD_PREFIX_SECTIONS:
        problems += compare(f'{name} CLAUDE.md', claude_md_template,
                            read(claude / 'CLAUDE.md'), title, prefix=True)
    return problems


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    projects = sorted(path.parent for path in (ROOT / 'examples').glob('*/.claude'))
    problems = [problem for project in projects for problem in check_example(project)]
    for problem in problems:
        print(problem)
    print(f'Checked {len(projects)} example project(s): {len(problems)} problem(s).')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
