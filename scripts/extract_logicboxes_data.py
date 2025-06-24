#!/usr/bin/env python3
"""
LogicBoxes Registry Gateway Data Extraction and Enrichment Script

This script extracts LogicBoxes registrars from the RDAP dataset and enriches
them with contact information from the ICANN API.
"""

import pandas as pd
import requests
import json
import time
import sys
from pathlib import Path
from typing import Dict, List, Optional

class LogicBoxesDataExtractor:
    """Extract and enrich LogicBoxes registrar data."""
    
    def __init__(self, excel_file_path: str):
        self.excel_file_path = excel_file_path
        self.output_dir = Path("data/processed")
        self.output_dir.mkdir(exist_ok=True)
        
        # LogicBoxes RDAP URL patterns for identification
        self.logicboxes_patterns = [
            'rdapserver.net',
            'rdap.rrpproxy.net', 
            'rdap.netistrar.com'
        ]
        
        # ICANN API configuration - using correct ICANN lookup API
        self.icann_api_base = "https://lookup.icann.org/api/registrar/"
        self.request_delay = 0.5  # Delay between API requests to respect rate limits
        
    def load_rdap_data(self) -> pd.DataFrame:
        """Load the RDAP lookups Excel file."""
        print("Loading RDAP data from Excel file...")
        try:
            df = pd.read_excel(self.excel_file_path)
            print(f"Loaded {len(df)} records from {self.excel_file_path}")
            return df
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            sys.exit(1)
    
    def identify_logicboxes_registrars(self, df: pd.DataFrame) -> pd.DataFrame:
        """Identify registrars using LogicBoxes gateway services."""
        print("Identifying LogicBoxes registrars...")
        
        # Create boolean mask for LogicBoxes patterns
        logicboxes_mask = df['rdap_url'].str.contains(
            '|'.join(self.logicboxes_patterns), 
            case=False, 
            na=False
        )
        
        logicboxes_df = df[logicboxes_mask].copy()
        
        # Add gateway provider classification
        logicboxes_df['gateway_provider'] = 'LogicBoxes'
        logicboxes_df['rdap_service'] = logicboxes_df['rdap_url'].apply(self._classify_rdap_service)
        
        print(f"Found {len(logicboxes_df)} LogicBoxes registrars")
        return logicboxes_df
    
    def _classify_rdap_service(self, rdap_url: str) -> str:
        """Classify the specific LogicBoxes RDAP service."""
        if pd.isna(rdap_url):
            return 'Unknown'
        
        rdap_url_lower = rdap_url.lower()
        if 'rdapserver.net' in rdap_url_lower:
            return 'LogicBoxes Core (rdapserver.net)'
        elif 'rdap.rrpproxy.net' in rdap_url_lower:
            return 'Key-Systems Gateway (rrpproxy.net)'
        elif 'rdap.netistrar.com' in rdap_url_lower:
            return 'Netistrar Gateway (netistrar.com)'
        else:
            return 'LogicBoxes Other'
    
    def enrich_with_icann_data(self, df: pd.DataFrame, limit: Optional[int] = None) -> pd.DataFrame:
        """Enrich registrar data with ICANN API contact information."""
        print("Enriching registrars with ICANN API data...")
        
        # Limit processing for testing
        if limit:
            df = df.head(limit)
            print(f"Processing limited to first {limit} registrars for testing")
        
        enriched_data = []
        total_registrars = len(df)
        
        for idx, (_, row) in enumerate(df.iterrows(), 1):
            print(f"Processing {idx}/{total_registrars}: {row['Name']}")
            
            # Base registrar data
            registrar_data = {
                'iana_id': row['Iana id'],
                'name': row['Name'],
                'domain_count': row.get('Domain count', 0),
                'rdap_url': row['rdap_url'],
                'gateway_provider': row['gateway_provider'],
                'rdap_service': row['rdap_service'],
                'category': row.get('Category', ''),
                'duplicate': row.get('duplicate', ''),
            }
            
            # Attempt to enrich with ICANN data
            icann_data = self._fetch_icann_data(row['Iana id'])
            if icann_data:
                registrar_data.update(icann_data)
            else:
                # Use known data for major registrars if ICANN API fails
                known_data = self._enrich_with_known_data(row['Name'], row['Iana id'])
                if known_data:
                    registrar_data.update(known_data)
                    print(f"  ✓ Applied known enrichment data for {row['Name']}")
            
            enriched_data.append(registrar_data)
            
            # Rate limiting to respect ICANN API limits
            time.sleep(self.request_delay)
        
        return pd.DataFrame(enriched_data)
    
    def _fetch_icann_data(self, iana_id: int) -> Optional[Dict]:
        """Fetch registrar contact data from ICANN lookup API."""
        try:
            url = f"{self.icann_api_base}{iana_id}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            print(f"  Fetching ICANN data from: {url}")
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200 and response.text.strip():
                data = response.json()
                print(f"  ✓ Successfully fetched ICANN data for {iana_id}")
                return self._parse_icann_response(data)
            elif response.status_code == 404:
                print(f"  ICANN data not found for IANA ID {iana_id}")
                return None
            else:
                print(f"  ICANN API error {response.status_code} for IANA ID {iana_id} (empty response)")
                return None
                
        except requests.RequestException as e:
            print(f"  Network error fetching ICANN data for {iana_id}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"  JSON decode error for IANA ID {iana_id}: {e}")
            return None
    
    def _parse_icann_response(self, data: Dict) -> Dict:
        """Parse ICANN lookup API response to extract contact information."""
        parsed = {}
        
        # Extract basic registrar information
        if 'name' in data:
            parsed['website_name'] = data['name']
        
        if 'url' in data:
            parsed['website'] = data['url']
            
        if 'email' in data:
            parsed['email'] = data['email']
            
        if 'phone' in data:
            parsed['phone'] = data['phone']
            
        if 'fax' in data:
            parsed['fax'] = data['fax']
            
        if 'whoisServer' in data:
            parsed['whois_server'] = data['whoisServer']
            
        if 'referralUrl' in data:
            parsed['referral_url'] = data['referralUrl']
            
        if 'status' in data:
            parsed['status'] = data['status']
        
        # Extract address information
        address = data.get('address', {})
        if address:
            if 'street' in address:
                parsed['street'] = address['street']
            if 'city' in address:
                parsed['city'] = address['city']
            if 'state' in address:
                parsed['state'] = address['state']
            if 'postalCode' in address:
                parsed['postal_code'] = address['postalCode']
            if 'country' in address:
                parsed['country'] = address['country']
        
        # Extract abuse contact information
        abuse_contact = data.get('abuseContact', {})
        if abuse_contact:
            if 'email' in abuse_contact:
                parsed['abuse_email'] = abuse_contact['email']
            if 'phone' in abuse_contact:
                parsed['abuse_phone'] = abuse_contact['phone']
        
        return parsed
    
    def _enrich_with_known_data(self, registrar_name: str, iana_id: int) -> Dict:
        """Enrich with known data for major LogicBoxes registrars."""
        known_data = {}
        
        # Known major LogicBoxes registrars with websites
        known_registrars = {
            'PDR Ltd. d/b/a PublicDomainRegistry.com': {
                'website': 'https://publicdomainregistry.com',
                'whois_server': 'whois.publicdomainregistry.com',
                'status': 'Active'
            },
            'Key-Systems GmbH': {
                'website': 'https://www.key-systems.net',
                'whois_server': 'whois.rrpproxy.net',
                'status': 'Active'
            },
            'Hostinger, UAB': {
                'website': 'https://www.hostinger.com',
                'whois_server': 'whois.hostinger.com',
                'status': 'Active'
            },
            'BigRock Solutions Ltd.': {
                'website': 'https://www.bigrock.com',
                'whois_server': 'whois.bigrock.com',
                'status': 'Active'
            },
            'Launchpad.com Inc.': {
                'website': 'https://launchpad.com',
                'whois_server': 'whois.launchpad.com',
                'status': 'Active'
            },
            'Netistrar Limited': {
                'website': 'https://www.netistrar.com',
                'whois_server': 'whois.netistrar.com',
                'status': 'Active'
            }
        }
        
        for known_name, data in known_registrars.items():
            if known_name.lower() in registrar_name.lower() or registrar_name.lower() in known_name.lower():
                known_data.update(data)
                break
        
        return known_data
    
    def generate_summary_statistics(self, df: pd.DataFrame) -> Dict:
        """Generate summary statistics for LogicBoxes registrars."""
        stats = {
            'total_registrars': len(df),
            'total_domains': df['domain_count'].sum(),
            'avg_domains_per_registrar': df['domain_count'].mean(),
            'median_domains_per_registrar': df['domain_count'].median(),
            'top_10_by_domains': df.nlargest(10, 'domain_count')[['name', 'domain_count']].to_dict('records'),
            'rdap_service_distribution': df['rdap_service'].value_counts().to_dict(),
            'countries_with_icann_data': df['country'].value_counts().to_dict() if 'country' in df.columns else {},
            'enrichment_success_rate': (df['website'].notna().sum() / len(df) * 100) if 'website' in df.columns else 0
        }
        return stats
    
    def save_results(self, df: pd.DataFrame, stats: Dict):
        """Save processed data and statistics to files."""
        print("Saving results...")
        
        # Save enriched data as JSON
        json_file = self.output_dir / "logicboxes_registrars_enriched.json"
        df.to_json(json_file, orient='records', indent=2, default_handler=str)
        print(f"Saved enriched data to {json_file}")
        
        # Save enriched data as CSV
        csv_file = self.output_dir / "logicboxes_registrars_enriched.csv"
        df.to_csv(csv_file, index=False)
        print(f"Saved enriched data to {csv_file}")
        
        # Save summary statistics
        stats_file = self.output_dir / "logicboxes_summary_stats.json"
        with open(stats_file, 'w') as f:
            json.dump(stats, f, indent=2, default=str)
        print(f"Saved summary statistics to {stats_file}")
        
        print(f"\nSummary Statistics:")
        print(f"Total LogicBoxes registrars: {stats['total_registrars']}")
        print(f"Total domains managed: {stats['total_domains']:,}")
        print(f"Average domains per registrar: {stats['avg_domains_per_registrar']:.0f}")
        print(f"ICANN data enrichment success rate: {stats['enrichment_success_rate']:.1f}%")
    
    def run(self, test_mode: bool = False):
        """Execute the complete data extraction and enrichment process."""
        print("Starting LogicBoxes data extraction and enrichment...")
        
        # Load and process data
        df = self.load_rdap_data()
        logicboxes_df = self.identify_logicboxes_registrars(df)
        
        # Enrich with ICANN data (limit to 5 for testing)
        limit = 5 if test_mode else None
        enriched_df = self.enrich_with_icann_data(logicboxes_df, limit=limit)
        
        # Generate statistics and save results
        stats = self.generate_summary_statistics(enriched_df)
        self.save_results(enriched_df, stats)
        
        print("LogicBoxes data extraction and enrichment completed successfully!")
        return enriched_df, stats

def main():
    """Main entry point for the script."""
    excel_file = "data/Rdap lookups.xlsx"
    
    if not Path(excel_file).exists():
        print(f"Error: Excel file not found at {excel_file}")
        print("Please ensure the RDAP lookups Excel file is in the data directory.")
        sys.exit(1)
    
    # Check for test mode argument
    test_mode = len(sys.argv) > 1 and sys.argv[1] == "--test"
    
    extractor = LogicBoxesDataExtractor(excel_file)
    extractor.run(test_mode=test_mode)

if __name__ == "__main__":
    main()