#!/usr/bin/env python3
import pandas as pd
from urllib.parse import urlparse

# Read data
df = pd.read_excel('data/Rdap lookups.xlsx')
df['Domain count'] = pd.to_numeric(df['Domain count'], errors='coerce').fillna(0)

# Extract RDAP domains
df['RDAP_Domain'] = df['rdap_url'].apply(
    lambda x: urlparse(str(x)).netloc.lower() if pd.notna(x) else None
)

# Find domains used by multiple registrars
rdap_counts = df.groupby('RDAP_Domain').agg({
    'Name': 'count',
    'Domain count': 'sum'
}).rename(columns={'Name': 'registrar_count'})

print('RDAP domains used by 2+ registrars (potential gateways):')
print('=' * 60)

multi_reg_domains = rdap_counts[rdap_counts['registrar_count'] >= 2].sort_values('Domain count', ascending=False)

for domain, stats in multi_reg_domains.head(25).iterrows():
    if domain and domain != '':
        print(f'{domain}:')
        print(f'  Registrars: {int(stats["registrar_count"])}')
        print(f'  Total domains: {int(stats["Domain count"]):,}')
        
        # Show registrars using this domain
        domain_regs = df[df['RDAP_Domain'] == domain].nlargest(3, 'Domain count')
        for _, reg in domain_regs.iterrows():
            print(f'    - {reg["Name"]}: {int(reg["Domain count"]):,} domains')
        print()