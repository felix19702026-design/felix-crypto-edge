from pathlib import Path
import textwrap

W, H = 595, 842  # A4
M = 42

pages = []
ops = []

RED = (0.86, 0.10, 0.10)
DARK_RED = (0.32, 0.02, 0.03)
BLACK = (0.04, 0.035, 0.035)
WHITE = (1, 1, 1)
TEXT = (0.09, 0.06, 0.06)
MUTED = (0.42, 0.32, 0.32)
LIGHT = (1.0, 0.94, 0.94)
PALE = (1.0, 0.88, 0.88)
GREEN = (0.05, 0.58, 0.26)


def rgb(c):
    return f"{c[0]} {c[1]} {c[2]}"


def esc(s):
    return (s.replace('\\', '\\\\')
             .replace('(', '\\(').replace(')', '\\)')
             .replace('€', 'EUR').replace('—', '-').replace('–', '-')
             .replace('“', '"').replace('”', '"').replace('’', "'")
             .replace('•', '-').replace('₿', 'BTC'))


def new_page(bg=None):
    global ops
    if bg:
        rect(0, 0, W, H, bg, None)
    if ops:
        pages.append('\n'.join(ops))
    ops = []


def text(x, y, s, size=11, font='F1', color=TEXT):
    ops.append(f"{rgb(color)} rg BT /{font} {size} Tf {x:.1f} {y:.1f} Td ({esc(s)}) Tj ET")


def wrapped(x, y, s, width=70, size=11, leading=15, font='F1', color=TEXT):
    for line in textwrap.wrap(s, width):
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
    # Approx circle with Beziers
    k = 0.55228475 * r
    ops.append(f"{rgb(fill)} rg {x+r:.1f} {y:.1f} m {x+r:.1f} {y+k:.1f} {x+k:.1f} {y+r:.1f} {x:.1f} {y+r:.1f} c {x-k:.1f} {y+r:.1f} {x-r:.1f} {y+k:.1f} {x-r:.1f} {y:.1f} c {x-r:.1f} {y-k:.1f} {x-k:.1f} {y-r:.1f} {x:.1f} {y-r:.1f} c {x+k:.1f} {y-r:.1f} {x+r:.1f} {y-k:.1f} {x+r:.1f} {y:.1f} c f")


def title_page():
    rect(0, 0, W, H, BLACK, None)
    rect(0, 0, W, 18, RED, None)
    rect(42, 118, 511, 520, (0.10, 0.02, 0.025), (0.55, 0.05, 0.06), 2)
    text(62, 590, 'FELIX CRYPTO EDGE', 34, 'F2', WHITE)
    text(62, 552, 'Trading for Beginners', 26, 'F2', (1, 0.78, 0.78))
    y = wrapped(62, 505, 'A simple visual guide for learning crypto charts, spotting possible buy/sell zones, and avoiding the biggest beginner mistakes.', 48, 15, 21, 'F1', WHITE)
    # fake chart
    rect(78, 230, 440, 190, (0.03,0.03,0.03), (0.9,0.1,0.1), 1)
    for i in range(1,6): line(78, 230+i*30, 518, 230+i*30, (0.18,0.08,0.08), 0.5)
    pts = [(90,260),(140,300),(185,285),(230,345),(275,325),(325,380),(370,355),(430,395),(500,370)]
    for a,b in zip(pts, pts[1:]): line(a[0],a[1],b[0],b[1], (1,0.18,0.18), 4)
    rect(90, 244, 410, 34, (0.35,0.02,0.02), (0.85,0.1,0.1), 1)
    text(100, 255, 'POSSIBLE BUY ZONE', 10, 'F2', (1,0.82,0.82))
    text(62, 76, 'Education only. Not financial advice. Crypto trading is risky and you can lose money.', 9, 'F1', (1,0.78,0.78))
    new_page()


def page_header(title, subtitle=None):
    rect(0, 0, W, H, WHITE, None)
    rect(0, H-16, W, 16, RED, None)
    text(M, H-58, title, 24, 'F2', BLACK)
    if subtitle:
        wrapped(M, H-82, subtitle, 78, 10, 14, 'F1', MUTED)
    line(M, H-96, W-M, H-96, RED, 1.2)


