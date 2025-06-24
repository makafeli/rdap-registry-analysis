#!/usr/bin/env python3
"""
Comprehensive RDAP Gateway Analysis
"""
import pandas as pd
import json
from collections import defaultdict, Counter
from urllib.parse import urlparse
import re

def identify_gateway_provider(rdap_url):
    """Identify gateway provider from RDAP URL patterns"""
    if pd.isna(rdap_url) or rdap_url.strip() == '':
        return None
    
    url_lower = rdap_url.lower()
    
    # Define patterns for each provider
    patterns = {
        'Tucows': [
            'tucows.com',
            'opensrs.net',
            'opensrs.com',
            'hover.com',
            'enom.com',  # Tucows acquired eNom
            'ascio.com'  # Part of Tucows
        ],
        'InternetX': [
            'internetx.com',
            'internetx.de',
            'autodnslive',
            'internetx.net'
        ],
        'RRPProxy/CentralNic': [
            'rrpproxy.net',
            'centralnic.com',
            'centralnic.net',
            'rrpproxy.com',
            'key-systems.net',  # Part of CentralNic
            'rrp-proxy.net',
            'hexonet.net'  # Part of CentralNic
        ],
        'LogicBoxes': [
            'logicboxes.com',
            'resellerclub.com',
            'bigrock.com',
            'publicdomainregistry.com',
            'stargate.com',
            'uniteddomains.com',
            'mitsu.com'
        ],
        'Gransy': [
            'gransy.com',
            'gransy.cz',
            'subreg.cz',
            'active24.com'
        ]
    }
    
    # Check for known patterns
    for provider, patterns_list in patterns.items():
        for pattern in patterns_list:
            if pattern in url_lower:
                return provider
    
    return None

