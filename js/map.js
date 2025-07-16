// Konfiguration
const CONFIG = {
    // Zentrale Koordinaten für Kronruthenien (basierend auf aktuellen Daten)
    CENTER: [50.33266544337678, 22.8076171875],
    ZOOM: 6,
    GEOJSON_PATH: 'data/orte_kronruthenien.geojson'
};

// Farbpalette für verschiedene Regionen
const REGION_COLORS = [
    '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6',
    '#1abc9c', '#e67e22', '#34495e', '#f1c40f', '#e91e63',
    '#8e44ad', '#27ae60', '#2980b9', '#d35400', '#7f8c8d'
];

// Globale Variablen
let map;
let regionColorMap = {};
let regionCounts = {};
let allMarkers = [];

/**
 * Initialisiert die Karte
 */
function initMap() {
    // Karte erstellen
    map = L.map('map').setView(CONFIG.CENTER, CONFIG.ZOOM);
    
    // OpenStreetMap Tiles hinzufügen
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 18
    }).addTo(map);
    
    // Vollbild-Kontrolle hinzufügen
    map.addControl(new L.Control.Fullscreen());
    
    // Home-Button zur Karte hinzufügen
    L.Control.homeButton = L.Control.extend({
        options: {
            position: 'topleft'
        },
        onAdd: function (map) {
            const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom');
            const button = L.DomUtil.create('a', 'leaflet-bar-part', container);
            button.innerHTML = '<svg style="width:18px;height:18px;display:block;margin-top:5px;" viewBox="0 0 24 24"><path fill="currentColor" d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z" /></svg>';
            button.href = '#';
            button.title = 'Zurück zur Startansicht';
            
            L.DomEvent.on(button, 'click', function(e) {
                L.DomEvent.preventDefault(e);
                map.setView(CONFIG.CENTER, CONFIG.ZOOM);
            });

            return container;
        }
    });
    map.addControl(new L.Control.homeButton());
    
    // Zoom-Event-Listener für dynamische Marker-Größe
    map.on('zoomend', updateMarkerSizes);
}

/**
 * Aktualisiert die Marker-Größen basierend auf der Zoom-Stufe
 */
function updateMarkerSizes() {
    const zoom = map.getZoom();
    
    // Größe basierend auf Zoom-Level berechnen
    let size, borderWidth;
    
    if (zoom <= 5) {
        size = 6;
        borderWidth = 1;
    } else if (zoom <= 7) {
        size = 8;
        borderWidth = 1;
    } else if (zoom <= 9) {
        size = 12;
        borderWidth = 2;
    } else if (zoom <= 11) {
        size = 16;
        borderWidth = 2;
    } else {
        size = 20;
        borderWidth = 3;
    }
    
    // Alle Marker aktualisieren
    allMarkers.forEach(marker => {
        const markerDot = marker.getElement()?.querySelector('.marker-dot');
        if (markerDot) {
            markerDot.style.width = size + 'px';
            markerDot.style.height = size + 'px';
            markerDot.style.borderWidth = borderWidth + 'px';
        }
        
        // Icon-Größe und Anker aktualisieren
        const icon = marker.getIcon();
        if (icon) {
            icon.options.iconSize = [size, size];
            icon.options.iconAnchor = [size / 2, size / 2];
        }
    });
}

/**
 * Generiert eine Farbe für eine Region
 */
function getRegionColor(region) {
    if (!regionColorMap[region]) {
        const colorIndex = Object.keys(regionColorMap).length % REGION_COLORS.length;
        regionColorMap[region] = REGION_COLORS[colorIndex];
    }
    return regionColorMap[region];
}

/**
 * Erstellt einen Marker für einen Ort
 */
function createMarker(feature) {
    const { name, region } = feature.properties;
    const [longitude, latitude] = feature.geometry.coordinates;
    
    // Farbe für die Region bestimmen
    const color = getRegionColor(region);
    
    // Custom Icon erstellen mit dynamischer Größe
    const icon = L.divIcon({
        className: 'custom-marker',
        html: `<div class="marker-dot" style="
            background-color: ${color};
            width: 12px;
            height: 12px;
            border-radius: 50%;
            border: 2px solid white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.3);
            transition: all 0.3s ease;
        "></div>`,
        iconSize: [12, 12],
        iconAnchor: [6, 6]
    });
    
    // Marker erstellen
    const marker = L.marker([latitude, longitude], { icon })
        .bindPopup(`
            <div class="popup-content">
                <div class="popup-title">${name}</div>
                <div class="popup-region">Region: ${region}</div>
            </div>
        `);
    
    return marker;
}

/**
 * Lädt und verarbeitet die GeoJSON-Daten
 */
async function loadGeoJsonData() {
    try {
        const response = await fetch(CONFIG.GEOJSON_PATH);
        
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const geojsonData = await response.json();
        
        // Überprüfen ob es sich um gültige GeoJSON-Daten handelt
        if (!geojsonData.features || !Array.isArray(geojsonData.features)) {
            throw new Error('Ungültige GeoJSON-Daten');
        }
        
        return geojsonData;
        
    } catch (error) {
        console.error('Fehler beim Laden der GeoJSON-Daten:', error);
        throw error;
    }
}

/**
 * Verarbeitet die GeoJSON-Daten und fügt Marker zur Karte hinzu
 */
