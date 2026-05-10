from pathlib import Path
import textwrap

# Clean PDF builder for Felix Crypto Edge.
# Design goal: no cramped multi-column cards, no overlapping badges, readable on phone.

W, H = 595, 842  # A4 points
M = 54
CONTENT_W = W - 2 * M
pages = []
ops = []

RED = (0.84, 0.06, 0.07)
DARK_RED = (0.38, 0.02, 0.03)
BLACK = (0.035, 0.03, 0.03)
WHITE = (1, 1, 1)
TEXT = (0.10, 0.07, 0.07)
MUTED = (0.42, 0.32, 0.32)
LIGHT = (1.0, 0.945, 0.945)
PALE = (1.0, 0.885, 0.885)
GREEN = (0.04, 0.55, 0.25)
GOLD = (0.92, 0.58, 0.08)
GRID = (0.18, 0.08, 0.08)


def rgb(c):
    return f"{c[0]} {c[1]} {c[2]}"


def esc(s):
    return (str(s).replace('\\', '\\\\')
            .replace('(', '\\(').replace(')', '\\)')
            .replace('€', 'EUR').replace('—', '-').replace('–', '-')
            .replace('“', '"').replace('”', '"').replace('’', "'")
            .replace('•', '-').replace('₿', 'BTC').replace('✓', 'OK'))


def rect(x, y, w, h, fill=None, stroke=None, lw=1):
    if fill:
        ops.append(f"{rgb(fill)} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")
    if stroke:
        ops.append(f"{rgb(stroke)} RG {lw} w {x:.1f} {y:.1f} {w:.1f} {h:.1f} re S")


def line(x1, y1, x2, y2, color=RED, lw=2):
    ops.append(f"{rgb(color)} RG {lw} w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S")


def circle(x, y, r, fill=RED):
    k = 0.55228475 * r
    ops.append(
        f"{rgb(fill)} rg {x+r:.1f} {y:.1f} m "
        f"{x+r:.1f} {y+k:.1f} {x+k:.1f} {y+r:.1f} {x:.1f} {y+r:.1f} c "
        f"{x-k:.1f} {y+r:.1f} {x-r:.1f} {y+k:.1f} {x-r:.1f} {y:.1f} c "
        f"{x-r:.1f} {y-k:.1f} {x-k:.1f} {y-r:.1f} {x:.1f} {y-r:.1f} c "
        f"{x+k:.1f} {y-r:.1f} {x+r:.1f} {y-k:.1f} {x+r:.1f} {y:.1f} c f"
    )


def text(x, y, s, size=11, font='F1', color=TEXT):
    ops.append(f"{rgb(color)} rg BT /{font} {size} Tf {x:.1f} {y:.1f} Td ({esc(s)}) Tj ET")


def width_est(s, size=11, bold=False):
    return len(esc(s)) * size * (0.60 if bold else 0.55)


def center_text(cx, y, s, size=11, font='F1', color=TEXT):
    text(cx - width_est(s, size, font == 'F2') / 2, y, s, size, font, color)


def wrapped(x, y, s, width_chars=68, size=11, leading=15, font='F1', color=TEXT):
    for para in str(s).split('\n'):
        if not para.strip():
            y -= leading
            continue
        for part in textwrap.wrap(para, width_chars):
            text(x, y, part, size, font, color)
            y -= leading
    return y


def finish_page():
    global ops
    pages.append('\n'.join(ops))
    ops = []


def header(title, subtitle=None):
    rect(0, 0, W, H, WHITE, None)
    rect(0, H - 14, W, 14, RED, None)
    center_text(W / 2, H - 54, title, 22, 'F2', BLACK)
    y = H - 80
    if subtitle:
        y = wrapped(M + 12, y, subtitle, 70, 10.5, 14, 'F1', MUTED) - 4
    line(M, y, W - M, y, RED, 1.2)
    return y - 34


def safe_card(y, heading, body, badge=None, h=92, fill=LIGHT):
    """Full-width readable card. Returns next y below the card."""
    x, w = M, CONTENT_W
    rect(x, y - h, w, h, fill, (0.88, 0.26, 0.26), 1)
    tx = x + 22
    if badge is not None:
        circle(x + 28, y - 28, 14, RED)
        center_text(x + 28, y - 33, str(badge), 8.5, 'F2', WHITE)
        tx = x + 58
    # Heading and body have separate vertical zones; no overlap.
    wrapped(tx, y - 25, heading, 50 if badge is not None else 58, 13, 15, 'F2', DARK_RED)
    wrapped(x + 22, y - 53, body, 67, 10.2, 13.5, 'F1', TEXT)
    return y - h - 18


