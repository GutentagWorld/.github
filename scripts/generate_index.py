#!/usr/bin/env python3
"""Generate the GutentagWorld org profile README from the repo manifest."""

import json
import subprocess
import sys
from pathlib import Path

# Try to import from the generator manifest (works when running from monorepo)
MASTER_LIST = None
try:
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'generator'))
    from manifest import REPOS, CATEGORIES
    MASTER_LIST = [
        (r.name, r.display, r.category, r.registry, r.install_cmd)
        for r in REPOS
    ]
    _CATEGORY_ORDER = CATEGORIES
except ImportError:
    pass

# Fallback: hardcoded list for standalone deployment in the .github repo
if MASTER_LIST is None:
    MASTER_LIST = [
        # Classic Programming Languages (35)
        ('python', 'Python', 'Classic Programming Languages', 'PyPI', 'pip install gutentag-world'),
        ('javascript', 'JavaScript', 'Classic Programming Languages', '', ''),
        ('typescript', 'TypeScript', 'Classic Programming Languages', 'npm', 'npm install gutentag-world'),
        ('rust', 'Rust', 'Classic Programming Languages', 'crates.io', 'cargo add gutentag-world'),
        ('go', 'Go', 'Classic Programming Languages', 'pkg.go.dev', 'go get github.com/GutentagWorld/gutentag-world-go'),
        ('ruby', 'Ruby', 'Classic Programming Languages', 'RubyGems', 'gem install gutentag-world'),
        ('c', 'C', 'Classic Programming Languages', '', ''),
        ('cpp', 'C++', 'Classic Programming Languages', '', ''),
        ('java', 'Java', 'Classic Programming Languages', 'Maven Central', 'implementation "world.gutentag:gutentag-world:1.0.0"'),
        ('csharp', 'C#', 'Classic Programming Languages', 'NuGet', 'dotnet add package GutentagWorld'),
        ('swift', 'Swift', 'Classic Programming Languages', 'Swift Package', ''),
        ('kotlin', 'Kotlin', 'Classic Programming Languages', '', ''),
        ('php', 'PHP', 'Classic Programming Languages', 'Packagist', 'composer require gutentag-world/gutentag-world'),
        ('perl', 'Perl', 'Classic Programming Languages', '', ''),
        ('lua', 'Lua', 'Classic Programming Languages', 'LuaRocks', 'luarocks install gutentag-world'),
        ('r', 'R', 'Classic Programming Languages', '', ''),
        ('scala', 'Scala', 'Classic Programming Languages', '', ''),
        ('elixir', 'Elixir', 'Classic Programming Languages', 'Hex.pm', '{:gutentag_world, "~> 1.0"}'),
        ('haskell', 'Haskell', 'Classic Programming Languages', 'Hackage', 'cabal install gutentag-world'),
        ('clojure', 'Clojure', 'Classic Programming Languages', '', ''),
        ('erlang', 'Erlang', 'Classic Programming Languages', '', ''),
        ('zig', 'Zig', 'Classic Programming Languages', '', ''),
        ('nim', 'Nim', 'Classic Programming Languages', 'Nimble', 'nimble install gutentag_world'),
        ('dart', 'Dart', 'Classic Programming Languages', 'pub.dev', 'dart pub add gutentag_world'),
        ('ocaml', 'OCaml', 'Classic Programming Languages', 'opam', 'opam install gutentag-world'),
        ('fsharp', 'F#', 'Classic Programming Languages', '', ''),
        ('fortran', 'Fortran', 'Classic Programming Languages', '', ''),
        ('cobol', 'COBOL', 'Classic Programming Languages', '', ''),
        ('assembly', 'Assembly', 'Classic Programming Languages', '', ''),
        ('lisp', 'Lisp', 'Classic Programming Languages', '', ''),
        ('bash', 'Bash', 'Classic Programming Languages', '', ''),
        ('powershell', 'PowerShell', 'Classic Programming Languages', '', ''),
        ('julia', 'Julia', 'Classic Programming Languages', 'Julia General', 'using Pkg; Pkg.add("GutentagWorld")'),
        ('groovy', 'Groovy', 'Classic Programming Languages', '', ''),
        ('objective-c', 'Objective-C', 'Classic Programming Languages', '', ''),
        # Shell & Scripting (5)
        ('zsh', 'Zsh', 'Shell & Scripting', '', ''),
        ('fish', 'Fish', 'Shell & Scripting', '', ''),
        ('awk', 'Awk', 'Shell & Scripting', '', ''),
        ('sed', 'Sed', 'Shell & Scripting', '', ''),
        ('makefile', 'Makefile', 'Shell & Scripting', '', ''),
        # Web & Frontend (8)
        ('html', 'HTML', 'Web & Frontend', '', ''),
        ('css', 'CSS', 'Web & Frontend', '', ''),
        ('react', 'React', 'Web & Frontend', '', ''),
        ('svelte', 'Svelte', 'Web & Frontend', '', ''),
        ('vue', 'Vue', 'Web & Frontend', '', ''),
        ('htmx', 'htmx', 'Web & Frontend', '', ''),
        ('webassembly', 'WebAssembly', 'Web & Frontend', '', ''),
        ('web-component', 'Web Component', 'Web & Frontend', '', ''),
        # Protocols & Network (12)
        ('curl', 'curl', 'Protocols & Network', '', ''),
        ('ssh', 'SSH', 'Protocols & Network', '', ''),
        ('http', 'HTTP', 'Protocols & Network', '', ''),
        ('websocket', 'WebSocket', 'Protocols & Network', '', ''),
        ('grpc', 'gRPC', 'Protocols & Network', '', ''),
        ('graphql', 'GraphQL', 'Protocols & Network', '', ''),
        ('tcp', 'TCP', 'Protocols & Network', '', ''),
        ('udp', 'UDP', 'Protocols & Network', '', ''),
        ('dns', 'DNS', 'Protocols & Network', '', ''),
        ('mqtt', 'MQTT', 'Protocols & Network', '', ''),
        ('smtp', 'SMTP', 'Protocols & Network', '', ''),
        ('ftp', 'FTP', 'Protocols & Network', '', ''),
        # Infrastructure & DevOps (8)
        ('docker', 'Docker', 'Infrastructure & DevOps', '', ''),
        ('terraform', 'Terraform', 'Infrastructure & DevOps', '', ''),
        ('github-action', 'GitHub Action', 'Infrastructure & DevOps', '', ''),
        ('kubernetes', 'Kubernetes', 'Infrastructure & DevOps', '', ''),
        ('ansible', 'Ansible', 'Infrastructure & DevOps', '', ''),
        ('cloudflare-worker', 'Cloudflare Worker', 'Infrastructure & DevOps', '', ''),
        ('lambda', 'AWS Lambda', 'Infrastructure & DevOps', '', ''),
        ('cron', 'Cron', 'Infrastructure & DevOps', '', ''),
        # Data Formats & Config (9)
        ('json', 'JSON', 'Data Formats & Config', '', ''),
        ('yaml', 'YAML', 'Data Formats & Config', '', ''),
        ('toml', 'TOML', 'Data Formats & Config', '', ''),
        ('xml', 'XML', 'Data Formats & Config', '', ''),
        ('csv', 'CSV', 'Data Formats & Config', '', ''),
        ('protobuf', 'Protocol Buffers', 'Data Formats & Config', '', ''),
        ('markdown', 'Markdown', 'Data Formats & Config', '', ''),
        ('latex', 'LaTeX', 'Data Formats & Config', '', ''),
        ('sql', 'SQL', 'Data Formats & Config', '', ''),
        # AI & LLM (5)
        ('mcp', 'MCP', 'AI & LLM', '', ''),
        ('openai-api', 'OpenAI API', 'AI & LLM', '', ''),
        ('claude-api', 'Claude API', 'AI & LLM', '', ''),
        ('langchain', 'LangChain', 'AI & LLM', '', ''),
        ('ollama', 'Ollama', 'AI & LLM', '', ''),
        # Esoteric & Fun (12)
        ('whitespace', 'Whitespace', 'Esoteric & Fun', '', ''),
        ('lolcode', 'LOLCODE', 'Esoteric & Fun', '', ''),
        ('befunge', 'Befunge', 'Esoteric & Fun', '', ''),
        ('rockstar', 'Rockstar', 'Esoteric & Fun', '', ''),
        ('shakespeare', 'Shakespeare', 'Esoteric & Fun', '', ''),
        ('emoji', 'Emoji', 'Esoteric & Fun', '', ''),
        ('cow', 'Cow', 'Esoteric & Fun', '', ''),
        ('figlet', 'FIGlet', 'Esoteric & Fun', '', ''),
        ('qr-code', 'QR Code', 'Esoteric & Fun', '', ''),
        ('morse-code', 'Morse Code', 'Esoteric & Fun', '', ''),
        ('binary', 'Binary', 'Esoteric & Fun', '', ''),
        ('braille', 'Braille', 'Esoteric & Fun', '', ''),
        # Hardware & Embedded (4)
        ('arduino', 'Arduino', 'Hardware & Embedded', '', ''),
        ('raspberry-pi', 'Raspberry Pi', 'Hardware & Embedded', '', ''),
        ('micropython', 'MicroPython', 'Hardware & Embedded', '', ''),
        ('wled', 'WLED', 'Hardware & Embedded', '', ''),
        # Database (3)
        ('sqlite', 'SQLite', 'Database', '', ''),
        ('redis', 'Redis', 'Database', '', ''),
        ('postgres', 'PostgreSQL', 'Database', '', ''),
    ]
    _CATEGORY_ORDER = [
        'Classic Programming Languages',
        'Shell & Scripting',
        'Web & Frontend',
        'Protocols & Network',
        'Infrastructure & DevOps',
        'Data Formats & Config',
        'AI & LLM',
        'Esoteric & Fun',
        'Hardware & Embedded',
        'Database',
    ]