def card(x, y, w, h, heading, body, icon=None):
    rect(x, y, w, h, LIGHT, (0.92,0.32,0.32), 1)
    if icon:
        circle(x+23, y+h-30, 14, RED)
        text(x+15, y+h-36, icon, 14, 'F2', WHITE)
        tx = x+48
    else:
        tx = x+14
    text(tx, y+h-28, heading, 13, 'F2', DARK_RED)
    wrapped(x+14, y+h-52, body, int((w-28)/6), 9.5, 13, 'F1', TEXT)


def candle_diagram():
    page_header('1. Candles: The Basic Building Block', 'A candle is just a picture of what price did during one period of time.')
    # green candle
    x=150; y=300
    line(x, y, x, y+260, GREEN, 3)
    rect(x-28, y+80, 56, 110, GREEN, GREEN, 1)
    text(80, 540, 'High', 12, 'F2', GREEN); line(116, 544, x, y+260, GREEN, 1)
    text(70, 460, 'Close', 12, 'F2', GREEN); line(116, 464, x-28, y+190, GREEN, 1)
    text(72, 365, 'Open', 12, 'F2', GREEN); line(116, 369, x-28, y+80, GREEN, 1)
    text(84, 295, 'Low', 12, 'F2', GREEN); line(116, 299, x, y, GREEN, 1)
    text(116, 250, 'Green candle: price closed higher than it opened.', 11, 'F2', TEXT)
    # red candle
    x=410; y=300
    line(x, y, x, y+260, RED, 3)
    rect(x-28, y+80, 56, 110, RED, RED, 1)
    text(333, 540, 'High', 12, 'F2', RED); line(370, 544, x, y+260, RED, 1)
    text(326, 460, 'Open', 12, 'F2', RED); line(370, 464, x-28, y+190, RED, 1)
    text(325, 365, 'Close', 12, 'F2', RED); line(370, 369, x-28, y+80, RED, 1)
    text(338, 295, 'Low', 12, 'F2', RED); line(370, 299, x, y, RED, 1)
    text(365, 250, 'Red candle: price closed lower than it opened.', 11, 'F2', TEXT)
    card(56, 108, 483, 92, 'Dummy rule', 'Do not trade from one candle alone. A candle matters most when it appears at support, resistance, or a trendline.', '!')
    new_page()


def support_resistance_page():
    page_header('2. Support and Resistance', 'Support is where buyers may step in. Resistance is where sellers may step in. Think zones, not perfect lines.')
    rect(65, 255, 465, 330, (0.03,0.03,0.03), (0.75,0.12,0.12), 1)
    for i in range(1,6): line(65,255+i*55,530,255+i*55,(0.16,0.08,0.08),0.5)
    rect(85, 485, 420, 48, (0.40,0.02,0.02), (0.95,0.15,0.15), 1)
    text(96, 503, 'RESISTANCE ZONE: price struggled here before', 11, 'F2', (1,0.85,0.85))
    rect(85, 295, 420, 48, (0.08,0.32,0.13), (0.12,0.70,0.32), 1)
    text(96, 313, 'SUPPORT ZONE: price bounced here before', 11, 'F2', (0.86,1,0.88))
    pts=[(90,330),(140,390),(190,350),(245,470),(300,435),(355,505),(410,455),(485,520)]
    for a,b in zip(pts,pts[1:]): line(a[0],a[1],b[0],b[1],(1,0.2,0.2),4)
    card(56, 120, 230, 88, 'Support', 'A possible area to look for buyers. It can break, so risk still matters.', 'S')
    card(310, 120, 230, 88, 'Resistance', 'A possible area to take profit, avoid chasing, or watch for rejection.', 'R')
    new_page()


