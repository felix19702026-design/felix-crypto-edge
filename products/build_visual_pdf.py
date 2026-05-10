from pathlib import Path
import textwrap
import re

W, H = 595, 842  # A4 points
M = 42
pages = []
ops = []

RED = (0.86, 0.08, 0.08)
DARK_RED = (0.35, 0.02, 0.03)
BLACK = (0.04, 0.035, 0.035)
WHITE = (1, 1, 1)
TEXT = (0.09, 0.06, 0.06)
MUTED = (0.42, 0.32, 0.32)
LIGHT = (1.0, 0.94, 0.94)
PALE = (1.0, 0.88, 0.88)
GREEN = (0.05, 0.58, 0.26)
GOLD = (0.93, 0.58, 0.08)


def rgb(c):
    return f"{c[0]} {c[1]} {c[2]}"


def esc(s):
    return (str(s).replace('\\', '\\\\')
            .replace('(', '\\(').replace(')', '\\)')
            .replace('€', 'EUR').replace('—', '-').replace('–', '-')
            .replace('“', '"').replace('”', '"').replace('’', "'")
            .replace('•', '-').replace('₿', 'BTC').replace('✓', 'OK'))


def finish_page():
    global ops
    pages.append('\n'.join(ops))
    ops = []


def text(x, y, s, size=11, font='F1', color=TEXT):
    ops.append(f"{rgb(color)} rg BT /{font} {size} Tf {x:.1f} {y:.1f} Td ({esc(s)}) Tj ET")


def wrapped(x, y, s, width=70, size=11, leading=15, font='F1', color=TEXT):
    for para in str(s).split('\n'):
        if not para.strip():
            y -= leading
            continue
        for line in textwrap.wrap(para, width):
            text(x, y, line, size, font, color)
            y -= leading
    return y


def rect(x, y, w, h, fill=None, stroke=None, lw=1):
    if fill:
        ops.append(f"{rgb(fill)} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f")
    if stroke:
        ops.append(f"{rgb(stroke)} RG {lw} w {x:.1f} {y:.1f} {w:.1f} {h:.1f} re S")


def line(x1, y1, x2, y2, color=RED, lw=2):
    ops.append(f"{rgb(color)} RG {lw} w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S")


def circle(x, y, r, fill=RED):
    k = 0.55228475 * r
    ops.append(f"{rgb(fill)} rg {x+r:.1f} {y:.1f} m {x+r:.1f} {y+k:.1f} {x+k:.1f} {y+r:.1f} {x:.1f} {y+r:.1f} c {x-k:.1f} {y+r:.1f} {x-r:.1f} {y+k:.1f} {x-r:.1f} {y:.1f} c {x-r:.1f} {y-k:.1f} {x-k:.1f} {y-r:.1f} {x:.1f} {y-r:.1f} c {x+k:.1f} {y-r:.1f} {x+r:.1f} {y-k:.1f} {x+r:.1f} {y:.1f} c f")


def header(title, subtitle=None):
    rect(0, 0, W, H, WHITE, None)
    rect(0, H - 16, W, 16, RED, None)
    text(M, H - 58, title, 23, 'F2', BLACK)
    if subtitle:
        wrapped(M, H - 82, subtitle, 79, 10, 14, 'F1', MUTED)
    line(M, H - 98, W - M, H - 98, RED, 1.2)


def card(x, y, w, h, heading, body, icon=None, fill=LIGHT):
    rect(x, y, w, h, fill, (0.92, 0.32, 0.32), 1)
    tx = x + 14
    if icon:
        circle(x + 22, y + h - 29, 13, RED)
        text(x + 18 - (len(str(icon))-1)*3, y + h - 34, icon, 9.5, 'F2', WHITE)
        tx = x + 45
    text(tx, y + h - 28, heading, 12.5, 'F2', DARK_RED)
    wrapped(x + 14, y + h - 50, body, max(20, int((w - 28) / 5.7)), 9.5, 12.5, 'F1', TEXT)


