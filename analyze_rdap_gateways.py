#!/usr/bin/env python3
"""
Analyze RDAP lookups to identify registrars using gateway solutions
"""
import csv
import json
from collections import defaultdict, Counter
from urllib.parse import urlparse
import re

def read_excel_as_csv():
    """Read Excel file by converting to CSV first"""
    import subprocess
    import os
    
    # Convert Excel to CSV using Python
    script = '''
import openpyxl
import csv
import sys

wb = openpyxl.load_workbook('data/Rdap lookups.xlsx', read_only=True)
sheet = wb.active

with open('data/rdap_lookups.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    for row in sheet.iter_rows(values_only=True):
        writer.writerow(row)
wb.close()
print("CSV conversion complete")
'''
    
    # Try to convert using system Python
    try:
        result = subprocess.run(['/usr/bin/python3', '-c', script], 
                              capture_output=True, text=True, cwd='/Users/yasinboelhouwer/rdap-registry-analysis')
        if result.returncode != 0:
            print(f"Error: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error converting Excel to CSV: {e}")
        return None
    
    # Read the CSV file
    data = []
    try:
        with open('/Users/yasinboelhouwer/rdap-registry-analysis/data/rdap_lookups.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return data
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None

def identify_gateway_provider(rdap_url):
    """Identify gateway provider from RDAP URL patterns"""
    if not rdap_url or rdap_url.strip() == '':
        return None
    
    url_lower = rdap_url.lower()
    
    # Define patterns for each provider
    patterns = {
        'Tucows': [
            'tucows.com',
            'opensrs.net',
            'opensrs.com',
            'hover.com',
            'enom.com'  # Tucows acquired eNom
        ],
        'InternetX': [
            'internetx.com',
            'internetx.de',
            'autodnslive'
        ],
        'RRPProxy/CentralNic': [
            'rrpproxy.net',
            'centralnic.com',
            'centralnic.net',
            'rrpproxy.com',
            'key-systems.net'  # Part of CentralNic
        ],
        'LogicBoxes': [
            'logicboxes.com',
            'resellerclub.com',
            'bigrock.com',
            'publicdomainregistry.com',
            'stargate.com'
        ],
        'Gransy': [
            'gransy.com',
            'gransy.cz'
        ]
    }
    
    # Check for known patterns
    for provider, patterns_list in patterns.items():
        for pattern in patterns_list:
            if pattern in url_lower:
                return provider
    
    # Additional pattern matching for common gateway indicators
    # Look for repeated domains that might indicate gateway providers
    try:
        parsed = urlparse(rdap_url)
        domain = parsed.netloc.lower()
        
        # Check for other potential gateway patterns
        if 'whois' in domain and 'registrar' in domain:
            return 'Potential Gateway'
        if 'rdap-service' in domain or 'rdap.service' in domain:
            return 'Potential Gateway'
        if domain.count('.') > 2:  # Subdomain patterns like rdap.provider.service.com
            return 'Potential Gateway'
            
    except:
        pass
    
    return None

def analyze_rdap_data():
    """Main analysis function"""
    print("Reading RDAP lookups data...")
    data = read_excel_as_csv()
    
    if not data:
        print("Failed to read data")
        return
    
    print(f"Total rows: {len(data)}")
    print(f"Columns: {list(data[0].keys()) if data else 'No data'}")
    print()
    
    # Find the relevant columns
    registrar_col = None
    rdap_url_col = None
    domain_count_col = None
    
    for key in data[0].keys():
        if 'registrar' in key.lower() and 'name' in key.lower():
            registrar_col = key
        elif 'rdap' in key.lower() and 'url' in key.lower():
            rdap_url_col = key
        elif 'domain' in key.lower() and ('count' in key.lower() or 'total' in key.lower()):
            domain_count_col = key
    
    print(f"Using columns:")
    print(f"  Registrar: {registrar_col}")
    print(f"  RDAP URL: {rdap_url_col}")
    print(f"  Domain Count: {domain_count_col}")
    print()
    
    if not rdap_url_col:
        print("Error: Could not find RDAP URL column")
        return
    
    # Analyze gateway usage
    gateway_stats = defaultdict(lambda: {
        'registrars': [],
        'total_domains': 0,
        'unique_urls': set()
    })
    
    # Track all RDAP URLs for pattern analysis
    url_counter = Counter()
    domain_counter = Counter()
    
    for row in data:
        rdap_url = row.get(rdap_url_col, '').strip()
        registrar_name = row.get(registrar_col, 'Unknown').strip() if registrar_col else 'Unknown'
        
        try:
            domain_count = int(float(row.get(domain_count_col, 0))) if domain_count_col else 0
        except:
            domain_count = 0
        
        if rdap_url:
            # Count URL occurrences
            url_counter[rdap_url] += 1
            
            # Extract domain from URL
            try:
                parsed = urlparse(rdap_url)
                domain = parsed.netloc.lower()
                if domain:
                    domain_counter[domain] += 1
            except:
                pass
            
            # Identify gateway provider
            provider = identify_gateway_provider(rdap_url)
            if provider:
                gateway_stats[provider]['registrars'].append({
                    'name': registrar_name,
                    'domain_count': domain_count,
                    'rdap_url': rdap_url
                })
                gateway_stats[provider]['total_domains'] += domain_count
                gateway_stats[provider]['unique_urls'].add(rdap_url)
    
    # Display results
    print("=" * 80)
    print("GATEWAY PROVIDER ANALYSIS")
    print("=" * 80)
    
    total_domains_all_gateways = 0
    
    for provider in ['Tucows', 'InternetX', 'RRPProxy/CentralNic', 'LogicBoxes', 'Gransy']:
        if provider in gateway_stats:
            stats = gateway_stats[provider]
            total_domains_all_gateways += stats['total_domains']
            
            print(f"\n{provider}:")
            print(f"  Total Registrars: {len(stats['registrars'])}")
            print(f"  Total Domains: {stats['total_domains']:,}")
            print(f"  Unique RDAP URLs: {len(stats['unique_urls'])}")
            
            # Top registrars by domain count
            top_registrars = sorted(stats['registrars'], 
                                  key=lambda x: x['domain_count'], 
                                  reverse=True)[:5]
            
            print(f"  Top 5 Registrars:")
            for reg in top_registrars:
                print(f"    - {reg['name']}: {reg['domain_count']:,} domains")
                print(f"      RDAP: {reg['rdap_url']}")
    
    # Check for potential unknown gateways
    print("\n" + "=" * 80)
    print("POTENTIAL UNKNOWN GATEWAY PROVIDERS")
    print("(Based on repeated RDAP domains)")
    print("=" * 80)
    
    # Find domains used by multiple registrars
    potential_gateways = []
    for domain, count in domain_counter.most_common(20):
        if count > 2 and domain:  # Used by more than 2 registrars
            # Check if it's not already identified
            is_known = False
            for provider in gateway_stats:
                if provider != 'Potential Gateway':
                    for reg in gateway_stats[provider]['registrars']:
                        if domain in reg['rdap_url'].lower():
                            is_known = True
                            break
                    if is_known:
                        break
            
            if not is_known:
                potential_gateways.append((domain, count))
    
    for domain, count in potential_gateways[:10]:
        print(f"  {domain}: used by {count} registrars")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total domains using identified gateways: {total_domains_all_gateways:,}")
    
    # Calculate market share
    total_domains_dataset = sum(int(float(row.get(domain_count_col, 0))) 
                               for row in data 
                               if domain_count_col and row.get(domain_count_col))
    
    if total_domains_dataset > 0:
        print(f"Total domains in dataset: {total_domains_dataset:,}")
        print(f"Gateway market share: {(total_domains_all_gateways/total_domains_dataset)*100:.2f}%")
        
        print("\nMarket share by provider:")
        for provider in ['Tucows', 'InternetX', 'RRPProxy/CentralNic', 'LogicBoxes', 'Gransy']:
            if provider in gateway_stats:
                share = (gateway_stats[provider]['total_domains'] / total_domains_dataset) * 100
                print(f"  {provider}: {share:.2f}%")
    
    # Save detailed results
    results = {
        'gateway_providers': {},
        'potential_gateways': potential_gateways[:20],
        'summary': {
            'total_domains_gateways': total_domains_all_gateways,
            'total_domains_dataset': total_domains_dataset,
            'gateway_market_share': (total_domains_all_gateways/total_domains_dataset)*100 if total_domains_dataset > 0 else 0
        }
    }
    
    for provider, stats in gateway_stats.items():
        results['gateway_providers'][provider] = {
            'registrar_count': len(stats['registrars']),
            'total_domains': stats['total_domains'],
            'market_share': (stats['total_domains'] / total_domains_dataset) * 100 if total_domains_dataset > 0 else 0,
            'unique_urls': list(stats['unique_urls']),
            'top_registrars': [
                {
                    'name': reg['name'],
                    'domains': reg['domain_count'],
                    'rdap_url': reg['rdap_url']
                }
                for reg in sorted(stats['registrars'], 
                                key=lambda x: x['domain_count'], 
                                reverse=True)[:10]
            ]
        }
    
    with open('/Users/yasinboelhouwer/rdap-registry-analysis/gateway_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: gateway_analysis_results.json")

if __name__ == "__main__":
    analyze_rdap_data()