def trend_page():
    page_header('3. Trends: Up, Down, or Sideways?', 'Before looking for entries, beginners should ask: what is the market doing overall?')
    # three mini charts
    labels = [('Uptrend: higher highs + higher lows', [(70,500),(120,535),(170,520),(220,570),(270,550)]),
              ('Downtrend: lower highs + lower lows', [(325,570),(375,535),(425,550),(475,505),(525,520)]),
              ('Range: bouncing between zones', [(90,315),(150,365),(210,315),(270,365),(330,315),(390,365),(450,315),(510,365)])]
    boxes=[(52,440,240,160),(303,440,240,160),(52,235,491,160)]
    for (label, pts), (x,y,w,h) in zip(labels,boxes):
        rect(x,y,w,h,(0.04,0.035,0.035),(0.8,0.15,0.15),1)
        for a,b in zip(pts,pts[1:]): line(a[0],a[1],b[0],b[1],RED,3)
        text(x+12,y+18,label,10.5,'F2',(1,0.86,0.86))
    card(56, 96, 483, 92, 'Dummy rule', 'If you cannot tell whether the chart is trending or ranging, you probably should not trade yet. First label the market condition.', '!')
    new_page()


def risk_page():
    page_header('4. The Most Important Part: Risk', 'Beginners obsess over entries. Survivors obsess over how much they can lose if wrong.')
    # trade plan diagram
    rect(70, 310, 455, 250, (0.03,0.03,0.03), (0.75,0.12,0.12), 1)
    line(95, 360, 500, 500, RED, 4)
    line(95, 390, 500, 390, (0.9,0.9,0.9), 1)
    text(420, 398, 'Entry', 11, 'F2', WHITE)
    line(95, 340, 500, 340, (0.15,0.75,0.32), 2)
    text(405, 348, 'Stop-loss', 11, 'F2', (0.8,1,0.84))
    line(95, 510, 500, 510, (1,0.4,0.4), 2)
    text(412, 518, 'Target', 11, 'F2', (1,0.84,0.84))
    card(56, 210, 230, 70, 'Example', 'Account: EUR1,000. Risk: 1%. Max loss: EUR10.', '€')
    card(310, 210, 230, 70, 'Key idea', 'The stop-loss decides how big your position can be.', '!')
    card(56, 93, 483, 84, 'Trading for dummies rule', 'A good trade is not one that must win. A good trade is one where the loss is controlled before you enter.', '✓')
    new_page()


def tool_page():
    page_header('5. How Felix Crypto Edge Helps', 'The tool is not a crystal ball. It is a training wheel that helps beginners follow a process.')
    rect(55, 230, 485, 360, (0.03,0.03,0.03), (0.75,0.12,0.12), 1)
    rect(80, 465, 420, 42, (0.37,0.02,0.02), (0.95,0.13,0.13), 1); text(92, 482, 'Possible sell / take-profit zone', 11, 'F2', (1,0.84,0.84))
    rect(80, 285, 420, 42, (0.05,0.25,0.10), (0.15,0.75,0.32), 1); text(92, 302, 'Possible buy / watch zone', 11, 'F2', (0.86,1,0.88))
    pts=[(90,310),(130,340),(170,325),(210,390),(250,370),(295,435),(335,415),(380,480),(425,455),(500,505)]
    for a,b in zip(pts,pts[1:]): line(a[0],a[1],b[0],b[1],RED,4)
    # side labels
    card(56, 130, 148, 72, 'Trend', 'Is price moving up, down, or sideways?', '1')
    card(224, 130, 148, 72, 'Zones', 'Where did price react before?', '2')
    card(392, 130, 148, 72, 'Risk', 'Where is the idea wrong?', '3')
    new_page()


def checklist_page():
    page_header('6. Beginner Checklist Before Any Trade', 'If you cannot answer these questions, skip the trade. Skipping bad trades is a skill.')
    questions = [
        'What coin am I trading?', 'What timeframe am I using?', 'Is the market trending or ranging?',
        'Where is support?', 'Where is resistance?', 'Why is this entry interesting?',
        'Where is my stop-loss?', 'Where is my target?', 'How much money am I risking?',
        'Am I calm, or am I chasing?'
    ]
    y=620
    for i,q in enumerate(questions,1):
        x = 62 if i<=5 else 315
        yy = y - ((i-1)%5)*82
        rect(x, yy-34, 220, 56, LIGHT, (0.9,0.25,0.25), 1)
        circle(x+20, yy-6, 11, RED); text(x+16, yy-11, str(i), 9, 'F2', WHITE)
        wrapped(x+42, yy+1, q, 24, 10.5, 13, 'F2', TEXT)
    card(56, 94, 483, 80, 'Final rule', 'The goal is not to trade more. The goal is to trade better, smaller, and with a clear reason.', '✓')
    new_page()


