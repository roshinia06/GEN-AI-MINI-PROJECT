import { useState, useEffect, useRef } from "react";

/* ─── GLOBAL STYLES ─────────────────────────────────────────── */
const GLOBAL_STYLE = `
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  :root {
    --sand:    #f8f5f0;
    --cream:   #ffffff;
    --ink:     #12100e;
    --bark:    #2d241d;
    --clay:    #7b5233;
    --rust:    #b35422;
    --amber:   #df8a2f;
    --sage:    #5a7a5f;
    --mist:    #94a3ab;
    --gold:    #c49a3c;
    --sky:     #3d6d8f;
    --white:   #ffffff;
    --shadow:  rgba(18,16,14,0.08);
    --radius:  20px;
    --radius-sm: 10px;
  }

  body {
    font-family: 'DM Sans', sans-serif;
    background: var(--sand);
    color: var(--ink);
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* Background texture */
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      radial-gradient(ellipse 80% 60% at 20% 10%, rgba(212,168,67,0.08) 0%, transparent 60%),
      radial-gradient(ellipse 60% 80% at 80% 90%, rgba(74,127,165,0.07) 0%, transparent 60%),
      url("data:image/svg+xml,%3Csvg width='60' height='60' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    pointer-events: none;
    z-index: 0;
  }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--sand); }
  ::-webkit-scrollbar-thumb { background: var(--clay); border-radius: 3px; }

  /* Animations */
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  @keyframes fadeIn {
    from { opacity: 0; }
    to   { opacity: 1; }
  }
  @keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.4; }
  }
  @keyframes dotBounce {
    0%, 80%, 100% { transform: scale(0); }
    40%            { transform: scale(1); }
  }
  @keyframes mapPin {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-6px); }
  }
  @keyframes progressFill {
    from { width: 0%; }
    to   { width: var(--target-width); }
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(-16px); }
    to   { opacity: 1; transform: translateX(0); }
  }
  @keyframes cardReveal {
    from { opacity: 0; transform: translateY(20px) scale(0.98); }
    to   { opacity: 1; transform: translateY(0) scale(1); }
  }
  input, select, textarea {
    transition: all 0.2s ease;
  }
  input:focus, select:focus, textarea:focus {
    border-color: var(--rust) !important;
    box-shadow: 0 0 0 4px rgba(179,84,34,0.1) !important;
  }
`;

/* ─── SVG ICONS ──────────────────────────────────────────────── */
const Icon = {
  Plane: () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M17.8 19.2L16 11l3.5-3.5C21 6 21 4 19.5 2.5S18 2 16.5 3.5L13 7 4.8 5.2 3.4 6.6l6.9 3.7-2.3 2.3-4-1-1.4 1.4 4 2 2 4 1.4-1.4-1-4 2.3-2.3z" />
    </svg>
  ),
  Map: () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21" />
      <line x1="9" y1="3" x2="9" y2="18" />
      <line x1="15" y1="6" x2="15" y2="21" />
    </svg>
  ),
  Budget: () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <line x1="12" y1="1" x2="12" y2="23" />
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
    </svg>
  ),
  Calendar: () => (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <rect x="3" y="4" width="18" height="18" rx="2" />
      <line x1="16" y1="2" x2="16" y2="6" />
      <line x1="8" y1="2" x2="8" y2="6" />
      <line x1="3" y1="10" x2="21" y2="10" />
    </svg>
  ),
  Sun: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  ),
  Moon: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  ),
  Food: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M18 8h1a4 4 0 0 1 0 8h-1" />
      <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z" />
      <line x1="6" y1="1" x2="6" y2="4" />
      <line x1="10" y1="1" x2="10" y2="4" />
      <line x1="14" y1="1" x2="14" y2="4" />
    </svg>
  ),
  Hotel: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
      <polyline points="9 22 9 12 15 12 15 22" />
    </svg>
  ),
  Download: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
      <polyline points="7 10 12 15 17 10" />
      <line x1="12" y1="15" x2="12" y2="3" />
    </svg>
  ),
  Star: () => (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
    </svg>
  ),
  Check: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  ),
  Arrow: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>
  ),
  Sparkle: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8">
      <path d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5z" />
      <path d="M5 3l.7 2.3L8 6l-2.3.7L5 9l-.7-2.3L2 6l2.3-.7z" />
      <path d="M19 14l.7 2.3 2.3.7-2.3.7L19 20l-.7-2.3-2.3-.7 2.3-.7z" />
    </svg>
  ),
  Alert: () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  ),
  Send: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  ),
  Chat: () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  ),
};

const slugify = (text) => text?.toLowerCase().replace(/[^\w\s-]/g, "").replace(/\s+/g, "-") || "itinerary";


/* ─── CONSTANTS ──────────────────────────────────────────────── */
const INTERESTS = [
  { id: "culture", label: "Culture & History", emoji: "🏛️" },
  { id: "food", label: "Food & Dining", emoji: "🍜" },
  { id: "adventure", label: "Adventure", emoji: "🧗" },
  { id: "nature", label: "Nature & Wildlife", emoji: "🌿" },
  { id: "nightlife", label: "Nightlife", emoji: "🌃" },
  { id: "shopping", label: "Shopping", emoji: "🛍️" },
  { id: "wellness", label: "Wellness & Spa", emoji: "🧘" },
  { id: "art", label: "Art & Museums", emoji: "🎨" },
];

const TRIP_MODES = [
  { id: "seasonal", label: "Seasonal", icon: "🌤️", desc: "Relaxed, seasonal focus" },
  { id: "short_trip", label: "Short Trip", icon: "⚡", desc: "Iconic, fast-paced" },
  { id: "surprise", label: "Surprise Me", icon: "🎁", desc: "Hidden gems, unique" },
];

