import { useState } from "react";

// ─── CONFIG COMPLÈTE LIGNE / MACHINE / FORMAT CANETTE / FORMAT CAISSE ──────
const CONFIG = {
  MC3: {
    GPI: {
      formats: ["355 ml Standard"],
      caisses: { "355 ml Standard": [12, 20, 24, 30, 36, 48] },
    },
    Keelclip: {
      formats: ["355 ml Standard"],
      caisses: { "355 ml Standard": [6] },
    },
  },
  MC2: {
    GPI: {
      formats: ["355 ml Standard", "355 ml Sleek", "473 ml Standard"],
      caisses: {
        "355 ml Standard": [12, 15, 18, 20, 24],
        "355 ml Sleek":    [12, 15, 18, 20, 24],
        "473 ml Standard": [12, 15, 18, 20, 24],
      },
    },
    Keelclip: {
      formats: ["355 ml Standard", "355 ml Sleek", "473 ml Standard"],
      caisses: {
        "355 ml Standard": [6],
        "355 ml Sleek":    [6],
        "473 ml Standard": [6, 4],
      },
    },
  },
};

const STOP_TYPES = [
  { value: "bris",              label: "🔧 Bris mécanique" },
  { value: "bris_electrique",   label: "⚡ Bris électrique" },
  { value: "desajustement",     label: "⚙️ Désajustement" },
  { value: "changement_format", label: "🔄 Départ après changement de format" },
];

const RESPONSABLES = {
  bris:             { nom: "Michael Gauthier-Guillet", email: "michael.gauthierguillet@labatt.com", titre: "Superviseur maintenance" },
  bris_electrique:  { nom: "Michael Gauthier-Guillet", email: "michael.gauthierguillet@labatt.com", titre: "Superviseur électrique" },
  desajustement:    { nom: "Michael Gauthier-Guillet", email: "michael.gauthierguillet@labatt.com", titre: "Chef d'équipe emballage" },
  changement_format:{ nom: "Michael Gauthier-Guillet", email: "michael.gauthierguillet@labatt.com", titre: "Coordinateur production" },
};

const SUGGESTIONS = {
  bris: {
    1:["La machine s'est arrêtée soudainement","Une pièce s'est brisée pendant la production","Le convoyeur a bloqué"],
    2:["Manque de lubrification","Pièce usée au-delà de sa durée de vie","Surcharge mécanique","Vibrations excessives"],
    3:["Programme de lubrification non respecté","Aucun suivi de l'usure des pièces","Procédure de démarrage non suivie"],
    4:["Pas de fiche de maintenance préventive","Opérateurs non formés aux signaux d'alarme"],
    5:["Manque de ressources pour la maintenance","Formation insuffisante","Aucun système de suivi des pannes"],
  },
  bris_electrique: {
    1:["Un défaut électrique a causé l'arrêt","Le moteur a surchauffé et déclenché","Un capteur a émis une alarme de défaut"],
    2:["Surtension sur le circuit","Câble ou connecteur défectueux","Capteur hors calibration","Problème de mise à la terre"],
    3:["Maintenance électrique préventive non effectuée","Câblage vieillissant non remplacé","Absence de test de continuité"],
    4:["Pas de plan de maintenance électrique","Procédures de vérification électrique absentes"],
    5:["Formation électrique insuffisante","Équipements de mesure non disponibles","Absence de registre des défauts électriques"],
  },
  desajustement: {
    1:["Les produits ne s'alignent pas sur la ligne","L'emballage est mal positionné","La pression de serrage est incorrecte"],
    2:["Réglage d'origine incorrect","Changement de lot de matière première","Vibrations ayant déplacé les guides"],
    3:["Procédure de réglage non standardisée","Pas de point de référence marqué"],
    4:["Fiches de réglage absentes ou incomplètes","Pas de formation pratique"],
    5:["Standardisation des procédures manquante","Documentation technique inaccessible"],
  },
  changement_format: {
    1:["La ligne ne démarre pas correctement après le changement","Le taux de rejet est anormalement élevé"],
    2:["Fiches de changement de format incomplètes","Outils nécessaires manquants"],
    3:["Procédures non standardisées","Pièces de rechange non préparées à l'avance"],
    4:["Absence de checklist de démarrage","Communication insuffisante entre équipes"],
    5:["Formation continue absente","Retours d'expérience non capitalisés"],
  },
};

// Filtre des hommes de métier selon le type de bris
const SPECIALITE_REQUISE = {
  bris:            "Mécanique",
  bris_electrique: "Électrique",
};

async function callClaude(prompt) {
  const resp = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      model: "claude-sonnet-4-20250514",
      max_tokens: 1000,
      messages: [{ role: "user", content: prompt }],
    }),
  });
  const data = await resp.json();
  return data?.content?.[0]?.text || "";
}