def mistake_page():
    page_header('7. Mistakes That Destroy Beginners', 'Avoiding these mistakes can be more valuable than finding another indicator.')
    mistakes=[('FOMO buying','Jumping in after a huge green candle.'),('No stop-loss','Refusing to decide where you are wrong.'),('Too much size','Risking so much that one loss hurts badly.'),('Signal chasing','Blindly copying strangers online.'),('Revenge trading','Trying to win money back immediately.'),('Too many indicators','Making the chart so messy you cannot think.')]
    y=595
    for i,(h,b) in enumerate(mistakes):
        x=58 if i%2==0 else 312
        yy=y-(i//2)*125
        card(x, yy-82, 225, 88, h, b, 'X')
    text(75, 102, 'Remember: the tool supports learning. It does not remove risk.', 17, 'F2', DARK_RED)
    new_page()


def final_page():
    rect(0,0,W,H,BLACK,None)
    text(60, 630, 'You do not need magic signals.', 30, 'F2', WHITE)
    text(60, 590, 'You need a repeatable process.', 30, 'F2', (1,0.78,0.78))
    y = wrapped(60, 525, 'Felix Crypto Edge is built to help beginners slow down, read charts clearly, understand risk, and learn why a trade setup might make sense.', 56, 14, 20, 'F1', WHITE)
    rect(60, 310, 475, 105, (0.12,0.02,0.02), (0.9,0.1,0.1), 1)
    text(82, 374, 'Education only. Not financial advice.', 18, 'F2', WHITE)
    wrapped(82, 345, 'Crypto trading is risky. You can lose money. Always use your own judgment and manage risk.', 52, 12, 17, 'F1', (1,0.82,0.82))
    text(60, 110, 'Felix Crypto Edge', 18, 'F2', (1,0.78,0.78))
    new_page()


def make_pdf(path):
    objects=[]
    def obj(s): objects.append(s); return len(objects)
    font1=obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>')
    font2=obj('<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>')
    page_ids=[]; content_ids=[]
    for stream in pages:
        data=stream.encode('latin-1','replace')
        cid=obj(f'<< /Length {len(data)} >>\nstream\n'+data.decode('latin-1')+'\nendstream')
        content_ids.append(cid); page_ids.append(obj(''))
    pages_id=obj('')
    catalog_id=obj(f'<< /Type /Catalog /Pages {pages_id} 0 R >>')
    for idx,pid in enumerate(page_ids):
        objects[pid-1]=f'<< /Type /Page /Parent {pages_id} 0 R /MediaBox [0 0 {W} {H}] /Resources << /Font << /F1 {font1} 0 R /F2 {font2} 0 R >> >> /Contents {content_ids[idx]} 0 R >>'
    objects[pages_id-1]=f'<< /Type /Pages /Kids ['+' '.join(f'{p} 0 R' for p in page_ids)+f'] /Count {len(page_ids)} >>'
    header='%PDF-1.4\n%\xe2\xe3\xcf\xd3\n'
    body=''; offsets=[]; pos=len(header.encode('latin-1'))
    for i,s in enumerate(objects,1):
        offsets.append(pos+len(body.encode('latin-1')))
        body += f'{i} 0 obj\n{s}\nendobj\n'
    xref_start=pos+len(body.encode('latin-1'))
    xref='xref\n0 '+str(len(objects)+1)+'\n0000000000 65535 f \n'
    for off in offsets: xref += f'{off:010d} 00000 n \n'
    trailer=f'trailer\n<< /Size {len(objects)+1} /Root {catalog_id} 0 R >>\nstartxref\n{xref_start}\n%%EOF\n'
    Path(path).write_bytes((header+body+xref+trailer).encode('latin-1'))


title_page()
candle_diagram()
support_resistance_page()
trend_page()
risk_page()
tool_page()
checklist_page()
mistake_page()
final_page()
make_pdf('products/felix-crypto-edge-guide-visual-preview.pdf')
print('created products/felix-crypto-edge-guide-visual-preview.pdf pages', len(pages))