function processGeoJsonData(geojsonData) {
    regionCounts = {};
    allMarkers = [];
    
    // Marker-Gruppe erstellen
    const markerGroup = L.layerGroup();
    
    geojsonData.features.forEach(feature => {
        const { region } = feature.properties;
        
        // Statistiken aktualisieren
        regionCounts[region] = (regionCounts[region] || 0) + 1;
        
        // Marker erstellen und zur Gruppe hinzufügen
        const marker = createMarker(feature);
        markerGroup.addLayer(marker);
        allMarkers.push(marker);
    });
    
    // Marker-Gruppe zur Karte hinzufügen
    markerGroup.addTo(map);
    
    // Initiale Marker-Größen setzen
    updateMarkerSizes();
    
    // Karte auf alle Marker zentrieren (optional - nur wenn nicht genug Marker im aktuellen View)
    if (allMarkers.length > 0) {
        const group = new L.featureGroup(allMarkers);
        const bounds = group.getBounds();
        
        // Prüfen ob die aktuellen Bounds die meisten Marker enthalten
        const currentBounds = map.getBounds();
        const markersInView = allMarkers.filter(marker => 
            currentBounds.contains(marker.getLatLng())
        ).length;
        
        // Nur neu zentrieren wenn weniger als 70% der Marker sichtbar sind
        if (markersInView < allMarkers.length * 0.7) {
            map.fitBounds(bounds.pad(0.05));
        }
    }
}

/**
 * Erstellt die Legende
 */
function createLegend() {
    const legendContent = document.getElementById('legend-content');
    
    if (Object.keys(regionColorMap).length === 0) {
        legendContent.innerHTML = '<p class="text-muted">Keine Regionen gefunden</p>';
        return;
    }
    
    let legendHTML = '';
    
    // Sortierte Regionen nach Anzahl der Orte
    const sortedRegions = Object.entries(regionCounts)
        .sort((a, b) => b[1] - a[1])
        .map(([region]) => region);
    
    sortedRegions.forEach(region => {
        const color = regionColorMap[region];
        const count = regionCounts[region];
        
        legendHTML += `
            <div class="legend-item">
                <div class="legend-color" style="background-color: ${color};"></div>
                <span title="${region} (${count} Orte)">${region} (${count})</span>
            </div>
        `;
    });
    
    legendContent.innerHTML = legendHTML;
}

/**
 * Erstellt die Statistiken
 */
function createStats() {
    const statsContent = document.getElementById('stats-content');
    
    const totalPlaces = Object.values(regionCounts).reduce((sum, count) => sum + count, 0);
    const totalRegions = Object.keys(regionCounts).length;
    
    const topRegion = Object.entries(regionCounts)
        .sort((a, b) => b[1] - a[1])[0];
    
    statsContent.innerHTML = `
        <div class="mb-2">
            <strong>Gesamtanzahl Orte:</strong><br>
            <span class="text-primary">${totalPlaces}</span>
        </div>
        <div class="mb-2">
            <strong>Anzahl Regionen:</strong><br>
            <span class="text-success">${totalRegions}</span>
        </div>
        ${topRegion ? `
        <div class="mb-2">
            <strong>Größte Region:</strong><br>
            <span class="text-warning">${topRegion[0]} (${topRegion[1]} Orte)</span>
        </div>
        ` : ''}
    `;
}

/**
 * Behandelt Fehler beim Laden der Daten
 */
function handleError(error) {
    console.error('Fehler:', error);
    
    const loadingDiv = document.getElementById('loading');
    loadingDiv.innerHTML = `
        <div class="alert alert-danger" role="alert">
            <h4 class="alert-heading">Fehler beim Laden der Daten</h4>
            <p>${error.message}</p>
            <hr>
            <p class="mb-0">
                Bitte stellen Sie sicher, dass die Datei <code>data/orte_kronruthenien.geojson</code> existiert 
                und gültige GeoJSON-Daten enthält.
            </p>
        </div>
    `;
}

/**
 * Hauptfunktion - wird beim Laden der Seite ausgeführt
 */
async function main() {
    try {
        // Karte initialisieren
        initMap();
        
        // GeoJSON-Daten laden
        const geojsonData = await loadGeoJsonData();
        
        // Daten verarbeiten und Marker hinzufügen
        processGeoJsonData(geojsonData);
        
        // Legende und Statistiken erstellen
        createLegend();
        createStats();
        
        // Loading-Indikator verstecken und Karte anzeigen
        document.getElementById('loading').style.display = 'none';
        document.getElementById('map').style.display = 'block';
        
        // Kartengröße neu berechnen und Ansicht setzen
        map.invalidateSize();
        map.setView(CONFIG.CENTER, CONFIG.ZOOM);
        
        console.log(`Karte erfolgreich geladen mit ${allMarkers.length} Orten`);
        
    } catch (error) {
        handleError(error);
    }
}

// Vollbild-Kontrolle für Leaflet
L.Control.Fullscreen = L.Control.extend({
    options: {
        position: 'topleft'
    },
    
    onAdd: function(map) {
        const container = L.DomUtil.create('div', 'leaflet-control-fullscreen leaflet-bar leaflet-control');
        const button = L.DomUtil.create('a', 'leaflet-control-fullscreen-button leaflet-bar-part', container);
        
        button.href = '#';
        button.title = 'Vollbild';
        button.innerHTML = '<svg style="width:18px;height:18px;" viewBox="0 0 24 24"><path fill="currentColor" d="M3,9H5V5H9V3H3V9M21,3V9H19V5H15V3H21M3,15H5V19H9V21H3V15M19,19H15V21H21V15H19V19Z" /></svg>';
        
        L.DomEvent.on(button, 'click', function(e) {
            L.DomEvent.preventDefault(e);
            this.toggleFullscreen();
        }, this);
        
        return container;
    },
    
    toggleFullscreen: function() {
        const mapContainer = this._map.getContainer();
        
        if (!document.fullscreenElement) {
            mapContainer.requestFullscreen().then(() => {
                this._map.invalidateSize();
            });
        } else {
            document.exitFullscreen();
        }
    }
});

// Seite laden
document.addEventListener('DOMContentLoaded', main);
