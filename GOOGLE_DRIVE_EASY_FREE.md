# Google Drive Setup - KOSTENLOS & EINFACH (Ohne Google Cloud)

**Kein Google Cloud nötig. Kein Rechnungskonto. 100% KOSTENLOS!** ✅

## Option A: Lokale Folder (EASIEST)

```bash
# 1. Erstelle lokalen Ordner
mkdir ~/beauty-tiktok-clips

# 2. Speichere Clips dort
cp ~/Downloads/clip.mp4 ~/beauty-tiktok-clips/

# 3. Starte Workflow
python3 tiktok_shorts_processor.py
```

**FERTIG!** Keine Google Registrierung nötig! 🎉

---

## Option B: Google Drive Sync (Mit Google Drive)

### Schritt 1: Installiere "Google Drive für Mac"
1. Gehe zu: https://drive.google.com
2. Oben rechts: **Einstellungen** ⚙️
3. **"Google Drive für Mac herunterladen"**
4. Installieren

### Schritt 2: Synchronisiere Google Drive
```bash
# Dein Google Drive ist jetzt ein lokaler Ordner!
# Normalerweise: ~/Google Drive/Mein Drive/

# Erstelle Ordner dort:
mkdir ~/Google\ Drive/Mein\ Drive/Beauty-TikTok-Raw
```

### Schritt 3: Update Workflow
Edit `.env`:
```bash
nano .env
```

Schreib rein:
```
GOOGLE_DRIVE_FOLDER=~/Google\ Drive/Mein\ Drive/Beauty-TikTok-Raw
```

### Schritt 4: Run!
```bash
python3 tiktok_shorts_processor.py
```

**FERTIG!** Videos werden automatisch von Drive synchronisiert! 🎉

---

## Das war's!

**Keine API-Keys nötig**
**Kein Google Cloud Projekt nötig**
**Kein Rechnungskonto nötig**
**100% KOSTENLOS!**

---

## Welche Option ist besser?

| | Option A (Lokal) | Option B (Drive Sync) |
|---|---|---|
| Setup Zeit | 2 Min | 5 Min |
| Kosten | $0 | $0 |
| Überall verfügbar | 📱❌ | 📱✅ |
| Einfach | ✅ | ✅ |

**Empfehlung:** Starten mit Option A (Lokal), später zu Option B upgraden!

---

**Bereit? Los geht's!** 🚀