def note_box(y, body, heading='Beginner rule'):
    return safe_card(y, heading, body, '!', 78, PALE)


def mini_chart(x, y, w, h, pts, zones=False, labels=False):
    rect(x, y, w, h, BLACK, (0.68, 0.10, 0.10), 1)
    for i in range(1, 5):
        line(x, y + h * i / 5, x + w, y + h * i / 5, GRID, 0.5)
        line(x + w * i / 5, y, x + w * i / 5, y + h, GRID, 0.5)
    if zones:
        rect(x + 20, y + h * 0.68, w - 40, 30, (0.36, 0.02, 0.02), (0.95, 0.13, 0.13), 0.8)
        rect(x + 20, y + h * 0.16, w - 40, 30, (0.04, 0.25, 0.10), (0.15, 0.72, 0.30), 0.8)
        if labels:
            text(x + 32, y + h * 0.68 + 11, 'SELL / TAKE-PROFIT WATCH AREA', 9.5, 'F2', (1, 0.84, 0.84))
            text(x + 32, y + h * 0.16 + 11, 'BUY / SUPPORT WATCH AREA', 9.5, 'F2', (0.86, 1, 0.88))
    scaled = [(x + px * w, y + py * h) for px, py in pts]
    for a, b in zip(scaled, scaled[1:]):
        line(a[0], a[1], b[0], b[1], RED, 3.2)


def cover():
    rect(0, 0, W, H, BLACK, None)
    rect(0, 0, W, 18, RED, None)
    rect(54, 110, CONTENT_W, 560, (0.10, 0.02, 0.025), (0.55, 0.05, 0.06), 2)
    center_text(W / 2, 610, 'FELIX CRYPTO EDGE', 34, 'F2', WHITE)
    center_text(W / 2, 570, 'Trading for Beginners', 26, 'F2', (1, 0.78, 0.78))
    wrapped(88, 522, 'A simple visual guide for reading crypto charts, planning trades, avoiding FOMO, and understanding risk.', 54, 15, 21, 'F1', WHITE)
    mini_chart(88, 250, 420, 185, [(0.03,0.15),(0.14,0.35),(0.25,0.25),(0.36,0.58),(0.48,0.47),(0.60,0.78),(0.72,0.61),(0.85,0.84),(0.96,0.70)], True, True)
    center_text(W / 2, 85, 'Version 0.3 clean preview', 10, 'F2', (1,0.78,0.78))
    center_text(W / 2, 66, 'Education only. Not financial advice. Crypto trading is risky.', 9, 'F1', (1,0.78,0.78))
    finish_page()


def card_page(title, subtitle, cards, note=None):
    y = header(title, subtitle)
    for i, (h, b) in enumerate(cards, 1):
        y = safe_card(y, h, b, i, 86 if len(b) < 115 else 98)
    if note:
        note_box(y, note)
    finish_page()


def disclaimer_page():
    card_page('Read This First', 'This product teaches chart-reading structure. It does not tell you what to buy or promise results.', [
        ('Education only', 'This guide is not financial advice, investment advice, trading advice, tax advice, or a guarantee of profit.'),
        ('Crypto is risky', 'Prices can move quickly, exchanges can fail, liquidity can disappear, and you can lose some or all money you trade.'),
        ('The tool is not a crystal ball', 'Felix Crypto Edge can help you organize a process. It cannot predict the future and cannot remove risk.'),
        ('Beginner promise', 'Before placing any real trade, know where you are wrong, how much you can lose, and why the setup makes sense.')
    ])


def contents_page():
    y = header('What You Will Learn', 'A plain-English path from chart basics to a repeatable practice routine.')
    items = ['Crypto trading basics', 'Beginner mindset', 'Candlesticks', 'Support and resistance', 'Trends and market structure', 'Timeframes', 'Indicators', 'Entries and exits', 'Position sizing', 'Example setup', 'When to skip', 'Felix tool workflow', 'Checklist', 'Common mistakes', 'Glossary', '7-day practice plan']
    for i, item in enumerate(items, 1):
        y = safe_card(y, item, 'One simple lesson explained visually and in plain English.', i, 54)
        if i == 8:
            finish_page(); y = header('What You Will Learn', 'Continued.')
    finish_page()