def mini_chart(x, y, w, h, pts, zones=False):
    rect(x, y, w, h, (0.035, 0.03, 0.03), (0.75, 0.12, 0.12), 1)
    for i in range(1, 5):
        line(x, y + i * h / 5, x + w, y + i * h / 5, (0.16, 0.08, 0.08), 0.45)
    if zones:
        rect(x + 16, y + h * 0.68, w - 32, 28, (0.38, 0.02, 0.02), (0.95, 0.13, 0.13), 0.7)
        rect(x + 16, y + h * 0.18, w - 32, 28, (0.04, 0.25, 0.10), (0.15, 0.75, 0.32), 0.7)
    scaled = [(x + px * w, y + py * h) for px, py in pts]
    for a, b in zip(scaled, scaled[1:]):
        line(a[0], a[1], b[0], b[1], RED, 3)


def cover():
    rect(0, 0, W, H, BLACK, None)
    rect(0, 0, W, 18, RED, None)
    rect(42, 116, 511, 540, (0.10, 0.02, 0.025), (0.55, 0.05, 0.06), 2)
    text(62, 600, 'FELIX CRYPTO EDGE', 34, 'F2', WHITE)
    text(62, 560, 'Trading for Dummies', 27, 'F2', (1, 0.78, 0.78))
    wrapped(62, 515, 'A simple visual beginner guide for reading crypto charts, planning trades, avoiding FOMO, and understanding risk.', 50, 15, 21, 'F1', WHITE)
    mini_chart(78, 240, 440, 185, [(0.03,0.15),(0.14,0.35),(0.25,0.25),(0.36,0.58),(0.48,0.47),(0.60,0.78),(0.72,0.61),(0.85,0.84),(0.96,0.70)], True)
    text(94, 377, 'RESISTANCE / TAKE-PROFIT WATCH AREA', 10, 'F2', (1,0.84,0.84))
    text(94, 285, 'SUPPORT / BUY WATCH AREA', 10, 'F2', (0.86,1,0.88))
    text(62, 83, 'Version 0.2 visual draft', 10, 'F2', (1,0.78,0.78))
    text(62, 64, 'Education only. Not financial advice. Crypto trading is risky and you can lose money.', 9, 'F1', (1,0.78,0.78))
    finish_page()


def disclaimer_page():
    header('Read This First: Risk Disclaimer', 'This product teaches chart-reading structure. It does not tell you what to buy or promise results.')
    card(58, 545, 480, 105, 'Education only', 'This guide is not financial advice, investment advice, trading advice, tax advice, or a guarantee of profit. Examples are fictional and simplified.', '!')
    card(58, 410, 480, 105, 'Crypto is risky', 'Prices can move quickly, exchanges can fail, liquidity can disappear, and you can lose some or all money you trade.', '!')
    card(58, 275, 480, 105, 'The tool is not a crystal ball', 'Felix Crypto Edge can help you organize a process. It cannot predict the future and cannot remove risk.', '!')
    wrapped(70, 180, 'Beginner promise: before you place any real trade, know where you are wrong, how much you can lose, and why the setup makes sense. If you cannot answer those points, skip it.', 64, 14, 20, 'F2', DARK_RED)
    finish_page()


def contents_page():
    header('What You Will Learn', 'A plain-English path from chart basics to a repeatable practice routine.')
    items = ['1. What crypto trading really is', '2. Beginner mindset', '3. Candlesticks', '4. Support and resistance', '5. Trends and market structure', '6. Timeframes', '7. Volume, moving averages, RSI', '8. Entries, exits, stops, targets', '9. Position sizing and risk', '10. Planned long example', '11. When to skip a trade', '12. Felix Crypto Edge workflow', '13. Checklist', '14. Mistakes', '15. Glossary', '16. 7-day practice plan']
    y = 645
    for i, item in enumerate(items):
        x = 62 if i < 8 else 318
        yy = y - (i % 8) * 61
        circle(x, yy - 4, 10, RED)
        text(x - 4 if i < 9 else x - 7, yy - 8, str(i + 1), 8, 'F2', WHITE)
        wrapped(x + 24, yy + 1, item.split('. ', 1)[1], 31, 11.5, 14, 'F2', TEXT)
    finish_page()


