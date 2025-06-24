#!/usr/bin/env python3
"""
Update gateway analysis data to:
1. Rename "RDAP Server" to "LogicBoxes"
2. Remove "NameBright" and "Network Solutions" 
3. Keep only core gateway providers: LogicBoxes, RRPProxy/CentralNic, and Tucows
4. Recalculate all statistics and market shares
"""

import json
from datetime import datetime
from pathlib import Path

def load_json(filepath):
    """Load JSON data from file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data, filepath):
    """Save JSON data to file with proper formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def update_comprehensive_analysis():
    """Update the comprehensive gateway analysis"""
    
    # Load the current data
    filepath = Path("comprehensive_gateway_analysis.json")
    data = load_json(filepath)
    
    # Keep only the three core gateway providers
    core_providers = {
        "Tucows": data["gateway_providers"]["Tucows"],
        "RRPProxy/CentralNic": data["gateway_providers"]["RRPProxy/CentralNic"],
        "LogicBoxes": data["gateway_providers"]["RDAP Server (Potential Gateway)"].copy()
    }
    
    # Update LogicBoxes data (rename from RDAP Server)
    core_providers["LogicBoxes"]["gateway_provider"] = "LogicBoxes"
    
    # Recalculate totals for gateway providers only
    total_gateway_domains = sum(provider["total_domains"] for provider in core_providers.values())
    total_gateway_registrars = sum(provider["registrar_count"] for provider in core_providers.values())
    
    # Calculate new market shares (as percentage of total market, not just gateway market)
    total_market_domains = data["dataset_summary"]["total_domains"]
    
    for provider_name, provider_data in core_providers.items():
        provider_data["market_share_percent"] = (provider_data["total_domains"] / total_market_domains) * 100
    
    # Update the main data structure
    data["gateway_providers"] = core_providers
    
    # Update gateway analysis totals
    data["gateway_analysis"] = {
        "total_gateway_domains": total_gateway_domains,
        "total_self_hosted_domains": total_market_domains - total_gateway_domains,
        "gateway_market_share_percent": (total_gateway_domains / total_market_domains) * 100,
        "self_hosted_market_share_percent": ((total_market_domains - total_gateway_domains) / total_market_domains) * 100
    }
    
    # Filter top_rdap_urls to only include our core providers
    core_rdap_urls = []
    for url_data in data["top_rdap_urls"]:
        if url_data["is_gateway"]:
            provider = url_data["gateway_provider"]
            if provider == "RDAP Server (Potential Gateway)":
                url_data["gateway_provider"] = "LogicBoxes"
                core_rdap_urls.append(url_data)
            elif provider in ["Tucows", "RRPProxy/CentralNic"]:
                core_rdap_urls.append(url_data)
        else:
            # Keep non-gateway URLs for reference
            core_rdap_urls.append(url_data)
    
    data["top_rdap_urls"] = core_rdap_urls
    
    # Update analysis date
    data["analysis_date"] = datetime.now().isoformat()
    
    # Save updated data
    save_json(data, filepath)
    print(f"Updated {filepath}")
    
    return data

def update_provider_summary():
    """Update the gateway provider summary"""
    
    # Load current data
    filepath = Path("gateway_provider_summary.json")
    data = load_json(filepath)
    
    # Filter to keep only core providers and rename RDAP Server to LogicBoxes
    core_data = []
    for item in data:
        provider = item["gateway_provider"]
        if provider == "Tucows":
            core_data.append(item)
        elif provider == "RRPProxy/CentralNic":
            core_data.append(item)
        elif provider == "RDAP Server":
            item["gateway_provider"] = "LogicBoxes"
            core_data.append(item)
    
    # Save updated data
    save_json(core_data, filepath)
    print(f"Updated {filepath}")
    
    return core_data

def update_all_gateway_registrars():
    """Update the all gateway registrars file"""
    
    # Load current data
    filepath = Path("all_gateway_registrars.json")
    data = load_json(filepath)
    
    # Filter to keep only registrars from core providers
    core_registrars = []
    for registrar in data:
        provider = registrar["gateway_provider"]
        if provider == "Tucows":
            core_registrars.append(registrar)
        elif provider == "RRPProxy/CentralNic":
            core_registrars.append(registrar)
        elif provider == "RDAP Server":
            registrar["gateway_provider"] = "LogicBoxes"
            core_registrars.append(registrar)
    
    # Save updated data
    save_json(core_registrars, filepath)
    print(f"Updated {filepath} - kept {len(core_registrars)} registrars from core providers")
    
    return core_registrars

def update_public_files():
    """Update files in the public/data/processed directory"""
    
    public_dir = Path("public/data/processed")
    if not public_dir.exists():
        print(f"Public directory {public_dir} does not exist, skipping...")
        return
    
    # Copy updated files to public directory
    files_to_copy = [
        "comprehensive_gateway_analysis.json",
        "gateway_provider_summary.json", 
        "all_gateway_registrars.json"
    ]
    
    for filename in files_to_copy:
        source = Path(filename)
        dest = public_dir / filename
        
        if source.exists():
            # Load and save to ensure consistent formatting
            data = load_json(source)
            save_json(data, dest)
            print(f"Updated {dest}")

def print_summary(comprehensive_data, provider_summary, registrars_data):
    """Print a summary of the updated data"""
    
    print("\n" + "="*60)
    print("UPDATED GATEWAY ANALYSIS SUMMARY")
    print("="*60)
    
    print(f"\nCore Gateway Providers: {len(comprehensive_data['gateway_providers'])}")
    print(f"Total Gateway Registrars: {sum(p['registrar_count'] for p in comprehensive_data['gateway_providers'].values())}")
    print(f"Total Gateway Domains: {comprehensive_data['gateway_analysis']['total_gateway_domains']:,}")
    print(f"Gateway Market Share: {comprehensive_data['gateway_analysis']['gateway_market_share_percent']:.2f}%")
    
    print("\nProvider Breakdown:")
    for name, data in comprehensive_data['gateway_providers'].items():
        print(f"  {name}:")
        print(f"    Registrars: {data['registrar_count']}")
        print(f"    Domains: {data['total_domains']:,}")
        print(f"    Market Share: {data['market_share_percent']:.2f}%")
    
    print(f"\nTotal registrars in all_gateway_registrars.json: {len(registrars_data)}")

def main():
    """Main function to update all gateway analysis files"""
    
    print("Starting gateway analysis update...")
    print("Focusing on core gateway providers: LogicBoxes, RRPProxy/CentralNic, and Tucows")
    
    try:
        # Update all files
        comprehensive_data = update_comprehensive_analysis()
        provider_summary = update_provider_summary()
        registrars_data = update_all_gateway_registrars()
        
        # Update public files
        update_public_files()
        
        # Print summary
        print_summary(comprehensive_data, provider_summary, registrars_data)
        
        print("\n✅ Successfully updated all gateway analysis files!")
        
    except Exception as e:
        print(f"❌ Error updating files: {e}")
        raise

if __name__ == "__main__":
    main()