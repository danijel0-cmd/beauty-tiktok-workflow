# 🚀 Quick Start - Beauty TikTok Shorts

## In 3 Schritten zu TikTok-Ready Videos

### Schritt 1: Clips hochladen
```bash
# Speichere deine Beauty-Clips hier:
~/Projects/beauty-tiktok-workflow/data/raw/

# Unterstützte Formate: .mp4, .mov, .avi, .mkv, .webm
```

### Schritt 2: Programm starten
```bash
cd ~/Projects/beauty-tiktok-workflow
python3 tiktok_shorts_processor.py
```

### Schritt 3: Outputs nutzen
```
data/processed/
├── short_001.mp4          ← Optimiert für TikTok (1080x1920)
├── short_001.txt          ← Description (copy-paste ready)
├── short_002.mp4
├── short_002.txt
└── metadata.json          ← Alle Daten (Hooks, Hashtags, Tips)
```

## Was automatisch passiert:

✅ Videos werden zu 9:16 Format konvertiert
✅ Helligkeit/Kontrast optimiert
✅ Virale Descriptions generiert
✅ Hashtags generiert
✅ Posting-Tipps gegeben
✅ Alles copy-paste ready

## Workflow

```
1. Clips in data/raw/ speichern
2. python3 tiktok_shorts_processor.py starten
3. Warten (2-5 Min je nach Clip-Länge)
4. Videos in CapCut öffnen (für Effekte)
5. Descriptions aus .txt kopieren
6. Auf TikTok hochladen
7. PROFIT! 💰
```

## Beispiel Output

**short_001.txt:**
```
DESCRIPTION:
Warte bis zum Ende, das Ergebnis ist KRASS! ✨

HASHTAGS:
#BeautyCommunity #TikTok #Viral #FYP #ForYou

TIP:
📱 Use trending sounds for 40% more views
```

## Skalierung

**Täglich routine:**
1. Neue Clips in `data/raw/` speichern
2. `python3 tiktok_shorts_processor.py` ausführen
3. Outputs nutzen
4. Posten!

Alles läuft automatisch. Keine manuelle Arbeit mehr nötig! 🤖

---

**Bereit?** Start mit: `python3 tiktok_shorts_processor.py`
