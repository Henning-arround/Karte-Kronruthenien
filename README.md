# Kronruthenien Ortskarte

Eine interaktive Webkarte zur Visualisierung historischer Orte in Kronruthenien basierend auf Wikidata-Informationen.

## 🗺️ Übersicht

Dieses Projekt erstellt eine interaktive Karte, die historische Orte in Kronruthenien visualisiert. Die Daten werden aus einer Excel-Datei extrahiert, über Wikidata mit Koordinaten angereichert und als GeoJSON-Datei gespeichert. Die Webanwendung zeigt diese Orte dann auf einer OpenStreetMap-Karte an, wobei verschiedene Regionen durch unterschiedliche Farben gekennzeichnet sind.

## 🚀 Live-Demo

Die Karte ist verfügbar unter: [GitHub Pages Link einfügen]

## 📋 Funktionen

- **Interaktive Karte**: Basierend auf OpenStreetMap mit Leaflet.js
- **Farbkodierung**: Verschiedene Regionen werden durch unterschiedliche Farben dargestellt
- **Popup-Informationen**: Klicken Sie auf einen Marker, um Details zum Ort anzuzeigen
- **Legende**: Zeigt alle Regionen mit ihren Farben und Ortszahlen
- **Statistiken**: Übersicht über Gesamtzahl der Orte und Regionen
- **Vollbild-Modus**: Karte kann im Vollbildmodus betrachtet werden
- **Responsive Design**: Funktioniert auf Desktop und mobilen Geräten

## 🛠️ Technische Details

### Verwendete Technologien
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Kartenengine**: Leaflet.js
- **Styling**: Bootstrap 5
- **Datenverarbeitung**: Python mit pandas, requests
- **Datenquelle**: Wikidata SPARQL API

### Projektstruktur
```
Map_Kronruthenien/
├── css/
│   └── style.css                       # Alle benutzerdefinierten Stile
├── data/
│   ├── Orte_Identifikation_factgrid.xlsx   # Excel-Quelldatei
│   └── orte_kronruthenien.geojson      # Generierte GeoJSON-Datei
├── js/
│   └── map.js                          # JavaScript-Logik für die Karte
├── scripts/
│   └── create_place_geojson.py         # Python-Skript zur Datenverarbeitung
├── index.html                          # Hauptseite der Webanwendung
├── requirements.txt                    # Python-Abhängigkeiten
└── README.md                           # Diese Datei
```