def simple_text_page(title, subtitle, cards, note=None):
    header(title, subtitle)
    y = 590
    for i, (h, b) in enumerate(cards):
        x = 58 if i % 2 == 0 else 312
        yy = y - (i // 2) * 142
        card(x, yy - 95, 225, 105, h, b, str(i + 1))
    if note:
        card(58, 92, 480, 80, 'Dummy rule', note, 'OK', PALE)
    finish_page()


def candle_page():
    header('Candlesticks Explained Simply', 'A candle is a compact picture of what price did during one selected period.')
    x, y = 150, 300
    line(x, y, x, y + 260, GREEN, 3); rect(x - 28, y + 80, 56, 110, GREEN, GREEN, 1)
    text(78, 540, 'High', 12, 'F2', GREEN); line(116, 544, x, y + 260, GREEN, 1)
    text(67, 460, 'Close', 12, 'F2', GREEN); line(116, 464, x - 28, y + 190, GREEN, 1)
    text(70, 365, 'Open', 12, 'F2', GREEN); line(116, 369, x - 28, y + 80, GREEN, 1)
    text(84, 295, 'Low', 12, 'F2', GREEN); line(116, 299, x, y, GREEN, 1)
    x = 410
    line(x, y, x, y + 260, RED, 3); rect(x - 28, y + 80, 56, 110, RED, RED, 1)
    text(333, 540, 'High', 12, 'F2', RED); line(370, 544, x, y + 260, RED, 1)
    text(326, 460, 'Open', 12, 'F2', RED); line(370, 464, x - 28, y + 190, RED, 1)
    text(325, 365, 'Close', 12, 'F2', RED); line(370, 369, x - 28, y + 80, RED, 1)
    text(338, 295, 'Low', 12, 'F2', RED); line(370, 299, x, y, RED, 1)
    card(56, 108, 483, 92, 'Beginner rule', 'Do not trade from one candle alone. A candle matters most when it appears at support, resistance, or a trendline.', '!')
    finish_page()


def zones_page():
    header('Support and Resistance Zones', 'Support is where buyers may step in. Resistance is where sellers may step in. Think zones, not perfect lines.')
    mini_chart(65, 260, 465, 325, [(0.05,0.22),(0.16,0.42),(0.27,0.30),(0.39,0.65),(0.51,0.53),(0.63,0.76),(0.75,0.60),(0.90,0.80)], True)
    text(96, 497, 'RESISTANCE ZONE: price struggled here before', 11, 'F2', (1,0.85,0.85))
    text(96, 318, 'SUPPORT ZONE: price bounced here before', 11, 'F2', (0.86,1,0.88))
    card(56, 120, 230, 88, 'Support', 'A possible area to look for buyers. It can break, so risk still matters.', 'S')
    card(310, 120, 230, 88, 'Resistance', 'A possible area to take profit, avoid chasing, or watch for rejection.', 'R')
    finish_page()


def trend_page():
    header('Trends: Up, Down, or Sideways?', 'Before entries, ask what the market is doing overall.')
    charts = [
        ('Uptrend: higher highs + higher lows', [(0.08,0.25),(0.27,0.47),(0.45,0.35),(0.64,0.68),(0.86,0.56)]),
        ('Downtrend: lower highs + lower lows', [(0.08,0.70),(0.27,0.45),(0.45,0.56),(0.64,0.28),(0.86,0.38)]),
        ('Range: bouncing between zones', [(0.07,0.25),(0.20,0.70),(0.33,0.28),(0.46,0.68),(0.59,0.26),(0.72,0.70),(0.86,0.31)])]
    boxes = [(52,440,240,160),(303,440,240,160),(52,235,491,160)]
    for (label, pts), box in zip(charts, boxes):
        mini_chart(*box, pts, False)
        text(box[0]+12, box[1]+18, label, 10.5, 'F2', (1,0.86,0.86))
    card(56, 96, 483, 92, 'Beginner rule', 'If you cannot tell whether the chart is trending or ranging, do not trade yet. First label the market condition.', '!')
    finish_page()


def timeframe_page():
    header('Timeframes Without Confusion', 'Start big, then zoom in. Do not jump around until you find an excuse to enter.')
    card(58, 500, 145, 130, 'Higher timeframe', 'Daily or 4-hour. Use this for the big direction: uptrend, downtrend, or range.', '1')
    card(225, 500, 145, 130, 'Planning timeframe', '4-hour or 1-hour. Mark zones and decide where a setup would make sense.', '2')
    card(392, 500, 145, 130, 'Entry timeframe', '1-hour or 15-minute. Use only after the bigger plan is already clear.', '3')
    line(203, 565, 225, 565, RED, 3); line(370,565,392,565,RED,3)
    card(70, 265, 455, 115, 'Bad habit', 'A beginner sees a bearish daily chart, then zooms into a tiny 5-minute bounce and buys anyway. That is not analysis. That is searching for permission.', 'X')
    card(70, 120, 455, 100, 'Simple routine', 'Check the daily or 4-hour first. If the big picture is unclear, stop. If it is clear, mark zones and then consider lower-timeframe confirmation.', 'OK')
    finish_page()


def indicator_page():
    header('Indicators: Helpful, Not Magic', 'Volume, moving averages, and RSI can support a plan, but they should not replace market structure.')
    card(58, 515, 480, 90, 'Volume', 'Shows how much trading happened. A breakout with stronger volume can be more meaningful than a weak, low-volume breakout.', 'V')
    card(58, 390, 480, 90, 'Moving averages', 'Smooth price. Price above major averages can suggest bullish structure; below them can suggest bearish structure.', 'MA')
    card(58, 265, 480, 90, 'RSI', 'Measures momentum. Above 70 can be overextended; below 30 can be oversold. Neither is a standalone buy or sell signal.', 'R')
    mini_chart(95, 92, 405, 120, [(0.03,0.25),(0.16,0.38),(0.30,0.35),(0.44,0.58),(0.58,0.62),(0.72,0.75),(0.90,0.66)], False)
    line(110, 132, 485, 172, GOLD, 2)
    text(112, 105, 'Price line + simple moving average example', 10, 'F2', (1,0.84,0.84))
    finish_page()


def risk_page():
    header('The Most Important Part: Risk', 'Beginners obsess over entries. Survivors obsess over how much they can lose if wrong.')
    mini_chart(70, 315, 455, 245, [(0.05,0.20),(0.22,0.36),(0.38,0.32),(0.56,0.55),(0.74,0.72),(0.92,0.63)], False)
    line(95, 405, 500, 405, (0.9,0.9,0.9), 1); text(420, 413, 'Entry', 11, 'F2', WHITE)
    line(95, 355, 500, 355, (0.15,0.75,0.32), 2); text(395, 363, 'Stop-loss', 11, 'F2', (0.8,1,0.84))
    line(95, 515, 500, 515, (1,0.4,0.4), 2); text(412, 523, 'Target', 11, 'F2', (1,0.84,0.84))
    card(56, 205, 230, 75, 'Example', 'Account: EUR 1,000. Risk: 1%. Maximum planned loss: EUR 10.', 'EUR')
    card(310, 205, 230, 75, 'Key idea', 'The stop-loss helps decide how big the position can be.', '!')
    card(56, 92, 483, 80, 'Rule', 'A good trade is not one that must win. A good trade is one where the loss is controlled before you enter.', 'OK')
    finish_page()


def position_size_page():
    header('Position Sizing Made Simple', 'Risk is money, not feelings. Decide the maximum planned loss before the trade.')
    card(60, 545, 475, 90, 'Step 1: choose account risk', 'Example: EUR 1,000 account and 1% risk. That means the maximum planned loss is EUR 10.', '1')
    card(60, 420, 475, 90, 'Step 2: measure stop distance', 'If entry is EUR 100 and stop-loss is EUR 95, the stop distance is EUR 5 per coin/token.', '2')
    card(60, 295, 475, 90, 'Step 3: calculate size', 'Position size = money risked / stop distance. EUR 10 / EUR 5 = 2 units.', '3')
    rect(85, 135, 425, 80, (0.08,0.02,0.025), (0.9,0.1,0.1), 1)
    text(110, 178, 'Formula: position size = money risked / stop distance', 14, 'F2', WHITE)
    text(110, 153, 'Smaller risk keeps your brain calmer and your account alive.', 11, 'F1', (1,0.82,0.82))
    finish_page()


def example_long_page():
    header('Example: A Planned Long Setup', 'Fictional and simplified. The point is the structure, not a prediction.')
    mini_chart(62, 345, 470, 250, [(0.04,0.20),(0.16,0.43),(0.28,0.32),(0.40,0.56),(0.52,0.46),(0.64,0.70),(0.76,0.55),(0.90,0.80)], True)
    text(90, 512, 'Target near next resistance', 10, 'F2', (1,0.84,0.84))
    text(90, 396, 'Pullback into support watch zone', 10, 'F2', (0.86,1,0.88))
    steps = ['4H trend is up', 'Price pulls back to support', 'Candle rejects and closes above zone', 'Stop goes below the zone', 'Target is next resistance', 'Risk is limited to 1%']
    y = 285
    for i, s in enumerate(steps):
        x = 70 if i < 3 else 320
        yy = y - (i % 3) * 58
        circle(x, yy, 11, RED); text(x-4, yy-4, str(i+1), 8, 'F2', WHITE)
        wrapped(x+24, yy+5, s, 30, 10.5, 13, 'F2', TEXT)
    finish_page()


def skip_page():
    simple_text_page('Example: When to Skip a Trade', 'A missed trade is not a loss. A forced trade can become one.', [
        ('Price already pumped', 'If you are buying only because a huge candle happened, you are probably late.'),
        ('No clear level', 'If you cannot identify support, resistance, or invalidation, there is no plan.'),
        ('Bad risk/reward', 'If the stop is far and the target is close, the setup may not be worth it.'),
        ('Emotional state', 'If you are angry, scared, or desperate to win back money, step away.'),
        ('Social signal only', 'Copying strangers online without your own plan is not a process.'),
        ('Too much size', 'If the loss would hurt badly, the position is too big.')
    ], 'Skipping bad trades is one of the fastest ways to improve.')


def tool_page():
    header('How Felix Crypto Edge Helps', 'Use the tool as a training wheel for process, not as a profit machine.')
    mini_chart(55, 255, 485, 335, [(0.04,0.20),(0.12,0.31),(0.22,0.26),(0.33,0.46),(0.43,0.40),(0.55,0.62),(0.67,0.55),(0.78,0.77),(0.90,0.66)], True)
    text(92, 477, 'Possible sell / take-profit zone', 11, 'F2', (1,0.84,0.84))
    text(92, 314, 'Possible buy / watch zone', 11, 'F2', (0.86,1,0.88))
    card(56, 140, 148, 72, 'Trend', 'Is price moving up, down, or sideways?', '1')
    card(224, 140, 148, 72, 'Zones', 'Where did price react before?', '2')
    card(392, 140, 148, 72, 'Risk', 'Where is the idea wrong?', '3')
    card(56, 55, 483, 60, 'Important', 'Good tool output should make you slower and more structured, not reckless.', '!')
    finish_page()


def checklist_page():
    header('Beginner Checklist Before Any Trade', 'If you cannot answer these questions, skip the trade. Skipping bad trades is a skill.')
    questions = ['What coin?', 'What timeframe?', 'Trending or ranging?', 'Where is support?', 'Where is resistance?', 'Why this entry?', 'Where is stop-loss?', 'Where is target?', 'How much risk?', 'Calm or chasing?']
    y = 620
    for i, q in enumerate(questions, 1):
        x = 62 if i <= 5 else 315
        yy = y - ((i - 1) % 5) * 82
        rect(x, yy - 34, 220, 56, LIGHT, (0.9,0.25,0.25), 1)
        circle(x + 20, yy - 6, 11, RED); text(x + 16 if i<10 else x+13, yy - 10, str(i), 8.5, 'F2', WHITE)
        wrapped(x + 42, yy + 1, q, 24, 11, 13, 'F2', TEXT)
    card(56, 94, 483, 80, 'Final rule', 'The goal is not to trade more. The goal is to trade better, smaller, and with a clear reason.', 'OK')
    finish_page()


def mistakes_page():
    simple_text_page('Mistakes That Destroy Beginners', 'Avoiding these mistakes can be more valuable than finding another indicator.', [
        ('FOMO buying', 'Jumping in after a huge green candle because you feel left behind.'),
        ('No stop-loss', 'Refusing to decide where the trade idea is wrong.'),
        ('Too much size', 'Risking so much that one normal loss hurts badly.'),
        ('Signal chasing', 'Blindly copying strangers online without your own plan.'),
        ('Revenge trading', 'Trying to win money back immediately after losing.'),
        ('Indicator overload', 'Making the chart so messy that you cannot think clearly.')
    ], 'The tool supports learning. It does not remove risk.')


def glossary_page(title, terms):
    header(title, 'Plain-English definitions for beginner chart reading.')
    y = 625
    for i, (term, definition) in enumerate(terms):
        x = 58 if i < 7 else 315
        yy = y - (i % 7) * 70
        text(x, yy, term, 12, 'F2', DARK_RED)
        wrapped(x, yy - 18, definition, 31, 9.5, 12, 'F1', TEXT)
    finish_page()


def practice_page():
    header('7-Day Practice Plan', 'Practice on charts before risking real money. The goal is pattern recognition and discipline.')
    days = [
        ('Day 1', 'Label open, high, low, and close on 20 candles.'),
        ('Day 2', 'Mark three support zones and three resistance zones on BTC.'),
        ('Day 3', 'Label uptrend, downtrend, or range on 10 charts.'),
        ('Day 4', 'Write entry, stop-loss, and target for practice setups.'),
        ('Day 5', 'Calculate position size for five fictional trades.'),
        ('Day 6', 'Review mistakes and identify your most likely weakness.'),
        ('Day 7', 'Build a one-page checklist and follow it every time.')]
    y = 620
    for i, (d, task) in enumerate(days):
        rect(65, y - i*72 - 30, 465, 48, LIGHT, (0.9,0.25,0.25), 1)
        text(85, y - i*72 - 3, d, 12, 'F2', DARK_RED)
        wrapped(155, y - i*72 + 2, task, 52, 10.5, 13, 'F1', TEXT)
    finish_page()


def final_page():
    rect(0, 0, W, H, BLACK, None)
    text(60, 640, 'You do not need magic signals.', 30, 'F2', WHITE)
    text(60, 598, 'You need a repeatable process.', 30, 'F2', (1,0.78,0.78))
    wrapped(60, 535, 'Felix Crypto Edge is built to help beginners slow down, read charts clearly, understand risk, and learn why a setup might make sense.', 56, 14, 20, 'F1', WHITE)
    rect(60, 315, 475, 110, (0.12,0.02,0.02), (0.9,0.1,0.1), 1)
    text(82, 382, 'Education only. Not financial advice.', 18, 'F2', WHITE)
    wrapped(82, 350, 'Crypto trading is risky. You can lose money. Always use your own judgment and manage risk.', 52, 12, 17, 'F1', (1,0.82,0.82))
    text(60, 110, 'Felix Crypto Edge - Version 0.2 visual draft', 15, 'F2', (1,0.78,0.78))
    finish_page()


def make_pdf(path):
    objects = []
    def obj(s):
        objects.append(s)
        return len(objects)
    font1 = obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    font2 = obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
    page_ids = []
    content_ids = []
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
    header_bytes = '%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'
    body = ''
    offsets = []
    pos = len(header_bytes.encode('latin-1'))
    for i, s in enumerate(objects, 1):
        offsets.append(pos + len(body.encode('latin-1')))
        body += f'{i} 0 obj\n{s}\nendobj\n'
    xref_start = pos + len(body.encode('latin-1'))
    xref = 'xref\n0 ' + str(len(objects) + 1) + '\n0000000000 65535 f \n'
    for off in offsets:
        xref += f'{off:010d} 00000 n \n'
    trailer = f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_start}\n%%EOF\n'
    Path(path).write_bytes((header_bytes + body + xref + trailer).encode('latin-1'))