const STYLE = `
  @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;900&family=Barlow:wght@300;400;500&display=swap');
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Barlow', sans-serif; background: #0a0e14; color: #e8eaf0; min-height: 100vh; }
  .app { min-height: 100vh; background: #0a0e14; background-image: repeating-linear-gradient(0deg,transparent,transparent 39px,rgba(255,255,255,.02) 40px),repeating-linear-gradient(90deg,transparent,transparent 39px,rgba(255,255,255,.02) 40px); }
  .header { background:#111620; border-bottom:3px solid #d4a017; padding:16px 24px; display:flex; align-items:center; gap:16px; position:sticky; top:0; z-index:100; }
  .header-logo { font-family:'Barlow Condensed',sans-serif; font-size:28px; font-weight:900; color:#d4a017; letter-spacing:2px; text-transform:uppercase; line-height:1; }
  .header-sub { font-size:11px; color:#8892a0; text-transform:uppercase; letter-spacing:1.5px; font-weight:500; }
  .header-badge { margin-left:auto; background:#d4a017; color:#0a0e14; font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:12px; padding:4px 10px; letter-spacing:1px; text-transform:uppercase; }
  .container { max-width:780px; margin:0 auto; padding:32px 20px; }
  .section-title { font-family:'Barlow Condensed',sans-serif; font-size:13px; font-weight:700; color:#d4a017; text-transform:uppercase; letter-spacing:2px; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
  .section-title::after { content:''; flex:1; height:1px; background:rgba(212,160,23,.25); }
  .card { background:#111620; border:1px solid #1e2530; border-left:3px solid #d4a017; padding:20px; margin-bottom:16px; }
  .grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:12px; }
  .field-label { font-size:11px; color:#8892a0; text-transform:uppercase; letter-spacing:1px; font-weight:600; margin-bottom:6px; }
  .field-select,.field-input,.field-textarea { width:100%; background:#0d1117; border:1px solid #1e2530; color:#e8eaf0; font-family:'Barlow',sans-serif; font-size:14px; padding:10px 12px; outline:none; transition:border-color .2s; appearance:none; }
  .field-select:focus,.field-input:focus,.field-textarea:focus { border-color:#d4a017; }
  .field-textarea { resize:vertical; min-height:80px; line-height:1.5; }
  .btn { font-family:'Barlow Condensed',sans-serif; font-weight:700; font-size:14px; text-transform:uppercase; letter-spacing:1.5px; padding:12px 24px; border:none; cursor:pointer; transition:all .2s; display:inline-flex; align-items:center; gap:8px; }
  .btn-primary { background:#d4a017; color:#0a0e14; }
  .btn-primary:hover { background:#e6b520; }
  .btn-primary:disabled { background:#4a3d0e; color:#6a5c30; cursor:not-allowed; }
  .btn-outline { background:transparent; color:#d4a017; border:1px solid #d4a017; }
  .btn-outline:hover { background:rgba(212,160,23,.1); }
  .btn-ghost { background:transparent; color:#8892a0; border:1px solid #1e2530; }
  .btn-ghost:hover { border-color:#8892a0; color:#e8eaf0; }
  .btn-full { width:100%; justify-content:center; }
  .why-step { background:#0d1117; border:1px solid #1e2530; border-left:3px solid transparent; padding:16px; margin-bottom:10px; transition:border-color .2s; }
  .why-step.active { border-left-color:#d4a017; }
  .why-step.done { border-left-color:#22c55e; }
  .why-number { font-family:'Barlow Condensed',sans-serif; font-size:11px; font-weight:700; color:#d4a017; text-transform:uppercase; letter-spacing:1.5px; margin-bottom:4px; }
  .why-question { font-size:13px; color:#8892a0; margin-bottom:10px; padding:8px 10px; background:rgba(212,160,23,.05); border-left:2px solid rgba(212,160,23,.3); font-style:italic; }
  .suggestion-chips { display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }
  .chip { font-size:11px; padding:4px 10px; background:rgba(212,160,23,.08); border:1px solid rgba(212,160,23,.25); color:#c49010; cursor:pointer; transition:all .15s; font-family:'Barlow',sans-serif; }
  .chip:hover { background:rgba(212,160,23,.2); color:#d4a017; }
  .alert { padding:12px 16px; margin-bottom:16px; font-size:13px; display:flex; gap:10px; align-items:flex-start; }
  .alert-info { background:rgba(59,130,246,.1); border:1px solid rgba(59,130,246,.25); }
  .alert-success { background:rgba(34,197,94,.1); border:1px solid rgba(34,197,94,.25); color:#86efac; }
  .alert-warn { background:rgba(212,160,23,.1); border:1px solid rgba(212,160,23,.25); color:#d4a017; }
  .loading-bar { height:2px; background:linear-gradient(90deg,#d4a017,#f5d060,#d4a017); background-size:200% 100%; animation:shimmer 1.2s infinite; margin-bottom:12px; }
  @keyframes shimmer { 0%{background-position:200% 0} 100%{background-position:-200% 0} }
  .rapport-box { background:#0d1117; border:1px solid #1e2530; padding:24px; font-size:13px; line-height:1.8; white-space:pre-wrap; }
  .email-box { background:#0d1117; border:1px solid rgba(34,197,94,.3); padding:20px; font-size:13px; line-height:1.7; white-space:pre-wrap; }
  .progress-bar-outer { background:#1e2530; height:4px; margin-bottom:24px; }
  .progress-bar-inner { background:#d4a017; height:100%; transition:width .4s ease; }
  .divider { border:none; border-top:1px solid #1e2530; margin:24px 0; }
  select option { background:#111620; }

  .selector-row { display:flex; gap:8px; flex-wrap:wrap; }
  .sel-btn { flex:1; min-width:80px; justify-content:center; padding:10px 8px; font-size:15px; }
  .caisse-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(80px,1fr)); gap:8px; }
  .caisse-btn { justify-content:center; padding:10px 6px; font-size:17px; font-family:'Barlow Condensed',sans-serif; font-weight:900; letter-spacing:1px; }
  .locked-info { background:rgba(212,160,23,.07); border:1px solid rgba(212,160,23,.2); padding:10px 14px; font-size:13px; color:#d4a017; font-weight:600; display:flex; align-items:center; gap:8px; }
`;

