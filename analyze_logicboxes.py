import pandas as pd
import numpy as np

# Read the Excel file
df = pd.read_excel('data/Rdap lookups.xlsx')

# Get all LogicBoxes users
key_systems = df[df['Name'].str.contains('key-systems|key systems', case=False, na=False)]
logicboxes_direct = df[df['Name'].str.contains('logicboxes', case=False, na=False)]
bigrock = df[df['Name'].str.contains('bigrock', case=False, na=False)]
netistrar = df[df['Name'].str.contains('netistrar', case=False, na=False)]
rrpproxy_users = df[df['rdap_url'] == 'rdap.rrpproxy.net']
rdapserver_users = df[df['rdap_url'] == 'rdapserver.net']

all_logicboxes = pd.concat([key_systems, logicboxes_direct, bigrock, netistrar, rrpproxy_users, rdapserver_users]).drop_duplicates()

# Sort by domain count (descending) for top registrars
logicboxes_sorted = all_logicboxes.sort_values('Domain count', ascending=False, na_position='last')

print('=== TOP 15 LOGICBOXES REGISTRARS BY DOMAIN COUNT ===')
top_15 = logicboxes_sorted.head(15)
for i, (idx, row) in enumerate(top_15.iterrows(), 1):
    domain_count = row['Domain count'] if pd.notna(row['Domain count']) else 'N/A'
    category = row['Category'] if pd.notna(row['Category']) else 'N/A'
    print(f'{i:2}. {row["Name"]}')
    print(f'    RDAP URL: {row["rdap_url"]}')
    if domain_count != 'N/A':
        print(f'    Domain Count: {domain_count:,.0f} domains')
    else:
        print(f'    Domain Count: {domain_count}')
    print(f'    Category: {category}')
    print()

print('=== SUMMARY STATISTICS ===')
print(f'Total LogicBoxes Gateway Users: {len(all_logicboxes)}')
print(f'Users with domain count data: {len(all_logicboxes[pd.notna(all_logicboxes["Domain count"])])}')

# Calculate total domains
domains_with_data = all_logicboxes[pd.notna(all_logicboxes['Domain count'])]
total_domains = domains_with_data['Domain count'].sum()
print(f'Total domains under LogicBoxes gateway: {total_domains:,.0f}')

print(f'\nBreakdown by RDAP service:')
rdap_breakdown = all_logicboxes['rdap_url'].value_counts()
for rdap, count in rdap_breakdown.items():
    domains_for_this_rdap = all_logicboxes[all_logicboxes['rdap_url'] == rdap]['Domain count'].sum()
    if pd.notna(domains_for_this_rdap):
        print(f'  {rdap}: {count} registrars ({domains_for_this_rdap:,.0f} total domains)')
    else:
        print(f'  {rdap}: {count} registrars (domain data not available)')

print('\n=== RDAP URL PATTERNS FOR LOGICBOXES ===')
print('Key LogicBoxes RDAP patterns identified:')
print('1. rdapserver.net - Main LogicBoxes RDAP service')
print('2. rdap.rrpproxy.net - Key-Systems gateway service')
print('3. rdap.netistrar.com - Netistrar service')

print('\n=== GATEWAY CATEGORIES ===')
gateway_count = len(all_logicboxes[all_logicboxes['Category'] == 'GATEWAY'])
print(f'Registrars explicitly marked as GATEWAY: {gateway_count}')

# Show all gateway registrars
gateway_registrars = all_logicboxes[all_logicboxes['Category'] == 'GATEWAY']
for idx, row in gateway_registrars.iterrows():
    domain_count = row['Domain count'] if pd.notna(row['Domain count']) else 'N/A'
    print(f'  {row["Name"]} - {domain_count} domains')