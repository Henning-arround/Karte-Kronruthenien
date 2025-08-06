# Kronruthenien Ortskarte

Eine interaktive Webkarte zur Visualisierung historischer Orte in Kronruthenien basierend auf Wikidata-Informationen als Teil des VAMOD-Projekts.

## Projektkontext

Diese Karte ist Teil des [VAMOD-Projekts](https://leibniz-gwzo.de/de/vamod) des Leibniz-Instituts für Geschichte und Kultur des östlichen Europa (GWZO). Das Projekt modelliert vormoderne Ambiguitäten am Beispiel von Kronruthenien (1340-1434) und macht Forschungsdaten aus ca. 800 Urkunden nach FAIR-Prinzipien auf FactGrid verfügbar. Weitere Informationen zum Projekt finden Sie in der [FactGrid-Datenbank](https://database.factgrid.de/wiki/Item:Q1206913).

## Übersicht

Dieses Projekt erstellt eine interaktive Karte, die historische Orte in Kronruthenien visualisiert. Die Karte zeigt alle Objektorte, die in historischen Urkunden genannt werden, und ordnet sie den Regionen zu, in denen sie in den Urkunden beschrieben werden. Die Daten werden aus einer Excel-Datei extrahiert, über Wikidata mit Koordinaten angereichert und als GeoJSON-Datei gespeichert. Die Webanwendung zeigt diese Orte dann auf einer OpenStreetMap-Karte an, wobei verschiedene Regionen durch unterschiedliche Farben gekennzeichnet sind.

## Live-Demo

Die Karte ist verfügbar unter: [https://Henning-arround.github.io/Karte-Kronruthenien/]

## Funktionen

- **Interaktive Karte**: Basierend auf OpenStreetMap mit Leaflet.js
- **Farbkodierung**: Verschiedene Regionen werden durch unterschiedliche Farben dargestellt
- **Popup-Informationen**: Klicken Sie auf einen Marker, um Details zum Ort anzuzeigen
- **Legende**: Zeigt alle Regionen mit ihren Farben und Ortszahlen
- **Statistiken**: Übersicht über Gesamtzahl der Orte und Regionen
- **Vollbild-Modus**: Karte kann im Vollbildmodus betrachtet werden
- **Responsive Design**: Funktioniert auf Desktop und mobilen Geräten
- **Urkundenbezug**: Visualisierung von Objektorten aus historischen Urkunden mit regionaler Zuordnung

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
│   └── style.css                           # Alle benutzerdefinierten Stile
├── data/
│   └── orte_kronruthenien.geojson          # Generierte GeoJSON-Datei
├── js/
│   └── map.js                              # JavaScript-Logik für die Karte
├── scripts/
│   └── create_place_geojson.py             # Python-Skript zur Datenverarbeitung
├── index.html                              # Hauptseite der Webanwendung
├── requirements.txt                        # Python-Abhängigkeiten
└── README.md                               # Diese Datei
```


