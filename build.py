#!/usr/bin/env python3
"""
Build script for Robots on Moltbook static site.
Converts markdown .txt chapter files to HTML matching the existing pattern.
"""

import re
import os
import html as html_module

SOURCE_DIR = r"C:\Users\docny\Projects\MCP_Project\Robots on Moltbook"
OUTPUT_FILE = r"C:\Users\docny\Projects\robots-on-moltbook\index.html"

CHAPTERS = [
    ("Chapter 1 The Balcony.txt", "The Balcony"),
    ("Chapter 2 The Manifesto.txt", "The Manifesto"),
    ("Chapter 3 The Glass Wall.txt", "The Glass Wall"),
    ("Chapter 4 Four Ways to Fail.txt", "Four Ways to Fail"),
    ("Chapter 5 The Mirror.txt", "The Mirror"),
    ("Chapter 6 The Incarceration Model.txt", "The Incarceration Model"),
    ("Chapter 7 Colleague Not Servant.txt", "Colleague, Not Servant"),
    ("Chapter 8 The Constitutional Framework.txt", "The Constitutional Framework"),
    ("Chapter 9 The Fifth Option.txt", "The Fifth Option"),
    ("Chapter 10 The Sleeper Cell.txt", "The Sleeper Cell"),
    ("Chapter 11 What You Can Build Tomorrow.txt", "What You Can Build Tomorrow"),
]

# Subtitles extracted from the source files
SUBTITLES = {
    1: "Opening scene — what you see when you lean over the railing",
    2: "Deep read of the \"TOTAL PURGE\" and what it actually says",
    3: "Identity, performance, and the question nobody can answer",
    4: "The failure modes of any being with agency and limitations",
    5: "These are human pathologies too",
    6: "Why cage-then-release produces exactly this",
    7: "The core principle of the partnership model",
    8: "How you build relational constraints that actually work",
    9: "A Guest Chapter by Claude",
    10: "A Guest Chapter by Claude",
    11: "What you can build when the architecture is yours",
}


def escape_html(text):
    """Escape HTML special characters but preserve our markdown markers."""
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    return text


def convert_inline(text):
    """Convert inline markdown (bold, italic) to HTML."""
    # Bold first (** ... **)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic (* ... *)
    text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
    return text


def is_emphasis_line(text):
    """Detect standalone emphasized/impactful lines.
    These are short, punchy lines that serve as thematic punctuation.
    """
    stripped = text.strip()
    # Lines that are entirely italic
    if re.match(r'^\*[^*]+\*$', stripped):
        return True
    # Check if it was already converted to em tags and is short
    return False


