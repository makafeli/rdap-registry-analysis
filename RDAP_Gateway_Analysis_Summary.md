# RDAP Gateway Analysis - Comprehensive Summary

## Executive Summary

This analysis examined 2,358 registrars managing 214.5 million domains to identify those using gateway solutions from known providers. The study revealed that **20.6% of all domains** are managed through gateway providers, significantly higher than initially expected.

## Key Findings

### Gateway Market Share: 20.6% (44.2M domains)
- **Traditional Known Gateways**: 10.5% (22.5M domains)
- **Newly Identified Gateways**: 10.1% (21.8M domains)
- **Self-Hosted RDAP**: 79.4% (170.3M domains)

## Gateway Provider Analysis

### 1. Tucows - Market Leader
- **Market Share**: 9.41% (20.2M domains)
- **Registrars**: 66 registrars using Tucows gateway
- **Top Registrars**:
  - Tucows Domains Inc.: 10.2M domains
  - eNom, LLC: 5.3M domains
  - Domain.com, LLC: 1.7M domains
  - Ascio Technologies: 935K domains
  - DreamHost, LLC: 725K domains
- **RDAP Infrastructure**: 21 unique RDAP URLs
- **Notable URLs**: opensrs.rdap.tucows.com, enom.rdap.tucows.com, rdap.ascio.com

### 2. RRPProxy/CentralNic
- **Market Share**: 1.06% (2.3M domains)
- **Registrars**: 8 registrars
- **Top Registrars**:
  - Key-Systems GmbH: 1.4M domains
  - Key-Systems, LLC: 465K domains
  - Moniker Online Services LLC: 381K domains
- **RDAP URL**: rdap.rrpproxy.net (single endpoint)

### 3. Newly Identified Gateway Providers

#### NameBright (Potential Gateway)
- **Market Share**: 2.54% (5.4M domains)
- **Registrars**: 1,252 registrars (highest count)
- **Pattern**: Many small registrars using rdap.namebright.com
- **Top Registrar**: TurnCommerce, Inc. DBA NameBright.com (837K domains)

#### Network Solutions (Potential Gateway)
- **Market Share**: 3.82% (8.2M domains)
- **Registrars**: 476 registrars
- **Top Registrar**: Network Solutions, LLC (6.9M domains)
- **RDAP URL**: rdap.networksolutions.com

#### RDAP Server (Potential Gateway)
- **Market Share**: 3.79% (8.1M domains)
- **Registrars**: 115 registrars
- **Top Registrar**: PDR Ltd. d/b/a PublicDomainRegistry.com (4.8M domains)
- **RDAP URL**: rdapserver.net

### 4. Missing Gateway Providers

The following providers were not found in the current dataset:
- **InternetX**: No registrars found using InternetX gateway patterns
- **LogicBoxes**: No clear LogicBoxes gateway patterns identified
- **Gransy**: No registrars found using Gransy gateway solutions

## Top Self-Hosted Registrars

The largest registrars managing their own RDAP infrastructure:

1. **GoDaddy.com, LLC**: 63.2M domains (rdap.godaddy.com)
2. **NameCheap, Inc.**: 10.3M domains (rdap.namecheap.com)
3. **Alibaba Cloud Computing (Beijing)**: 6.7M domains (whois.aliyun.com)
4. **Alibaba Cloud Computing Ltd.**: 5.4M domains (whois.aliyun.com)
5. **GMO Internet, Inc.**: 5.3M domains (rdap.gmo-onamae.com)
6. **Google LLC**: 4.9M domains (domainsrdap.googleapis.com)
7. **1&1 IONOS SE**: 4.9M domains (rdap.ionos.com)

## Technical Analysis

### RDAP URL Distribution
- **Total Unique RDAP URLs**: 349
- **Gateway URLs**: 24 (6.9%)
- **Self-Hosted URLs**: 325 (93.1%)

### Gateway Concentration
- **Top 5 Gateway Providers**: Control 20.6% of total market
- **Tucows Dominance**: Nearly half of all gateway domains
- **Long Tail**: Many small potential gateways serving niche markets

## Market Implications

### Traditional Gateway Market
- **Tucows**: Maintains strong market position with comprehensive service
- **RRPProxy/CentralNic**: Smaller but focused on specific registrar segments
- **Combined Traditional Share**: 10.5% of total market

### Emerging Gateway Patterns
- **NameBright**: Serves many small registrars (1,252 registrars, small average size)
- **Network Solutions**: Traditional registrar expanding into gateway services
- **RDAP Server**: Generic service serving diverse registrar types

### Self-Hosted Preference
- **79.4% of domains** remain on self-hosted RDAP infrastructure
- **Large registrars** (GoDaddy, NameCheap, Alibaba) prefer self-hosting
- **Technical capability** appears to be a key factor in self-hosting decision

## Conclusions

1. **Gateway adoption is higher than expected** at 20.6% market share
2. **Tucows dominates** the traditional gateway market with 9.4% total market share
3. **New gateway providers** have emerged, particularly serving smaller registrars
4. **LogicBoxes, InternetX, and Gransy** have limited presence in this dataset
5. **Self-hosting remains dominant** among large registrars
6. **Gateway fragmentation** is occurring with multiple smaller providers

## Recommendations for Further Analysis

1. **Verify potential gateways** through direct registrar contacts
2. **Analyze regional patterns** in gateway adoption
3. **Investigate technical capabilities** of newly identified gateways
4. **Monitor market evolution** as smaller registrars consolidate
5. **Assess service quality** differences between gateway providers

---

*Analysis completed: June 24, 2025*  
*Dataset: 2,358 registrars, 214.5M domains*  
*Methodology: RDAP URL pattern analysis*