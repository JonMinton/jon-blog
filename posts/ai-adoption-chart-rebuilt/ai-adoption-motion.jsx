import { useState, useEffect, useRef } from "react";

// ---------------------------------------------------------------------------
// Regenerated "Each dot is ~N million people" chart, 2023 → 2026
// Snapshots triangulated from Microsoft AI Economy Institute diffusion
// reports (H1/H2 2025, Q1 2026), OpenAI/Reuters user disclosures, Microsoft
// earnings (Copilot), and ITU connectivity data. Values in millions.
// ---------------------------------------------------------------------------

const SNAPSHOTS = [
  // t = decimal year
  { t: 2023.5,  label: "Jun 2023", pop: 8045, offline: 2600, users: 350,  usersLo: 200,  usersHi: 500,  paid: 2,  paidLo: 1,  paidHi: 4,  code: 1.5, codeLo: 1,  codeHi: 2 },
  { t: 2024.0,  label: "Dec 2023", pop: 8080, offline: 2600, users: 500,  usersLo: 350,  usersHi: 700,  paid: 5,  paidLo: 3,  paidHi: 8,  code: 2,   codeLo: 1.5,codeHi: 3 },
  { t: 2024.5,  label: "Jun 2024", pop: 8120, offline: 2500, users: 650,  usersLo: 450,  usersHi: 900,  paid: 10, paidLo: 7,  paidHi: 14, code: 2.8, codeLo: 2,  codeHi: 4 },
  { t: 2025.0,  label: "Dec 2024", pop: 8160, offline: 2400, users: 800,  usersLo: 600,  usersHi: 1000, paid: 16, paidLo: 11, paidHi: 25, code: 3.8, codeLo: 3,  codeHi: 6 },
  { t: 2025.5,  label: "Jun 2025", pop: 8190, offline: 2300, users: 810,  usersLo: 700,  usersHi: 1100, paid: 40, paidLo: 30, paidHi: 55, code: 5,   codeLo: 4,  codeHi: 8 },
  { t: 2026.0,  label: "Dec 2025", pop: 8230, offline: 2200, users: 880,  usersLo: 800,  usersHi: 1300, paid: 60, paidLo: 45, paidHi: 85, code: 8,   codeLo: 6,  codeHi: 11 },
  { t: 2026.25, label: "Mar 2026", pop: 8250, offline: 2200, users: 965,  usersLo: 850,  usersHi: 1400, paid: 70, paidLo: 55, paidHi: 95, code: 9,   codeLo: 7,  codeHi: 12 },
];

const T_MIN = SNAPSHOTS[0].t;
const T_MAX = SNAPSHOTS[SNAPSHOTS.length - 1].t;

const MILESTONES = [
  { t: 2023.2,  label: "GPT-4" },
  { t: 2023.95, label: "Gemini" },
  { t: 2024.37, label: "GPT-4o" },
  { t: 2025.05, label: "DeepSeek-R1" },
  { t: 2025.6,  label: "GPT-5" },
];

const N_SIDE = 50;
const N_DOTS = N_SIDE * N_SIDE;

const TIERS = [
  { key: "offline",     name: "Offline — no internet access", color: "#A89F93" },
  { key: "neverOnline", name: "Online, never used gen AI",    color: "#DAD6CE" },
  { key: "free",        name: "Free-tier user",               color: "#6FA877" },
  { key: "paid",        name: "Paid subscriber",              color: "#D9A441" },
  { key: "code",        name: "Coding-tool user",             color: "#B5493F" },
];

function lerp(a, b, f) { return a + (b - a) * f; }

// Interpolate every field between the two bracketing snapshots
function stateAt(t) {
  const clamped = Math.min(Math.max(t, T_MIN), T_MAX);
  let i = 0;
  while (i < SNAPSHOTS.length - 2 && SNAPSHOTS[i + 1].t < clamped) i++;
  const a = SNAPSHOTS[i], b = SNAPSHOTS[i + 1];
  const f = (clamped - a.t) / (b.t - a.t);
  const g = (k) => lerp(a[k], b[k], f);
  return {
    pop: g("pop"), offline: g("offline"),
    users: g("users"), usersLo: g("usersLo"), usersHi: g("usersHi"),
    paid: g("paid"), paidLo: g("paidLo"), paidHi: g("paidHi"),
    code: g("code"), codeLo: g("codeLo"), codeHi: g("codeHi"),
  };
}

