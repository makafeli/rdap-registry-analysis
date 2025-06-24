# Claude Code CLI Instructions

## Quick Start

1. **Navigate to the project folder:**
   ```bash
   cd /users/yasinboelhouwer/rdap-registry-analysis
   ```

2. **Make scripts executable:**
   ```bash
   chmod +x setup.sh
   chmod +x scripts/enrich_registrars.sh
   ```

3. **Run setup:**
   ```bash
   ./setup.sh
   ```

4. **Start Claude Code CLI:**
   ```bash
   claude-code .
   ```

## Project Commands

Once in Claude Code CLI, you can:

### React Dashboard
- `npm start` - Start the development server
- `npm run build` - Build for production

### Data Analysis
- `node scripts/analyze_rdap.js "../Rdap lookups.xlsx"` - Analyze the Excel file

### Data Enrichment
- `cd scripts && ./enrich_registrars.sh` - Run bash enrichment
- `cd scripts && python enrich_registrars.py` - Run Python enrichment

## Key Features to Explore

1. **Enhance Dashboard**
   - Add more visualizations
   - Implement data filtering
   - Add export functionality

2. **API Integration**
   - Build REST API endpoints
   - Add real-time ICANN data fetching
   - Implement caching

3. **Database Integration**
   - Add PostgreSQL/MongoDB support
   - Create data models
   - Build CRUD operations

4. **Advanced Analytics**
   - Trend analysis over time
   - Predictive modeling
   - Market concentration metrics

## File Locations

- **React Components**: `src/components/`
- **Scripts**: `scripts/`
- **Data Files**: `data/`
- **Documentation**: `docs/`
