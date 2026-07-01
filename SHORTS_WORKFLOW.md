# Beauty TikTok Shorts Workflow

Vollautomatisiertes System für Beauty-Videos → TikTok Shorts mit Hooks + Hashtags

## 🚀 Quick Start

```bash
cd ~/Projects/beauty-tiktok-workflow
python3 tiktok_shorts_processor.py
```

## 📋 Workflow (5 Phasen)

### Phase 1: Clips vorbereiten
- System sucht alle `.mp4`, `.mov`, `.avi` in `data/raw/`
- Zeigt Länge + FPS an

### Phase 2: Schneiden & Optimieren
- Konvertiert zu TikTok-Format (1080x1920, 9:16)
- Optimiert Helligkeit/Kontrast
- Speichert als `short_001.mp4`, `short_002.mp4`, etc.

### Phase 3: Effekte
- ℹ️ Du öffnest die Videos in CapCut für Effekte
- System bereitet alles vor

### Phase 4: Hooks generieren
- Erstellt automatisch virale Descriptions
- Generiert relevante Hashtags
- Gibt TikTok-Tipps (beste Uhrzeit, etc.)
- Speichert alles in `metadata.json`

### Phase 5: Export ready
- Für jedes Video eine `.txt` Datei mit:
  - Hook/Description (copy-paste ready)
  - Hashtags
  - Tipps
- Alles im `data/processed/` Ordner

## 📁 Folder-Struktur

```
~/Projects/beauty-tiktok-workflow/
├── data/
│   ├── raw/                          ← DEINE CLIPS HIER REIN
│   │   ├── clip_1.mp4
│   │   ├── clip_2.mp4
│   │   └── ...
│   └── processed/                    ← OUTPUTS HIER
│       ├── short_001.mp4             ← Optimiert für TikTok
│       ├── short_001.txt             ← Description
│       ├── short_002.mp4
│       ├── short_002.txt
│       └── metadata.json             ← Alle Daten
└── tiktok_shorts_processor.py        ← DAS PROGRAMM
```

## 🎯 Wie du es benutzt

### Schritt 1: Clips hochladen
```bash
# Speichere deine Clips hier:
~/Projects/beauty-tiktok-workflow/data/raw/
```

### Schritt 2: Programm ausführen
```bash
python3 tiktok_shorts_processor.py
```

### Schritt 3: Warten (2-5 Min je nach Clip-Länge)
- System verarbeitet automatisch

### Schritt 4: Outputs nutzen
- `short_XXX.mp4` → CapCut öffnen (Effekte + Untertitel)
- `short_XXX.txt` → Description kopieren
- `metadata.json` → Alle Hashtags + Tips

### Schritt 5: Posten
- Video hochladen
- Description + Hashtags einfügen
- Post!

## 💡 Features

✅ Automatische TikTok-Optimierung (9:16)
✅ Virale Hooks/Descriptions
✅ Hashtag-Generierung
✅ Posting-Tipps
✅ Batch-Processing (mehrere Clips gleichzeitig)
✅ Copy-Paste ready Outputs

## 🔄 Workflow für Skalierung

**Täglich:**
1. Neue Clips in `data/raw/` speichern
2. `python3 tiktok_shorts_processor.py` ausführen
3. Outputs nutzen
4. Posten!

**Passiert automatisch:**
- ✅ Schneiden
- ✅ Optimieren
- ✅ Hooks generieren
- ✅ Hashtags generieren
- ✅ Tipps generieren

## 📊 Output-Beispiel

```
[1] clip_1.mp4: 2.5s @ 30fps
[1] Verarbeite: clip_1.mp4
✅ Optimiert: short_001.mp4

DESCRIPTION:
Dieser Beauty-Hack ist WILD 😍

HASHTAGS:
#BeautyTok #MakeupTutorial #SkincareRoutine #BeautyHacks #MakeupArtist

TIP:
🕐 Best time to post: 18:00-20:00 (peak engagement)
```

## ⚙️ Customization

Willst du andere Hooks oder Hashtags? Edit diese in der Python-Datei:
- Zeile ~120: `beauty_hooks` Liste
- Zeile ~128: `hashtags` Liste
- Zeile ~133: `tips` Liste

## 🐛 Troubleshooting

**"Keine Clips gefunden"**
→ Speichere Clips in: `data/raw/`

**"Fehler beim Optimieren"**
→ Stelle sicher, dass die Clips .mp4 oder .mov sind

**Videos sind zu groß**
→ Das ist normal! TikTok komprimiert automatisch

## 📞 Support

Alles läuft lokal auf deinem Mac. Keine Internet-Verbindung nötig!

---

**Built for scalability. Made to make money.** 🚀