def candle_page():
    y = header('Candlesticks Explained Simply', 'A candle is a compact picture of what price did during one selected period.')
    # Centered candle diagram with generous spacing.
    base_y = 315
    gx = 185
    rx = 410
    line(gx, base_y, gx, base_y + 235, GREEN, 3)
    rect(gx - 30, base_y + 75, 60, 105, GREEN, GREEN, 1)
    line(rx, base_y, rx, base_y + 235, RED, 3)
    rect(rx - 30, base_y + 75, 60, 105, RED, RED, 1)
    center_text(gx, base_y - 35, 'Green: closed higher', 11, 'F2', GREEN)
    center_text(rx, base_y - 35, 'Red: closed lower', 11, 'F2', RED)
    text(100, 530, 'High', 11, 'F2', GREEN); line(132, 534, gx, base_y + 235, GREEN, 1)
    text(92, 455, 'Close', 11, 'F2', GREEN); line(132, 459, gx - 30, base_y + 180, GREEN, 1)
    text(96, 350, 'Open', 11, 'F2', GREEN); line(132, 354, gx - 30, base_y + 75, GREEN, 1)
    text(108, 305, 'Low', 11, 'F2', GREEN); line(132, 309, gx, base_y, GREEN, 1)
    y = note_box(190, 'Do not trade from one candle alone. A candle matters most when it appears at support, resistance, or a trendline.')
    finish_page()


def chart_page(title, subtitle, chart_labels, cards, note=None):
    y = header(title, subtitle)
    mini_chart(75, 365, 445, 245, [(0.04,0.18),(0.15,0.39),(0.27,0.29),(0.40,0.61),(0.52,0.50),(0.64,0.76),(0.77,0.58),(0.92,0.82)], True, chart_labels)
    y = 320
    for i, (h, b) in enumerate(cards, 1):
        y = safe_card(y, h, b, i, 72)
    if note:
        note_box(y, note)
    finish_page()


def trends_page():
    y = header('Trends: Up, Down, or Sideways?', 'Before entries, ask what the market is doing overall.')
    charts = [
        ('Uptrend', [(0.08,0.25),(0.27,0.47),(0.45,0.35),(0.64,0.68),(0.86,0.56)]),
        ('Downtrend', [(0.08,0.70),(0.27,0.45),(0.45,0.56),(0.64,0.28),(0.86,0.38)]),
        ('Range', [(0.07,0.25),(0.20,0.70),(0.33,0.28),(0.46,0.68),(0.59,0.26),(0.72,0.70),(0.86,0.31)])
    ]
    yy = 555
    for label, pts in charts:
        mini_chart(100, yy - 85, 395, 90, pts, False, False)
        center_text(W / 2, yy - 103, label, 12, 'F2', DARK_RED)
        yy -= 140
    note_box(150, 'If you cannot tell whether the chart is trending or ranging, do not trade yet. First label the market condition.')
    finish_page()


def risk_page():
    y = header('Risk Comes First', 'Beginners obsess over entries. Survivors obsess over how much they can lose if wrong.')
    mini_chart(75, 380, 445, 220, [(0.05,0.20),(0.22,0.36),(0.38,0.32),(0.56,0.55),(0.74,0.72),(0.92,0.63)], False, False)
    line(105, 470, 490, 470, WHITE, 1); text(430, 478, 'Entry', 11, 'F2', WHITE)
    line(105, 425, 490, 425, GREEN, 2); text(400, 433, 'Stop-loss', 11, 'F2', (0.8,1,0.84))
    line(105, 560, 490, 560, RED, 2); text(420, 568, 'Target', 11, 'F2', (1,0.84,0.84))
    y = 325
    y = safe_card(y, 'Example', 'Account: EUR 1,000. Risk: 1%. Maximum planned loss: EUR 10.', 1, 72)
    y = safe_card(y, 'Rule', 'A good trade is not one that must win. A good trade is one where the loss is controlled before you enter.', 2, 78)
    finish_page()


def formula_page():
    y = header('Position Sizing Made Simple', 'Risk is money, not feelings. Decide the maximum planned loss before the trade.')
    y = safe_card(y, 'Step 1: choose account risk', 'Example: EUR 1,000 account and 1% risk. That means the maximum planned loss is EUR 10.', 1, 88)
    y = safe_card(y, 'Step 2: measure stop distance', 'If entry is EUR 100 and stop-loss is EUR 95, the stop distance is EUR 5 per coin/token.', 2, 88)
    y = safe_card(y, 'Step 3: calculate size', 'Position size = money risked / stop distance. EUR 10 / EUR 5 = 2 units.', 3, 88)
    rect(75, 145, 445, 82, BLACK, RED, 1)
    center_text(W / 2, 190, 'Position size = money risked / stop distance', 14, 'F2', WHITE)
    center_text(W / 2, 166, 'Smaller risk keeps your brain calmer and your account alive.', 11, 'F1', (1,0.82,0.82))
    finish_page()