def make_html(md_path, html_path):
    md = Path(md_path).read_text()
    def inline(s):
        s = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', s)
        return s
    out = ['<!doctype html><html><head><meta charset="utf-8"><title>Felix Crypto Edge Guide</title><style>',
           '@page{size:A4;margin:18mm}body{font-family:Arial,Helvetica,sans-serif;line-height:1.55;color:#1a1010}h1{color:#b91c1c;font-size:34px;margin-bottom:0}h2{color:#111;font-size:24px;margin-top:32px;border-bottom:2px solid #ef4444;padding-bottom:6px}h3{color:#7f1d1d;margin-top:22px}p{margin:10px 0}li{margin:5px 0}.cover{min-height:620px;display:flex;flex-direction:column;justify-content:center;background:linear-gradient(135deg,#090909,#2b0505);color:white;margin:-18mm -18mm 20mm;padding:30mm}.cover h1{color:white;font-size:48px;line-height:1}.cover h2{color:#fecaca;border:0}.disclaimer{background:#fff1f2;border-left:5px solid #dc2626;padding:12px 16px}strong{color:#7f1d1d}blockquote{background:#fff1f2;border-left:5px solid #dc2626;margin:18px 0;padding:10px 16px}',
           '</style></head><body>']
    in_ul = False
    cover_open = False
    for line0 in md.splitlines():
        line = line0.rstrip()
        if not line:
            if in_ul:
                out.append('</ul>'); in_ul = False
            continue
        if line == '---':
            if in_ul: out.append('</ul>'); in_ul = False
            if cover_open:
                out.append('</section>')
                cover_open = False
            out.append('<hr>'); continue
        if line.startswith('# '):
            out.append(f'<section class="cover"><h1>{inline(line[2:])}</h1>')
            cover_open = True
            continue
        if line.startswith('## '):
            if in_ul: out.append('</ul>'); in_ul = False
            cls = ' class="disclaimer"' if 'Disclaimer' in line else ''
            out.append(f'<h2{cls}>{inline(line[3:])}</h2>'); continue
        if line.startswith('### '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<h3>{inline(line[4:])}</h3>'); continue
        if line.startswith('- '):
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append(f'<li>{inline(line[2:])}</li>'); continue
        if re.match(r'^\d+\. ', line):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<p>{inline(line)}</p>'); continue
        if line.startswith('> '):
            if in_ul: out.append('</ul>'); in_ul = False
            out.append(f'<blockquote>{inline(line[2:])}</blockquote>'); continue
        out.append(f'<p>{inline(line)}</p>')
    if in_ul: out.append('</ul>')
    if cover_open: out.append('</section>')
    out.append('</body></html>')
    Path(html_path).write_text('\n'.join(out))


cover()
disclaimer_page()
contents_page()
simple_text_page('What Crypto Trading Really Is', 'Trading is not guessing. It is planning, managing risk, and accepting uncertainty.', [
    ('Not a prediction game', 'A trader does not need to know the future. A trader needs a plan for what to do if price moves either way.'),
    ('Repeatable process', 'Look for trend, zones, entry reason, invalidation, risk, and reward in the same order every time.'),
    ('Losses are normal', 'Even good setups can fail. The goal is to keep losses small enough to continue learning.'),
    ('No guarantees', 'No indicator, tool, or signal provider can guarantee profit in crypto markets.')
], 'If you cannot explain the trade in one simple sentence, you probably do not have a trade yet.')
simple_text_page('The Beginner Mindset', 'Most beginners lose because they rush. Slow decisions are usually better decisions.', [
    ('Survival first', 'Do not blow up the account. A small account that survives can learn; a destroyed account cannot.'),
    ('Structure second', 'Use the same checklist every time so you can improve your process instead of reacting randomly.'),
    ('Learning third', 'Review what happened after each practice setup. Ask what you saw, what you missed, and what to improve.'),
    ('Emotion control', 'If you feel panic, revenge, or FOMO, step away. Emotion turns small mistakes into expensive ones.')
], 'The market will still be there tomorrow. You do not need to chase today.')
candle_page()
zones_page()
trend_page()
timeframe_page()
indicator_page()
risk_page()
position_size_page()
example_long_page()
skip_page()
tool_page()
checklist_page()
mistakes_page()
glossary_page('Mini Glossary, Part 1', [
    ('Altcoin', 'Any crypto asset that is not Bitcoin.'), ('Breakout', 'Price moving beyond a support or resistance area.'), ('Confirmation', 'Extra evidence before entry, such as a candle close above a level.'), ('FOMO', 'Fear of missing out; chasing because price is moving fast.'), ('Liquidity', 'How easily an asset can be bought or sold.'), ('Long', 'A trade that benefits if price rises.'), ('Pullback', 'A temporary move against the trend.')])
glossary_page('Mini Glossary, Part 2', [
    ('Range', 'Sideways market between support and resistance.'), ('Resistance', 'Area where price may struggle to move higher.'), ('Risk/reward', 'Comparison between possible loss and possible profit.'), ('Short', 'A trade that benefits if price falls; risky for beginners.'), ('Stop-loss', 'Planned exit if the trade idea is wrong.'), ('Support', 'Area where price may stop falling or bounce.'), ('Volatility', 'How fast and strongly price moves.')])
practice_page()
final_page()

make_pdf('products/felix-crypto-edge-guide-visual-preview.pdf')
make_html('products/felix-crypto-edge-guide.md', 'products/felix-crypto-edge-guide.html')
print('created products/felix-crypto-edge-guide-visual-preview.pdf pages', len(pages))
