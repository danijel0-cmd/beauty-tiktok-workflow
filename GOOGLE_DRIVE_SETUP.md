# Google Drive API Setup (KOSTENLOS!)

Verbinde deinen Workflow mit Google Drive. **0€ Kosten!**

## 🚀 Setup (5 Minuten)

### Schritt 1: Google Cloud Projekt erstellen
1. Gehe zu: https://console.cloud.google.com
2. Klick **"Projekt erstellen"**
3. Name: `beauty-tiktok-workflow`
4. Klick **"Erstellen"**

### Schritt 2: Google Drive API aktivieren
1. Suchbar oben: Schreibe `Google Drive API`
2. Klick auf **"Google Drive API"**
3. Klick **"Aktivieren"**

### Schritt 3: Service Account erstellen
1. Linkes Menü: **"Anmeldedaten"**
2. Klick **"Anmeldedaten erstellen"**
3. Wähle: **"Service Account"**
4. Name: `beauty-tiktok`
5. Klick **"Erstellen und fortfahren"**
6. Skip die nächsten Schritte
7. Klick **"Fertig"**

### Schritt 4: JSON-Key generieren
1. Unter "Service Accounts" findest du `beauty-tiktok`
2. Klick drauf
3. Tab: **"Schlüssel"**
4. **"Schlüssel hinzufügen"** → **"Neuer Schlüssel"**
5. **"JSON"** → **"Erstellen"**
6. Datei wird heruntergeladen! `xxx-key.json`

### Schritt 5: Key in Projekt speichern
```bash
# Verschiebe die JSON-Datei:
mv ~/Downloads/xxx-key.json ~/Projects/beauty-tiktok-workflow/config/google-credentials.json
```

### Schritt 6: Google Drive Ordner erstellen
1. Gehe zu: https://drive.google.com
2. Erstelle neuen Ordner: `Beauty-TikTok-Raw`
3. Klick auf Ordner
4. In URL kannst du die Folder-ID sehen:
   ```
   https://drive.google.com/drive/folders/XXXX-FOLDER-ID-XXXX
   ```
5. Kopiere die **FOLDER-ID**

### Schritt 7: Folder-ID eintragen
```bash
# Edit diese Datei:
nano ~/Projects/beauty-tiktok-workflow/.env

# Und schreib rein:
GOOGLE_DRIVE_FOLDER_ID=XXXX-DEINE-FOLDER-ID-XXXX
```

## ✅ Fertig!

Jetzt lädt der Workflow automatisch Videos von Google Drive! 

```bash
python3 tiktok_shorts_with_drive.py
```

## 📁 So funktioniert's

```
Google Drive
├── Beauty-TikTok-Raw/
│   ├── clip_1.mp4          ← Du speicherst hier rein
│   ├── clip_2.mp4
│   └── clip_3.mp4
│
└── Beauty-TikTok-Output/   ← System speichert hier raus
    ├── short_001.mp4
    ├── short_001.txt
    └── metadata.json
```

## 💰 Kosten

**$0.00** - Komplett kostenlos!
- Google Drive API: Kostenlos
- Service Account: Kostenlos
- Unlimited Storage: (Du zahlst nur für Storage wenn du willst)

---

**Fertig eingerichtet?** Dann starten mit:
```bash
python3 tiktok_shorts_with_drive.py
```