def checklist_page():
    y = header('Beginner Checklist', 'If you cannot answer these questions, skip the trade. Skipping bad trades is a skill.')
    questions = ['What coin am I trading?', 'What timeframe am I using?', 'Is the market trending or ranging?', 'Where is support?', 'Where is resistance?', 'Why is this entry interesting?', 'Where is my stop-loss?', 'Where is my target?', 'How much money am I risking?', 'Am I calm, or am I chasing?']
    for i, q in enumerate(questions, 1):
        y = safe_card(y, q, 'Write a clear answer before entering the trade.', i, 54)
        if i == 5:
            finish_page(); y = header('Beginner Checklist', 'Continued.')
    finish_page()


def final_page():
    rect(0, 0, W, H, BLACK, None)
    center_text(W / 2, 635, 'You do not need magic signals.', 28, 'F2', WHITE)
    center_text(W / 2, 595, 'You need a repeatable process.', 28, 'F2', (1,0.78,0.78))
    wrapped(88, 520, 'Felix Crypto Edge is built to help beginners slow down, read charts clearly, understand risk, and learn why a trade setup might make sense.', 54, 14, 21, 'F1', WHITE)
    rect(75, 305, 445, 115, (0.12,0.02,0.02), RED, 1)
    center_text(W / 2, 372, 'Education only. Not financial advice.', 17, 'F2', WHITE)
    wrapped(100, 342, 'Crypto trading is risky. You can lose money. Always use your own judgment and manage risk.', 50, 12, 17, 'F1', (1,0.82,0.82))
    center_text(W / 2, 108, 'Felix Crypto Edge - Version 0.3 clean preview', 13, 'F2', (1,0.78,0.78))
    finish_page()


def make_pdf(path):
    objects = []
    def obj(s):
        objects.append(s)
        return len(objects)
    font1 = obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    font2 = obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
    page_ids, content_ids = [], []
    for stream in pages:
        data = stream.encode('latin-1', 'replace')
        cid = obj(f'<< /Length {len(data)} >>\nstream\n' + data.decode('latin-1') + '\nendstream')
        content_ids.append(cid)
        page_ids.append(obj(''))
    pages_id = obj('')
    catalog_id = obj(f'<< /Type /Catalog /Pages {pages_id} 0 R >>')
    for idx, pid in enumerate(page_ids):
        objects[pid - 1] = f'<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> /Contents {content_ids[idx]} 0 R >>'
    objects[pages_id - 1] = f'<< /Type /Pages /Kids [' + ' '.join(f'{p} 0 R' for p in page_ids) + f'] /Count {len(page_ids)} >>'
    header_pdf = '%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'
    body, offsets = '', []
    pos = len(header_pdf.encode('latin-1'))
    for i, s in enumerate(objects, 1):
        offsets.append(pos + len(body.encode('latin-1')))
        body += f'{i} 0 obj\n{s}\nendobj\n'
    xref_start = pos + len(body.encode('latin-1'))
    xref = 'xref\n0 ' + str(len(objects) + 1) + '\n0000000000 65535 f \n'
    for off in offsets:
        xref += f'{off:010d} 00000 n \n'
    trailer = f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_start}\n%%EOF\n'
    Path(path).write_bytes((header_pdf + body + xref + trailer).encode('latin-1'))