const ACCOMMODATION_TYPES = ["Luxury", "Mid-range", "Budget", "Unique stays", "Hostel"];
const API_BASE = "http://localhost:8000";

/* ─── HELPERS ────────────────────────────────────────────────── */
function formatCurrency(n, currencySymbol = "₹") {
  if (n == null) return "—";
  const formatter = new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: currencySymbol === "$" ? "USD" : currencySymbol === "€" ? "EUR" : "INR",
    maximumFractionDigits: 0
  });

  let result = formatter.format(n);
  if (currencySymbol !== "₹" && currencySymbol !== "$" && currencySymbol !== "€") {
    return `${currencySymbol} ${n.toLocaleString("en-IN")}`;
  }
  return result;
}



/* ─── LOADING ANIMATION ──────────────────────────────────────── */
function LoadingScreen({ phase }) {
  const phases = [
    { label: "Gathering destination intelligence…", icon: "🔍" },
    { label: "Querying Wikipedia & Geoapify…", icon: "🌐" },
    { label: "AI crafting your itinerary…", icon: "🤖" },
    { label: "Validating budget constraints…", icon: "💰" },
    { label: "Polishing the final plan…", icon: "✨" },
  ];

  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center",
      minHeight: "400px", gap: "32px", padding: "48px",
      animation: "fadeIn 0.4s ease",
    }}>
      <div style={{ position: "relative", width: "96px", height: "96px" }}>
        <div style={{
          width: "96px", height: "96px", borderRadius: "50%",
          border: "3px solid var(--sand)",
          borderTop: "3px solid var(--rust)",
          borderRight: "3px solid var(--amber)",
          animation: "spin 1.2s linear infinite",
        }} />
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px", width: "100%", maxWidth: "360px" }}>
        {phases.map((p, i) => (
          <div key={i} style={{
            display: "flex", alignItems: "center", gap: "12px", padding: "10px 16px",
            borderRadius: "var(--radius-sm)",
            background: i < phase ? "rgba(107,143,113,0.15)" : i === phase ? "rgba(196,98,45,0.12)" : "rgba(26,22,18,0.04)",
            border: `1px solid ${i < phase ? "rgba(107,143,113,0.3)" : i === phase ? "rgba(196,98,45,0.2)" : "transparent"}`,
            transition: "all 0.4s ease",
            animation: i === phase ? "pulse 1.5s ease infinite" : "none",
          }}>
            <span style={{
              fontFamily: "'DM Mono', monospace", fontSize: "12px",
              color: i < phase ? "var(--sage)" : i === phase ? "var(--rust)" : "var(--mist)",
              fontWeight: i === phase ? "500" : "400",
            }}>
              {i < phase ? "✓ " : i === phase ? "▶ " : "○ "}{p.label}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ─── BUDGET BAR ─────────────────────────────────────────────── */
function BudgetBar({ label, amount, total, color, currencySymbol }) {
  const pct = total > 0 ? Math.min((amount / total) * 100, 100) : 0;
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "6px" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: "13px", color: "var(--bark)", fontWeight: "500" }}>{label}</span>
        <span style={{ fontFamily: "'DM Mono', monospace", fontSize: "12px", color: "var(--clay)" }}>
          {formatCurrency(amount, currencySymbol)}
        </span>
      </div>
      <div style={{ height: "6px", borderRadius: "3px", background: "rgba(26,22,18,0.08)", overflow: "hidden" }}>
        <div style={{
          height: "100%", borderRadius: "3px", background: color,
          width: `${pct}%`, transition: "width 1s cubic-bezier(0.4,0,0.2,1)",
        }} />
      </div>
    </div>
  );
}

