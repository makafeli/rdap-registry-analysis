# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a React-based data analysis dashboard for analyzing RDAP (Registration Data Access Protocol) registry data. The project focuses on understanding domain registrar patterns and Registry Gateway (LogicBoxes) services across 2,358 domain registrars.

## Tech Stack

- **Frontend**: React 18.2 with JavaScript (JSX)
- **Styling**: Tailwind CSS
- **Data Visualization**: Recharts
- **Data Processing**: Python (pandas), Node.js, Bash
- **Build Tool**: Create React App

## Common Commands

```bash
# Development
npm start          # Start React development server (port 3000)
npm build          # Build for production
npm test           # Run tests

# Data Processing
npm run analyze    # Run Node.js analysis script
npm run enrich     # Run Python enrichment script

# Manual script execution (from scripts directory)
python enrich_registrars.py    # Enrich registrar data via ICANN API
./enrich_registrars.sh         # Alternative bash enrichment
node analyze_rdap.js           # Analyze RDAP patterns
```

## Architecture Overview

The project consists of three main layers:

### 1. Frontend Layer (React)
- **App.jsx**: Main application container with tab navigation
- **RDAPAnalysisDashboard.jsx**: Core dashboard component that visualizes RDAP data patterns, market concentration, and registrar distribution
- **RegistrarEnrichmentTool.jsx**: Interactive tool for enriching registrar data with ICANN contact information

### 2. Data Processing Layer
The project uses multiple languages for different processing needs:
- **Python (enrich_registrars.py)**: Heavy data processing using pandas, handles ICANN API integration
- **Bash (enrich_registrars.sh)**: Lightweight alternative using curl/jq for quick enrichment
- **Node.js (analyze_rdap.js)**: JavaScript-based analysis for RDAP patterns

### 3. Data Flow
1. Input: Excel file with RDAP lookup data (`data/Rdap lookups.xlsx`)
2. Enrichment: ICANN API provides registrar contact details
3. Processing: Scripts analyze patterns and market concentration
4. Visualization: React dashboard displays insights

## Data Source Details

### Primary Dataset: `data/Rdap lookups.xlsx`
The core dataset contains **2,358 registry records** with **30 columns** of IANA registry and RDAP infrastructure data:

#### Key Columns:
- **Iana id**: Unique IANA registry identifier (2,358 records)
- **Name**: Registry/registrar organization name
- **Domain count**: Number of domains managed (available for 98% of records)
- **Category**: Service type breakdown:
  - DROPCATCH: 1,803 records (76.5%) - Domain drop-catching services
  - REGISTRAR: 4 records - Direct registrars
  - GATEWAY: 7 records - Registry gateways
  - SUBSIDIARY: 4 records - Subsidiary services
- **rdap_url**: RDAP endpoint URLs (349 unique URLs across all records)

#### Network Infrastructure Data:
- **IPv4/IPv6 addresses**: Server infrastructure details (15% have IPv4, 6% have IPv6)
- **ASN information**: Autonomous System Numbers with geographic distribution
- **RDAP network details**: Registration data with country codes (US: 101, CN: 53, DE: 43)

#### Data Insights:
- **Top RDAP Providers**: NameBright (1,252 records), Network Solutions (476 records)
- **Geographic Focus**: Primarily US-based with global presence
- **Network Coverage**: Rich metadata available for ~15% of records with full infrastructure details

## Key Data Insights

The dashboard analyzes:
- Registry Gateway (LogicBoxes) serves 115 registrars managing 8.1M domains
- Top 3 RDAP providers serve ~78% of all registrars
- Market concentration analysis across different RDAP service providers

## Development Guidelines

### React Components
- Components use functional style with hooks
- Tailwind CSS for styling (className attributes)
- Recharts for data visualization
- No TypeScript - pure JavaScript/JSX

### Data Processing Scripts
- Python scripts require: `pip install pandas requests openpyxl`
- Bash scripts require: curl, jq
- Node.js scripts use built-in modules only

### File Organization
```
/
├── src/
│   ├── App.jsx                     # Main app container
│   ├── RDAPAnalysisDashboard.jsx   # Dashboard component
│   └── RegistrarEnrichmentTool.jsx # Enrichment tool
├── scripts/
│   ├── enrich_registrars.py        # Python enrichment
│   ├── enrich_registrars.sh        # Bash enrichment
│   └── analyze_rdap.js             # Node.js analysis
└── public/                         # Static assets
```

## API Integration

### ICANN API
- Endpoint: `https://rdap.iana.org/autnum/{registrar_id}`
- Used for enriching registrar data with contact information
- Rate limiting considerations in scripts

## Important Notes

1. This is a client-side only application - no backend server
2. Data files are processed locally
3. ICANN API calls are made directly from scripts
4. The project analyzes static snapshots of RDAP data