const selBtnStyle = (active) => ({
  background: active ? "#d4a017" : "transparent",
  color: active ? "#0a0e14" : "#8892a0",
  border: `1px solid ${active ? "#d4a017" : "#1e2530"}`,
});

const radioStyle = (active) => ({
  background: active ? "rgba(212,160,23,0.15)" : "transparent",
  color: active ? "#d4a017" : "#8892a0",
  border: `1px solid ${active ? "#d4a017" : "#1e2530"}`,
  fontFamily: "Barlow, sans-serif",
  fontWeight: 500,
  fontSize: 14,
  textTransform: "none",
  letterSpacing: 0.5,
  padding: "9px 14px",
  flex: 1,
  justifyContent: "flex-start",
});

export default function App() {
  const [step, setStep] = useState("form");
  const [form, setForm] = useState({
    ligne: "", machine: "", format: "", formatCaisse: "",
    stopType: "", duree: "", date: new Date().toISOString().split("T")[0],
    operateur: "", hommeMetier: "", probleme: "",
  });
  const [whys, setWhys] = useState(["","","","",""]);
  const [aiQ, setAiQ] = useState(["","","","",""]);
  const [curWhy, setCurWhy] = useState(0);
  const [loading, setLoading] = useState(false);
  const [rapport, setRapport] = useState("");
  const [email, setEmail] = useState("");
  const [genRapport, setGenRapport] = useState(false);
  const [showEmailPreview, setShowEmailPreview] = useState(false);
  const [emailDest, setEmailDest] = useState("");
  const [hommesMetier, setHommesMetier] = useState([]);
  const [newHom, setNewHom] = useState({ nom:"", specialite:"", email:"" });
  const [showAddHom, setShowAddHom] = useState(false);
  const [copied, setCopied] = useState(false);

  useState(() => {
    (async () => {
      try {
        const r = await window.storage.get("hommes-metier");
        if (r) setHommesMetier(JSON.parse(r.value));
      } catch {}
    })();
  });

  const saveHomme = async () => {
    if (!newHom.nom.trim() || !newHom.specialite) return;
    const updated = [...hommesMetier, { ...newHom, id: Date.now() }];
    setHommesMetier(updated);
    await window.storage.set("hommes-metier", JSON.stringify(updated));
    upd("hommeMetier", newHom.nom);
    setNewHom({ nom:"", specialite:"", email:"" });
    setShowAddHom(false);
  };

  const removeHomme = async (id) => {
    const updated = hommesMetier.filter(h => h.id !== id);
    setHommesMetier(updated);
    await window.storage.set("hommes-metier", JSON.stringify(updated));
  };

  const upd = (k, v) => setForm(f => ({ ...f, [k]: v }));

  const pickLigne = (v) => setForm(f => ({ ...f, ligne: v, machine: "", format: "", formatCaisse: "" }));
  const pickMachine = (v) => setForm(f => ({ ...f, machine: v, format: "", formatCaisse: "" }));
  const pickFormat = (v) => {
    const caisses = form.ligne && form.machine ? CONFIG[form.ligne][form.machine].caisses[v] : [];
    const autoC = caisses.length === 1 ? caisses[0] : "";
    setForm(f => ({ ...f, format: v, formatCaisse: autoC }));
  };
  const pickStopType = (v) => {
    // Reset homme de métier lors du changement de type
    setForm(f => ({ ...f, stopType: v, hommeMetier: "" }));
  };

  const machinesCfg = form.ligne ? Object.keys(CONFIG[form.ligne]) : [];
  const formatsCfg = form.ligne && form.machine ? CONFIG[form.ligne][form.machine].formats : [];
  const caissesCfg = form.ligne && form.machine && form.format
    ? CONFIG[form.ligne][form.machine].caisses[form.format] || []
    : [];
  const autoSingleCaisse = caissesCfg.length === 1;

  // Hommes de métier filtrés selon la spécialité requise par le type de bris
  const specialiteRequise = SPECIALITE_REQUISE[form.stopType];
  const hommesFiltres = specialiteRequise
    ? hommesMetier.filter(h => h.specialite === specialiteRequise)
    : [];

  // Forcer la spécialité du nouveau homme de métier selon le type de bris sélectionné
  const specialiteFixee = specialiteRequise || null;

  const canStart = form.ligne && form.machine && form.format && form.formatCaisse &&
    form.stopType && form.duree && form.operateur && form.probleme;

  const updateWhy = (i, v) => setWhys(w => { const n = [...w]; n[i] = v; return n; });

  const startWhys = async () => {
    setStep("whys");
    setLoading(true);
    const typeLabel = STOP_TYPES.find(t => t.value === form.stopType)?.label || form.stopType;
    const q = await callClaude(
      `Expert résolution problèmes industriels brasserie. Ligne ${form.ligne}, machine ${form.machine}, format canette ${form.format}, caisse de ${form.formatCaisse}. Problème: "${form.probleme}" (arrêt: ${typeLabel}, ${form.duree} min).
      Génère UNE question courte (max 15 mots) pour "Pourquoi 1" sur la cause immédiate visible. Réponds SEULEMENT avec la question en français.`
    );
    setAiQ(a => { const n=[...a]; n[0]=q; return n; });
    setLoading(false);
  };

  const nextWhy = async (i) => {
    if (!whys[i].trim()) return;
    if (i >= 4) { generateRapport(); return; }
    const next = i + 1;
    setCurWhy(next);
    setLoading(true);
    const ctx = whys.slice(0, i+1).map((w, idx) => `P${idx+1}: ${w}`).join("\n");
    const q = await callClaude(
      `Ligne ${form.ligne}, ${form.machine}, ${form.format}, problème: "${form.probleme}"\n${ctx}\n\nGénère UNE question (max 15 mots) pour "Pourquoi ${next+1}" creusant vers la cause racine. SEULEMENT la question en français.`
    );
    setAiQ(a => { const n=[...a]; n[next]=q; return n; });
    setLoading(false);
  };

  const generateRapport = async () => {
    setStep("rapport");
    setGenRapport(true);
    const whysText = whys.map((w,i) => `Pourquoi ${i+1}: ${w}`).join("\n");
    const typeLabel = STOP_TYPES.find(t => t.value === form.stopType)?.label || form.stopType;
    const text = await callClaude(
      `Rapport 5 Pourquoi — Labatt Montréal.
      Ligne: ${form.ligne} | Machine: ${form.machine} | Format canette: ${form.format} | Caisse: ${form.formatCaisse} can/caisse
      Type arrêt: ${typeLabel} | Durée: ${form.duree} min | Date: ${form.date} | Opérateur: ${form.operateur}${form.hommeMetier ? ` | Homme de métier: ${form.hommeMetier} (${hommesMetier.find(h=>h.nom===form.hommeMetier)?.specialite||""})` : ""}
      Problème: ${form.probleme}
      ${whysText}
      Génère rapport professionnel en français:
      1. RÉSUMÉ DU PROBLÈME (2-3 lignes)
      2. ANALYSE 5 POURQUOI (liste numérotée)
      3. CAUSE RACINE IDENTIFIÉE
      4. ACTIONS CORRECTIVES (3-4 actions concrètes)
      5. MESURES PRÉVENTIVES (2-3 points)
      Format texte simple, concis, industriel.`
    );
    setRapport(text);
    const resp = RESPONSABLES[form.stopType] || RESPONSABLES.bris;
    const em = await callClaude(
      `Courriel professionnel court en français.
      À: ${resp.nom} (${resp.titre})
      De: ${form.operateur} — Opérateur ${form.machine} ${form.ligne}
      Sujet: Rapport 5 Pourquoi — ${form.machine} ${form.ligne} ${form.format} caisse/${form.formatCaisse} — ${form.date}
      Problème: ${form.probleme} | Cause racine: ${whys[4]}
      Poli, factuel, rapport en pièce jointe. Max 120 mots.`
    );
    setEmail(em);
    setGenRapport(false);
  };

  const copy = (txt) => {
    navigator.clipboard.writeText(txt);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const openEmailPreview = () => {
    const resp = RESPONSABLES[form.stopType] || RESPONSABLES.bris;
    setEmailDest(resp.email);
    setShowEmailPreview(true);
  };

  const sendEmail = () => {
    const sub = encodeURIComponent(`Rapport 5 Pourquoi — ${form.machine} ${form.ligne} — ${form.date}`);
    const body = encodeURIComponent(`${email}\n\n── RAPPORT COMPLET ──\n${rapport}`);
    window.open(`mailto:${emailDest}?subject=${sub}&body=${body}`);
    setShowEmailPreview(false);
  };

  const reset = () => {
    setStep("form");
    setForm({ ligne:"",machine:"",format:"",formatCaisse:"",stopType:"",duree:"",date:new Date().toISOString().split("T")[0],operateur:"",hommeMetier:"",probleme:"" });
    setWhys(["","","","",""]);
    setAiQ(["","","","",""]);
    setCurWhy(0); setRapport(""); setEmail("");
  };

  const responsable = RESPONSABLES[form.stopType] || RESPONSABLES.bris;
  const progress = step==="form" ? 20 : step==="whys" ? 25+(curWhy+1)/5*55 : step==="rapport" ? (genRapport?85:100) : 100;

  // Section homme de métier — affichée pour bris mécanique ET bris électrique
  const showHommeMetier = form.stopType === "bris" || form.stopType === "bris_electrique";
  const homLabel = form.stopType === "bris_electrique" ? "Électricien assigné" : "Homme de métier assigné";
  const homIcon = form.stopType === "bris_electrique" ? "⚡" : "🔧";

  return (
    <>
      <style>{STYLE}</style>
      <div className="app">

        {/* ── MODAL VÉRIFICATION EMAIL ── */}
        {showEmailPreview && (
          <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,0.75)", zIndex:200, display:"flex", alignItems:"center", justifyContent:"center", padding:20 }}>
            <div style={{ background:"#111620", border:"1px solid #d4a017", maxWidth:480, width:"100%", padding:28 }}>
              <div style={{ fontFamily:"Barlow Condensed, sans-serif", fontSize:16, fontWeight:700, color:"#d4a017", textTransform:"uppercase", letterSpacing:2, marginBottom:20 }}>
                ✉ Vérification avant envoi
              </div>
              <div style={{ marginBottom:14 }}>
                <div className="field-label">Destinataire</div>
                <input className="field-input" value={emailDest} onChange={e=>setEmailDest(e.target.value)}
                  placeholder="courriel@labatt.com" />
                <div style={{ fontSize:11, color:"#8892a0", marginTop:4 }}>
                  Vous pouvez modifier l'adresse si nécessaire avant d'envoyer.
                </div>
              </div>
              <div style={{ marginBottom:14 }}>
                <div className="field-label">Sujet</div>
                <div style={{ background:"#0d1117", border:"1px solid #1e2530", padding:"10px 12px", fontSize:13, color:"#c8d0dc" }}>
                  Rapport 5 Pourquoi — {form.machine} {form.ligne} — {form.date}
                </div>
              </div>
              <div style={{ marginBottom:20 }}>
                <div className="field-label">Aperçu du courriel</div>
                <div style={{ background:"#0d1117", border:"1px solid #1e2530", padding:"12px 14px", fontSize:12, color:"#c8d0dc", lineHeight:1.7, maxHeight:160, overflowY:"auto", whiteSpace:"pre-wrap" }}>
                  {email}
                </div>
              </div>
              <div style={{ display:"flex", gap:10 }}>
                <button className="btn btn-primary" style={{ flex:1, justifyContent:"center" }}
                  disabled={!emailDest.includes("@")} onClick={sendEmail}>
                  📧 Envoyer à {emailDest}
                </button>
                <button className="btn btn-ghost" onClick={()=>setShowEmailPreview(false)}>
                  Annuler
                </button>
              </div>
            </div>
          </div>
        )}

        {/* HEADER */}
        <div className="header">
          <div>
            <div className="header-logo">⚙ Labatt 5-Pourquoi</div>
            <div className="header-sub">Emballage MC2 &amp; MC3 — Montréal</div>
          </div>
          <div className="header-badge">IA Assisté</div>
        </div>

        <div className="container">
          <div className="progress-bar-outer">
            <div className="progress-bar-inner" style={{ width: `${progress}%` }} />
          </div>

          {/* ── FORMULAIRE ── */}
          {step === "form" && (
            <>
              <div className="section-title">Étape 1 — Identification de l'arrêt</div>
              <div className="card">

                {/* LIGNE */}
                <div style={{ marginBottom: 18 }}>
                  <div className="field-label">Ligne de production *</div>
                  <div className="selector-row">
                    {["MC2","MC3"].map(l => (
                      <button key={l} className="btn sel-btn" style={selBtnStyle(form.ligne===l)} onClick={() => pickLigne(l)}>
                        {l}
                      </button>
                    ))}
                  </div>
                </div>

                {/* MACHINE */}
                {form.ligne && (
                  <div style={{ marginBottom: 18 }}>
                    <div className="field-label">Machine *</div>
                    <div className="selector-row">
                      {machinesCfg.map(m => (
                        <button key={m} className="btn sel-btn" style={selBtnStyle(form.machine===m)} onClick={() => pickMachine(m)}>
                          {m}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* FORMAT CANETTE */}
                {form.machine && (
                  <div style={{ marginBottom: 18 }}>
                    <div className="field-label">Format canette *</div>
                    {formatsCfg.length === 1 ? (
                      <div className="locked-info">
                        🥫 {formatsCfg[0]} <span style={{ fontSize:11, color:"#8892a0", fontWeight:400 }}>— seul format disponible sur {form.machine} {form.ligne}</span>
                      </div>
                    ) : (
                      <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                        {formatsCfg.map(f => (
                          <button key={f} className="btn" style={radioStyle(form.format===f)} onClick={() => pickFormat(f)}>
                            {form.format===f ? "◉" : "○"} &nbsp;{f}
                          </button>
                        ))}
                      </div>
                    )}
                    {formatsCfg.length === 1 && !form.format && (() => { setTimeout(()=>pickFormat(formatsCfg[0]),0); return null; })()}
                  </div>
                )}

                {/* FORMAT CAISSE */}
                {form.format && (
                  <div style={{ marginBottom: 18 }}>
                    <div className="field-label">Format de caisse *</div>
                    {autoSingleCaisse ? (
                      <div className="locked-info">
                        📦 Caisse de <strong style={{ marginLeft:4 }}>{caissesCfg[0]} canettes</strong>
                        <span style={{ fontSize:11, color:"#8892a0", fontWeight:400, marginLeft:6 }}>— seul format disponible</span>
                      </div>
                    ) : (
                      <div className="caisse-grid">
                        {caissesCfg.map(n => (
                          <button key={n} className="btn caisse-btn" style={{
                            background: form.formatCaisse===n ? "rgba(212,160,23,0.18)" : "transparent",
                            color: form.formatCaisse===n ? "#d4a017" : "#8892a0",
                            border: `1px solid ${form.formatCaisse===n ? "#d4a017" : "#1e2530"}`,
                          }} onClick={() => upd("formatCaisse", n)}>
                            {n}
                          </button>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                {/* RÉSUMÉ CONFIG */}
                {form.formatCaisse && (
                  <div className="alert alert-info" style={{ marginBottom: 18 }}>
                    <span>📋</span>
                    <span>
                      <strong>{form.ligne} — {form.machine}</strong> &nbsp;|&nbsp;
                      {form.format} &nbsp;|&nbsp; Caisse de <strong>{form.formatCaisse} canettes</strong>
                    </span>
                  </div>
                )}

                {/* SUITE FORMULAIRE */}
                {form.formatCaisse && (
                  <>
                    <div className="grid-2" style={{ marginBottom: 14 }}>
                      <div>
                        <div className="field-label">Type d'arrêt *</div>
                        <div style={{ display:"flex", flexDirection:"column", gap:6 }}>
                          {STOP_TYPES.map(t => (
                            <button key={t.value} className="btn" style={{
                              ...radioStyle(form.stopType === t.value),
                              justifyContent: "flex-start",
                              fontSize: 13,
                              padding: "9px 12px",
                              flex: "unset",
                              width: "100%",
                            }} onClick={() => pickStopType(t.value)}>
                              {form.stopType === t.value ? "◉" : "○"} &nbsp;{t.label}
                            </button>
                          ))}
                        </div>
                      </div>
                      <div>
                        <div>
                          <div className="field-label">Durée (minutes) *</div>
                          <input className="field-input" type="number" placeholder="ex: 45" min="1" value={form.duree} onChange={e=>upd("duree",e.target.value)} />
                        </div>
                        <div style={{ marginTop: 12 }}>
                          <div className="field-label">Date *</div>
                          <input className="field-input" type="date" value={form.date} onChange={e=>upd("date",e.target.value)} />
                        </div>
                      </div>
                    </div>

                    <div style={{ marginBottom: 14 }}>
                      <div className="field-label">Opérateur *</div>
                      <input className="field-input" placeholder="Prénom et nom" value={form.operateur} onChange={e=>upd("operateur",e.target.value)} />
                    </div>

                    {/* HOMME DE MÉTIER — bris mécanique OU bris électrique */}
                    {showHommeMetier && (
                      <div style={{ marginBottom: 14 }}>
                        <div className="field-label">{homIcon} {homLabel}</div>

                        {/* Badge indiquant le filtre actif */}
                        <div style={{
                          fontSize: 11, color: form.stopType === "bris_electrique" ? "#60a5fa" : "#f59e0b",
                          background: form.stopType === "bris_electrique" ? "rgba(96,165,250,0.08)" : "rgba(245,158,11,0.08)",
                          border: `1px solid ${form.stopType === "bris_electrique" ? "rgba(96,165,250,0.25)" : "rgba(245,158,11,0.25)"}`,
                          padding: "5px 10px", marginBottom: 8, display: "inline-block",
                        }}>
                          {form.stopType === "bris_electrique" ? "⚡ Affiche uniquement les électriciens" : "🔧 Affiche uniquement les mécaniciens"}
                        </div>

                        {hommesFiltres.length > 0 && (
                          <div style={{ display:"flex", flexDirection:"column", gap:6, marginBottom:8 }}>
                            {hommesFiltres.map(h => (
                              <button key={h.id} className="btn" style={{
                                ...radioStyle(form.hommeMetier === h.nom),
                                justifyContent:"space-between",
                              }} onClick={() => upd("hommeMetier", form.hommeMetier === h.nom ? "" : h.nom)}>
                                <span>
                                  {form.hommeMetier === h.nom ? "◉" : "○"} &nbsp;
                                  <strong>{h.nom}</strong>
                                  <span style={{ marginLeft:8, fontSize:11, opacity:0.7,
                                    color: h.specialite==="Mécanique" ? "#f59e0b" : "#60a5fa" }}>
                                    {h.specialite === "Mécanique" ? "🔧" : "⚡"} {h.specialite}
                                  </span>
                                  {h.email && <span style={{ marginLeft:8, fontSize:11, opacity:0.6 }}>{h.email}</span>}
                                </span>
                              </button>
                            ))}
                          </div>
                        )}

                        {hommesFiltres.length === 0 && !showAddHom && (
                          <div style={{ fontSize:12, color:"#8892a0", fontStyle:"italic", marginBottom:8, padding:"8px 10px",
                            background:"rgba(255,255,255,0.02)", border:"1px solid #1e2530" }}>
                            Aucun {form.stopType === "bris_electrique" ? "électricien" : "mécanicien"} dans le dossier.
                          </div>
                        )}

                        {!showAddHom && (
                          <button className="btn btn-ghost" style={{ fontSize:12, padding:"7px 14px", gap:6 }}
                            onClick={()=>{ setShowAddHom(true); setNewHom({ nom:"", specialite: specialiteFixee || "", email:"" }); }}>
                            + Ajouter au dossier
                          </button>
                        )}

                        {showAddHom && (
                          <div style={{ background:"#0d1117", border:"1px solid rgba(212,160,23,0.3)", padding:14, marginTop:6 }}>
                            <div style={{ fontSize:11, color:"#d4a017", textTransform:"uppercase", letterSpacing:1.5, fontWeight:700, marginBottom:12 }}>
                              Nouveau — {form.stopType === "bris_electrique" ? "Électricien" : "Homme de métier"}
                            </div>
                            <div className="grid-2" style={{ marginBottom:10 }}>
                              <div>
                                <div className="field-label">Nom complet *</div>
                                <input className="field-input" placeholder="Prénom et nom" value={newHom.nom}
                                  onChange={e=>setNewHom(n=>({...n,nom:e.target.value}))} />
                              </div>
                              <div>
                                <div className="field-label">Spécialité *</div>
                                {/* Si type bris électrique, spécialité verrouillée à Électrique */}
                                {specialiteFixee ? (
                                  <div style={{
                                    background: specialiteFixee === "Électrique" ? "rgba(96,165,250,0.12)" : "rgba(245,158,11,0.12)",
                                    border: `1px solid ${specialiteFixee === "Électrique" ? "#60a5fa" : "#f59e0b"}`,
                                    color: specialiteFixee === "Électrique" ? "#60a5fa" : "#f59e0b",
                                    padding: "10px 12px", fontSize: 13, fontWeight: 600,
                                  }}>
                                    {specialiteFixee === "Électrique" ? "⚡" : "🔧"} {specialiteFixee} <span style={{ fontSize:10, opacity:0.7 }}>(fixé par le type d'arrêt)</span>
                                  </div>
                                ) : (
                                  <div style={{ display:"flex", gap:6 }}>
                                    {["Mécanique","Électrique"].map(s=>(
                                      <button key={s} className="btn" style={{
                                        flex:1, justifyContent:"center", padding:"10px 6px", fontSize:12,
                                        background: newHom.specialite===s ? (s==="Mécanique"?"rgba(245,158,11,0.2)":"rgba(96,165,250,0.2)") : "transparent",
                                        color: newHom.specialite===s ? (s==="Mécanique"?"#f59e0b":"#60a5fa") : "#8892a0",
                                        border: `1px solid ${newHom.specialite===s ? (s==="Mécanique"?"#f59e0b":"#60a5fa") : "#1e2530"}`,
                                      }} onClick={()=>setNewHom(n=>({...n,specialite:s}))}>
                                        {s==="Mécanique"?"🔧":"⚡"} {s}
                                      </button>
                                    ))}
                                  </div>
                                )}
                              </div>
                            </div>
                            <div style={{ marginBottom:10 }}>
                              <div className="field-label">Courriel (optionnel)</div>
                              <input className="field-input" placeholder="prenom.nom@labatt.com" value={newHom.email}
                                onChange={e=>setNewHom(n=>({...n,email:e.target.value}))} />
                            </div>
                            <div style={{ display:"flex", gap:8 }}>
                              <button className="btn btn-primary" style={{ fontSize:12, padding:"8px 16px" }}
                                disabled={!newHom.nom.trim()||!newHom.specialite} onClick={saveHomme}>
                                Sauvegarder au dossier
                              </button>
                              <button className="btn btn-ghost" style={{ fontSize:12, padding:"8px 14px" }}
                                onClick={()=>{ setShowAddHom(false); setNewHom({nom:"",specialite:"",email:""}); }}>
                                Annuler
                              </button>
                            </div>
                          </div>
                        )}

                        {hommesMetier.length > 0 && (
                          <details style={{ marginTop:10 }}>
                            <summary style={{ fontSize:11, color:"#8892a0", cursor:"pointer", userSelect:"none" }}>
                              Gérer le dossier complet ({hommesMetier.length} personnes)
                            </summary>
                            <div style={{ marginTop:8, display:"flex", flexDirection:"column", gap:4 }}>
                              {hommesMetier.map(h=>(
                                <div key={h.id} style={{ display:"flex", justifyContent:"space-between", alignItems:"center",
                                  background:"#0d1117", padding:"7px 12px", border:"1px solid #1e2530", fontSize:12 }}>
                                  <span>
                                    {h.nom} — <span style={{ color: h.specialite==="Électrique"?"#60a5fa":"#f59e0b", opacity:0.8 }}>
                                      {h.specialite === "Électrique" ? "⚡" : "🔧"} {h.specialite}
                                    </span>
                                  </span>
                                  <button style={{ background:"none", border:"none", color:"#ef4444", cursor:"pointer", fontSize:13 }}
                                    onClick={()=>removeHomme(h.id)}>✕</button>
                                </div>
                              ))}
                            </div>
                          </details>
                        )}
                      </div>
                    )}

                    <div>
                      <div className="field-label">Description du problème *</div>
                      <textarea className="field-textarea"
                        placeholder={`Ex: La ${form.machine} sur ${form.ligne} s'est arrêtée, les canettes ${form.format} caisse/${form.formatCaisse} n'avançaient plus...`}
                        value={form.probleme} onChange={e=>upd("probleme",e.target.value)} />
                    </div>
                  </>
                )}
              </div>

              {form.stopType && (
                <div className="alert alert-info">
                  <span>📧</span>
                  <span>Rapport dirigé vers : <strong>{responsable.nom}</strong> — {responsable.titre}</span>
                </div>
              )}

              <button className="btn btn-primary btn-full" disabled={!canStart} onClick={startWhys}>
                Démarrer l'analyse 5 Pourquoi →
              </button>
            </>
          )}

          {/* ── 5 POURQUOI ── */}
          {step === "whys" && (
            <>
              <div className="section-title">Étape 2 — Analyse des 5 Pourquoi</div>
              <div className="alert alert-warn" style={{ marginBottom: 20 }}>
                <span>🎯</span>
                <span><strong>{form.ligne} / {form.machine} / {form.format} / caisse {form.formatCaisse}</strong><br />{form.probleme}</span>
              </div>

              {[0,1,2,3,4].map(i => {
                const isDone = whys[i].trim().length > 0 && i < curWhy;
                const isActive = i === curWhy;
                const sugg = SUGGESTIONS[form.stopType]?.[i+1] || [];
                return (
                  <div key={i} className={`why-step ${isActive?"active":isDone?"done":""}`}>
                    <div className="why-number">{isDone ? "✓" : "⬡"} Pourquoi {i+1}</div>
                    {aiQ[i] && <div className="why-question">💬 {aiQ[i]}</div>}
                    {!aiQ[i] && isActive && loading && <div className="loading-bar" />}
                    {isActive && sugg.length > 0 && (
                      <div className="suggestion-chips">
                        {sugg.map((s,si)=>(
                          <span key={si} className="chip" onClick={()=>updateWhy(i,s)}>+ {s}</span>
                        ))}
                      </div>
                    )}
                    <textarea className="field-textarea" style={{ minHeight:60, background:isActive?"#0f1520":"#0a0e14", opacity:!isActive&&!isDone?0.4:1 }}
                      placeholder={isActive?"Décrivez la cause identifiée...":isDone?"":"En attente..."}
                      value={whys[i]} disabled={!isActive}
                      onChange={e=>updateWhy(i,e.target.value)} />
                    {isActive && (
                      <div style={{ display:"flex", gap:8, marginTop:8 }}>
                        <button className="btn btn-primary" onClick={()=>nextWhy(i)} disabled={!whys[i].trim()||loading}>
                          {i===4 ? "Générer le rapport ✓" : `Valider → Pourquoi ${i+2}`}
                        </button>
                        {i > 0 && <button className="btn btn-ghost" onClick={()=>setCurWhy(i-1)}>← Retour</button>}
                      </div>
                    )}
                  </div>
                );
              })}
            </>
          )}

          {/* ── RAPPORT ── */}
          {step === "rapport" && (
            <>
              <div className="section-title">Étape 3 — Rapport &amp; Envoi</div>
              {genRapport && (
                <><div className="loading-bar" />
                <div className="alert alert-info">⏳ Génération du rapport par l'IA...</div></>
              )}
              {rapport && (
                <>
                  <div className="card" style={{ marginBottom:16 }}>
                    <div style={{ display:"flex", justifyContent:"space-between", alignItems:"center", marginBottom:12 }}>
                      <div className="field-label">📋 Rapport 5 Pourquoi</div>
                      <button className="btn btn-outline" style={{ padding:"6px 14px",fontSize:12 }} onClick={()=>copy(rapport)}>
                        {copied ? "✓ Copié!" : "Copier"}
                      </button>
                    </div>
                    <div className="rapport-box">{rapport}</div>
                  </div>
                  {email && (
                    <div className="card">
                      <div style={{ marginBottom:12 }}>
                        <div className="field-label">📧 Courriel prêt à envoyer</div>
                        <div style={{ fontSize:12, color:"#8892a0", marginTop:4 }}>
                          À : <strong style={{ color:"#d4a017" }}>{responsable.email}</strong>
                        </div>
                      </div>
                      <div className="email-box">{email}</div>
                      <div style={{ display:"flex", gap:8, marginTop:12 }}>
                        <button className="btn btn-primary" onClick={openEmailPreview}>📧 Vérifier &amp; Envoyer</button>
                        <button className="btn btn-outline" onClick={()=>copy(`${email}\n\n── RAPPORT COMPLET ──\n${rapport}`)}>Copier tout</button>
                      </div>
                    </div>
                  )}
                  <hr className="divider" />
                  <div className="alert alert-success">
                    ✅ {form.ligne} | {form.machine} | {form.format} | Caisse {form.formatCaisse} | {form.duree} min | {form.operateur}
                  </div>
                  <button className="btn btn-ghost btn-full" onClick={reset}>+ Nouveau rapport 5 Pourquoi</button>
                </>
              )}
            </>
          )}
        </div>
      </div>
    </>
  );
}