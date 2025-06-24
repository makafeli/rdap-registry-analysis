#!/usr/bin/env python3
"""
COMPREHENSIVE RDAP GATEWAY ANALYSIS - FINAL REPORT
"""
import pandas as pd
import json
from collections import Counter
from urllib.parse import urlparse

def analyze_comprehensive_gateways():
    """Complete gateway analysis"""
    
    print("COMPREHENSIVE RDAP GATEWAY ANALYSIS")
    print("=" * 80)
    
    # Read data
    df = pd.read_excel('/Users/yasinboelhouwer/rdap-registry-analysis/data/Rdap lookups.xlsx')
    df['Domain count'] = pd.to_numeric(df['Domain count'], errors='coerce').fillna(0)
    
    total_registrars = len(df)
    total_domains = df['Domain count'].sum()
    
    print(f"Dataset Overview:")
    print(f"  Total registrars: {total_registrars:,}")
    print(f"  Total domains: {total_domains:,.0f}")
    print(f"  Unique RDAP URLs: {df['rdap_url'].nunique()}")
    
    # 1. IDENTIFY KNOWN GATEWAYS
    print(f"\n1. KNOWN GATEWAY PROVIDERS")
    print("-" * 50)
    
    # Define known gateway patterns based on the data
    gateway_patterns = {
        'Tucows': [
            'tucows.com', 'opensrs.rdap.tucows.com', 'enom.rdap.tucows.com',
            'endurance.rdap.tucows.com', 'rdap.ascio.com', 'dreamhost.rdap.tucows.com',
            'domainpeople.rdap.tucows.com', 'epag.rdap.tucows.com', 'brs.rdap.tucows.com',
            'eig.rdap.tucows.com', 'netregistry.rdap.tucows.com', 'tpp.rdap.tucows.com'
        ],
        'RRPProxy/CentralNic': [
            'rdap.rrpproxy.net'
        ],
        'NameBright (Potential Gateway)': [
            'rdap.namebright.com'
        ],
        'Network Solutions (Potential Gateway)': [
            'rdap.networksolutions.com'
        ],
        'RDAP Server (Potential Gateway)': [
            'rdapserver.net'
        ]
    }
    
    def identify_gateway(url):
        if pd.isna(url):
            return None
        url_str = str(url).lower()
        for provider, patterns in gateway_patterns.items():
            for pattern in patterns:
                if pattern in url_str:
                    return provider
        return None
    
    df['Gateway_Provider'] = df['rdap_url'].apply(identify_gateway)
    
    # Analyze each gateway provider
    gateway_stats = {}
    total_gateway_domains = 0
    
    for provider in gateway_patterns.keys():
        provider_df = df[df['Gateway_Provider'] == provider]
        
        if len(provider_df) > 0:
            registrar_count = len(provider_df)
            domain_total = provider_df['Domain count'].sum()
            total_gateway_domains += domain_total
            
            gateway_stats[provider] = {
                'registrars': registrar_count,
                'domains': int(domain_total),
                'market_share': (domain_total / total_domains) * 100
            }
            
            print(f"\n{provider}:")
            print(f"  Registrars: {registrar_count}")
            print(f"  Total domains: {int(domain_total):,}")
            print(f"  Market share: {(domain_total / total_domains) * 100:.2f}%")
            
            # Top registrars using this gateway
            top_regs = provider_df.nlargest(5, 'Domain count')
            print(f"  Top registrars:")
            for i, (_, reg) in enumerate(top_regs.iterrows(), 1):
                print(f"    {i}. {reg['Name']}: {int(reg['Domain count']):,} domains")
            
            # RDAP URLs used
            unique_urls = provider_df['rdap_url'].unique()
            print(f"  RDAP URLs ({len(unique_urls)}): {', '.join(unique_urls)}")
    
    # 2. ANALYZE ALL RDAP URL PATTERNS
    print(f"\n2. TOP RDAP DOMAINS BY USAGE")
    print("-" * 50)
    print("(All RDAP URLs ranked by number of registrars using them)")
    
    url_counts = df['rdap_url'].value_counts()
    
    for i, (url, count) in enumerate(url_counts.head(20).items(), 1):
        url_df = df[df['rdap_url'] == url]
        total_url_domains = url_df['Domain count'].sum()
        
        # Check if this is a known gateway
        is_gateway = not url_df['Gateway_Provider'].isna().all()
        gateway_type = url_df['Gateway_Provider'].dropna().iloc[0] if is_gateway else "Self-hosted"
        
        print(f"\n{i}. {url} ({'Gateway: ' + gateway_type if is_gateway else gateway_type})")
        print(f"   Registrars: {count}")
        print(f"   Total domains: {int(total_url_domains):,}")
        
        # Show sample registrars
        sample_regs = url_df.nlargest(2, 'Domain count')
        for _, reg in sample_regs.iterrows():
            print(f"     - {reg['Name']}: {int(reg['Domain count']):,} domains")
    
    # 3. MARKET ANALYSIS
    print(f"\n3. MARKET SHARE ANALYSIS")
    print("-" * 50)
    
    print(f"Total domains: {int(total_domains):,}")
    print(f"Gateway domains: {int(total_gateway_domains):,}")
    print(f"Gateway market share: {(total_gateway_domains / total_domains) * 100:.2f}%")
    print(f"Self-hosted domains: {int(total_domains - total_gateway_domains):,}")
    print(f"Self-hosted market share: {((total_domains - total_gateway_domains) / total_domains) * 100:.2f}%")
    
    print(f"\nGateway provider rankings:")
    sorted_gateways = sorted(gateway_stats.items(), key=lambda x: x[1]['domains'], reverse=True)
    for i, (provider, stats) in enumerate(sorted_gateways, 1):
        print(f"  {i}. {provider}:")
        print(f"     Market share: {stats['market_share']:.2f}%")
        print(f"     Domains: {stats['domains']:,}")
        print(f"     Registrars: {stats['registrars']}")
    
    # 4. TOP SELF-HOSTED REGISTRARS
    print(f"\n4. LARGEST SELF-HOSTED REGISTRARS")
    print("-" * 50)
    
    self_hosted = df[df['Gateway_Provider'].isna()]
    top_self_hosted = self_hosted.nlargest(15, 'Domain count')
    
    for i, (_, reg) in enumerate(top_self_hosted.iterrows(), 1):
        print(f"  {i}. {reg['Name']}: {int(reg['Domain count']):,} domains")
        print(f"     RDAP: {reg['rdap_url']}")
    
    # 5. ANALYSIS BY GATEWAY TYPE
    print(f"\n5. GATEWAY ANALYSIS SUMMARY")
    print("-" * 50)
    
    # Traditional known gateways
    traditional_gateways = ['Tucows', 'RRPProxy/CentralNic']
    traditional_domains = sum(gateway_stats.get(gw, {}).get('domains', 0) for gw in traditional_gateways)
    
    # Potential new gateways identified
    potential_gateways = ['NameBright (Potential Gateway)', 'Network Solutions (Potential Gateway)', 'RDAP Server (Potential Gateway)']
    potential_domains = sum(gateway_stats.get(gw, {}).get('domains', 0) for gw in potential_gateways)
    
    print(f"Traditional known gateways:")
    print(f"  Domains: {traditional_domains:,} ({(traditional_domains/total_domains)*100:.2f}%)")
    for gw in traditional_gateways:
        if gw in gateway_stats:
            stats = gateway_stats[gw]
            print(f"    {gw}: {stats['domains']:,} domains ({stats['registrars']} registrars)")
    
    print(f"\nPotential new gateways identified:")
    print(f"  Domains: {potential_domains:,} ({(potential_domains/total_domains)*100:.2f}%)")
    for gw in potential_gateways:
        if gw in gateway_stats:
            stats = gateway_stats[gw]
            print(f"    {gw}: {stats['domains']:,} domains ({stats['registrars']} registrars)")
    
    # 6. SAVE COMPREHENSIVE RESULTS
    results = {
        'analysis_date': pd.Timestamp.now().isoformat(),
        'dataset_summary': {
            'total_registrars': total_registrars,
            'total_domains': int(total_domains),
            'unique_rdap_urls': int(df['rdap_url'].nunique())
        },
        'gateway_analysis': {
            'total_gateway_domains': int(total_gateway_domains),
            'total_self_hosted_domains': int(total_domains - total_gateway_domains),
            'gateway_market_share_percent': float((total_gateway_domains / total_domains) * 100),
            'self_hosted_market_share_percent': float(((total_domains - total_gateway_domains) / total_domains) * 100)
        },
        'gateway_providers': {},
        'top_rdap_urls': [],
        'largest_self_hosted': []
    }
    
    # Add gateway provider details
    for provider, stats in gateway_stats.items():
        provider_df = df[df['Gateway_Provider'] == provider]
        results['gateway_providers'][provider] = {
            'registrar_count': stats['registrars'],
            'total_domains': stats['domains'],
            'market_share_percent': float(stats['market_share']),
            'rdap_urls': provider_df['rdap_url'].unique().tolist(),
            'top_registrars': [
                {
                    'name': reg['Name'],
                    'domains': int(reg['Domain count'])
                }
                for _, reg in provider_df.nlargest(5, 'Domain count').iterrows()
            ]
        }
    
    # Add top RDAP URLs
    for url, count in url_counts.head(15).items():
        url_df = df[df['rdap_url'] == url]
        total_url_domains = url_df['Domain count'].sum()
        
        results['top_rdap_urls'].append({
            'url': url,
            'registrar_count': int(count),
            'total_domains': int(total_url_domains),
            'is_gateway': not url_df['Gateway_Provider'].isna().all(),
            'gateway_provider': url_df['Gateway_Provider'].dropna().iloc[0] if not url_df['Gateway_Provider'].isna().all() else None
        })
    
    # Add largest self-hosted
    for _, reg in top_self_hosted.head(10).iterrows():
        results['largest_self_hosted'].append({
            'name': reg['Name'],
            'domains': int(reg['Domain count']),
            'rdap_url': reg['rdap_url']
        })
    
    # Save results
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/comprehensive_gateway_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save detailed CSV
    df_export = df[['Name', 'Domain count', 'rdap_url', 'Gateway_Provider']].copy()
    df_export.to_csv('/Users/yasinboelhouwer/rdap-registry-analysis/registrars_with_gateways.csv', index=False)
    
    print(f"\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"✓ Comprehensive results saved to: comprehensive_gateway_analysis.json")
    print(f"✓ Detailed registrar data saved to: registrars_with_gateways.csv")
    
    print(f"\nKEY FINDINGS:")
    print(f"- Total gateway market share: {(total_gateway_domains / total_domains) * 100:.1f}%")
    print(f"- Traditional gateways (Tucows, RRPProxy): {(traditional_domains/total_domains)*100:.1f}%")
    print(f"- Potential new gateways identified: {(potential_domains/total_domains)*100:.1f}%")
    print(f"- Largest gateway provider: {sorted_gateways[0][0]} ({sorted_gateways[0][1]['market_share']:.1f}%)")

if __name__ == "__main__":
    analyze_comprehensive_gateways()