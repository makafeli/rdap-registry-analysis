#!/usr/bin/env python3
"""
Update the LogicBoxes summary stats to reflect the new filtered data
"""

import json
from pathlib import Path

def update_logicboxes_stats():
    """Update the LogicBoxes summary stats file"""
    
    # Load the all gateway registrars data
    with open('all_gateway_registrars.json', 'r') as f:
        all_registrars = json.load(f)
    
    # Filter only LogicBoxes registrars
    logicboxes_registrars = [r for r in all_registrars if r['gateway_provider'] == 'LogicBoxes']
    
    # Calculate stats
    total_registrars = len(logicboxes_registrars)
    
    # Filter out registrars with null domain counts
    registrars_with_domains = [r for r in logicboxes_registrars if r['domain_count'] is not None]
    
    total_domains = sum(r['domain_count'] for r in registrars_with_domains)
    avg_domains = total_domains / len(registrars_with_domains) if registrars_with_domains else 0
    
    # Calculate median
    domain_counts = sorted([r['domain_count'] for r in registrars_with_domains])
    median_domains = domain_counts[len(domain_counts) // 2] if domain_counts else 0
    
    # Get top 10 by domains
    top_10 = sorted(registrars_with_domains, key=lambda x: x['domain_count'], reverse=True)[:10]
    top_10_formatted = [
        {
            "name": r['name'],
            "domain_count": r['domain_count']
        }
        for r in top_10
    ]
    
    # Count RDAP service distribution
    rdap_distribution = {}
    for r in logicboxes_registrars:
        url = r['rdap_url']
        if url == 'rdapserver.net':
            key = 'LogicBoxes Core (rdapserver.net)'
        elif url == 'rdap.rrpproxy.net':
            key = 'RRPProxy/CentralNic Gateway (rrpproxy.net)'
        else:
            key = f'Other ({url})'
        
        rdap_distribution[key] = rdap_distribution.get(key, 0) + 1
    
    # Create updated stats
    updated_stats = {
        "total_registrars": total_registrars,
        "total_domains": total_domains,
        "avg_domains_per_registrar": avg_domains,
        "median_domains_per_registrar": median_domains,
        "top_10_by_domains": top_10_formatted,
        "rdap_service_distribution": rdap_distribution,
        "countries_with_icann_data": {},
        "enrichment_success_rate": 0.0,  # Reset since we're not tracking enrichment
        "note": "Updated for core gateway providers only: LogicBoxes, RRPProxy/CentralNic, and Tucows"
    }
    
    # Save updated stats
    stats_file = Path('data/processed/logicboxes_summary_stats.json')
    with open(stats_file, 'w') as f:
        json.dump(updated_stats, f, indent=2)
    
    print(f"Updated {stats_file}")
    print(f"LogicBoxes registrars: {total_registrars}")
    print(f"Total domains: {total_domains:,}")
    print(f"Average domains per registrar: {avg_domains:,.1f}")
    
    return updated_stats

if __name__ == "__main__":
    update_logicboxes_stats()