def build():
    cover()
    disclaimer_page()
    contents_page()
    card_page('What Crypto Trading Really Is', 'Trading is not guessing. It is building a repeatable decision process.', [
        ('The wrong idea', 'Beginners often think the goal is to know exactly where price goes next.'),
        ('The better idea', 'A trader builds a plan: trend, zones, entry, stop-loss, target, and risk.'),
        ('Your job', 'You do not need to be right every time. You need to protect yourself when you are wrong.')
    ], 'If you cannot explain the trade in one simple sentence, you probably do not have a trade.')
    card_page('Beginner Mindset', 'Most new traders lose because they rush, chase, and risk too much.', [
        ('Survival first', 'Your first goal is not getting rich. It is staying in the game long enough to learn.'),
        ('Structure beats emotion', 'Use the same checklist every time so you are not making random decisions.'),
        ('Small risk', 'Risk small enough that one loss does not make you panic or revenge trade.')
    ])
    candle_page()
    chart_page('Support and Resistance', 'Support is where buyers may step in. Resistance is where sellers may step in. Think zones, not perfect lines.', True, [
        ('Support', 'A possible area to look for buyers. It can break, so risk still matters.'),
        ('Resistance', 'A possible area to take profit, avoid chasing, or watch for rejection.')
    ])
    trends_page()
    card_page('Timeframes Without Confusion', 'Start big, then zoom in. Do not jump around until you find an excuse to enter.', [
        ('Higher timeframe', 'Daily or 4-hour. Use this for the big direction: uptrend, downtrend, or range.'),
        ('Planning timeframe', '4-hour or 1-hour. Mark zones and decide where a setup would make sense.'),
        ('Entry timeframe', '1-hour or 15-minute. Use only after the bigger plan is already clear.')
    ], 'Check the daily or 4-hour first. If the big picture is unclear, stop.')
    card_page('Indicators: Helpful, Not Magic', 'Volume, moving averages, and RSI can support a plan, but they should not replace market structure.', [
        ('Volume', 'Shows how much trading happened. A breakout with stronger volume can be more meaningful.'),
        ('Moving averages', 'Smooth price. Price above major averages can suggest bullish structure; below them can suggest bearish structure.'),
        ('RSI', 'Measures momentum. Above 70 can be overextended; below 30 can be oversold. It is not a standalone signal.')
    ])
    risk_page()
    formula_page()
    chart_page('Example: Planned Long Setup', 'Fictional and simplified. The point is the structure, not a prediction.', True, [
        ('Step 1', 'Trend is up on the higher timeframe.'),
        ('Step 2', 'Price pulls back into a support watch zone.'),
        ('Step 3', 'Stop-loss goes below the zone. Target is near next resistance.')
    ])
    card_page('When to Skip a Trade', 'A missed trade is not a loss. A forced trade can become one.', [
        ('Price already pumped', 'If you are buying only because a huge green candle happened, you are probably late.'),
        ('No clear level', 'If you cannot identify support, resistance, or invalidation, there is no plan.'),
        ('Emotional state', 'If you are angry, scared, or desperate to win back money, step away.')
    ], 'Skipping bad trades is one of the fastest ways to improve.')
    chart_page('How Felix Crypto Edge Helps', 'Use the tool as a training wheel for process, not as a profit machine.', True, [
        ('Trend', 'Is price moving up, down, or sideways?'),
        ('Zones', 'Where did price react before?'),
        ('Risk', 'Where is the idea wrong?')
    ], 'Good tool output should make you slower and more structured, not reckless.')
    checklist_page()
    card_page('Common Beginner Mistakes', 'Avoiding these mistakes can be more valuable than finding another indicator.', [
        ('FOMO buying', 'Jumping in after a huge green candle.'),
        ('No stop-loss', 'Refusing to decide where you are wrong.'),
        ('Too much size', 'Risking so much that one loss hurts badly.'),
        ('Signal chasing', 'Blindly copying strangers online.'),
        ('Revenge trading', 'Trying to win money back immediately.'),
        ('Too many indicators', 'Making the chart so messy you cannot think.')
    ])
    card_page('Glossary', 'Plain meanings for words beginners see constantly.', [
        ('Entry', 'The price area where you open a trade.'),
        ('Stop-loss', 'The price where you exit if your idea is wrong.'),
        ('Target', 'The price area where you plan to take profit.'),
        ('Risk/reward', 'Comparison between possible loss and possible gain.'),
        ('Support', 'An area where price previously bounced.'),
        ('Resistance', 'An area where price previously rejected.')
    ])
    card_page('7-Day Practice Plan', 'Practice without real money first. Build skill before adding pressure.', [
        ('Day 1', 'Learn candles and mark highs/lows.'),
        ('Day 2', 'Draw support and resistance zones.'),
        ('Day 3', 'Label trend or range on 10 charts.'),
        ('Day 4', 'Add moving average and RSI context.'),
        ('Day 5', 'Write five fake trade plans.'),
        ('Day 6', 'Review what would have failed.'),
        ('Day 7', 'Create your personal checklist.')
    ])
    final_page()


if __name__ == '__main__':
    build()
    out = 'products/felix-crypto-edge-guide-visual-preview.pdf'
    make_pdf(out)
    print(f'created {out} pages {len(pages)}')
