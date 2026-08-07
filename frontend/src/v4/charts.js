// Gentelella 2026 v4 — ECharts integration
// Dynamic-imports ECharts only when a [data-chart] element is present on the
// page, keeping pages without charts free of the ~400kB cost.

const tokens = () => {
  const cs = getComputedStyle(document.documentElement);
  return {
    primary: cs.getPropertyValue('--primary').trim(),
    primaryDk: cs.getPropertyValue('--primary-dk').trim(),
    azure: cs.getPropertyValue('--azure').trim(),
    blue: cs.getPropertyValue('--blue').trim(),
    yellow: cs.getPropertyValue('--yellow').trim(),
    green: cs.getPropertyValue('--green').trim(),
    red: cs.getPropertyValue('--red').trim(),
    purple: cs.getPropertyValue('--purple').trim(),
    text: cs.getPropertyValue('--text').trim(),
    textMuted: cs.getPropertyValue('--text-muted').trim(),
    borderLight: cs.getPropertyValue('--border-color-light').trim(),
    bgSurface: cs.getPropertyValue('--bg-surface').trim()
  };
};

const fontFamily = "'Inter', -apple-system, BlinkMacSystemFont, sans-serif";

function baseOption(t) {
  return {
    textStyle: { fontFamily, fontSize: 11, color: t.textMuted },
    grid: { left: 36, right: 12, top: 16, bottom: 28, containLabel: false },
    tooltip: {
      backgroundColor: t.bgSurface,
      borderColor: t.borderLight,
      borderWidth: 1,
      padding: [8, 10],
      textStyle: { color: t.text, fontSize: 12, fontFamily },
      extraCssText: 'box-shadow: 0 2px 8px rgba(30,38,51,0.08); border-radius: 6px;'
    }
  };
}

// logic from charts, the graph. WHICH IS TO BE THE DOWNOAD LOG ACTIVITY
function dashboardNetwork(echarts, el, t) {
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const sessions = [420, 580, 510, 720, 680, 790, 752];
  const pageviews = [320, 460, 410, 580, 540, 660, 620];
  const chart = echarts.init(el);
  chart.setOption({
    ...baseOption(t),
    tooltip: { ...baseOption(t).tooltip, trigger: 'axis', axisPointer: { type: 'line', lineStyle: { color: t.borderLight } } },
    legend: { show: false },
    xAxis: {
      type: 'category',
      data: days,
      boundaryGap: false,
      axisLine: { lineStyle: { color: t.borderLight } },
      axisTick: { show: false },
      axisLabel: { color: t.textMuted, fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: t.borderLight, type: [4, 3] } },
      axisLabel: { color: t.textMuted, fontSize: 10 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [
      {
        name: 'Sessions',
        type: 'line',
        smooth: true,
        symbol: 'circle',
        symbolSize: 5,
        showSymbol: false,
        data: sessions,
        lineStyle: { color: t.primary, width: 2 },
        itemStyle: { color: t.primary, borderColor: t.bgSurface, borderWidth: 2 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: t.primary + '33' },
            { offset: 1, color: t.primary + '00' }
          ])
        }
      },
      {
        name: 'Page views',
        type: 'line',
        smooth: true,
        showSymbol: false,
        data: pageviews,
        lineStyle: { color: t.azure, width: 1.5, type: 'dashed' },
        itemStyle: { color: t.azure }
      }
    ]
  });
  return chart;
}

function revenueLine(echarts, el, t) {
  const months = ['May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr'];
  const rev = [12400, 14200, 15600, 17800, 19200, 21500, 23100, 24800, 26200, 27900, 29400, 30100];
  const chart = echarts.init(el);
  chart.setOption({
    ...baseOption(t),
    tooltip: { ...baseOption(t).tooltip, trigger: 'axis', valueFormatter: (v) => '$' + v.toLocaleString() },
    xAxis: {
      type: 'category',
      data: months,
      boundaryGap: false,
      axisLine: { lineStyle: { color: t.borderLight } },
      axisTick: { show: false },
      axisLabel: { color: t.textMuted, fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: t.borderLight, type: [4, 3] } },
      axisLabel: { color: t.textMuted, fontSize: 10, formatter: (v) => '$' + (v / 1000) + 'k' },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [{
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: rev,
      lineStyle: { color: t.primary, width: 2 },
      itemStyle: { color: t.primary },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: t.primary + '40' },
          { offset: 1, color: t.primary + '00' }
        ])
      }
    }]
  });
  return chart;
}

