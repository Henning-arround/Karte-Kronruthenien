import pandas as pd
import requests
import json
import time
from typing import Dict, List, Optional, Tuple
import re

def extract_wikidata_id(url: str) -> Optional[str]:
    """
    Extrahiert die Wikidata-ID aus einer Wikidata-URL.
    
    Args:
        url: Wikidata-URL (z.B. "https://www.wikidata.org/wiki/Q123456")
        
    Returns:
        Wikidata-ID (z.B. "Q123456") oder None falls nicht gefunden
    """
    if not url or pd.isna(url):
        return None
    
    # Pattern für Wikidata-ID (Q gefolgt von Zahlen)
    pattern = r'Q\d+'
    match = re.search(pattern, str(url))
    
    return match.group() if match else None

def get_coordinates_from_wikidata(wikidata_id: str) -> Optional[Tuple[float, float]]:
    """
    Ruft die Koordinaten (P625) von Wikidata ab.
    
    Args:
        wikidata_id: Wikidata-ID (z.B. "Q123456")
        
    Returns:
        Tuple mit (Latitude, Longitude) oder None falls nicht gefunden
    """
    if not wikidata_id:
        return None
    
    # Wikidata SPARQL Endpoint
    sparql_url = "https://query.wikidata.org/sparql"
    
    # SPARQL Query für Koordinaten (P625)
    query = f"""
    SELECT ?coordinates WHERE {{
        wd:{wikidata_id} wdt:P625 ?coordinates.
    }}
    """
    
    headers = {
        'User-Agent': 'Python Script for Map Creation/1.0 (https://example.com/contact)',
        'Accept': 'application/sparql-results+json'
    }
    
    try:
        response = requests.get(
            sparql_url,
            params={'query': query, 'format': 'json'},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            if data['results']['bindings']:
                coords_string = data['results']['bindings'][0]['coordinates']['value']
                
                # Koordinaten aus dem Format "Point(longitude latitude)" extrahieren
                coords_match = re.search(r'Point\(([+-]?\d+\.?\d*)\s+([+-]?\d+\.?\d*)\)', coords_string)
                if coords_match:
                    longitude = float(coords_match.group(1))
                    latitude = float(coords_match.group(2))
                    return (latitude, longitude)
                    
        return None
        
    except Exception as e:
        print(f"Fehler beim Abrufen der Koordinaten für {wikidata_id}: {e}")
        return None

def create_geojson_feature(name: str, region: str, coordinates: Tuple[float, float]) -> Dict:
    """
    Erstellt ein GeoJSON-Feature für einen Ort.
    
    Args:
        name: Name des Ortes (aus Spalte "Schreibweise Ortsregister")
        region: Region des Ortes (aus Spalte "Region")
        coordinates: Tuple mit (Latitude, Longitude)
        
    Returns:
        GeoJSON-Feature als Dictionary
    """
    latitude, longitude = coordinates
    
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [longitude, latitude]  # GeoJSON verwendet [lng, lat]
        },
        "properties": {
            "name": name,
            "region": region
        }
    }

def process_excel_to_geojson(excel_file: str, output_file: str = "orte.geojson"):
    """
    Verarbeitet die Excel-Datei und erstellt eine GeoJSON-Datei.
    
    Args:
        excel_file: Pfad zur Excel-Datei
        output_file: Pfad zur Ausgabe-GeoJSON-Datei
    """
    print(f"Lade Excel-Datei: {excel_file}")
    
    try:
        # Excel-Datei laden
        df = pd.read_excel(excel_file)
        
        # Spaltennamen prüfen
        required_columns = ["Wikidata URL", "Schreibweise Ortsregister", "Region"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Fehlende Spalten: {missing_columns}")
            print(f"Verfügbare Spalten: {list(df.columns)}")
            return
        
        print(f"Gefundene Einträge: {len(df)}")
        
        # GeoJSON-Struktur initialisieren
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        successful_count = 0
        failed_count = 0
        
        # Jeden Eintrag verarbeiten
        for index, row in df.iterrows():
            name = row["Schreibweise Ortsregister"]
            region = row["Region"]
            wikidata_url = row["Wikidata URL"]
            
            # Überspringe Einträge ohne Namen
            if pd.isna(name) or not name.strip():
                print(f"Überspringe Eintrag {index + 1}: Kein Name")
                continue
            
            # Wikidata-ID extrahieren
            wikidata_id = extract_wikidata_id(wikidata_url)
            if not wikidata_id:
                print(f"Überspringe '{name}': Keine gültige Wikidata-ID in URL '{wikidata_url}'")
                failed_count += 1
                continue
            
            print(f"Verarbeite '{name}' (ID: {wikidata_id})...")
            
            # Koordinaten von Wikidata abrufen
            coordinates = get_coordinates_from_wikidata(wikidata_id)
            if coordinates:
                # GeoJSON-Feature erstellen
                feature = create_geojson_feature(name, region, coordinates)
                geojson["features"].append(feature)
                successful_count += 1
                print(f"  ✓ Koordinaten gefunden: {coordinates}")
            else:
                print(f"  ✗ Keine Koordinaten gefunden für '{name}'")
                failed_count += 1
            
            # Kurze Pause um Wikidata-Server nicht zu überlasten
            time.sleep(0.5)
        
        # GeoJSON-Datei speichern
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)
        
        print(f"\nVerarbeitung abgeschlossen:")
        print(f"  ✓ Erfolgreich: {successful_count} Orte")
        print(f"  ✗ Fehlgeschlagen: {failed_count} Orte")
        print(f"  📁 GeoJSON gespeichert als: {output_file}")
        
    except Exception as e:
        print(f"Fehler beim Verarbeiten der Excel-Datei: {e}")

def main():
    """
    Hauptfunktion - verarbeitet die Excel-Datei und erstellt GeoJSON
    """
    excel_file = "../data/Orte_Identifikation_factgrid.xlsx"
    output_file = "../data/orte_kronruthenien.geojson"

    print("=== Kronruthenien Orte GeoJSON Generator ===\n")
    
    # Verarbeitung starten
    process_excel_to_geojson(excel_file, output_file)

if __name__ == "__main__":
    main()