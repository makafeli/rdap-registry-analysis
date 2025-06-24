# RDAP Registry Analysis Dashboard

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/makafeli/rdap-registry-analysis)

Comprehensive analysis of RDAP (Registration Data Access Protocol) adoption patterns and gateway solutions across domain registrars. Interactive dashboard showcasing gateway provider market insights and registrar ecosystem analysis.

## 🚀 Live Demo

Deploy your own instance instantly with Vercel: **[Deploy Now →](https://vercel.com/new/clone?repository-url=https://github.com/makafeli/rdap-registry-analysis)**

## 📊 Project Overview

This project analyzes RDAP endpoints and identifies gateway solution providers, focusing on the core infrastructure providers that serve multiple independent registrars through shared RDAP services.

### Key Insights
- **3 Core Gateway Providers**: LogicBoxes, Tucows, RRPProxy/CentralNic
- **Market Coverage**: 14.3% of domains (30.6M) use gateway solutions  
- **Registrar Efficiency**: 189 gateway registrars vs 2,169 self-hosted
- **Market Leaders**: Tucows (66 registrars), LogicBoxes (115 registrars), RRPProxy/CentralNic (8 registrars)

## ✨ Key Features

- **🔒 Password Protection**: Secure login screen with configurable authentication
- **🔍 Comprehensive Gateway Analysis**: Interactive dashboard with market share insights
- **📋 Registry Gateway Users**: Searchable table of all 189 gateway registrars
- **📈 Data Visualizations**: Charts showing provider distribution and domain metrics
- **💾 Export Functionality**: CSV export for all data tables
- **🎨 Professional UI**: Clean, responsive design with Tailwind CSS
- **⚡ Performance Optimized**: Fast loading with optimized build
- **🛡️ Session Management**: Automatic logout after configurable session duration

## 🛠️ Quick Start

### Prerequisites
- Node.js 16+ and npm/yarn
- Git

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/makafeli/rdap-registry-analysis.git
   cd rdap-registry-analysis
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm start
   ```

4. **Configure authentication (optional)**:
   ```bash
   # Copy environment template
   cp .env.example .env.local
   
   # Edit .env.local to set your password
   REACT_APP_DASHBOARD_PASSWORD=your-secure-password
   ```

5. **Build for production**:
   ```bash
   npm run build
   ```

### Deploy to Vercel

#### Option 1: One-Click Deploy
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/makafeli/rdap-registry-analysis)

#### Option 2: Vercel CLI
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy from your local directory
vercel

# Or deploy from GitHub
vercel --prod
```

#### Option 3: GitHub Integration
1. Connect your GitHub account to Vercel
2. Import this repository
3. **Set environment variables** in Vercel dashboard:
   - `REACT_APP_DASHBOARD_PASSWORD`: Your secure password
   - `REACT_APP_SESSION_DURATION_HOURS`: Session duration (default: 24)
4. Deploy automatically with each push

## 🔒 Authentication

### Default Credentials
- **Password**: `rdap2024`
- **Session Duration**: 24 hours

### Custom Configuration
Set environment variables to customize authentication:

```bash
# In .env.local (local development)
REACT_APP_DASHBOARD_PASSWORD=your-secure-password
REACT_APP_SESSION_DURATION_HOURS=8

# In Vercel dashboard (production)
# Add environment variables under Settings > Environment Variables
```

### Security Features
- **Client-side authentication** with localStorage session management
- **Auto-logout** after configurable session duration
- **Password masking** with show/hide toggle
- **Session persistence** across browser refreshes
- **Secure logout** with confirmation prompt

## 📁 Project Structure

```
rdap-registry-analysis/
├── src/                           # React application source
│   ├── components/               # Dashboard components
│   │   ├── GatewayComparison.jsx # Main analysis dashboard
│   │   └── RegistryGatewayUsers.jsx # Registrar table
│   └── App.jsx                   # Main application
├── public/                       # Static assets
│   └── data/processed/          # JSON data files for dashboard
├── data/                        # Raw and processed datasets
├── scripts/                     # Analysis and enrichment tools
├── docs/                        # Documentation and reports
├── vercel.json                  # Vercel deployment configuration
└── package.json                 # Dependencies and scripts
```

## 📊 Dashboard Components

### 1. RDAP Analysis Dashboard
- **Market Share Visualization**: Pie charts and bar graphs
- **Key Metrics**: Domain counts, registrar statistics, gateway adoption
- **Provider Breakdown**: Detailed analysis of each gateway provider
- **Export Options**: CSV download for analysis data

### 2. Registry Gateway Users
- **Interactive Table**: All 189 gateway registrars with sorting/filtering
- **Search Functionality**: Find registrars by name, IANA ID, or provider
- **Provider Filtering**: Filter by LogicBoxes, Tucows, or RRPProxy/CentralNic
- **Domain Range Filters**: Small, medium, large, enterprise categories

## 🔧 Analysis Tools

### Data Enrichment Scripts
```bash
# Extract LogicBoxes registrar data
python scripts/extract_logicboxes_data.py

# Enrich registrar contact information  
python scripts/enrich_logicboxes_websites.py

# Comprehensive gateway analysis
python scripts/analyze_rdap_gateways.py
```

### Requirements
- Python 3.8+ with pandas, requests
- Access to ICANN registrar database
- RDAP endpoint data

## 📈 Analysis Results

### Gateway Provider Market Share
| Provider | Registrars | Domains | Market Share |
|----------|------------|---------|--------------|
| **Tucows** | 66 | 20.2M | 9.41% |
| **LogicBoxes** | 115 | 8.1M | 3.79% |
| **RRPProxy/CentralNic** | 8 | 2.3M | 1.06% |
| **Total Gateway** | **189** | **30.6M** | **14.26%** |

### Key Findings
- **Efficiency Advantage**: Gateway providers show higher domain-to-registrar ratios
- **Market Concentration**: Top 3 providers serve 189 registrars efficiently
- **Growth Potential**: 85.7% market still uses self-hosted RDAP infrastructure
- **Infrastructure Sharing**: Successful model for smaller registrars

## 🌐 Data Sources

- **ICANN Registrar Database**: Official registrar information and contact details
- **RDAP Endpoints**: Live RDAP server configurations and response data  
- **Domain Statistics**: Registrar domain portfolio sizes and market share
- **Gateway Analysis**: Custom analysis of shared infrastructure patterns

## 🚀 Technologies Used

- **Frontend**: React 18, Recharts, Tailwind CSS, Lucide Icons
- **Build Tools**: Create React App, Vite-compatible
- **Data Processing**: Python (pandas, requests, json)
- **Deployment**: Vercel with automatic GitHub integration
- **Analysis**: JavaScript, Python scripting

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### Development Guidelines
- Follow existing code style and structure
- Add appropriate error handling
- Update documentation for new features
- Test locally before submitting PR

## 📝 License

This project is for research and analysis purposes. Please credit data sources appropriately when using this analysis.

## 📞 Contact & Support

- **Repository**: [GitHub Issues](https://github.com/makafeli/rdap-registry-analysis/issues)
- **Documentation**: See `docs/` directory for detailed analysis reports
- **Deployment**: [Vercel Documentation](https://vercel.com/docs)

---

**Built with ❤️ for the domain industry research community**

🤖 *Generated with [Claude Code](https://claude.ai/code)*