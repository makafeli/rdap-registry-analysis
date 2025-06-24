#!/usr/bin/env python3
"""
RDAP Registrar Enrichment Script
Fetches contact information for Registry Gateway registrars from ICANN API
"""

import requests
import pandas as pd
import time
import json
from datetime import datetime
from typing import Dict, List, Optional

# Registry Gateway registrars with domain counts
REGISTRY_GATEWAY_REGISTRARS = [
    {"iana_id": 303, "name": "PDR Ltd. d/b/a PublicDomainRegistry.com", "domains": 4845099},
    {"iana_id": 955, "name": "Launchpad.com Inc.", "domains": 729662},
    {"iana_id": 1636, "name": "Hostinger, UAB", "domains": 590290},
    {"iana_id": 1495, "name": "BigRock Solutions Ltd.", "domains": 276454},
    {"iana_id": 1091, "name": "IHS Telekom, Inc.", "domains": 160821},
    {"iana_id": 1005, "name": "NetEarth One Inc. d/b/a NetEarth", "domains": 142479},
    {"iana_id": 609, "name": "Sav.com, LLC", "domains": 135595},
    {"iana_id": 1586, "name": "MAT BAO CORPORATION", "domains": 134504},
    {"iana_id": 3806, "name": "Beget LLC", "domains": 103122},
    {"iana_id": 1600, "name": "Tecnocrática Centro de Datos, S.L.", "domains": 101516},
    {"iana_id": 1432, "name": "Alpine Domains Inc.", "domains": 81068},
    {"iana_id": 1534, "name": "Aerotek Bilisim Sanayi ve Ticaret AS", "domains": 80389},
    {"iana_id": 819, "name": "Reg2C.com Inc.", "domains": 75272},
    {"iana_id": 1483, "name": "Neubox Internet S.A. de C.V.", "domains": 62661},
    {"iana_id": 1710, "name": "Nhan Hoa Software Company Ltd.", "domains": 57102},
    {"iana_id": 1112, "name": "Internet Invest, Ltd. dba Imena.ua", "domains": 47650},
    {"iana_id": 1913, "name": "DOTSERVE INC.", "domains": 41645},
    {"iana_id": 1895, "name": "Namespro Solutions Inc.", "domains": 38321},
    {"iana_id": 1082, "name": "Register4Less, Inc.", "domains": 33943},
    {"iana_id": 1660, "name": "Domainshype.com, LLC", "domains": 33214}
]

def fetch_registrar_data(iana_id: int) -> Optional[Dict]:
    """
    Fetch registrar information from ICANN API
    
    Args:
        iana_id: IANA registrar ID
        
    Returns:
        Dictionary with registrar data or None if error
    """
    url = f"https://lookup.icann.org/api/registrar/{iana_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for IANA ID {iana_id}: {e}")
        return None

