# RDAP Registry Analysis Project

This project analyzes RDAP (Registration Data Access Protocol) lookups data, focusing on Registry Gateway (LogicBoxes) service patterns and registrar distribution.

## Project Structure

```
rdap-registry-analysis/
├── src/                        # React components for visualization
│   ├── components/
│   │   ├── RDAPAnalysisDashboard.jsx
│   │   └── RegistrarEnrichmentTool.jsx
│   ├── App.jsx
│   └── index.js
├── scripts/                    # Data processing scripts
│   ├── enrich_registrars.sh   # Bash script for ICANN API
│   ├── enrich_registrars.py   # Python script for bulk processing
│   └── analyze_rdap.js        # JavaScript analysis script
├── data/                       # Data files and templates
│   ├── registry_gateway_template.csv
│   └── sample_enriched_data.json
├── docs/                       # Documentation
│   └── analysis_report.md
├── package.json               # React project configuration
└── README.md                  # This file
```

## Key Findings

### Registry Gateway (LogicBoxes)
- **115 registrars** use rdapserver.net (Registry Gateway by LogicBoxes)
- Manages **8.1 million domains** (6.3% of all tracked domains)
- Average: **70,707 domains per registrar**
- Top user: PDR Ltd. with 4.8M domains

### Market Distribution
- Total registrars analyzed: **2,358**
- Unique RDAP URLs: **382**
- Market leaders:
  - rdap.namebright.com: 53.1% of registrars
  - rdap.networksolutions.com: 20.2%
  - rdapserver.net: 4.9%

## Getting Started

### 1. Install Dependencies
```bash
npm install
```

### 2. Run the React Dashboard
```bash
npm start
```

### 3. Enrich Registrar Data

#### Using Bash Script:
```bash
cd scripts
chmod +x enrich_registrars.sh
./enrich_registrars.sh
```

#### Using Python:
```bash
cd scripts
pip install -r requirements.txt
python enrich_registrars.py
```

## Data Sources

1. **Original Excel File**: `Rdap lookups.xlsx`
   - Contains IANA IDs, registrar names, RDAP URLs
   - Domain count data in second sheet

2. **ICANN API**: For enriching with contact information
   - Endpoint: `https://lookup.icann.org/api/registrar/{IANA_ID}`

3. **ICANN Bulk Export**: Weekly CSV with all registrar data
   - URL: https://www.icann.org/registrar-reports/accredited-list.html

## Tools Included

### 1. RDAP Analysis Dashboard
Interactive React dashboard showing:
- Market distribution pie charts
- Domain distribution analysis
- Registry Gateway user list with search
- Key insights and patterns

### 2. Registrar Enrichment Tool
React component for:
- Selecting registrars to enrich
- Generating bash/Python scripts
- Preview of enriched data format

### 3. Data Processing Scripts
- **enrich_registrars.sh**: Bash script using curl and jq
- **enrich_registrars.py**: Python script with pandas
- **analyze_rdap.js**: Node.js script for data analysis

## Usage with Claude Code CLI

To continue development with Claude Code CLI:

```bash
cd /Users/yasinboelhouwer/rdap-registry-analysis
claude-code .
```

Then you can:
- Enhance the React visualizations
- Add more data analysis features
- Integrate with additional data sources
- Build an API backend
- Add database storage

## Next Steps

1. **Data Enrichment**: Run the enrichment scripts to add contact information
2. **Database Integration**: Store enriched data in a database
3. **API Development**: Create REST API for data access
4. **Advanced Analytics**: Add trend analysis and predictions
5. **Export Features**: Generate reports in various formats

## License

This project is for analysis purposes. Please respect ICANN's terms of service when accessing their APIs.
