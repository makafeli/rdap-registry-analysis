#!/bin/bash

# RDAP Registry Analysis - Quick Start Script

echo "==================================="
echo "RDAP Registry Analysis Setup"
echo "==================================="
echo ""

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js first."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
npm install

# Check if the Excel file exists
if [ ! -f "../Rdap lookups.xlsx" ]; then
    echo ""
    echo "⚠️  Warning: 'Rdap lookups.xlsx' not found in parent directory"
    echo "Please copy your Excel file to: $(dirname "$PWD")/Rdap lookups.xlsx"
fi

echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Available commands:"
echo ""
echo "1. Start React Dashboard:"
echo "   npm start"
echo ""
echo "2. Analyze Excel Data:"
echo "   node scripts/analyze_rdap.js '../Rdap lookups.xlsx'"
echo ""
echo "3. Enrich Registrar Data (Bash):"
echo "   cd scripts && ./enrich_registrars.sh"
echo ""
echo "4. Enrich Registrar Data (Python):"
echo "   cd scripts && pip install -r requirements.txt && python enrich_registrars.py"
echo ""
echo "5. Build for Production:"
echo "   npm run build"
echo ""
echo "For Claude Code CLI:"
echo "   cd $(pwd) && claude-code ."
echo ""