def enrich_registrar_data(registrars: List[Dict]) -> pd.DataFrame:
    """
    Enrich registrar data with contact information from ICANN
    
    Args:
        registrars: List of registrar dictionaries with iana_id, name, and domains
        
    Returns:
        DataFrame with enriched registrar data
    """
    enriched_data = []
    total = len(registrars)
    
    print(f"Starting enrichment for {total} registrars...")
    print("-" * 50)
    
    for idx, registrar in enumerate(registrars, 1):
        iana_id = registrar["iana_id"]
        print(f"[{idx}/{total}] Fetching data for IANA ID {iana_id}: {registrar['name']}")
        
        # Fetch data from ICANN
        api_data = fetch_registrar_data(iana_id)
        
        if api_data:
            # Extract relevant fields
            enriched_record = {
                "iana_id": iana_id,
                "name": api_data.get("name", registrar["name"]),
                "website": api_data.get("url", "N/A"),
                "email": api_data.get("email", "N/A"),
                "phone": api_data.get("phone", "N/A"),
                "abuse_email": api_data.get("abuseContact", {}).get("email", "N/A"),
                "abuse_phone": api_data.get("abuseContact", {}).get("phone", "N/A"),
                "whois_server": api_data.get("whoisServer", "N/A"),
                "referral_url": api_data.get("referralUrl", "N/A"),
                "status": api_data.get("status", "N/A"),
                "street": api_data.get("address", {}).get("street", "N/A"),
                "city": api_data.get("address", {}).get("city", "N/A"),
                "state": api_data.get("address", {}).get("state", "N/A"),
                "postal_code": api_data.get("address", {}).get("postalCode", "N/A"),
                "country": api_data.get("address", {}).get("country", "N/A"),
                "rdap_url": "rdapserver.net",
                "service_provider": "LogicBoxes",
                "domains": registrar["domains"],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            print(f"  ✓ Successfully enriched: {enriched_record['website']}")
        else:
            # Use fallback data
            enriched_record = {
                "iana_id": iana_id,
                "name": registrar["name"],
                "website": "Error fetching data",
                "email": "N/A",
                "phone": "N/A",
                "abuse_email": "N/A",
                "abuse_phone": "N/A",
                "whois_server": "N/A",
                "referral_url": "N/A",
                "status": "N/A",
                "street": "N/A",
                "city": "N/A",
                "state": "N/A",
                "postal_code": "N/A",
                "country": "N/A",
                "rdap_url": "rdapserver.net",
                "service_provider": "LogicBoxes",
                "domains": registrar["domains"],
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            print(f"  ✗ Error fetching data")
        
        enriched_data.append(enriched_record)
        
        # Rate limiting (1 second between requests)
        if idx < total:
            time.sleep(1)
    
    return pd.DataFrame(enriched_data)

def save_results(df: pd.DataFrame):
    """Save enriched data to multiple formats"""
    # Save to CSV
    csv_path = "../data/enriched_registrars.csv"
    df.to_csv(csv_path, index=False)
    print(f"\n✓ Saved to CSV: {csv_path}")
    
    # Save to JSON
    json_path = "../data/enriched_registrars.json"
    df.to_json(json_path, orient="records", indent=2)
    print(f"✓ Saved to JSON: {json_path}")
    
    # Save summary statistics
    summary_path = "../data/enrichment_summary.txt"
    with open(summary_path, "w") as f:
        f.write("RDAP Registry Gateway Enrichment Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total registrars enriched: {len(df)}\n")
        f.write(f"Total domains managed: {df['domains'].sum():,}\n")
        f.write(f"Average domains per registrar: {df['domains'].mean():,.0f}\n")
        f.write(f"Enrichment timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Top registrars by domain count
        f.write("Top 10 Registrars by Domain Count:\n")
        f.write("-" * 50 + "\n")
        top_10 = df.nlargest(10, 'domains')[['name', 'domains', 'website']]
        for _, row in top_10.iterrows():
            f.write(f"{row['name']}: {row['domains']:,} domains - {row['website']}\n")
    
    print(f"✓ Saved summary: {summary_path}")

def main():
    """Main execution function"""
    print("RDAP Registry Gateway Enrichment Script")
    print("=" * 50)
    print(f"Service Provider: LogicBoxes")
    print(f"RDAP URL: rdapserver.net")
    print(f"Registrars to process: {len(REGISTRY_GATEWAY_REGISTRARS)}")
    print("=" * 50 + "\n")
    
    # Enrich data
    enriched_df = enrich_registrar_data(REGISTRY_GATEWAY_REGISTRARS)
    
    # Display summary
    print("\n" + "=" * 50)
    print("Enrichment Complete!")
    print("=" * 50)
    print(f"\nTotal registrars processed: {len(enriched_df)}")
    print(f"Total domains: {enriched_df['domains'].sum():,}")
    print(f"Countries represented: {enriched_df['country'].nunique()}")
    
    # Show sample results
    print("\nSample enriched data:")
    print(enriched_df[['name', 'website', 'email', 'domains']].head())
    
    # Save results
    save_results(enriched_df)
    
    print("\n✓ Enrichment process completed successfully!")

if __name__ == "__main__":
    main()
