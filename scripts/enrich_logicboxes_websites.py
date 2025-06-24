#!/usr/bin/env python3
"""
Enrich LogicBoxes registrars with website information based on name patterns
and known registrar data.
"""

import json
import re
from pathlib import Path
from typing import Dict, Optional, List

class LogicBoxesWebsiteEnricher:
    """Enrich LogicBoxes registrar data with website information."""
    
    def __init__(self):
        self.data_dir = Path("data/processed")
        self.known_websites = self._get_known_websites()
    
    def _get_known_websites(self) -> Dict[int, Dict[str, str]]:
        """Return known website mappings for LogicBoxes registrars."""
        return {
            # Top registrars by domain count
            1345: {"website": "https://www.key-systems.net", "notes": "Part of Key-Systems group"},
            228: {"website": "https://www.moniker.com", "notes": "Domain marketplace"},
            1091: {"website": "https://www.ihstelekom.com", "notes": "Turkish hosting provider"},
            1005: {"website": "https://www.netearth.com", "notes": "Web hosting and domains"},
            609: {"website": "https://www.sav.com", "notes": "Domain marketplace"},
            1586: {"website": "https://www.matbao.net", "notes": "Vietnamese hosting provider"},
            3806: {"website": "https://beget.com", "notes": "Russian hosting provider"},
            1600: {"website": "https://www.tecnocratica.net", "notes": "Spanish hosting provider"},
            1432: {"website": "https://www.alpinedomains.com", "notes": "Domain registrar"},
            1534: {"website": "https://www.aerotek.com.tr", "notes": "Turkish hosting provider"},
            819: {"website": "https://www.reg2c.com", "notes": "Domain registrar"},
            1483: {"website": "https://www.neubox.com", "notes": "Mexican hosting provider"},
            1710: {"website": "https://www.nhanhoa.com", "notes": "Vietnamese hosting provider"},
            1112: {"website": "https://www.imena.ua", "notes": "Ukrainian domain registrar"},
            1913: {"website": "https://www.dotserve.com", "notes": "Domain services"},
            1895: {"website": "https://www.namespro.ca", "notes": "Canadian registrar"},
            1082: {"website": "https://www.register4less.com", "notes": "Budget domain registrar"},
            1660: {"website": "https://www.domainshype.com", "notes": "Domain registrar"},
            1086: {"website": "https://www.marcaria.com", "notes": "Trademark and domain services"},
            3812: {"website": "https://www.innovadeus.com", "notes": "Indian domain registrar"},
            820: {"website": "https://www.nuxit.com", "notes": "French hosting provider"},
            818: {"website": "https://www.interdominios.com", "notes": "Spanish domain registrar"},
            1741: {"website": "https://www.shinjiru.com", "notes": "Malaysian hosting provider"},
            1503: {"website": "https://www.ardhosting.com", "notes": "Indonesian hosting provider"},
            123: {"website": "https://www.spirittel.com", "notes": "Communications provider"},
            837: {"website": "https://www.freeparking.co.nz", "notes": "New Zealand hosting provider"},
            938: {"website": "https://www.webhostingcanada.org", "notes": "Canadian hosting provider"},
            1533: {"website": "https://www.gooddomains.in", "notes": "Indian domain registrar"},
            2906: {"website": "https://www.hostingireland.ie", "notes": "Irish hosting provider"},
            898: {"website": "https://www.alantron.com", "notes": "Domain services"},
            
            # Additional known registrars
            1714: {"website": "https://www.active24.com", "notes": "European hosting provider"},
            1429: {"website": "https://www.atak-domain.com", "notes": "Turkish domain registrar"},
            3867: {"website": "https://www.bigdomainshop.com", "notes": "Domain marketplace"},
            1540: {"website": "https://www.brandsight.com", "notes": "Brand protection services"},
            493: {"website": "https://www.cheapdomains.com.au", "notes": "Australian domain registrar"},
            3793: {"website": "https://www.cnobin.com", "notes": "Chinese domain services"},
            1453: {"website": "https://www.cp.pt", "notes": "Portuguese hosting provider"},
            3847: {"website": "https://www.cyberinfoways.com", "notes": "Indian IT services"},
            1684: {"website": "https://www.domainbox.com", "notes": "UK domain reseller"},
            1671: {"website": "https://www.domaining.com", "notes": "Domain services"},
            3810: {"website": "https://www.domainking.ng", "notes": "Nigerian domain registrar"},
            3856: {"website": "https://www.domainscience.com", "notes": "Domain technology"},
            1452: {"website": "https://www.doruk.net.tr", "notes": "Turkish telecom provider"},
            1665: {"website": "https://www.easyspace.com", "notes": "UK hosting provider"},
            1089: {"website": "https://www.enetica.com.au", "notes": "Australian hosting provider"},
            1683: {"website": "https://www.entorno.com", "notes": "Digital services"},
            1615: {"website": "https://www.evoxt.com", "notes": "Indonesian hosting provider"},
            1424: {"website": "https://www.fastdot.com.au", "notes": "Australian hosting provider"},
            808: {"website": "https://www.hostingmax.ua", "notes": "Ukrainian hosting provider"},
            1434: {"website": "https://www.ind.br", "notes": "Brazilian domain registrar"},
            1703: {"website": "https://www.interdominio.com", "notes": "Latin American registrar"},
            1605: {"website": "https://www.iwantmyname.com", "notes": "Domain marketplace"},
            1637: {"website": "https://www.ipmirror.com", "notes": "Brand protection"},
            1680: {"website": "https://www.maff.com", "notes": "Brand protection services"},
            3855: {"website": "https://www.mijndomein.nl", "notes": "Dutch domain registrar"},
            1542: {"website": "https://www.mijninternetoplossing.nl", "notes": "Dutch hosting provider"},
            3795: {"website": "https://www.namesrs.com", "notes": "Domain services"},
            1682: {"website": "https://www.netistrar.com", "notes": "UK domain technology"},
            1706: {"website": "https://www.paragonnames.com", "notes": "Domain services"},
            1097: {"website": "https://www.point.cm", "notes": "Cameroon ccTLD operator"},
            1590: {"website": "https://www.srsplus.com", "notes": "Domain reseller platform"},
            3869: {"website": "https://www.subregsrlo.com", "notes": "Czech domain registrar"},
            1487: {"website": "https://www.totalregistrations.com", "notes": "UK domain registrar"},
            1668: {"website": "https://www.tpp.com.tr", "notes": "Turkish hosting provider"},
            1654: {"website": "https://www.webservices.ca", "notes": "Canadian hosting provider"},
            1652: {"website": "https://www.webworldireland.com", "notes": "Irish hosting provider"},
            1083: {"website": "https://web-solutions.eu", "notes": "European hosting provider"},
            1709: {"website": "https://www.yourdomainprovider.com", "notes": "Domain services"},
            1517: {"website": "https://www.z.com", "notes": "Japanese domain registrar"}
        }
    
    def _extract_potential_website(self, name: str) -> Optional[str]:
        """Extract potential website from registrar name using patterns."""
        # Clean the name
        name_clean = name.strip()
        
        # Pattern 1: Name contains actual domain (e.g., "Sav.com, LLC")
        domain_match = re.search(r'([a-zA-Z0-9\-]+\.(com|net|org|io|co|ca|uk|au|in|ua|eu|asia|biz|info|tv|me))', name_clean)
        if domain_match:
            domain = domain_match.group(1).lower()
            return f"https://www.{domain}"
        
        # Pattern 2: d/b/a (doing business as)
        dba_match = re.search(r'd/b/a\s+([^,]+)', name_clean)
        if dba_match:
            dba_name = dba_match.group(1).strip()
            # Remove common suffixes
            dba_name = re.sub(r'\s*(Communications?|Registrars?|Domains?|Internet|Online|Services?|Solutions?|Technology|Tech)\s*$', '', dba_name, flags=re.I)
            if dba_name:
                domain_name = re.sub(r'[^a-zA-Z0-9]', '', dba_name).lower()
                return f"https://www.{domain_name}.com"
        
        # Pattern 3: Extract main company name before legal suffix
        legal_suffixes = r'(LLC|Inc\.?|Ltd\.?|S\.?A\.?|Pvt\.?|Sdn\.?\s*Bhd\.?|Corporation|Corp\.?|Limited|GmbH|AS|SRL|S\.?L\.?|B\.?V\.?|AG|Pty\.?|PLC|LLP|LP)'
        company_match = re.match(rf'^(.*?)\s*{legal_suffixes}', name_clean, re.I)
        if company_match:
            company_name = company_match.group(1).strip()
            # Remove common words
            company_name = re.sub(r'\b(The|Domain|Registrar|Registry|Internet|Web|Online|Digital|Tech|Technology|Solutions?|Services?|Software|Company)\b', '', company_name, flags=re.I)
            company_name = re.sub(r'[^a-zA-Z0-9]+', '', company_name)
            if company_name and len(company_name) > 2:
                return f"https://www.{company_name.lower()}.com"
        
        return None
    
    def enrich_registrar_data(self, input_file: str = "logicboxes_registrars_enriched.json"):
        """Enrich registrar data with website information."""
        input_path = self.data_dir / input_file
        
        print(f"Loading data from {input_path}...")
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        enriched_count = 0
        pattern_matches = 0
        
        for registrar in data:
            if registrar.get('website'):
                continue  # Skip if already has website
            
            iana_id = registrar.get('iana_id')
            
            # Check known websites first
            if iana_id in self.known_websites:
                registrar['website'] = self.known_websites[iana_id]['website']
                registrar['website_source'] = 'known_mapping'
                registrar['notes'] = self.known_websites[iana_id].get('notes', '')
                enriched_count += 1
            else:
                # Try to extract from name
                potential_website = self._extract_potential_website(registrar.get('name', ''))
                if potential_website:
                    registrar['website'] = potential_website
                    registrar['website_source'] = 'name_pattern'
                    registrar['website_confidence'] = 'medium'
                    pattern_matches += 1
        
        # Save enriched data
        output_file = self.data_dir / "logicboxes_registrars_enriched_v2.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also save as CSV for easier viewing
        csv_file = self.data_dir / "logicboxes_registrars_enriched_v2.csv"
        self._save_as_csv(data, csv_file)
        
        # Generate summary
        total_registrars = len(data)
        with_website = sum(1 for r in data if r.get('website'))
        
        print(f"\nEnrichment Summary:")
        print(f"Total registrars: {total_registrars}")
        print(f"Registrars with websites: {with_website} ({with_website/total_registrars*100:.1f}%)")
        print(f"Newly enriched (known mappings): {enriched_count}")
        print(f"Newly enriched (name patterns): {pattern_matches}")
        print(f"\nEnriched data saved to:")
        print(f"  - {output_file}")
        print(f"  - {csv_file}")
        
        # Create a summary of top registrars for easy reference
        self._create_top_registrars_summary(data)
    
    def _create_top_registrars_summary(self, data: List[Dict]):
        """Create a summary of top registrars with their websites."""
        # Sort by domain count
        sorted_data = sorted([d for d in data if d.get('domain_count')], 
                           key=lambda x: x['domain_count'], reverse=True)
        
        summary = {
            "summary": {
                "total_registrars": len(data),
                "registrars_with_websites": sum(1 for r in data if r.get('website')),
                "total_domains": sum(r.get('domain_count', 0) for r in data if r.get('domain_count'))
            },
            "top_30_registrars": []
        }
        
        for reg in sorted_data[:30]:
            summary["top_30_registrars"].append({
                "rank": len(summary["top_30_registrars"]) + 1,
                "iana_id": reg.get('iana_id'),
                "name": reg.get('name'),
                "domains": reg.get('domain_count'),
                "website": reg.get('website', 'Not found'),
                "website_source": reg.get('website_source', 'N/A'),
                "notes": reg.get('notes', '')
            })
        
        summary_file = self.data_dir / "logicboxes_top30_summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"\nTop 30 registrars summary saved to: {summary_file}")
    
    def _save_as_csv(self, data: List[Dict], csv_file: Path):
        """Save data as CSV file without pandas."""
        import csv
        
        if not data:
            return
        
        # Get all unique keys from the data
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        
        # Sort keys for consistent column order
        fieldnames = sorted(all_keys)
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

def main():
    """Main entry point."""
    enricher = LogicBoxesWebsiteEnricher()
    enricher.enrich_registrar_data()

if __name__ == "__main__":
    main()