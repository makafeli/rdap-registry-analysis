# RDAP Registry Analysis Report

## Executive Summary

This analysis examines 2,358 domain registrars and their RDAP (Registration Data Access Protocol) service providers, with a special focus on the Registry Gateway service provided by LogicBoxes.

### Key Findings

1. **Market Concentration**: Two providers (Namebright and Network Solutions) serve 73.3% of all registrars
2. **Registry Gateway Success**: 115 registrars use LogicBoxes' Registry Gateway, managing 8.1M domains
3. **Efficiency Model**: Registry Gateway averages 70,707 domains per registrar vs. industry average of ~4,000
4. **No Duplicates**: Every registrar has a unique name, confirming individual ICANN accreditations

## Registry Gateway (LogicBoxes) Analysis

### Overview
- **Service Provider**: LogicBoxes
- **RDAP URL**: rdapserver.net
- **Total Registrars**: 115 (4.9% of all registrars)
- **Total Domains**: 8,131,328 (6.3% of all tracked domains)
- **Average Domains/Registrar**: 70,707

### Top Registry Gateway Users

| Rank | Registrar | IANA ID | Domains | % of RG Domains |
|------|-----------|---------|---------|-----------------|
| 1 | PDR Ltd. (PublicDomainRegistry) | 303 | 4,845,099 | 59.6% |
| 2 | Launchpad.com Inc. | 955 | 729,662 | 9.0% |
| 3 | Hostinger, UAB | 1636 | 590,290 | 7.3% |
| 4 | BigRock Solutions Ltd. | 1495 | 276,454 | 3.4% |
| 5 | IHS Telekom, Inc. | 1091 | 160,821 | 2.0% |

*Top 5 registrars account for 81.3% of all Registry Gateway domains*

### Business Model

Registry Gateway allows registrars to:
- Maintain their own ICANN accreditations
- Use shared technical infrastructure for RDAP/WHOIS
- Benefit from automated ICANN compliance (WDRP, ERRP, Registrant Verification)
- Reduce operational overhead while maintaining independence

## Market Distribution

### RDAP Service Models

1. **Direct Service** (53.1%)
   - Single registrar using their own RDAP infrastructure
   - Example: rdap.namebright.com

2. **Shared Platform** (20.2%)
   - Multiple subsidiaries under one provider
   - Example: rdap.networksolutions.com

3. **Registry Gateway** (4.9%)
   - Independent registrars sharing infrastructure
   - Example: rdapserver.net (LogicBoxes)

4. **Small Providers** (21.8%)
   - 362+ smaller independent RDAP implementations

### Domain Distribution by Provider

| Provider | Domains | Registrars | Avg Domains/Registrar |
|----------|---------|------------|----------------------|
| GoDaddy | 63.2M | 1 | 63,168,934 |
| Aliyun | 12.9M | 4 | 3,232,956 |
| Namecheap | 10.3M | 3 | 3,441,321 |
| Registry Gateway | 8.1M | 115 | 70,707 |
| Network Solutions | 8.2M | 476 | 17,195 |
| Namebright | 5.4M | 1,252 | 4,346 |

## Technical Implementation

### RDAP URLs Structure
- Total unique RDAP URLs: 382
- Format patterns:
  - rdap.{company}.com (most common)
  - {company}.rdap.{provider}.com
  - whois.{company}.com
  - Custom implementations

### Data Enrichment Process

To enrich registrar data with contact information:

1. **ICANN API**: https://lookup.icann.org/api/registrar/{IANA_ID}
2. **Available Data**:
   - Website URL
   - Email contacts
   - Phone numbers
   - Abuse contacts
   - Physical address
   - WHOIS server
   - Accreditation status

3. **Bulk Sources**:
   - ICANN weekly CSV export
   - Registry operator databases
   - Direct provider APIs

## Conclusions

1. **Market Efficiency**: Registry Gateway demonstrates that shared infrastructure models can be highly efficient, managing more domains per registrar than traditional models.

2. **Concentration Concerns**: The top 6 RDAP providers control 85% of all domains, indicating significant market concentration.

3. **Innovation Opportunity**: The success of Registry Gateway suggests room for similar shared-service models in the domain industry.

4. **Compliance Benefits**: Shared infrastructure providers like LogicBoxes handle ICANN compliance requirements, reducing burden on individual registrars.

## Recommendations

1. **For New Registrars**: Consider shared infrastructure models like Registry Gateway to reduce operational overhead while maintaining ICANN accreditation.

2. **For Existing Registrars**: Evaluate whether current RDAP infrastructure costs justify independent operation vs. shared services.

3. **For Industry**: Monitor concentration trends and ensure competitive market dynamics are maintained.

4. **For Researchers**: Use ICANN's bulk data exports for comprehensive registrar analysis rather than individual API calls.

---

*Report generated: January 2024*  
*Data source: RDAP lookups Excel file with 2,358 registrars*  
*Analysis tools: React dashboard, Python/JavaScript scripts*