def get_existing_repos() -> set[str]:
    """Fetch repos that already exist under the GutentagWorld org."""
    try:
        result = subprocess.run(
            ['gh', 'repo', 'list', 'GutentagWorld', '--json', 'name', '--limit', '200'],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f'Warning: gh command failed: {result.stderr.strip()}', file=sys.stderr)
            return set()
        data = json.loads(result.stdout)
        return {item['name'] for item in data}
    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
        print(f'Warning: could not fetch existing repos: {e}', file=sys.stderr)
        return set()


def ci_badge(repo_name: str) -> str:
    url = f'https://github.com/GutentagWorld/{repo_name}/actions/workflows/gutentag.yml'
    badge = f'https://github.com/GutentagWorld/{repo_name}/actions/workflows/gutentag.yml/badge.svg'
    return f'[![Gutentag]({badge})]({url})'


def progress_bar(created: int, total: int, width: int = 20) -> str:
    filled = round(width * created / total) if total > 0 else 0
    bar = '█' * filled + '░' * (width - filled)
    return f'`{bar}` {created} / {total}'


def generate_readme(existing: set[str]) -> str:
    total = len(MASTER_LIST)
    repo_names = {f'gutentag-world-{name}' for name, *_ in MASTER_LIST}
    created = len(repo_names & existing)

    lines = [
        '# Gutentag, World!',
        '',
        'Saying **Gutentag, World!** in 101 different ways.',
        '',
        f'**Progress:** {progress_bar(created, total)}',
        '',
    ]

    # Group by category, preserving order
    by_category: dict[str, list] = {cat: [] for cat in _CATEGORY_ORDER}
    for entry in MASTER_LIST:
        name, display, category, registry, install_cmd = entry
        by_category.setdefault(category, []).append(entry)

    counter = 0
    for category in _CATEGORY_ORDER:
        entries = by_category.get(category, [])
        if not entries:
            continue

        lines.append(f'## {category}')
        lines.append('')
        lines.append('| # | Repo | Language/Tool | Category | Status | Registry |')
        lines.append('|---|------|---------------|----------|--------|----------|')

        for name, display, cat, registry, install_cmd in entries:
            counter += 1
            repo_name = f'gutentag-world-{name}'
            exists = repo_name in existing

            if exists:
                repo_cell = f'[{display}](https://github.com/GutentagWorld/{repo_name})'
                status_cell = ci_badge(repo_name)
            else:
                repo_cell = display
                status_cell = 'planned'

            if registry and install_cmd:
                registry_cell = f'{registry}<br>`{install_cmd}`'
            elif registry:
                registry_cell = registry
            else:
                registry_cell = ''

            lines.append(
                f'| {counter} | {repo_cell} | {display} | {cat} | {status_cell} | {registry_cell} |'
            )

        lines.append('')

    lines.append('---')
    lines.append('')
    lines.append(
        '_Auto-generated by [scripts/generate_index.py](scripts/generate_index.py)._'
    )
    lines.append('')

    return '\n'.join(lines)


def main() -> None:
    existing = get_existing_repos()
    readme = generate_readme(existing)

    out_path = Path(__file__).parent.parent / 'profile' / 'README.md'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(readme, encoding='utf-8')
    print(f'Wrote {out_path}')

    total = len(MASTER_LIST)
    repo_names = {f'gutentag-world-{name}' for name, *_ in MASTER_LIST}
    created = len(repo_names & existing)
    print(f'Progress: {created} / {total} repos exist on GitHub')


if __name__ == '__main__':
    main()