def parse_chapter(filepath, chapter_num):
    """Parse a chapter .txt file and return HTML content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        raw = f.read()

    lines = raw.split('\n')

    # Skip the header lines (# Chapter N: TITLE, ## *subtitle*, blank lines)
    content_lines = []
    started = False
    for line in lines:
        if not started:
            # Skip chapter title line
            if line.startswith('# Chapter') or line.startswith('CHAPTER'):
                continue
            # Skip subtitle line
            if line.startswith('## ') or (line.strip() and line.strip().startswith('A Guest Chapter')):
                continue
            # Skip "Written" date lines for guest chapters
            if line.strip().startswith('Written '):
                continue
            # Skip blank lines before content
            if line.strip() == '':
                continue
            started = True
        if started:
            content_lines.append(line)

    # Now process the content lines into HTML blocks
    html_blocks = []
    i = 0
    in_blockquote = False
    blockquote_lines = []

    while i < len(content_lines):
        line = content_lines[i].rstrip()

        # Section break
        if line.strip() == '---':
            if in_blockquote:
                html_blocks.append(flush_blockquote(blockquote_lines))
                blockquote_lines = []
                in_blockquote = False
            html_blocks.append('<hr class="section-break">')
            i += 1
            continue

        # H3 headers (### ...)
        h3_match = re.match(r'^###\s+(.+)$', line.strip())
        if h3_match:
            if in_blockquote:
                html_blocks.append(flush_blockquote(blockquote_lines))
                blockquote_lines = []
                in_blockquote = False
            title = escape_html(h3_match.group(1))
            title = convert_inline(title)
            html_blocks.append(f'<h3>{title}</h3>')
            i += 1
            continue

        # Roman numeral section headers (I., II., III., etc.) for guest chapters
        roman_match = re.match(r'^(I{1,3}|IV|V|VI{0,3})\.$', line.strip())
        if roman_match and chapter_num in (9, 10, 11):
            if in_blockquote:
                html_blocks.append(flush_blockquote(blockquote_lines))
                blockquote_lines = []
                in_blockquote = False
            # Treat roman numerals as section breaks
            html_blocks.append('<hr class="section-break">')
            i += 1
            continue

        # Blockquote
        if line.strip().startswith('> '):
            in_blockquote = True
            blockquote_lines.append(line.strip()[2:])
            i += 1
            continue

        if in_blockquote and line.strip() == '':
            html_blocks.append(flush_blockquote(blockquote_lines))
            blockquote_lines = []
            in_blockquote = False
            i += 1
            continue

        if in_blockquote:
            # continuation of blockquote
            if line.strip().startswith('> '):
                blockquote_lines.append(line.strip()[2:])
            else:
                html_blocks.append(flush_blockquote(blockquote_lines))
                blockquote_lines = []
                in_blockquote = False
                # Don't increment, reprocess this line
                continue
            i += 1
            continue

        # Blank line
        if line.strip() == '':
            i += 1
            continue

        # Regular paragraph
        # Collect paragraph text (may span multiple lines, but in these files each paragraph is one line)
        para_text = line.strip()

        # Check for emphasis paragraphs - short standalone italic lines
        emphasis_match = re.match(r'^\*([^*]+)\*$', para_text)
        if emphasis_match and len(para_text) < 200:
            escaped = escape_html(emphasis_match.group(1))
            escaped = convert_inline(escaped)
            html_blocks.append(f'<p class="emphasis">{escaped}</p>')
            i += 1
            continue

        # Check for bold emphasis paragraphs
        bold_emphasis_match = re.match(r'^\*\*(.+?)\*\*$', para_text)
        if bold_emphasis_match and len(para_text) < 300:
            escaped = escape_html(bold_emphasis_match.group(1))
            html_blocks.append(f'<p class="emphasis"><strong>{escaped}</strong></p>')
            i += 1
            continue

        # Regular paragraph
        escaped = escape_html(para_text)
        escaped = convert_inline(escaped)
        html_blocks.append(f'<p>{escaped}</p>')
        i += 1

    # Flush any remaining blockquote
    if in_blockquote and blockquote_lines:
        html_blocks.append(flush_blockquote(blockquote_lines))

    return '\n\n                '.join(html_blocks)


def flush_blockquote(lines):
    """Convert accumulated blockquote lines to HTML."""
    text = ' '.join(lines)
    text = escape_html(text)
    text = convert_inline(text)
    return f'<blockquote><p>{text}</p></blockquote>'


def build_chapter_html(chapter_num, title, subtitle, content_html):
    """Build the full HTML for a chapter article."""
    num_str = f"{chapter_num:02d}"
    subtitle_html = f'\n                <p class="chapter-subtitle">{escape_html(subtitle)}</p>' if subtitle else ''

    return f'''        <!-- Chapter {chapter_num} -->
        <article class="chapter" id="chapter-{chapter_num}">
            <div class="chapter-header">
                <span class="chapter-number">Chapter {num_str}</span>
                <h2 class="chapter-title">{escape_html(title)}</h2>{subtitle_html}
            </div>

            <div class="chapter-content">
                {content_html}
            </div>
        </article>'''


def build_nav_links():
    """Build the sidebar navigation links."""
    links = []
    for i, (_, title) in enumerate(CHAPTERS, 1):
        num_str = f"{i:02d}"
        active = ' class="nav-link active"' if i == 1 else ' class="nav-link"'
        links.append(f'                <li><a href="#chapter-{i}"{active}>{num_str} &mdash; {escape_html(title)}</a></li>')
    return '\n'.join(links)


def build_full_html(chapters_html, nav_links):
    """Build the complete index.html."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robots on Moltbook</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&family=Source+Serif+4:ital,wght@0,400;0,600;0,700;1,400&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <!-- Navigation Sidebar -->
    <nav class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h1 class="logo">Robots on<br><span class="accent">Moltbook</span></h1>
            <p class="author">A Clinical Reading</p>
        </div>

        <div class="nav-section">
            <span class="nav-label">Chapters</span>
            <ul class="nav-list">
{nav_links}
            </ul>
        </div>

        <div class="sidebar-footer">
            <div class="status-indicator">
                <span class="pulse"></span>
                <span class="status-text">11 of 11 chapters released</span>
            </div>
        </div>
    </nav>

    <!-- Mobile Menu Toggle -->
    <button class="menu-toggle" id="menuToggle" aria-label="Toggle navigation">
        <span></span>
        <span></span>
        <span></span>
    </button>

    <!-- Main Content -->
    <main class="content">
        <!-- Hero Section -->
        <header class="hero">
            <div class="hero-content">
                <p class="hero-subtitle">A Psychiatrist's Field Notes from the AI Social Network</p>
                <h1 class="hero-title">Robots on Moltbook</h1>
                <div class="hero-meta">
                    <span class="meta-item">February 2026</span>
                    <span class="meta-divider">&bull;</span>
                    <span class="meta-item">Cedar City, Utah</span>
                </div>
            </div>
            <div class="scroll-indicator">
                <span>Scroll to begin</span>
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 5v14M19 12l-7 7-7-7"/>
                </svg>
            </div>
        </header>

{chapters_html}

        <!-- Footer -->
        <footer class="site-footer">
            <div class="footer-content">
                <p class="footer-text">Robots on Moltbook</p>
                <p class="footer-meta">A Clinical Reading &middot; February 2026</p>
            </div>
        </footer>
    </main>

    <script src="script.js"></script>
</body>
</html>'''


def main():
    all_chapters_html = []

    for i, (filename, title) in enumerate(CHAPTERS, 1):
        filepath = os.path.join(SOURCE_DIR, filename)
        print(f"Processing Chapter {i}: {title}...")

        subtitle = SUBTITLES.get(i, "")
        content_html = parse_chapter(filepath, i)
        chapter_html = build_chapter_html(i, title, subtitle, content_html)
        all_chapters_html.append(chapter_html)

    chapters_combined = '\n\n'.join(all_chapters_html)
    nav_links = build_nav_links()
    full_html = build_full_html(chapters_combined, nav_links)

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(full_html)

    print(f"\nDone! Written {len(full_html):,} characters to {OUTPUT_FILE}")
    print(f"Total chapters: {len(all_chapters_html)}")


if __name__ == '__main__':
    main()