def analyze_rdap_gateways():
    """Main analysis function"""
    print("Reading RDAP lookups Excel file...")
    
    # Read the Excel file
    df = pd.read_excel('/Users/yasinboelhouwer/rdap-registry-analysis/data/Rdap lookups.xlsx')
    
    print(f"Total rows: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print()
    
    # Identify relevant columns
    registrar_col = 'Name'  # Based on the actual column names
    rdap_url_col = 'rdap_url'
    domain_count_col = 'Domain count'
    
    print(f"Using columns:")
    print(f"  Registrar: {registrar_col}")
    print(f"  RDAP URL: {rdap_url_col}")
    print(f"  Domain Count: {domain_count_col}")
    print()
    
    # Add gateway provider column
    df['Gateway_Provider'] = df[rdap_url_col].apply(identify_gateway_provider)
    
    # Analyze gateway usage
    gateway_stats = {}
    
    # Known providers to analyze
    providers = ['Tucows', 'InternetX', 'RRPProxy/CentralNic', 'LogicBoxes', 'Gransy']
    
    for provider in providers:
        provider_df = df[df['Gateway_Provider'] == provider].copy()
        
        if len(provider_df) > 0:
            # Calculate statistics
            total_registrars = len(provider_df)
            total_domains = provider_df[domain_count_col].sum()
            
            # Get top registrars
            top_registrars = provider_df.nlargest(10, domain_count_col)
            
            # Get unique RDAP URLs
            unique_urls = provider_df[rdap_url_col].unique()
            
            gateway_stats[provider] = {
                'total_registrars': total_registrars,
                'total_domains': int(total_domains),
                'unique_rdap_urls': len(unique_urls),
                'rdap_urls': unique_urls.tolist(),
                'top_registrars': []
            }
            
            for _, row in top_registrars.iterrows():
                gateway_stats[provider]['top_registrars'].append({
                    'name': row[registrar_col],
                    'domains': int(row[domain_count_col]),
                    'rdap_url': row[rdap_url_col]
                })
    
    # Find potential unknown gateways
    # Extract domains from RDAP URLs
    df['RDAP_Domain'] = df[rdap_url_col].apply(lambda x: urlparse(x).netloc.lower() if pd.notna(x) else None)
    
    # Count domain occurrences
    domain_counts = df['RDAP_Domain'].value_counts()
    
    # Filter domains used by multiple registrars
    potential_gateways = []
    for domain, count in domain_counts.items():
        if count > 2 and domain:  # Used by more than 2 registrars
            # Check if it's not already identified
            domain_df = df[df['RDAP_Domain'] == domain]
            if domain_df['Gateway_Provider'].isna().all():
                total_domains = domain_df[domain_count_col].sum()
                potential_gateways.append({
                    'domain': domain,
                    'registrar_count': count,
                    'total_domains': int(total_domains),
                    'sample_registrars': domain_df.nlargest(3, domain_count_col)[registrar_col].tolist()
                })
    
    # Sort by total domains
    potential_gateways.sort(key=lambda x: x['total_domains'], reverse=True)
    
    # Calculate totals
    total_domains_all_gateways = sum(stats['total_domains'] for stats in gateway_stats.values())
    total_domains_dataset = df[domain_count_col].sum()
    
    # Print results
    print("=" * 80)
    print("RDAP GATEWAY PROVIDER ANALYSIS")
    print("=" * 80)
    
    for provider, stats in gateway_stats.items():
        market_share = (stats['total_domains'] / total_domains_dataset) * 100
        
        print(f"\n{provider}:")
        print(f"  Total Registrars: {stats['total_registrars']}")
        print(f"  Total Domains: {stats['total_domains']:,}")
        print(f"  Market Share: {market_share:.2f}%")
        print(f"  Unique RDAP URLs: {stats['unique_rdap_urls']}")
        
        print(f"  Top 5 Registrars:")
        for i, reg in enumerate(stats['top_registrars'][:5]):
            print(f"    {i+1}. {reg['name']}: {reg['domains']:,} domains")
            print(f"       RDAP: {reg['rdap_url']}")
    
    print("\n" + "=" * 80)
    print("POTENTIAL UNKNOWN GATEWAY PROVIDERS")
    print("(Domains used by 3+ registrars)")
    print("=" * 80)
    
    for i, gateway in enumerate(potential_gateways[:10]):
        print(f"\n{i+1}. {gateway['domain']}")
        print(f"   Used by {gateway['registrar_count']} registrars")
        print(f"   Total domains: {gateway['total_domains']:,}")
        print(f"   Sample registrars: {', '.join(gateway['sample_registrars'][:3])}")
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total domains in dataset: {int(total_domains_dataset):,}")
    print(f"Total domains using identified gateways: {total_domains_all_gateways:,}")
    print(f"Gateway market share: {(total_domains_all_gateways/total_domains_dataset)*100:.2f}%")
    
    print("\nMarket share by provider:")
    for provider, stats in sorted(gateway_stats.items(), key=lambda x: x[1]['total_domains'], reverse=True):
        share = (stats['total_domains'] / total_domains_dataset) * 100
        print(f"  {provider}: {share:.2f}% ({stats['total_domains']:,} domains)")
    
    # Save results
    results = {
        'gateway_providers': gateway_stats,
        'potential_gateways': potential_gateways[:20],
        'summary': {
            'total_domains_dataset': int(total_domains_dataset),
            'total_domains_gateways': total_domains_all_gateways,
            'gateway_market_share_percent': (total_domains_all_gateways/total_domains_dataset)*100
        }
    }
    
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/gateway_analysis_comprehensive.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Save CSV with gateway provider information
    df_export = df[[registrar_col, domain_count_col, rdap_url_col, 'Gateway_Provider']].copy()
    df_export.to_csv('/Users/yasinboelhouwer/rdap-registry-analysis/rdap_gateways_analysis.csv', index=False)
    
    print(f"\n✓ Detailed JSON results saved to: gateway_analysis_comprehensive.json")
    print(f"✓ CSV with gateway providers saved to: rdap_gateways_analysis.csv")

if __name__ == "__main__":
    analyze_rdap_gateways()