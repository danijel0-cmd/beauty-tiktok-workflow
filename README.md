# Beauty TikTok Auto-Workflow

Automatisierter Workflow zum Schneiden und Optimieren von Beauty-Videos für TikTok — mit Hook-Erkennung, Auto-Schnitt und viraler Optimierung.

## Features

- 🎬 **Hook-Erkennung**: Findet die besten 1-3 Sekunden für maximales Engagement
- ✂️ **Auto-Schnitt**: TikTok-optimierte Schnitte (9:16, schnell, viral-gerecht)
- 💬 **Text-Overlays**: Automatische Captions & Emojis (Beauty-spezifisch)
- 📱 **CapCut-Export**: Fertig zum Upload in CapCut oder direkt exportieren
- ☁️ **Google Drive Integration**: Automatisches Abrufen & Speichern
- 📊 **Metadaten**: Auto-generierte Hashtags & Beschreibungen

## Quick Start

```bash
# 1. Dependencies installieren
pip install -r requirements.txt

# 2. Google Drive verbinden (siehe Setup)
cp config/.env.example .env
# Trage deine Google Drive API-Keys ein

# 3. Test-Video verarbeiten
python src/main.py --input data/raw/sample.mp4

# 4. Ergebnis in CapCut öffnen
open data/processed/output.capcut
```

## Struktur

```
.
├── src/                    # Python Scripts
│   ├── main.py            # Hauptprogramm
│   ├── hook_detector.py   # Hook-Erkennung
│   ├── video_editor.py    # Auto-Schnitt
│   ├── google_drive.py    # Drive API
│   └── metadata.py        # Metadaten-Generator
├── config/
│   ├── settings.json      # Globale Einstellungen
│   └── beauty_prompts.txt # Beauty-spezifische Erkennungen
├── templates/             # CapCut & Overlay Templates
├── data/
│   ├── raw/              # Rohmaterial (Google Drive)
│   └── processed/        # Fertige Videos
└── tests/                # Unit Tests
```

## Setup-Anleitung

### 1. Google Drive API
1. Gehe zu [Google Cloud Console](https://console.cloud.google.com)
2. Neues Projekt erstellen
3. Google Drive API aktivieren
4. Service Account erstellen
5. JSON-Key herunterladen → `config/google-credentials.json`

### 2. Environment-Variablen
```bash
cp config/.env.example .env
# Editiere .env mit deinen Credentials
```

### 3. CapCut Templates
- Platziere deine liebsten CapCut-Vorlagen in `templates/`
- Der Workflow wird diese automatisch verwenden

## Roadmap

- [ ] Phase 1: Google Drive API + Basis-Struktur
- [ ] Phase 2: Hook-Erkennung (Szenen, Schnitte, Reaktionen)
- [ ] Phase 3: Auto-Schnitt & TikTok-Optimierung
- [ ] Phase 4: CapCut-Export Automation
- [ ] Phase 5: Google Drive Watcher (Auto-Processing)
- [ ] Phase 6: Metadaten-Generator (Tags, Captions)

## Support

Brauchst du Hilfe? Öffne ein Issue oder kontaktiere mich!
