#!/usr/bin/env python3
"""
Final Comprehensive RDAP Gateway Analysis
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
    
    # Comprehensive patterns for each provider
    patterns = {
        'Tucows': [
            'tucows.com',
            'opensrs.rdap.tucows.com',
            'enom.rdap.tucows.com',
            'endurance.rdap.tucows.com',
            'rdap.ascio.com',
            'dreamhost.rdap.tucows.com',
            'domainpeople.rdap.tucows.com',
            'epag.rdap.tucows.com',
            'webcentralgroup.rdap.tucows.com',
            'tpp.rdap.tucows.com',
            'netregistry.rdap.tucows.com',
            'easyspace.rdap.tucows.com',
            'paragon.rdap.tucows.com',
            'easydns.rdap.tucows.com',
            'papaki.rdap.tucows.com',
            'iregister.rdap.tucows.com',
            'registerca.rdap.tucows.com',
            'interplanet.rdap.tucows.com',
            'authenticweb.rdap.tucows.com',
            'eig.rdap.tucows.com',
            'peoplebrowsr.rdap.tucows.com',
            'brs.rdap.tucows.com'
        ],
        'InternetX': [
            'internetx.com',
            'internetx.de',
            'internetx.net',
            'autodnslive'
        ],
        'RRPProxy/CentralNic': [
            'rdap.rrpproxy.net',
            'centralnic.com',
            'centralnic.net',
            'rrpproxy.com',
            'key-systems.net',
            'hexonet.net'
        ],
        'LogicBoxes': [
            'logicboxes.com',
            'resellerclub.com',
            'bigrock.com',
            'publicdomainregistry.com',
            'stargate.com',
            'uniteddomains.com',
            'resellerspanel.com'
        ],
        'Gransy': [
            'gransy.com',
            'gransy.cz',
            'subreg.cz',
            'active24.com'
        ],
        'GoDaddy': [
            'rdap.secureserver.net'  # GoDaddy's RDAP service
        ],
        'NameCheap': [
            'rdap.namecheap.com'  # NameCheap's RDAP service
        ]
    }
    
    # Check for exact matches first
    for provider, patterns_list in patterns.items():
        for pattern in patterns_list:
            if pattern == url_lower or url_lower == f"https://{pattern}" or url_lower == f"http://{pattern}":
                return provider
            if pattern in url_lower:
                return provider
    
    return None

def find_potential_gateways(df):
    """Find potential gateway providers based on URL patterns"""
    
    # Extract domain from RDAP URLs
    df['rdap_domain'] = df['rdap_url'].apply(lambda x: urlparse(x.strip()).netloc.lower() if pd.notna(x) else None)
    
    # Count how many registrars use each domain
    domain_stats = df.groupby('rdap_domain').agg({
        'Name': 'count',
        'Domain count': 'sum'
    }).rename(columns={'Name': 'registrar_count'})
    
    # Filter for domains used by multiple registrars (potential gateways)
    potential_gateways = domain_stats[domain_stats['registrar_count'] > 1].copy()
    potential_gateways = potential_gateways.sort_values('Domain count', ascending=False)
    
    return potential_gateways

def main():
    """Main analysis function"""
    print("Reading RDAP lookups Excel file...")
    
    df = pd.read_excel('/Users/yasinboelhouwer/rdap-registry-analysis/data/Rdap lookups.xlsx')
    
    print(f"Total registrars: {len(df)}")
    print(f"Total domains: {df['Domain count'].sum():,}")
    print()
    
    # Add gateway provider identification
    df['gateway_provider'] = df['rdap_url'].apply(identify_gateway_provider)
    
    # Find all potential gateways
    potential_gateways = find_potential_gateways(df)
    
    print("="*100)
    print("COMPREHENSIVE RDAP GATEWAY ANALYSIS")
    print("="*100)
    
    # Analysis of known gateway providers
    print("\n1. KNOWN GATEWAY PROVIDERS:")
    print("-" * 50)
    
    gateway_stats = {}
    total_gateway_domains = 0
    
    for provider in ['Tucows', 'InternetX', 'RRPProxy/CentralNic', 'LogicBoxes', 'Gransy', 'GoDaddy', 'NameCheap']:
        provider_df = df[df['gateway_provider'] == provider]
        
        if len(provider_df) > 0:
            total_registrars = len(provider_df)
            total_domains = provider_df['Domain count'].sum()
            total_gateway_domains += total_domains
            
            gateway_stats[provider] = {
                'registrars': total_registrars,
                'domains': int(total_domains),
                'market_share': 0  # Will calculate after
            }
            
            print(f"\n{provider}:")
            print(f"  Registrars using this gateway: {total_registrars}")
            print(f"  Total domains: {int(total_domains):,}")
            
            # Show unique RDAP URLs for this provider
            unique_urls = provider_df['rdap_url'].unique()
            print(f"  RDAP URLs: {', '.join(unique_urls)}")
            
            # Top registrars
            top_registrars = provider_df.nlargest(3, 'Domain count')
            print(f"  Top registrars:")
            for _, reg in top_registrars.iterrows():
                domain_count = reg['Domain count']
                if pd.notna(domain_count):
                    print(f"    - {reg['Name']}: {int(domain_count):,} domains")
                else:
                    print(f"    - {reg['Name']}: N/A domains")
    
    # Analysis of potential unknown gateways
    print(f"\n2. POTENTIAL UNKNOWN GATEWAY PROVIDERS:")
    print("-" * 50)
    print("(RDAP domains used by multiple registrars)")
    
    unknown_gateways = []
    
    for domain, stats in potential_gateways.head(20).iterrows():
        if domain and stats['registrar_count'] > 1:
            # Check if this domain is already identified as a known gateway
            domain_df = df[df['rdap_domain'] == domain]
            is_known = not domain_df['gateway_provider'].isna().all()
            
            if not is_known:
                unknown_gateways.append({
                    'domain': domain,
                    'registrar_count': int(stats['registrar_count']),
                    'total_domains': int(stats['Domain count']),
                    'sample_registrars': domain_df.nlargest(3, 'Domain count')['Name'].tolist()
                })
                
                print(f"\n{domain}:")
                print(f"  Used by {int(stats['registrar_count'])} registrars")
                print(f"  Total domains: {int(stats['Domain count']):,}")
                
                # Show sample registrars
                sample_regs = domain_df.nlargest(3, 'Domain count')
                print(f"  Sample registrars:")
                for _, reg in sample_regs.iterrows():
                    domain_count = reg['Domain count']
                    if pd.notna(domain_count):
                        print(f"    - {reg['Name']}: {int(domain_count):,} domains")
                    else:
                        print(f"    - {reg['Name']}: N/A domains")
    
    # 3. Analysis of all RDAP domains
    print(f"\n3. ALL RDAP DOMAINS ANALYSIS:")
    print("-" * 50)
    print("(Top 20 RDAP domains by total domains managed)")
    
    for domain, stats in potential_gateways.head(20).iterrows():
        if domain:
            domain_df = df[df['rdap_domain'] == domain]
            is_known_gateway = not domain_df['gateway_provider'].isna().all()
            gateway_type = domain_df['gateway_provider'].dropna().iloc[0] if is_known_gateway else "Unknown"
            
            print(f"\n{domain} ({'Gateway: ' + gateway_type if is_known_gateway else 'Self-hosted'}):")
            print(f"  Registrars: {int(stats['registrar_count'])}")
            print(f"  Total domains: {int(stats['Domain count']):,}")
    
    # Summary calculations
    total_domains = df['Domain count'].sum()
    
    # Calculate market shares
    for provider in gateway_stats:
        gateway_stats[provider]['market_share'] = (gateway_stats[provider]['domains'] / total_domains) * 100
    
    print(f"\n4. MARKET SHARE SUMMARY:")
    print("-" * 50)
    print(f"Total domains in dataset: {int(total_domains):,}")
    print(f"Total domains using identified gateways: {total_gateway_domains:,}")
    print(f"Gateway market share: {(total_gateway_domains/total_domains)*100:.2f}%")
    
    print(f"\nMarket share by gateway provider:")
    for provider, stats in sorted(gateway_stats.items(), key=lambda x: x[1]['domains'], reverse=True):
        print(f"  {provider}: {stats['market_share']:.2f}% ({stats['domains']:,} domains, {stats['registrars']} registrars)")
    
    # Identify the largest self-hosted registrars
    self_hosted = df[df['gateway_provider'].isna()]
    print(f"\n5. LARGEST SELF-HOSTED REGISTRARS:")
    print("-" * 50)
    largest_self_hosted = self_hosted.nlargest(10, 'Domain count')
    for _, reg in largest_self_hosted.iterrows():
        domain_count = reg['Domain count']
        if pd.notna(domain_count):
            print(f"  {reg['Name']}: {int(domain_count):,} domains - {reg['rdap_url']}")
        else:
            print(f"  {reg['Name']}: N/A domains - {reg['rdap_url']}")
    
    # Save comprehensive results
    results = {
        'analysis_summary': {
            'total_registrars': len(df),
            'total_domains': int(total_domains),
            'gateway_domains': total_gateway_domains,
            'gateway_market_share_percent': (total_gateway_domains/total_domains)*100,
            'self_hosted_domains': int(total_domains - total_gateway_domains),
            'self_hosted_market_share_percent': ((total_domains - total_gateway_domains)/total_domains)*100
        },
        'known_gateway_providers': gateway_stats,
        'potential_unknown_gateways': unknown_gateways[:10],
        'top_rdap_domains': [],
        'largest_self_hosted': []
    }
    
    # Add top RDAP domains
    for domain, stats in potential_gateways.head(15).items():
        if domain:
            domain_df = df[df['rdap_domain'] == domain]
            is_known_gateway = not domain_df['gateway_provider'].isna().all()
            gateway_type = domain_df['gateway_provider'].dropna().iloc[0] if is_known_gateway else None
            
            results['top_rdap_domains'].append({
                'domain': domain,
                'registrar_count': int(stats['registrar_count']),
                'total_domains': int(stats['Domain count']),
                'is_gateway': is_known_gateway,
                'gateway_provider': gateway_type,
                'top_registrars': domain_df.nlargest(3, 'Domain count')[['Name', 'Domain count']].to_dict('records')
            })
    
    # Add largest self-hosted
    for _, reg in largest_self_hosted.head(10).iterrows():
        results['largest_self_hosted'].append({
            'name': reg['Name'],
            'domains': int(reg['Domain count']),
            'rdap_url': reg['rdap_url']
        })
    
    # Save results
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/final_gateway_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save a detailed CSV
    df_detailed = df[['Name', 'Domain count', 'rdap_url', 'gateway_provider', 'rdap_domain']].copy()
    df_detailed.to_csv('/Users/yasinboelhouwer/rdap-registry-analysis/detailed_gateway_analysis.csv', index=False)
    
    print(f"\n✓ Comprehensive results saved to: final_gateway_analysis.json")
    print(f"✓ Detailed CSV saved to: detailed_gateway_analysis.csv")

if __name__ == "__main__":
    main()