// Exclusive tier counts (millions) from nested totals
function tiersOf(s) {
  const code = s.code;
  const paid = Math.max(s.paid - s.code, 0);
  const free = Math.max(s.users - s.paid, 0);
  const offline = s.offline;
  const neverOnline = Math.max(s.pop - s.users - s.offline, 0);
  return { offline, neverOnline, free, paid, code };
}

// Largest-remainder allocation to exactly N_DOTS, min 1 dot per non-zero tier
function allocateDots(counts, pop) {
  const keys = TIERS.map((t) => t.key);
  const raw = keys.map((k) => (counts[k] / pop) * N_DOTS);
  const base = raw.map((r, i) => {
    const fl = Math.floor(r);
    return counts[keys[i]] > 0 && fl === 0 ? 1 : fl;
  });
  let short = N_DOTS - base.reduce((a, b) => a + b, 0);
  const rem = raw.map((r, i) => ({ i, rem: r - Math.floor(r) }))
    .sort((a, b) => b.rem - a.rem);
  let j = 0;
  while (short > 0) { base[rem[j % rem.length].i] += 1; short--; j++; }
  while (short < 0) {
    const big = base.indexOf(Math.max(...base));
    base[big] -= 1; short++;
  }
  return base; // dots per tier, in TIERS order
}

function fmt(m) {
  if (m >= 1000) return (m / 1000).toFixed(2) + " bn";
  if (m >= 100) return Math.round(m) + " M";
  return m >= 10 ? m.toFixed(0) + " M" : m.toFixed(1) + " M";
}

function pct(m, pop) {
  const p = (m / pop) * 100;
  if (p >= 1) return p.toFixed(0) + "%";
  if (p >= 0.1) return p.toFixed(1) + "%";
  return p.toFixed(2) + "%";
}

