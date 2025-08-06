#!/usr/bin/env python3
"""
Script to add Wikidata URLs to places in orte_kronruthenien.geojson
based on the Excel file Orte_Identifikation_factgrid.xlsx

This script reads the Excel file containing place names and their Wikidata URLs,
then adds the wikidata_url property to matching places in the GeoJSON file.
"""

import pandas as pd
import json
import os
from pathlib import Path

def load_excel_data(excel_path):
    """
    Load place names and Wikidata URLs from Excel file.
    
    Args:
        excel_path (str): Path to the Excel file
        
    Returns:
        dict: Dictionary mapping place names to Wikidata URLs
    """
    try:
        # Read Excel file
        df = pd.read_excel(excel_path)
        
        # Print column names for debugging
        print("Available columns in Excel file:")
        print(df.columns.tolist())
        
        # Check if required columns exist
        required_columns = ["Schreibweise Ortsregister", "Wikidata URL"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            print(f"Warning: Missing columns: {missing_columns}")
            print("Available columns:", df.columns.tolist())
            return {}
        
        # Create mapping dictionary, filtering out rows with empty values
        place_wikidata_map = {}
        for _, row in df.iterrows():
            place_name = row["Schreibweise Ortsregister"]
            wikidata_url = row["Wikidata URL"]
            
            # Only add if both values are not empty/NaN
            if pd.notna(place_name) and pd.notna(wikidata_url) and place_name.strip() and wikidata_url.strip():
                place_wikidata_map[place_name.strip()] = wikidata_url.strip()
        
        print(f"Loaded {len(place_wikidata_map)} place-Wikidata mappings from Excel file")
        return place_wikidata_map
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return {}

def load_geojson(geojson_path):
    """
    Load GeoJSON data from file.
    
    Args:
        geojson_path (str): Path to the GeoJSON file
        
    Returns:
        dict: GeoJSON data
    """
    try:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading GeoJSON file: {e}")
        return None

def save_geojson(geojson_data, output_path):
    """
    Save GeoJSON data to file.
    
    Args:
        geojson_data (dict): GeoJSON data
        output_path (str): Path to save the file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(geojson_data, f, indent=2, ensure_ascii=False)
        print(f"GeoJSON saved to: {output_path}")
    except Exception as e:
        print(f"Error saving GeoJSON file: {e}")

def add_wikidata_urls(geojson_data, place_wikidata_map):
    """
    Add Wikidata URLs to GeoJSON features based on place name matching.
    
    Args:
        geojson_data (dict): GeoJSON data
        place_wikidata_map (dict): Dictionary mapping place names to Wikidata URLs
        
    Returns:
        tuple: (updated_geojson_data, match_count, total_features)
    """
    if not geojson_data or 'features' not in geojson_data:
        print("Invalid GeoJSON data")
        return geojson_data, 0, 0
    
    match_count = 0
    total_features = len(geojson_data['features'])
    
    # Track which Excel entries were matched
    matched_excel_entries = set()
    
    for feature in geojson_data['features']:
        if 'properties' in feature and 'name' in feature['properties']:
            place_name = feature['properties']['name'].strip()
            
            # Try exact match first
            if place_name in place_wikidata_map:
                feature['properties']['wikidata_url'] = place_wikidata_map[place_name]
                matched_excel_entries.add(place_name)
                match_count += 1
                print(f"Matched: {place_name} -> {place_wikidata_map[place_name]}")
            else:
                # Try case-insensitive match
                for excel_name, wikidata_url in place_wikidata_map.items():
                    if place_name.lower() == excel_name.lower():
                        feature['properties']['wikidata_url'] = wikidata_url
                        matched_excel_entries.add(excel_name)
                        match_count += 1
                        print(f"Matched (case-insensitive): {place_name} -> {wikidata_url}")
                        break
    
    # Report unmatched Excel entries
    unmatched_excel = set(place_wikidata_map.keys()) - matched_excel_entries
    if unmatched_excel:
        print(f"\nUnmatched Excel entries ({len(unmatched_excel)}):")
        for name in sorted(unmatched_excel):
            print(f"  - {name}")
    
    return geojson_data, match_count, total_features

def main():
    """Main function to execute the script."""
    # Set up file paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / "data"
    excel_path = data_dir / "Orte_Identifikation_factgrid.xlsx"
    geojson_path = data_dir / "orte_kronruthenien.geojson"
    output_path = data_dir / "orte_kronruthenien_with_wikidata.geojson"
    
    print("=== Adding Wikidata URLs to GeoJSON ===")
    print(f"Excel file: {excel_path}")
    print(f"GeoJSON file: {geojson_path}")
    print(f"Output file: {output_path}")
    print()
    
    # Check if files exist
    if not excel_path.exists():
        print(f"Error: Excel file not found: {excel_path}")
        return
    
    if not geojson_path.exists():
        print(f"Error: GeoJSON file not found: {geojson_path}")
        return
    
    # Load data
    print("Loading Excel data...")
    place_wikidata_map = load_excel_data(excel_path)
    if not place_wikidata_map:
        print("No valid data found in Excel file. Exiting.")
        return
    
    print("Loading GeoJSON data...")
    geojson_data = load_geojson(geojson_path)
    if not geojson_data:
        print("Failed to load GeoJSON data. Exiting.")
        return
    
    # Add Wikidata URLs
    print("\nMatching places and adding Wikidata URLs...")
    updated_geojson, match_count, total_features = add_wikidata_urls(geojson_data, place_wikidata_map)
    
    # Save updated GeoJSON
    save_geojson(updated_geojson, output_path)
    
    # Summary
    print(f"\n=== Summary ===")
    print(f"Total places in GeoJSON: {total_features}")
    print(f"Places in Excel with Wikidata URLs: {len(place_wikidata_map)}")
    print(f"Successfully matched and updated: {match_count}")
    print(f"Match rate: {match_count/total_features*100:.1f}%")
    
    if match_count > 0:
        print(f"\nUpdated GeoJSON saved to: {output_path}")
        
        # Ask if user wants to replace the original file
        replace_original = input("\nDo you want to replace the original file? (y/N): ").strip().lower()
        if replace_original == 'y':
            import shutil
            shutil.copy2(output_path, geojson_path)
            print(f"Original file updated: {geojson_path}")
    else:
        print("\nNo matches found. No changes made.")

if __name__ == "__main__":
    main()
