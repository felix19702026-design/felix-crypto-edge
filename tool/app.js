const demoMarkets = {
  BTC: {
    symbol: 'BTC/USDT',
    prices: [62400, 63150, 62820, 63950, 64600, 64220, 65180, 66050, 65680, 66840, 67410, 67120, 68180, 69040, 68660, 69880, 70450, 69960, 71180, 72420, 71940, 73250, 74110, 73680],
    note: 'Higher highs with pullbacks near the moving average'
  },
  ETH: {
    symbol: 'ETH/USDT',
    prices: [2890, 2925, 2880, 2840, 2910, 2965, 3010, 2985, 3045, 3090, 3060, 3125, 3180, 3155, 3205, 3260, 3235, 3310, 3365, 3320, 3380, 3450, 3415, 3490],
    note: 'Steady grind up with clear support reactions'
  },
  SOL: {
    symbol: 'SOL/USDT',
    prices: [141, 146, 144, 151, 158, 154, 162, 169, 164, 172, 177, 174, 181, 188, 184, 179, 173, 176, 182, 190, 187, 194, 201, 197],
    note: 'More volatile swings; position size matters'
  }
};

const $ = (id) => document.getElementById(id);
const fmt = (value, symbol) => symbol === 'SOL/USDT' ? `$${value.toFixed(2)}` : `$${Math.round(value).toLocaleString()}`;

function movingAverage(values, period = 5) {
  return values.map((_, index) => {
    const start = Math.max(0, index - period + 1);
    const slice = values.slice(start, index + 1);
    return slice.reduce((sum, value) => sum + value, 0) / slice.length;
  });
}

function rsiLike(values, period = 14) {
  const start = Math.max(1, values.length - period);
  let gains = 0;
  let losses = 0;
  for (let i = start; i < values.length; i++) {
    const change = values[i] - values[i - 1];
    if (change >= 0) gains += change;
    else losses += Math.abs(change);
  }
  if (losses === 0) return 82;
  const rs = gains / losses;
  return 100 - (100 / (1 + rs));
}

function trendText(values, ma) {
  const last = values.at(-1);
  const prev = values.at(-6);
  const lastMa = ma.at(-1);
  if (last > lastMa && last > prev) return 'Uptrend watch';
  if (last < lastMa && last < prev) return 'Downtrend caution';
  return 'Sideways / wait';
}

function pathFor(points) {
  return points.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x.toFixed(1)} ${point.y.toFixed(1)}`).join(' ');
}

function render(assetKey) {
  const market = demoMarkets[assetKey];
  const prices = market.prices;
  const ma = movingAverage(prices);
  const rsi = rsiLike(prices);
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  const pad = (max - min) * 0.16;
  const low = min - pad;
  const high = max + pad;
  const support = Math.min(...prices.slice(-12));
  const resistance = Math.max(...prices.slice(-12));
  const buyLow = support;
  const buyHigh = support + (max - min) * 0.12;
  const sellLow = resistance - (max - min) * 0.12;
  const sellHigh = resistance;

  const width = 920;
  const height = 430;
  const margin = { top: 34, right: 70, bottom: 44, left: 58 };
  const innerW = width - margin.left - margin.right;
  const innerH = height - margin.top - margin.bottom;
  const x = (index) => margin.left + (index / (prices.length - 1)) * innerW;
  const y = (value) => margin.top + ((high - value) / (high - low)) * innerH;
  const points = prices.map((value, index) => ({ x: x(index), y: y(value) }));
  const maPoints = ma.map((value, index) => ({ x: x(index), y: y(value) }));

  const chart = $('chart');
  chart.innerHTML = `
    <title id="chartTitle">${market.symbol} educational demo chart</title>
    <desc id="chartDesc">Demo line chart showing price, moving average, support zone, resistance zone, and educational watch labels.</desc>
    ${[0,1,2,3,4].map(i => `<line class="grid-line" x1="${margin.left}" x2="${width - margin.right}" y1="${margin.top + i * innerH / 4}" y2="${margin.top + i * innerH / 4}" />`).join('')}
    ${[0,1,2,3,4,5].map(i => `<line class="grid-line" y1="${margin.top}" y2="${height - margin.bottom}" x1="${margin.left + i * innerW / 5}" x2="${margin.left + i * innerW / 5}" />`).join('')}
    <rect class="zone-rect" x="${margin.left}" y="${y(sellHigh)}" width="${innerW}" height="${Math.max(8, y(sellLow) - y(sellHigh))}" fill="#f59e0b" />
    <rect class="zone-rect" x="${margin.left}" y="${y(buyHigh)}" width="${innerW}" height="${Math.max(8, y(buyLow) - y(buyHigh))}" fill="#22c55e" />
    <path class="ma-line" d="${pathFor(maPoints)}" />
    <path class="price-line" d="${pathFor(points)}" />
    <circle class="price-dot" cx="${points.at(-1).x}" cy="${points.at(-1).y}" r="7" />
    <text class="axis-text" x="${width - margin.right + 12}" y="${y(resistance) + 5}">${fmt(resistance, market.symbol)}</text>
    <text class="axis-text" x="${width - margin.right + 12}" y="${y(support) + 5}">${fmt(support, market.symbol)}</text>
    <rect class="label-box" x="${margin.left + 18}" y="${Math.max(20, y(sellHigh) - 38)}" width="234" height="34" stroke="#f59e0b" />
    <text class="label-text" x="${margin.left + 32}" y="${Math.max(43, y(sellHigh) - 15)}">Possible sell zone</text>
    <rect class="label-box" x="${margin.left + 18}" y="${Math.min(height - 78, y(buyLow) + 12)}" width="236" height="34" stroke="#22c55e" />
    <text class="label-text" x="${margin.left + 32}" y="${Math.min(height - 55, y(buyLow) + 35)}">Possible buy zone</text>
  `;

  $('assetTitle').textContent = market.symbol;
  $('scenarioBadge').textContent = market.note;
  $('lastPrice').textContent = fmt(prices.at(-1), market.symbol);
  $('trendRead').textContent = trendText(prices, ma);
  const rsiRounded = Math.round(rsi);
  $('rsiRead').textContent = `${rsiRounded} / 100 ${rsiRounded > 70 ? '(hot)' : rsiRounded < 35 ? '(weak)' : '(neutral)'}`;
  $('supportRead').textContent = `${fmt(buyLow, market.symbol)}–${fmt(buyHigh, market.symbol)}`;
  $('resistanceRead').textContent = `${fmt(sellLow, market.symbol)}–${fmt(sellHigh, market.symbol)}`;
  $('buyLabel').textContent = `${fmt(buyLow, market.symbol)}–${fmt(buyHigh, market.symbol)}`;
  $('sellLabel').textContent = `${fmt(sellLow, market.symbol)}–${fmt(sellHigh, market.symbol)}`;
}

$('assetSelect').addEventListener('change', (event) => render(event.target.value));
render('BTC');
