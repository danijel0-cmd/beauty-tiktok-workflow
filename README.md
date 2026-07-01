# Beauty TikTok Shorts Workflow

Automatisierter Workflow: Rohmaterial → TikTok-Ready Videos (mit Hooks + Hashtags)

**Keine Google Cloud nötig. Keine API-Keys. 100% KOSTENLOS!** ✅

---

## 🚀 Quick Start (2 Minuten!)

### 1. Dependencies installieren
```bash
pip3 install -r requirements.txt
```

### 2. Clips speichern
```bash
# Deine Videos hier:
~/Projects/beauty-tiktok-workflow/data/raw/

# Einfach deine .mp4 Dateien reincopieren!
```

### 3. Programm starten
```bash
cd ~/Projects/beauty-tiktok-workflow
python3 tiktok_shorts_processor.py
```

### 4. Fertig!
```
data/processed/
├── short_001.mp4          ← Optimiert für TikTok
├── short_001.txt          ← Description (copy-paste ready!)
├── short_002.mp4
├── short_002.txt
└── metadata.json
```

---

## 📋 Was passiert automatisch?

✅ **Phase 1:** Clips erkennen
✅ **Phase 2:** In 1080x1920 (9:16 TikTok Format) konvertieren
✅ **Phase 3:** Helligkeit/Kontrast optimieren
✅ **Phase 4:** Virale Hooks generieren
✅ **Phase 5:** Hashtags + Tipps generieren

**Alles copy-paste ready für TikTok!**

---

## 📁 Folder-Struktur

```
beauty-tiktok-workflow/
├── data/
│   ├── raw/              ← DEINE CLIPS HIER REIN
│   │   ├── clip_1.mp4
│   │   └── clip_2.mp4
│   └── processed/        ← FERTIGE VIDEOS HIER RAUS
│       ├── short_001.mp4
│       ├── short_001.txt
│       └── metadata.json
├── tiktok_shorts_processor.py
├── QUICK_START.md
└── GOOGLE_DRIVE_EASY_FREE.md
```

---

## 💡 Google Drive Option

Willst du Videos direkt von Google Drive verarbeiten?

👉 Siehe: **GOOGLE_DRIVE_EASY_FREE.md** (auch kostenlos!)

---

## 📊 Workflow-Ausgabe

Jedes Video bekommt automatisch:

```
DESCRIPTION:
Warte bis zum Ende, das Ergebnis ist KRASS! ✨

HASHTAGS:
#BeautyCommunity #TikTok #Viral #FYP #ForYou

TIP:
📱 Use trending sounds for 40% more views
```

**Einfach kopieren & auf TikTok posten!** 📱

---

## 🔄 Skalierung

```
Tag 1: 2 Videos → 2 Shorts
Tag 2: 5 Videos → 5 Shorts
Tag 3: 10 Videos → 10 Shorts
...

Alles automatisch! 🤖
```

---

## ❓ Fragen?

Siehe die Docs:
- **QUICK_START.md** — 3-Schritt Übersicht
- **GOOGLE_DRIVE_EASY_FREE.md** — Kostenlose Cloud-Option
- **SHORTS_WORKFLOW.md** — Detaillierter Workflow

---

**Bereit? Los geht's!** 🚀

```bash
python3 tiktok_shorts_processor.py
```
