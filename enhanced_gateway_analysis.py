#!/usr/bin/env python3
"""
Enhanced RDAP Gateway Analysis - Looking for all gateway providers
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
    
    # Expanded patterns for each provider
    patterns = {
        'Tucows': [
            'tucows.com',
            'opensrs.net',
            'opensrs.com',
            'hover.com',
            'enom.com',
            'ascio.com',
            'epag.com',
            'dreamhost.com',
            'domainpeople.com',
            'netregistry.com',
            'easyspace.com',
            'easydns.com',
            'papaki.com',
            'iregister.com',
            'interplanet.com',
            'authenticweb.com',
            'peoplebrowsr.com'
        ],
        'InternetX': [
            'internetx.com',
            'internetx.de',
            'internetx.net',
            'autodnslive'
        ],
        'RRPProxy/CentralNic': [
            'rrpproxy.net',
            'centralnic.com',
            'centralnic.net',
            'rrpproxy.com',
            'key-systems.net',
            'rrp-proxy.net',
            'hexonet.net'
        ],
        'LogicBoxes': [
            'logicboxes.com',
            'resellerclub.com',
            'bigrock.com',
            'publicdomainregistry.com',
            'stargate.com',
            'uniteddomains.com',
            'mitsu.com',
            'resellerspanel.com',
            'endurance.com',
            'bluehost.com',
            'hostgator.com'
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

def analyze_comprehensive_gateways():
    """Comprehensive gateway analysis"""
    print("Reading RDAP lookups Excel file...")
    
    df = pd.read_excel('/Users/yasinboelhouwer/rdap-registry-analysis/data/Rdap lookups.xlsx')
    
    # Clean data
    df = df.dropna(subset=['rdap_url'])
    df = df[df['rdap_url'].str.strip() != '']
    
    print(f"Total rows with RDAP URLs: {len(df)}")
    
    # Extract domains from RDAP URLs
    df['rdap_domain'] = df['rdap_url'].apply(lambda x: urlparse(x).netloc.lower())
    
    # Add gateway provider column
    df['gateway_provider'] = df['rdap_url'].apply(identify_gateway_provider)
    
    # Find potential gateways (domains used by multiple registrars)
    domain_stats = df.groupby('rdap_domain').agg({
        'Name': 'count',
        'Domain count': 'sum'
    }).rename(columns={'Name': 'registrar_count'})
    
    # Filter for domains used by 3+ registrars
    potential_gateways = domain_stats[domain_stats['registrar_count'] >= 3].copy()
    potential_gateways = potential_gateways.sort_values('Domain count', ascending=False)
    
    print("\n" + "="*80)
    print("POTENTIAL GATEWAY PROVIDERS")
    print("(Domains used by 3+ registrars)")
    print("="*80)
    
    for domain, row in potential_gateways.head(30).iterrows():
        # Check if already identified
        domain_rows = df[df['rdap_domain'] == domain]
        is_known = not domain_rows['gateway_provider'].isna().all()
        
        status = "KNOWN" if is_known else "UNKNOWN"
        known_provider = domain_rows['gateway_provider'].dropna().iloc[0] if is_known else "N/A"
        
        print(f"\n{domain} ({status})")
        if is_known:
            print(f"  Provider: {known_provider}")
        print(f"  Registrars: {row['registrar_count']}")
        print(f"  Total domains: {int(row['Domain count']):,}")
        
        # Show top registrars
        top_regs = domain_rows.nlargest(3, 'Domain count')
        print(f"  Top registrars:")
        for _, reg in top_regs.iterrows():
            print(f"    - {reg['Name']}: {int(reg['Domain count']):,} domains")
    
    # Analyze known gateway providers
    print("\n" + "="*80)
    print("KNOWN GATEWAY PROVIDER ANALYSIS")
    print("="*80)
    
    gateway_summary = {}
    
    for provider in ['Tucows', 'InternetX', 'RRPProxy/CentralNic', 'LogicBoxes', 'Gransy']:
        provider_df = df[df['gateway_provider'] == provider]
        
        if len(provider_df) > 0:
            total_registrars = len(provider_df)
            total_domains = provider_df['Domain count'].sum()
            unique_domains = provider_df['rdap_domain'].nunique()
            
            gateway_summary[provider] = {
                'registrars': total_registrars,
                'domains': int(total_domains),
                'unique_domains': unique_domains
            }
            
            print(f"\n{provider}:")
            print(f"  Registrars: {total_registrars}")
            print(f"  Total domains: {int(total_domains):,}")
            print(f"  Unique RDAP domains: {unique_domains}")
            
            # Show top registrars
            top_regs = provider_df.nlargest(5, 'Domain count')
            print(f"  Top registrars:")
            for _, reg in top_regs.iterrows():
                print(f"    - {reg['Name']}: {int(reg['Domain count']):,} domains")
    
    # Look for other patterns that might indicate gateways
    print("\n" + "="*80)
    print("ADDITIONAL GATEWAY PATTERN ANALYSIS")
    print("="*80)
    
    # Look for common subdomain patterns
    rdap_patterns = Counter()
    for url in df['rdap_url'].unique():
        try:
            parsed = urlparse(url)
            domain_parts = parsed.netloc.split('.')
            if len(domain_parts) >= 2:
                base_domain = '.'.join(domain_parts[-2:])
                rdap_patterns[base_domain] += 1
        except:
            continue
    
    print("\nMost common base domains in RDAP URLs:")
    for domain, count in rdap_patterns.most_common(20):
        if count > 2:
            domain_df = df[df['rdap_url'].str.contains(domain, na=False)]
            total_domains = domain_df['Domain count'].sum()
            print(f"  {domain}: {count} URLs, {int(total_domains):,} domains")
    
    # Summary
    total_domains_all = df['Domain count'].sum()
    total_domains_gateways = sum(stats['domains'] for stats in gateway_summary.values())
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print(f"Total domains with RDAP URLs: {int(total_domains_all):,}")
    print(f"Total domains using identified gateways: {total_domains_gateways:,}")
    print(f"Gateway market share: {(total_domains_gateways/total_domains_all)*100:.2f}%")
    
    print("\nMarket share by provider:")
    for provider, stats in sorted(gateway_summary.items(), key=lambda x: x[1]['domains'], reverse=True):
        share = (stats['domains'] / total_domains_all) * 100
        print(f"  {provider}: {share:.2f}% ({stats['domains']:,} domains, {stats['registrars']} registrars)")
    
    # Save enhanced results
    results = {
        'known_gateway_providers': gateway_summary,
        'potential_gateways': [],
        'rdap_domain_patterns': dict(rdap_patterns.most_common(50)),
        'summary': {
            'total_domains_with_rdap': int(total_domains_all),
            'total_domains_known_gateways': total_domains_gateways,
            'gateway_market_share_percent': (total_domains_gateways/total_domains_all)*100
        }
    }
    
    # Add potential gateways to results
    for domain, row in potential_gateways.head(20).iterrows():
        domain_rows = df[df['rdap_domain'] == domain]
        is_known = not domain_rows['gateway_provider'].isna().all()
        
        if not is_known:  # Only add unknown potential gateways
            results['potential_gateways'].append({
                'domain': domain,
                'registrar_count': int(row['registrar_count']),
                'total_domains': int(row['Domain count']),
                'sample_registrars': domain_rows.nlargest(3, 'Domain count')['Name'].tolist()
            })
    
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/enhanced_gateway_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Enhanced results saved to: enhanced_gateway_analysis.json")

if __name__ == "__main__":
    analyze_comprehensive_gateways()