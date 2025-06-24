#!/usr/bin/env python3
"""
Simple and Robust RDAP Gateway Analysis
"""
import pandas as pd
import json
from collections import Counter
from urllib.parse import urlparse

def identify_gateway_provider(rdap_url):
    """Identify gateway provider from RDAP URL patterns"""
    if pd.isna(rdap_url) or rdap_url.strip() == '':
        return None
    
    url_lower = str(rdap_url).lower().strip()
    
    # Define gateway patterns
    patterns = {
        'Tucows': [
            'tucows.com', 'opensrs.rdap.tucows.com', 'enom.rdap.tucows.com',
            'endurance.rdap.tucows.com', 'rdap.ascio.com', 'dreamhost.rdap.tucows.com',
            'domainpeople.rdap.tucows.com', 'epag.rdap.tucows.com', 'brs.rdap.tucows.com'
        ],
        'RRPProxy/CentralNic': [
            'rdap.rrpproxy.net', 'centralnic.com', 'hexonet.net'
        ],
        'InternetX': [
            'internetx.com', 'internetx.de', 'autodnslive'
        ],
        'LogicBoxes': [
            'logicboxes.com', 'resellerclub.com', 'bigrock.com', 
            'publicdomainregistry.com', 'stargate', 'resellerspanel'
        ],
        'Gransy': [
            'gransy.com', 'gransy.cz', 'subreg.cz', 'active24.com'
        ]
    }
    
    # Check patterns
    for provider, provider_patterns in patterns.items():
        for pattern in provider_patterns:
            if pattern in url_lower:
                return provider
    
    return None

def main():
    """Main analysis"""
    print("Reading RDAP Excel file...")
    df = pd.read_excel('/Users/yasinboelhouwer/rdap-registry-analysis/data/Rdap lookups.xlsx')
    
    # Clean domain count column
    df['Domain count'] = pd.to_numeric(df['Domain count'], errors='coerce').fillna(0)
    
    print(f"Total registrars: {len(df)}")
    print(f"Total domains: {df['Domain count'].sum():,.0f}")
    
    # Identify gateways
    df['Gateway'] = df['rdap_url'].apply(identify_gateway_provider)
    
    # Extract RDAP domains
    df['RDAP_Domain'] = df['rdap_url'].apply(
        lambda x: urlparse(str(x)).netloc.lower() if pd.notna(x) else None
    )
    
    print("\n" + "="*80)
    print("GATEWAY PROVIDER ANALYSIS")
    print("="*80)
    
    # Analyze known gateways
    gateway_results = {}
    total_gateway_domains = 0
    
    for provider in ['Tucows', 'RRPProxy/CentralNic', 'InternetX', 'LogicBoxes', 'Gransy']:
        provider_data = df[df['Gateway'] == provider]
        
        if len(provider_data) > 0:
            registrar_count = len(provider_data)
            domain_total = provider_data['Domain count'].sum()
            total_gateway_domains += domain_total
            
            gateway_results[provider] = {
                'registrars': registrar_count,
                'domains': int(domain_total)
            }
            
            print(f"\n{provider}:")
            print(f"  Registrars: {registrar_count}")
            print(f"  Total domains: {int(domain_total):,}")
            
            # Top registrars
            top_regs = provider_data.nlargest(3, 'Domain count')
            print("  Top registrars:")
            for _, reg in top_regs.iterrows():
                print(f"    - {reg['Name']}: {int(reg['Domain count']):,} domains")
            
            # RDAP URLs used
            unique_urls = provider_data['rdap_url'].unique()
            print(f"  RDAP URLs ({len(unique_urls)}): {', '.join(unique_urls[:3])}...")
    
    # Find potential gateways (domains used by multiple registrars)
    print(f"\n" + "="*80)
    print("POTENTIAL GATEWAY PROVIDERS")
    print("(RDAP domains used by 2+ registrars)")
    print("="*80)
    
    # Count registrars per RDAP domain
    rdap_domain_counts = df.groupby('RDAP_Domain').agg({
        'Name': 'count',
        'Domain count': 'sum'
    }).rename(columns={'Name': 'registrar_count'})
    
    # Filter for potential gateways
    potential_gateways = rdap_domain_counts[
        (rdap_domain_counts['registrar_count'] >= 2) & 
        (rdap_domain_counts.index.notna())
    ].sort_values('Domain count', ascending=False)
    
    print(f"\nTop potential gateway domains:")
    for domain, stats in potential_gateways.head(15).iterrows():
        # Check if already identified
        domain_data = df[df['RDAP_Domain'] == domain]
        is_known = not domain_data['Gateway'].isna().all()
        
        status = "KNOWN" if is_known else "POTENTIAL"
        provider = domain_data['Gateway'].dropna().iloc[0] if is_known else "Unknown"
        
        print(f"\n{domain} ({status})")
        if is_known:
            print(f"  Provider: {provider}")
        print(f"  Registrars: {int(stats['registrar_count'])}")
        print(f"  Domains: {int(stats['Domain count']):,}")
        
        # Sample registrars
        sample_regs = domain_data.nlargest(2, 'Domain count')
        for _, reg in sample_regs.iterrows():
            print(f"    - {reg['Name']}: {int(reg['Domain count']):,}")
    
    # Summary
    total_domains = df['Domain count'].sum()
    
    print(f"\n" + "="*80)
    print("MARKET SUMMARY")
    print("="*80)
    print(f"Total domains: {int(total_domains):,}")
    print(f"Gateway domains: {int(total_gateway_domains):,}")
    print(f"Gateway market share: {(total_gateway_domains/total_domains)*100:.2f}%")
    
    print(f"\nBy provider:")
    for provider, stats in sorted(gateway_results.items(), key=lambda x: x[1]['domains'], reverse=True):
        share = (stats['domains'] / total_domains) * 100
        print(f"  {provider}: {share:.2f}% ({stats['domains']:,} domains, {stats['registrars']} registrars)")
    
    # Top self-hosted registrars
    print(f"\n" + "="*80)
    print("TOP SELF-HOSTED REGISTRARS")
    print("="*80)
    
    self_hosted = df[df['Gateway'].isna()]
    top_self_hosted = self_hosted.nlargest(10, 'Domain count')
    
    for _, reg in top_self_hosted.iterrows():
        print(f"  {reg['Name']}: {int(reg['Domain count']):,} domains")
        print(f"    RDAP: {reg['rdap_url']}")
    
    # Save results
    results = {
        'summary': {
            'total_domains': int(total_domains),
            'gateway_domains': int(total_gateway_domains),
            'gateway_market_share': float((total_gateway_domains/total_domains)*100)
        },
        'gateway_providers': gateway_results,
        'potential_gateways': []
    }
    
    # Add potential gateways
    for domain, stats in potential_gateways.head(10).iterrows():
        domain_data = df[df['RDAP_Domain'] == domain]
        is_known = not domain_data['Gateway'].isna().all()
        
        if not is_known:  # Only unknown ones
            results['potential_gateways'].append({
                'domain': domain,
                'registrars': int(stats['registrar_count']),
                'domains': int(stats['Domain count'])
            })
    
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/gateway_analysis_final.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Results saved to: gateway_analysis_final.json")

if __name__ == "__main__":
    main()