/* ─── DAY CARD ───────────────────────────────────────────────── */
function DayCard({ day, index }) {
  const [open, setOpen] = useState(index === 0);


  return (
    <div style={{
      borderRadius: "var(--radius)",
      border: "1.5px solid rgba(26,22,18,0.1)",
      background: "var(--cream)",
      overflow: "hidden",
      animation: `cardReveal 0.5s ease ${index * 0.08}s both`,
      boxShadow: open ? "0 8px 32px var(--shadow)" : "0 2px 8px rgba(26,22,18,0.06)",
      transition: "box-shadow 0.3s ease",
    }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          width: "100%", display: "flex", alignItems: "center", gap: "16px",
          padding: "20px 24px", background: "none", border: "none", cursor: "pointer",
          textAlign: "left",
        }}
      >
        <div style={{
          width: "48px", height: "48px", borderRadius: "12px", flexShrink: 0,
          background: "linear-gradient(135deg, var(--rust), var(--amber))",
          display: "flex", alignItems: "center", justifyContent: "center",
          fontFamily: "'Playfair Display', serif", fontSize: "18px",
          fontWeight: "700", color: "white",
        }}>
          {day.day || (index + 1)}
        </div>
        <div style={{ flex: 1 }}>
          <div style={{ fontFamily: "'Playfair Display', serif", fontSize: "17px", fontWeight: "700", color: "var(--ink)", marginBottom: "2px" }}>
            Day {day.day || (index + 1)}
          </div>
          {day.theme && (
            <div style={{ fontSize: "13px", color: "var(--clay)" }}>{day.theme}</div>
          )}
        </div>
        <div style={{
          transform: open ? "rotate(90deg)" : "rotate(0deg)", transition: "transform 0.3s ease",
          color: "var(--mist)",
        }}>
          <Icon.Arrow />
        </div>
      </button>

      {open && (
        <div style={{ borderTop: "1px solid rgba(26,22,18,0.07)", padding: "20px 24px", display: "flex", flexDirection: "column", gap: "16px" }}>
          {day.activities && day.activities.length > 0 ? (
            <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              {day.activities.map((act, idx) => (
                <div key={idx} style={{ display: "flex", gap: "12px", animation: "fadeUp 0.3s ease" }}>
                  <div style={{ color: "var(--rust)", flexShrink: 0, marginTop: "4px", fontSize: "12px" }}>✦</div>
                  <p style={{ fontSize: "14px", lineHeight: "1.6", color: "var(--bark)", margin: 0 }}>{act}</p>
                </div>
              ))}
            </div>
          ) : (
            <p style={{ fontSize: "14px", color: "var(--mist)" }}>No detailed activities listed for this day.</p>
          )}

          <div style={{ display: "flex", flexWrap: "wrap", gap: "12px", marginTop: "4px" }}>
            {day.meals && day.meals.length > 0 && (
              <div style={{
                padding: "8px 14px", borderRadius: "var(--radius-sm)",
                background: "rgba(212,168,67,0.08)", border: "1px solid rgba(212,168,67,0.18)",
                display: "flex", gap: "8px", alignItems: "center",
              }}>
                <span style={{ color: "var(--gold)", fontSize: "14px" }}><Icon.Food /></span>
                <span style={{ fontSize: "12px", fontWeight: "600", color: "var(--gold)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Meals: {day.meals.join(", ")}
                </span>
              </div>
            )}
            
            {day.city && (
              <div style={{
                padding: "8px 14px", borderRadius: "var(--radius-sm)",
                background: "rgba(74,127,165,0.07)", border: "1px solid rgba(74,127,165,0.15)",
                display: "flex", gap: "8px", alignItems: "center",
              }}>
                <span style={{ color: "var(--sky)", fontSize: "14px" }}>📍</span>
                <span style={{ fontSize: "12px", fontWeight: "600", color: "var(--sky)", textTransform: "uppercase", letterSpacing: "0.05em" }}>
                  Stay: {day.city}
                </span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/* ─── RESULT VIEW ────────────────────────────────────────────── */
function ItineraryResult({ data, onReset, onDownload, downloading, chatHistory, onChat, chatMessage, setChatMessage, isChatting }) {
  const [activeTab, setActiveTab] = useState("itinerary");
  const [activeOptionIndex, setActiveOptionIndex] = useState(0);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatHistory]);

  if (!data) return null;

  const options = data.options || [];
  const activeOption = options[activeOptionIndex] || (options.length > 0 ? options[0] : null);
  
  const days = activeOption?.itinerary || [];
  const budget = activeOption?.budget_breakdown || {};
  const totalCost = activeOption?.pricing?.total_cost || 0;
  const currencySymbol = data.currency_symbol || "₹";
  const alerts = data.warning ? [data.warning] : [];

  const budgetItems = [
    { label: "Accommodation", key: "accommodation", color: "var(--sky)" },
    { label: "Food", key: "food", color: "var(--amber)" },
    { label: "Activities", key: "activities", color: "var(--sage)" },
    { label: "Buffer", key: "buffer", color: "var(--mist)" },
  ];

  return (
    <div style={{ animation: "fadeUp 0.6s ease", display: "flex", flexDirection: "column", gap: "32px" }}>
      <div style={{
        borderRadius: "var(--radius)", overflow: "hidden",
        background: "linear-gradient(135deg, var(--bark) 0%, #2a1a10 100%)",
        padding: "40px 40px 36px", position: "relative",
      }}>
        <div style={{ position: "absolute", top: "-40px", right: "-40px", width: "200px", height: "200px", borderRadius: "50%", background: "rgba(196,98,45,0.15)" }} />
        <div style={{ position: "absolute", bottom: "-20px", right: "80px", width: "120px", height: "120px", borderRadius: "50%", background: "rgba(232,148,58,0.1)" }} />

        <div style={{ position: "relative", zIndex: 1 }}>
          <div style={{ fontFamily: "'DM Mono', monospace", fontSize: "11px", letterSpacing: "0.15em", color: "var(--amber)", marginBottom: "8px", textTransform: "uppercase" }}>
            ✦ Your Professional Itinerary
          </div>
          <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: "clamp(28px, 5vw, 42px)", fontWeight: "900", color: "var(--white)", marginBottom: "12px", lineHeight: "1.2" }}>
            {data.destination || "Your Journey"}
          </h2>

          {/* Option Selector */}
          <div style={{ display: "flex", gap: "10px", marginBottom: "28px", flexWrap: "wrap" }}>
            {options.map((opt, idx) => (
              <button
                key={idx}
                onClick={() => setActiveOptionIndex(idx)}
                style={{
                  padding: "8px 16px", borderRadius: "20px",
                  border: `1.5px solid ${activeOptionIndex === idx ? "var(--rust)" : "rgba(255,255,255,0.2)"}`,
                  background: activeOptionIndex === idx ? "var(--rust)" : "transparent",
                  color: "white", cursor: "pointer", fontSize: "13px", fontWeight: "600",
                  transition: "all 0.2s ease"
                }}
              >
                {opt.option_id}
              </button>
            ))}
          </div>

          <div style={{ display: "flex", flexWrap: "wrap", gap: "20px", marginBottom: "28px" }}>
            {[
              { icon: <Icon.Calendar />, label: `${days.length} Days` },
              { icon: <Icon.Budget />, label: formatCurrency(totalCost, currencySymbol) },
              { icon: <Icon.Hotel />, label: activeOption?.hotel?.name || "Premium Stay" },
              { icon: <Icon.Map />, label: activeOption?.transport_facility || "Private Vehicle" },
            ].map((item, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: "8px", color: "rgba(255,255,255,0.75)", fontSize: "14px" }}>
                <span style={{ color: "var(--amber)" }}>{item.icon}</span>
                {item.label}
              </div>
            ))}
          </div>

          <div style={{ display: "flex", gap: "12px", flexWrap: "wrap" }}>
            <div style={{ display: "flex", background: "rgba(255,255,255,0.1)", borderRadius: "var(--radius-sm)", padding: "4px" }}>
              <button
                onClick={() => setActiveTab("itinerary")}
                style={{
                  padding: "8px 16px", borderRadius: "6px", border: "none",
                  background: activeTab === "itinerary" ? "var(--rust)" : "transparent",
                  color: "white", cursor: "pointer", fontSize: "14px", fontWeight: "600",
                  transition: "all 0.2s ease"
                }}
              >
                Itinerary
              </button>
              <button
                onClick={() => setActiveTab("chat")}
                style={{
                  padding: "8px 16px", borderRadius: "6px", border: "none",
                  background: activeTab === "chat" ? "var(--rust)" : "transparent",
                  color: "white", cursor: "pointer", fontSize: "14px", fontWeight: "600",
                  transition: "all 0.2s ease"
                }}
              >
                Chat Concierge
              </button>
            </div>
            <div style={{ width: "1px", background: "rgba(255,255,255,0.2)", margin: "0 8px" }} />
            <button
              onClick={onDownload}
              disabled={downloading}
              style={{
                display: "flex", alignItems: "center", gap: "8px",
                padding: "12px 24px", borderRadius: "var(--radius-sm)",
                background: downloading ? "rgba(255,255,255,0.1)" : "var(--rust)",
                color: "white", border: "none", cursor: downloading ? "not-allowed" : "pointer",
                fontFamily: "'DM Sans', sans-serif", fontSize: "14px", fontWeight: "600",
                transition: "all 0.2s ease",
              }}
            >
              <Icon.Download />
              {downloading ? "Generating PDF…" : "Download PDF"}
            </button>
            <button
              onClick={onReset}
              style={{
                padding: "12px 24px", borderRadius: "var(--radius-sm)",
                background: "rgba(255,255,255,0.1)", color: "rgba(255,255,255,0.85)",
                border: "1px solid rgba(255,255,255,0.2)", cursor: "pointer",
                fontFamily: "'DM Sans', sans-serif", fontSize: "14px", fontWeight: "500",
                backdropFilter: "blur(8px)", transition: "all 0.2s ease",
              }}
            >
              Plan Another Trip
            </button>
          </div>
        </div>
      </div>

      {alerts.length > 0 && (
        <div style={{ display: "flex", flexDirection: "column", gap: "8px" }}>
          {alerts.map((alert, i) => (
            <div key={i} style={{
              padding: "12px 16px", borderRadius: "var(--radius-sm)",
              background: "rgba(232,148,58,0.1)", border: "1px solid rgba(232,148,58,0.25)",
              display: "flex", gap: "10px", alignItems: "flex-start",
              animation: `slideIn 0.3s ease ${i * 0.1}s both`,
              fontSize: "13px", color: "var(--bark)", lineHeight: "1.5",
            }}>
              <span style={{ color: "var(--amber)", flexShrink: 0 }}><Icon.Alert /></span>
              {alert}
            </div>
          ))}
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "1fr 320px", gap: "24px", alignItems: "start" }}>
        <div style={{ minHeight: "600px" }}>
          {activeTab === "itinerary" ? (
            <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
              <h3 style={{ fontFamily: "'Playfair Display', serif", fontSize: "20px", fontWeight: "700", color: "var(--ink)", marginBottom: "4px" }}>
                Day-by-Day Itinerary
              </h3>
              {days.length > 0 ? (
                days.map((day, i) => <DayCard key={i} day={day} index={i} />)
              ) : (
                <div style={{ padding: "32px", textAlign: "center", color: "var(--mist)", background: "var(--cream)", borderRadius: "var(--radius)", border: "1px dashed rgba(26,22,18,0.15)" }}>
                  No day-by-day breakdown available yet.
                </div>
              )}

              {/* Package Details */}
              <div style={{ marginTop: "24px", display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                <div style={{ padding: "20px", background: "rgba(107,143,113,0.06)", borderRadius: "var(--radius-sm)", border: "1.5px solid rgba(107,143,113,0.15)" }}>
                  <h4 style={{ fontSize: "14px", fontWeight: "700", color: "var(--sage)", marginBottom: "12px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Inclusions</h4>
                  <ul style={{ paddingLeft: "18px", margin: 0, display: "flex", flexDirection: "column", gap: "6px" }}>
                    {data.inclusions?.map((item, idx) => (
                      <li key={idx} style={{ fontSize: "13px", color: "var(--bark)" }}>{item}</li>
                    ))}
                  </ul>
                </div>
                <div style={{ padding: "20px", background: "rgba(196,98,45,0.06)", borderRadius: "var(--radius-sm)", border: "1.5px solid rgba(196,98,45,0.15)" }}>
                  <h4 style={{ fontSize: "14px", fontWeight: "700", color: "var(--rust)", marginBottom: "12px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Exclusions</h4>
                  <ul style={{ paddingLeft: "18px", margin: 0, display: "flex", flexDirection: "column", gap: "6px" }}>
                    {data.exclusions?.map((item, idx) => (
                      <li key={idx} style={{ fontSize: "13px", color: "var(--bark)" }}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              <div style={{ padding: "20px", background: "rgba(26,22,18,0.03)", borderRadius: "var(--radius-sm)", border: "1.5px solid rgba(26,22,18,0.08)" }}>
                <h4 style={{ fontSize: "14px", fontWeight: "700", color: "var(--bark)", marginBottom: "12px", textTransform: "uppercase", letterSpacing: "0.05em" }}>Terms & Conditions</h4>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px" }}>
                  {data.terms?.map((item, idx) => (
                    <div key={idx} style={{ fontSize: "12px", color: "var(--mist)", display: "flex", gap: "8px" }}>
                      <span>•</span> {item}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div style={{
              height: "600px", display: "flex", flexDirection: "column",
              background: "var(--cream)", borderRadius: "var(--radius)",
              border: "1.5px solid rgba(26,22,18,0.1)", overflow: "hidden",
              animation: "cardReveal 0.4s ease",
            }}>
              <div style={{ flex: 1, padding: "24px", overflowY: "auto", display: "flex", flexDirection: "column", gap: "16px" }}>
                {chatHistory.length === 0 && (
                  <div style={{ textAlign: "center", margin: "auto", maxWidth: "400px" }}>
                    <div style={{ fontSize: "48px", marginBottom: "16px" }}>🎒</div>
                    <h4 style={{ fontFamily: "'Playfair Display', serif", fontSize: "20px", marginBottom: "8px" }}>Your Travel Concierge</h4>
                    <p style={{ color: "var(--mist)", fontSize: "14px", lineHeight: "1.6" }}>
                      I'm ready to help! You can ask me about local secrets, budget tips, or even ask me to change the plan.
                    </p>
                  </div>
                )}
                {chatHistory.map((msg, i) => (
                  <div key={i} style={{
                    alignSelf: msg.role === "user" ? "flex-end" : "flex-start",
                    maxWidth: "80%", padding: "12px 18px", borderRadius: "16px",
                    background: msg.role === "user" ? "var(--rust)" : "rgba(26,22,18,0.05)",
                    color: msg.role === "user" ? "white" : "var(--ink)",
                    fontSize: "14px", lineHeight: "1.6",
                    borderBottomRightRadius: msg.role === "user" ? "4px" : "16px",
                    borderBottomLeftRadius: msg.role === "user" ? "16px" : "4px",
                    animation: "fadeUp 0.3s ease",
                  }}>
                    {msg.content}
                  </div>
                ))}
                {isChatting && (
                  <div style={{ alignSelf: "flex-start", padding: "12px 18px", borderRadius: "16px", background: "rgba(26,22,18,0.05)", display: "flex", gap: "4px" }}>
                    <div style={{ width: "6px", height: "6px", borderRadius: "50%", background: "var(--mist)", animation: "dotBounce 1s infinite 0.1s" }} />
                    <div style={{ width: "6px", height: "6px", borderRadius: "50%", background: "var(--mist)", animation: "dotBounce 1s infinite 0.2s" }} />
                    <div style={{ width: "6px", height: "6px", borderRadius: "50%", background: "var(--mist)", animation: "dotBounce 1s infinite 0.3s" }} />
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              <form onSubmit={onChat} style={{ padding: "16px 24px", background: "rgba(26,22,18,0.02)", borderTop: "1px solid rgba(26,22,18,0.08)", display: "flex", gap: "12px" }}>
                <input
                  value={chatMessage}
                  onChange={e => setChatMessage(e.target.value)}
                  placeholder="Ask me anything about your trip…"
                  style={{
                    flex: 1, padding: "12px 16px", borderRadius: "var(--radius-sm)",
                    border: "1.5px solid rgba(26,22,18,0.12)", background: "white",
                    fontFamily: "'DM Sans', sans-serif", fontSize: "14px",
                  }}
                />
                <button
                  type="submit"
                  disabled={isChatting || !chatMessage.trim()}
                  style={{
                    width: "44px", height: "44px", borderRadius: "var(--radius-sm)",
                    background: "var(--rust)", color: "white", border: "none",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    cursor: "pointer", transition: "all 0.2s ease",
                    opacity: (!chatMessage.trim() || isChatting) ? 0.6 : 1,
                  }}
                >
                  <Icon.Send />
                </button>
              </form>
            </div>
          )}
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: "16px", position: "sticky", top: "24px" }}>
          <div style={{
            borderRadius: "var(--radius)", border: "1.5px solid rgba(26,22,18,0.1)",
            background: "var(--cream)", padding: "24px", boxShadow: "0 4px 20px rgba(26,22,18,0.07)",
          }}>
            <h4 style={{ fontFamily: "'Playfair Display', serif", fontSize: "17px", fontWeight: "700", color: "var(--ink)", marginBottom: "20px" }}>
              Budget Breakdown
            </h4>
            <div style={{ display: "flex", flexDirection: "column", gap: "14px" }}>
              {budgetItems.map(({ label, key, color }) =>
                budget[key] != null ? (
                  <BudgetBar key={key} label={label} amount={budget[key]} total={totalCost} color={color} currencySymbol={currencySymbol} />
                ) : null
              )}
            </div>
            {totalCost > 0 && (
              <div style={{
                marginTop: "20px", paddingTop: "16px", borderTop: "1px solid rgba(26,22,18,0.08)",
                display: "flex", justifyContent: "space-between", alignItems: "center",
              }}>
                <span style={{ fontWeight: "600", fontSize: "14px", color: "var(--bark)" }}>Total</span>
                <span style={{ fontFamily: "'Playfair Display', serif", fontSize: "20px", fontWeight: "700", color: "var(--rust)" }}>
                  {formatCurrency(totalCost, currencySymbol)}
                </span>
              </div>
            )}
          </div>

          {data.tips && data.tips.length > 0 && (
            <div style={{
              borderRadius: "var(--radius)", border: "1.5px solid rgba(107,143,113,0.2)",
              background: "rgba(107,143,113,0.06)", padding: "20px",
            }}>
              <h4 style={{ fontFamily: "'Playfair Display', serif", fontSize: "15px", fontWeight: "700", color: "var(--sage)", marginBottom: "12px" }}>
                ✦ Travel Tips
              </h4>
              <ul style={{ display: "flex", flexDirection: "column", gap: "8px", listStyle: "none" }}>
                {data.tips.map((tip, i) => (
                  <li key={i} style={{ display: "flex", gap: "8px", fontSize: "13px", color: "var(--bark)", lineHeight: "1.5" }}>
                    <span style={{ color: "var(--sage)", flexShrink: 0, marginTop: "2px" }}><Icon.Check /></span>
                    {tip}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* ─── MAIN APP ───────────────────────────────────────────────── */
export default function App() {
  const [startingPlace, setStartingPlace] = useState("");
  const [destination, setDestination] = useState("");
  const [mode, setMode] = useState("seasonal");
  const [days, setDays] = useState(5);
  const [budget, setBudget] = useState("");
  const [interests, setInterests] = useState([]);
  const [accommodation, setAccommodation] = useState("Mid-range");
  const [peopleCount, setPeopleCount] = useState(1);
  const [notes, setNotes] = useState("");
  const [dietaryPreference, setDietaryPreference] = useState("Both");
  const [chatMessage, setChatMessage] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isChatting, setIsChatting] = useState(false);

  const [step, setStep] = useState("form");
  const [loadPhase, setLoadPhase] = useState(0);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [downloading, setDownloading] = useState(false);

  const phaseRef = useRef(null);

  useEffect(() => {
    if (step === "loading") {
      setLoadPhase(0);
      phaseRef.current = setInterval(() => setLoadPhase(p => p + 1), 2800);
    } else {
      clearInterval(phaseRef.current);
    }
    return () => clearInterval(phaseRef.current);
  }, [step]);

  const toggleInterest = (id) => {
    setInterests(prev => prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]);
  };

  const handleSubmit = async () => {
    if (mode !== "surprise" && !destination.trim()) { setError("Please enter a destination."); return; }
    if (interests.length === 0) { setError("Pick at least one interest."); return; }
    setError(null);
    setStep("loading");

    const payload = {
      starting_place: startingPlace.trim() || "Your location",
      destination: destination.trim(),
      days: days,
      budget: budget || "50000",
      mode: mode,
      people_count: peopleCount,
      interests: interests,
      dietary_preference: dietaryPreference,
      accommodation_type: accommodation,
      notes: notes,
      include_meals: true,
      include_hotel: true
    };

    try {
      const res = await fetch(`${API_BASE}/api/generate-itinerary`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Server error ${res.status}`);
      }
      const data = await res.json();
      setResult(data);
      setStep("result");
    } catch (e) {
      setError(e.message || "Something went wrong. Is the backend running?");
      setStep("form");
    }
  };

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const payload = {
        starting_place: result.starting_place || "Your location",
        destination: result.destination,
        days: result.itinerary.length,
        budget: result.total_cost.toString(),
        mode: result.mode || "seasonal",
        people_count: result.people_count || 1,
        dietary_preference: result.dietary_preference || dietaryPreference,
        interests: result.interests || interests,
        accommodation_type: result.accommodation_type || accommodation,
        notes: result.notes || notes
      };
      const res = await fetch(`${API_BASE}/api/generate-pdf`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!res.ok) throw new Error("PDF generation failed");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${slugify(result.destination || "itinerary")}-travel-plan.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (e) {
      alert("Could not download PDF: " + e.message);
    } finally {
      setDownloading(false);
    }
  };

  const handleChat = async (e) => {
    if (e) e.preventDefault();
    if (!chatMessage.trim()) return;

    const userMsg = { role: "user", content: chatMessage };
    setChatHistory(prev => [...prev, userMsg]);
    setChatMessage("");
    setIsChatting(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: chatMessage,
          itinerary: result,
          history: chatHistory
        })
      });
      const data = await res.json();
      setChatHistory(prev => [...prev, { role: "assistant", content: data.response }]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsChatting(false);
    }
  };

  const labelStyle = {
    fontFamily: "'DM Mono', monospace", fontSize: "11px",
    letterSpacing: "0.1em", color: "var(--clay)", textTransform: "uppercase",
    marginBottom: "8px", display: "block",
  };

  const inputStyle = {
    width: "100%", padding: "13px 16px",
    borderRadius: "var(--radius-sm)",
    border: "1.5px solid rgba(26,22,18,0.14)",
    background: "var(--white)",
    fontFamily: "'DM Sans', sans-serif", fontSize: "15px", boxShadow: "0 4px 16px var(--shadow)",
    outline: "none", transition: "all 0.2s ease",
    appearance: "none",
  };

  return (
    <>
      <style>{GLOBAL_STYLE}</style>

      <div style={{ position: "relative", zIndex: 1, minHeight: "100vh" }}>
        <nav style={{
          position: "sticky", top: 0, zIndex: 100,
          borderBottom: "1px solid rgba(26,22,18,0.08)",
          background: "rgba(245,240,232,0.85)", backdropFilter: "blur(12px)",
          padding: "0 40px",
        }}>
          <div style={{ maxWidth: "1400px", margin: "0 auto", display: "flex", alignItems: "center", height: "64px", justifyContent: "space-between" }}>
            <div style={{ display: "flex", alignItems: "center", gap: "10px" }}>
              <div style={{
                width: "34px", height: "34px", borderRadius: "8px",
                background: "linear-gradient(135deg, var(--rust), var(--amber))",
                display: "flex", alignItems: "center", justifyContent: "center",
                animation: "mapPin 2s ease-in-out infinite",
              }}>
                <span style={{ fontSize: "18px" }}>✈</span>
              </div>
              <span style={{ fontFamily: "'Playfair Display', serif", fontSize: "22px", fontWeight: "900", color: "var(--ink)", letterSpacing: "-0.02em" }}>
                WANDERER <span style={{ color: "var(--rust)" }}>AI</span>
              </span>
            </div>
          </div>
        </nav>

        <main style={{ maxWidth: "1400px", margin: "0 auto", padding: "48px 40px 80px" }}>
          {step === "form" && (
            <div style={{ maxWidth: "1200px", margin: "0 auto", animation: "fadeUp 0.6s ease" }}>
              <div>
                <div style={{ marginBottom: "40px" }}>
                  <div style={{ fontFamily: "'DM Mono', monospace", fontSize: "11px", letterSpacing: "0.15em", color: "var(--rust)", marginBottom: "12px", textTransform: "uppercase" }}>
                    ✦ AI-Powered Trip Planning
                  </div>
                  <h1 style={{ fontFamily: "'Playfair Display', serif", fontSize: "clamp(28px,4.5vw,48px)", fontWeight: "900", color: "var(--ink)", lineHeight: "1.1", marginBottom: "16px" }}>
                    Plan Your Perfect<br />
                    <em style={{ color: "var(--rust)" }}>Journey</em>
                  </h1>
                </div>

                {error && (
                  <div style={{
                    padding: "14px 18px", borderRadius: "var(--radius-sm)",
                    background: "rgba(196,98,45,0.08)", border: "1px solid rgba(196,98,45,0.25)",
                    display: "flex", gap: "10px", alignItems: "center",
                    marginBottom: "24px", fontSize: "14px", color: "var(--rust)",
                    animation: "fadeIn 0.3s ease",
                  }}>
                    <Icon.Alert /> {error}
                  </div>
                )}

                <div style={{ display: "flex", flexDirection: "column", gap: "28px" }}>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                    <div>
                      <label style={labelStyle}>From</label>
                      <div style={{ position: "relative" }}>
                        <span style={{ position: "absolute", left: "14px", top: "50%", transform: "translateY(-50%)", color: "var(--mist)" }}><Icon.Map /></span>
                        <input
                          type="text" value={startingPlace} onChange={e => setStartingPlace(e.target.value)}
                          placeholder="e.g. New York or Delhi"
                          style={{ ...inputStyle, paddingLeft: "44px" }}
                        />
                      </div>
                    </div>
                    <div>
                      <label style={labelStyle}>To</label>
                      <div style={{ position: "relative" }}>
                        <span style={{ position: "absolute", left: "14px", top: "50%", transform: "translateY(-50%)", color: "var(--mist)" }}><Icon.Map /></span>
                        <input
                          type="text" value={destination} onChange={e => setDestination(e.target.value)}
                          placeholder={mode === "surprise" ? "Random Destination" : "e.g. Paris or Tokyo"}
                          disabled={mode === "surprise" && !destination}
                          style={{ ...inputStyle, paddingLeft: "44px", background: (mode === "surprise" && !destination) ? "var(--sand)" : "var(--white)" }}
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Trip Mode</label>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: "12px" }}>
                      {TRIP_MODES.map(m => (
                        <button
                          key={m.id}
                          onClick={() => setMode(m.id)}
                          style={{
                            padding: "16px 12px", borderRadius: "var(--radius-sm)",
                            border: `2px solid ${mode === m.id ? "var(--rust)" : "rgba(26,22,18,0.08)"}`,
                            background: mode === m.id ? "rgba(196,98,45,0.05)" : "var(--white)",
                            cursor: "pointer", transition: "all 0.2s ease",
                            display: "flex", flexDirection: "column", alignItems: "center", gap: "8px",
                            boxShadow: mode === m.id ? "0 4px 20px rgba(196,98,45,0.15)" : "none",
                          }}
                        >
                          <span style={{ fontSize: "24px" }}>{m.icon}</span>
                          <div style={{ textAlign: "center" }}>
                            <div style={{ fontFamily: "'Playfair Display', serif", fontSize: "14px", fontWeight: "700", color: mode === m.id ? "var(--rust)" : "var(--ink)" }}>{m.label}</div>
                            <div style={{ fontSize: "10px", color: "var(--mist)", marginTop: "2px", fontWeight: "400" }}>{m.desc}</div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Duration — {days} {days === 1 ? "day" : "days"}</label>
                    <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                      <input
                        type="range" min={1} max={21} value={days}
                        onChange={e => setDays(Number(e.target.value))}
                        style={{ flex: 1, accentColor: "var(--rust)", height: "4px", cursor: "pointer" }}
                      />
                      <div style={{
                        width: "56px", height: "40px", borderRadius: "var(--radius-sm)",
                        background: "var(--white)", border: "1.5px solid rgba(26,22,18,0.14)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        fontFamily: "'Playfair Display', serif", fontSize: "18px", fontWeight: "700", color: "var(--rust)",
                      }}>
                        {days}
                      </div>
                    </div>
                  </div>

                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px" }}>
                    <div>
                      <label style={labelStyle}>Travellers</label>
                      <div style={{ display: "flex", alignItems: "center", gap: "10px", height: "48px" }}>
                        <button onClick={() => setPeopleCount(Math.max(1, peopleCount - 1))} style={{ width: "40px", height: "40px", borderRadius: "var(--radius-sm)", border: "1.5px solid rgba(26,22,18,0.14)", background: "var(--white)", cursor: "pointer", fontSize: "18px" }}>-</button>
                        <div style={{ flex: 1, textAlign: "center", fontFamily: "'Playfair Display', serif", fontSize: "18px", fontWeight: "700" }}>{peopleCount}</div>
                        <button onClick={() => setPeopleCount(peopleCount + 1)} style={{ width: "40px", height: "40px", borderRadius: "var(--radius-sm)", border: "1.5px solid rgba(26,22,18,0.14)", background: "var(--white)", cursor: "pointer", fontSize: "18px" }}>+</button>
                      </div>
                    </div>
                    <div>
                      <label style={labelStyle}>Budget (e.g. 50k rupees, 1000 dollars)</label>
                      <div style={{ position: "relative" }}>
                        <span style={{ position: "absolute", left: "14px", top: "50%", transform: "translateY(-50%)", color: "var(--mist)" }}><Icon.Budget /></span>
                        <input
                          type="text" value={budget} onChange={e => setBudget(e.target.value)}
                          placeholder="Total budget for the trip"
                          style={{ ...inputStyle, paddingLeft: "44px" }}
                        />
                      </div>
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Your Interests</label>
                    <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: "8px" }}>
                      {INTERESTS.map(({ id, label, emoji }) => {
                        const active = interests.includes(id);
                        return (
                          <button
                            key={id}
                            onClick={() => toggleInterest(id)}
                            style={{
                              padding: "10px 8px", borderRadius: "var(--radius-sm)",
                              border: `1.5px solid ${active ? "var(--rust)" : "rgba(26,22,18,0.12)"}`,
                              background: active ? "rgba(196,98,45,0.08)" : "var(--white)",
                              cursor: "pointer", transition: "all 0.18s ease",
                              display: "flex", flexDirection: "column", alignItems: "center", gap: "4px",
                            }}
                          >
                            <span style={{ fontSize: "18px" }}>{emoji}</span>
                            <span style={{ fontSize: "10px", fontWeight: "500", color: active ? "var(--rust)" : "var(--bark)", textAlign: "center" }}>{label}</span>
                          </button>
                        );
                      })}
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Accommodation</label>
                    <div style={{ display: "flex", gap: "8px", flexWrap: "wrap" }}>
                      {ACCOMMODATION_TYPES.map(t => (
                        <button
                          key={t}
                          onClick={() => setAccommodation(t)}
                          style={{
                            padding: "9px 16px", borderRadius: "20px",
                            border: `1.5px solid ${accommodation === t ? "var(--rust)" : "rgba(26,22,18,0.12)"}`,
                            background: accommodation === t ? "var(--rust)" : "var(--white)",
                            color: accommodation === t ? "white" : "var(--bark)",
                            cursor: "pointer", fontSize: "13px", fontWeight: "500",
                          }}
                        >
                          {t}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Food Preference</label>
                    <div style={{ display: "flex", gap: "8px" }}>
                      {["Veg", "Non-Veg", "Both"].map(t => (
                        <button
                          key={t}
                          onClick={() => setDietaryPreference(t)}
                          style={{
                            padding: "9px 24px", borderRadius: "20px",
                            border: `1.5px solid ${dietaryPreference === t ? "var(--rust)" : "rgba(26,22,18,0.12)"}`,
                            background: dietaryPreference === t ? "var(--rust)" : "var(--white)",
                            color: dietaryPreference === t ? "white" : "var(--bark)",
                            cursor: "pointer", fontSize: "13px", fontWeight: "600", flex: 1,
                            transition: "all 0.2s ease"
                          }}
                        >
                          {t}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label style={labelStyle}>Additional Notes</label>
                    <textarea
                      value={notes} onChange={e => setNotes(e.target.value)}
                      placeholder="Dietary preferences, accessibility, specific spots…"
                      rows={3}
                      style={{ ...inputStyle, resize: "vertical" }}
                    />
                  </div>

                  <button
                    onClick={handleSubmit}
                    style={{
                      display: "flex", alignItems: "center", justifyContent: "center", gap: "10px",
                      padding: "18px 32px", borderRadius: "var(--radius-sm)",
                      background: "linear-gradient(135deg, var(--rust), var(--amber))",
                      color: "white", border: "none", cursor: "pointer",
                      fontSize: "16px", fontWeight: "700", boxShadow: "0 8px 32px rgba(196,98,45,0.35)",
                    }}
                  >
                    <Icon.Sparkle /> Generate My Itinerary <Icon.Arrow />
                  </button>
                </div>
              </div>
            </div>
          )}

          {step === "loading" && (
            <div style={{ maxWidth: "600px", margin: "0 auto" }}>
              <div style={{ borderRadius: "var(--radius)", background: "var(--cream)", border: "1.5px solid rgba(26,22,18,0.1)", boxShadow: "0 8px 40px var(--shadow)" }}>
                <div style={{ padding: "32px 40px 0", borderBottom: "1px solid rgba(26,22,18,0.08)" }}>
                  <h2 style={{ fontFamily: "'Playfair Display', serif", fontSize: "26px", fontWeight: "700", color: "var(--ink)", marginBottom: "24px" }}>
                    Crafting your <em style={{ color: "var(--rust)" }}>{destination}</em> itinerary…
                  </h2>
                </div>
                <LoadingScreen phase={loadPhase} />
              </div>
            </div>
          )}

          {step === "result" && result && (
            <ItineraryResult
              data={result}
              onReset={() => { setStep("form"); setResult(null); setChatHistory([]); }}
              onDownload={handleDownload}
              downloading={downloading}
              chatHistory={chatHistory}
              onChat={handleChat}
              chatMessage={chatMessage}
              setChatMessage={setChatMessage}
              isChatting={isChatting}
            />
          )}
        </main>
      </div>
    </>
  );
}