export default function App() {
  const [t, setT] = useState(T_MAX); // open on the up-to-date frame
  const [playing, setPlaying] = useState(false);
  const raf = useRef(null);
  const reduced = typeof window !== "undefined" &&
    window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  useEffect(() => {
    if (!playing) return;
    let last = performance.now();
    const step = (now) => {
      const dt = (now - last) / 1000;
      last = now;
      setT((prev) => {
        const speed = reduced ? 2.0 : 0.55; // years per second
        const next = prev + dt * speed;
        if (next >= T_MAX) { setPlaying(false); return T_MAX; }
        return next;
      });
      raf.current = requestAnimationFrame(step);
    };
    raf.current = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf.current);
  }, [playing, reduced]);

  const s = stateAt(t);
  const tiers = tiersOf(s);
  const dots = allocateDots(tiers, s.pop);

  // Build cumulative thresholds → colour per dot index (row-major fill)
  const thresholds = [];
  let acc = 0;
  dots.forEach((d) => { acc += d; thresholds.push(acc); });
  const colorFor = (idx) => {
    for (let i = 0; i < thresholds.length; i++)
      if (idx < thresholds[i]) return TIERS[i].color;
    return TIERS[TIERS.length - 1].color;
  };

  const perDot = s.pop / N_DOTS;
  const dateLabel = (() => {
    const yr = Math.floor(t);
    const m = Math.round((t - yr) * 12);
    const names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
    return m >= 12 ? `Jan ${yr + 1}` : `${names[m]} ${yr}`;
  })();

  const CELL = 10, GAP = 2.2;
  const size = N_SIDE * CELL;

  const rows = [
    { tier: TIERS[0], v: tiers.offline, range: null },
    { tier: TIERS[1], v: tiers.neverOnline, range: null },
    { tier: TIERS[2], v: tiers.free, range: [Math.max(s.usersLo - s.paid, 0), s.usersHi - s.paid] },
    { tier: TIERS[3], v: tiers.paid, range: [s.paidLo - s.code, s.paidHi - s.code] },
    { tier: TIERS[4], v: tiers.code, range: [s.codeLo, s.codeHi] },
  ];

  return (
    <div style={{
      minHeight: "100vh", background: "#FBFAF7", color: "#26231F",
      fontFamily: "ui-monospace, 'SF Mono', Menlo, monospace",
      display: "flex", justifyContent: "center", padding: "28px 14px 48px",
    }}>
      <div style={{ width: "100%", maxWidth: 640 }}>
        <h1 style={{
          fontFamily: "Georgia, 'Times New Roman', serif",
          fontWeight: 400, fontSize: "clamp(24px, 5.5vw, 34px)",
          textAlign: "center", margin: "0 0 8px",
        }}>
          Each dot is ~{perDot.toFixed(1)} million people
        </h1>
        <p style={{
          textAlign: "center", fontSize: 12, color: "#7A756C",
          margin: "0 0 20px", lineHeight: 1.5,
        }}>
          2,500 dots = {(s.pop / 1000).toFixed(2)} billion humans.
          Colour = deepest gen-AI engagement, <strong style={{ color: "#26231F" }}>{dateLabel}</strong>.
        </p>

        <svg
          viewBox={`0 0 ${size} ${size}`}
          style={{ width: "100%", display: "block" }}
          role="img"
          aria-label={`Waffle chart of global AI adoption tiers, ${dateLabel}`}
        >
          {Array.from({ length: N_DOTS }, (_, i) => {
            const x = (i % N_SIDE) * CELL;
            const y = Math.floor(i / N_SIDE) * CELL;
            return (
              <rect
                key={i}
                x={x + GAP / 2} y={y + GAP / 2}
                width={CELL - GAP} height={CELL - GAP}
                rx={1.4}
                fill={colorFor(i)}
                style={reduced ? undefined : { transition: "fill 220ms linear" }}
              />
            );
          })}
        </svg>

        {/* Legend with live counts and uncertainty ranges */}
        <div style={{ margin: "20px 0 24px", fontSize: 12.5, lineHeight: 1.4 }}>
          {rows.map(({ tier, v, range }) => (
            <div key={tier.key} style={{
              display: "flex", alignItems: "baseline", gap: 8,
              padding: "3.5px 0",
            }}>
              <span style={{
                width: 12, height: 12, borderRadius: 2.5,
                background: tier.color, flexShrink: 0,
                alignSelf: "center",
              }} />
              <span style={{ flexGrow: 1 }}>{tier.name}</span>
              <span style={{ fontWeight: 700 }}>{fmt(v)}</span>
              <span style={{ color: "#9B958A", minWidth: 52, textAlign: "right" }}>
                {pct(v, s.pop)}
              </span>
              {range && (
                <span style={{ color: "#B8B2A6", fontSize: 10.5, minWidth: 88, textAlign: "right" }}>
                  [{fmt(Math.max(range[0], 0))}–{fmt(range[1])}]
                </span>
              )}
            </div>
          ))}
        </div>

        {/* Timeline scrubber with model-release milestones */}
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <button
            onClick={() => {
              if (playing) { setPlaying(false); return; }
              if (t >= T_MAX - 0.01) setT(T_MIN);
              setPlaying(true);
            }}
            aria-label={playing ? "Pause" : "Play timeline"}
            style={{
              width: 44, height: 44, borderRadius: "50%",
              border: "1.5px solid #26231F", background: playing ? "#26231F" : "transparent",
              color: playing ? "#FBFAF7" : "#26231F",
              fontSize: 15, cursor: "pointer", flexShrink: 0,
              display: "flex", alignItems: "center", justifyContent: "center",
            }}
          >
            {playing ? "❚❚" : "▶"}
          </button>
          <div style={{ flexGrow: 1, position: "relative", paddingBottom: 26 }}>
            <input
              type="range"
              min={T_MIN} max={T_MAX} step={0.005}
              value={t}
              onChange={(e) => { setPlaying(false); setT(parseFloat(e.target.value)); }}
              aria-label="Timeline position"
              style={{ width: "100%", accentColor: "#6FA877", cursor: "pointer" }}
            />
            {/* milestone ticks */}
            {MILESTONES.map((m) => {
              const left = ((m.t - T_MIN) / (T_MAX - T_MIN)) * 100;
              return (
                <div key={m.label} style={{
                  position: "absolute", left: `${left}%`, top: 24,
                  transform: "translateX(-50%)", textAlign: "center",
                }}>
                  <div style={{ width: 1, height: 5, background: "#B8B2A6", margin: "0 auto 2px" }} />
                  <div style={{ fontSize: 8.5, color: "#9B958A", whiteSpace: "nowrap" }}>
                    {m.label}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <p style={{ fontSize: 10, color: "#B0AA9E", lineHeight: 1.55, marginTop: 26 }}>
          Sources: Microsoft AI Economy Institute diffusion reports (H1/H2 2025, Q1 2026 —
          gen-AI use as share of working-age population, telemetry-based); OpenAI / Reuters
          user and subscriber disclosures; Microsoft earnings (GitHub Copilot); ITU
          connectivity estimates. Pre-2025 user totals are triangulated and carry wide
          uncertainty (ranges in brackets). Tiers shown as exclusive; in reality they nest
          and overlap. The viral February 2026 original (Damian Player) understated paid
          and coding users by roughly 3–5×.
        </p>
      </div>
    </div>
  );
}