function salesBar(echarts, el, t) {
  const channels = ['Web', 'Mobile', 'Email', 'Social', 'Direct', 'Partner'];
  const values = [82, 96, 64, 45, 88, 58];
  const colors = [t.primary, t.azure, t.yellow, t.green, t.purple, t.red];
  const chart = echarts.init(el);
  chart.setOption({
    ...baseOption(t),
    grid: { ...baseOption(t).grid, left: 28 },
    tooltip: { ...baseOption(t).tooltip, trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: channels,
      axisLine: { lineStyle: { color: t.borderLight } },
      axisTick: { show: false },
      axisLabel: { color: t.textMuted, fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: t.borderLight, type: [4, 3] } },
      axisLabel: { color: t.textMuted, fontSize: 10 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [{
      type: 'bar',
      data: values.map((v, i) => ({ value: v, itemStyle: { color: colors[i], borderRadius: [4, 4, 0, 0] } })),
      barWidth: '52%'
    }]
  });
  return chart;
}

// DETELE THIS
function trafficDonut(echarts, el, t) {
  const chart = echarts.init(el);
  chart.setOption({
    textStyle: { fontFamily, color: t.textMuted },
    tooltip: {
      ...baseOption(t).tooltip,
      trigger: 'item',
      formatter: '{b}: {d}%'
    },
    legend: { show: false },
    series: [{
      type: 'pie',
      radius: ['62%', '88%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      label: { show: false },
      labelLine: { show: false },
      data: [
        { value: 40, name: 'Organic', itemStyle: { color: t.primary, borderColor: t.bgSurface, borderWidth: 2 } },
        { value: 20, name: 'Direct',  itemStyle: { color: t.azure,   borderColor: t.bgSurface, borderWidth: 2 } },
        { value: 15, name: 'Referral',itemStyle: { color: t.yellow,  borderColor: t.bgSurface, borderWidth: 2 } },
        { value: 12, name: 'Social',  itemStyle: { color: t.purple,  borderColor: t.bgSurface, borderWidth: 2 } },
        { value: 13, name: 'Email',   itemStyle: { color: t.green,   borderColor: t.bgSurface, borderWidth: 2 } }
      ]
    }]
  });
  return chart;
}

function donut(echarts, el, t, segments, _totalLabel) {
  const chart = echarts.init(el);
  chart.setOption({
    textStyle: { fontFamily, color: t.textMuted },
    tooltip: {
      ...baseOption(t).tooltip,
      trigger: 'item',
      formatter: '{b}: {d}%'
    },
    legend: { show: false },
    series: [{
      type: 'pie',
      radius: ['62%', '88%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      label: { show: false },
      labelLine: { show: false },
      data: segments.map(([name, value, color]) => ({
        name,
        value,
        itemStyle: { color: t[color] || color, borderColor: t.bgSurface, borderWidth: 2 }
      }))
    }]
  });
  return chart;
}

// data to be passed here from API, for role distribution
const deviceUsage = (echarts, el, t) => donut(echarts, el, t, [
  ['Students',     50, 'primary'],
  ['Admins', 2, 'azure'],
  ['Owner', 1, 'yellow'],
  ['Lectures',  0, 'purple'],
]);



// ────────────────────────
//  Mixed bar+line — bars with a trend line on a secondary axis
// ────────────────────────
function mixedBarLine(echarts, el, t) {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'];
  const orders = [240, 312, 285, 360, 420, 395, 460, 510];
  const aov = [82, 88, 86, 92, 95, 94, 99, 104];
  const chart = echarts.init(el);
  chart.setOption({
    ...baseOption(t),
    tooltip: { ...baseOption(t).tooltip, trigger: 'axis' },
    legend: {
      data: ['Orders', 'Avg order value'],
      bottom: 0, itemGap: 16, icon: 'circle', itemWidth: 8, itemHeight: 8,
      textStyle: { color: t.textMuted, fontSize: 11 }
    },
    grid: { ...baseOption(t).grid, right: 44, bottom: 36 },
    xAxis: {
      type: 'category', data: months,
      axisLine: { lineStyle: { color: t.borderLight } },
      axisTick: { show: false },
      axisLabel: { color: t.textMuted, fontSize: 10 }
    },
    yAxis: [
      {
        type: 'value', name: 'Orders',
        nameTextStyle: { color: t.textMuted, fontSize: 10 },
        splitLine: { lineStyle: { color: t.borderLight, type: [4, 3] } },
        axisLabel: { color: t.textMuted, fontSize: 10 },
        axisLine: { show: false }, axisTick: { show: false }
      },
      {
        type: 'value', name: 'AOV $',
        nameTextStyle: { color: t.textMuted, fontSize: 10 },
        splitLine: { show: false },
        axisLabel: { color: t.textMuted, fontSize: 10, formatter: '${value}' },
        axisLine: { show: false }, axisTick: { show: false }
      }
    ],
    series: [
      {
        name: 'Orders', type: 'bar', yAxisIndex: 0, data: orders,
        barWidth: '40%',
        itemStyle: { color: t.azure, borderRadius: [4, 4, 0, 0] }
      },
      {
        name: 'Avg order value', type: 'line', yAxisIndex: 1, data: aov,
        smooth: true, symbol: 'circle', symbolSize: 6,
        lineStyle: { color: t.primary, width: 2 },
        itemStyle: { color: t.primary, borderColor: t.bgSurface, borderWidth: 2 }
      }
    ]
  });
  return chart;
}


// ────────────────────────
//  Calendar heatmap — GitHub-contribution-style year view
// ────────────────────────
function calendarHeatmap(echarts, el, t) {
  // Build a year of synthetic activity ending today.
  const today = new Date();
  const start = new Date(today);
  start.setMonth(start.getMonth() - 11);
  start.setDate(1);
  const data = [];
  for (let d = new Date(start); d <= today; d.setDate(d.getDate() + 1)) {
    const dow = d.getDay();
    const wd = dow >= 1 && dow <= 5 ? 1 : 0.4;
    const v = Math.max(0, Math.round(wd * (Math.random() * 100)));
    data.push([d.toISOString().slice(0, 10), v]);
  }
  const chart = echarts.init(el);
  chart.setOption({
    textStyle: { fontFamily, color: t.textMuted },
    tooltip: { ...baseOption(t).tooltip, formatter: (p) => `${p.value[0]}: ${p.value[1]} contributions` },
    visualMap: {
      min: 0, max: 100,
      show: false,
      inRange: { color: [t.borderLight, t.primary, t.primaryDk] }
    },
    calendar: {
      top: 30, left: 24, right: 24, bottom: 12,
      cellSize: ['auto', 14],
      range: [start.toISOString().slice(0, 7), today.toISOString().slice(0, 10)],
      itemStyle: { color: t.bgSurfaceSecondary || t.borderLight, borderColor: t.bgSurface, borderWidth: 2 },
      splitLine: { show: false },
      yearLabel: { show: false },
      monthLabel: { color: t.textMuted, fontSize: 10, fontFamily },
      dayLabel: { color: t.textMuted, fontSize: 10, fontFamily, firstDay: 1 }
    },
    series: { type: 'heatmap', coordinateSystem: 'calendar', data }
  });
  return chart;
}


const charts = {
  'dashboard-network': dashboardNetwork,
  'revenue-line':      revenueLine,
  'sales-bar':         salesBar,
  'traffic-donut':     trafficDonut,
  'device-usage':      deviceUsage,

  'mixed-bar-line':    mixedBarLine,

  'calendar-heatmap':  calendarHeatmap,
  
};

/**
 * Mount ECharts on every `<div data-chart="…">` on the page. The `data-chart`
 * value selects a registered factory (see `charts` map below — e.g.
 * `revenue-line`, `traffic-donut`). Charts auto-resize on window resize and
 * re-init when the document `data-theme` attribute changes so they pick up
 * fresh CSS-custom-property colors.
 *
 * Lazily imports `echarts/core` + the chart types and components actually used;
 * the import never fires on pages without a matching element.
 * @returns {Promise<void>}
 */
export async function initCharts() {
  const elements = document.querySelectorAll('[data-chart]');
  if (!elements.length) {return;}
  // Show skeleton placeholders while ECharts loads. Removed once each chart
  // mounts. Skipped if the page already pre-renders content inside the host.
  elements.forEach((el) => {
    if (!el.children.length && !el.classList.contains('skeleton')) {
      el.classList.add('skeleton', 'chart-skeleton');
    }
  });

  // Modular import keeps the bundle smaller than the full echarts barrel.
  const [
    echartsCore,
    {
      LineChart, BarChart, PieChart,
      RadarChart, GaugeChart, ScatterChart,
      HeatmapChart, FunnelChart, CandlestickChart,
      TreemapChart, SankeyChart, CustomChart
    },
    {
      GridComponent, TooltipComponent, LegendComponent,
      VisualMapComponent, PolarComponent, CalendarComponent
    },
    { CanvasRenderer }
  ] = await Promise.all([
    import('echarts/core'),
    import('echarts/charts'),
    import('echarts/components'),
    import('echarts/renderers')
  ]);
  echartsCore.use([
    LineChart, BarChart, PieChart,
    RadarChart, GaugeChart, ScatterChart,
    HeatmapChart, FunnelChart, CandlestickChart,
    TreemapChart, SankeyChart, CustomChart,
    GridComponent, TooltipComponent, LegendComponent,
    VisualMapComponent, PolarComponent, CalendarComponent,
    CanvasRenderer
  ]);

  const mounted = []; // { el, factory, instance }

  const buildAll = () => {
    const t = tokens();
    elements.forEach((el) => {
      const factory = charts[el.dataset.chart];
      if (!factory) {return;}
      el.classList.remove('skeleton', 'chart-skeleton');
      mounted.push({ el, factory, instance: factory(echartsCore, el, t) });
    });
  };

  buildAll();

  // Resize all charts on viewport changes.
  let timer;
  window.addEventListener('resize', () => {
    clearTimeout(timer);
    timer = setTimeout(() => mounted.forEach((m) => m.instance.resize()), 120);
  });

  // Rebuild all charts when the theme changes — tokens come from CSS custom
  // properties, so a fresh setOption isn't enough; dispose + re-init picks up
  // new colors cleanly. Listens for both data-theme attribute changes (light/
  // dark toggle) and a 'themechange' custom event (theme generator page).
  const rebuild = () => {
    const t = tokens();
    mounted.forEach((m) => {
      m.instance.dispose();
      m.instance = m.factory(echartsCore, m.el, t);
    });
  };
  const themeObserver = new MutationObserver((records) => {
    if (records.some((r) => r.attributeName === 'data-theme')) {rebuild();}
  });
  themeObserver.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
  document.documentElement.addEventListener('themechange', rebuild);
}
