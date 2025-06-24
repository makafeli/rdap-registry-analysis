import React, { useState } from 'react';
import { Download, Globe, Mail, Phone, Building2, AlertCircle, CheckCircle2, ExternalLink } from 'lucide-react';

const RegistrarEnrichmentTool = () => {
  const [selectedRegistrars, setSelectedRegistrars] = useState([]);
  
  // Sample Registry Gateway registrars for enrichment
  const registrarsToEnrich = [
    { ianaId: 303, name: 'PDR Ltd. d/b/a PublicDomainRegistry.com', domains: 4845099 },
    { ianaId: 955, name: 'Launchpad.com Inc.', domains: 729662 },
    { ianaId: 1636, name: 'Hostinger, UAB', domains: 590290 },
    { ianaId: 1495, name: 'BigRock Solutions Ltd.', domains: 276454 },
    { ianaId: 1091, name: 'IHS Telekom, Inc.', domains: 160821 }
  ];
  
  // Sample enriched data (in real implementation, this would come from API calls)
  const enrichedDataSample = {
    303: {
      website: 'https://publicdomainregistry.com',
      email: 'compliance@publicdomainregistry.com',
      phone: '+1.2026219164',
      abuseEmail: 'abuse@publicdomainregistry.com',
      whoisServer: 'whois.publicdomainregistry.com',
      status: 'Accredited'
    },
    955: {
      website: 'https://launchpad.com',
      email: 'support@launchpad.com',
      phone: '+1.4165350123',
      abuseEmail: 'abuse@launchpad.com',
      whoisServer: 'whois.launchpad.com',
      status: 'Accredited'
    },
    1636: {
      website: 'https://www.hostinger.com',
      email: 'domains@hostinger.com',
      phone: '+370.52071558',
      abuseEmail: 'abuse@hostinger.com',
      whoisServer: 'whois.hostinger.com',
      status: 'Accredited'
    }
  };
  
  const handleSelectAll = () => {
    if (selectedRegistrars.length === registrarsToEnrich.length) {
      setSelectedRegistrars([]);
    } else {
      setSelectedRegistrars(registrarsToEnrich.map(r => r.ianaId));
    }
  };
  
  const handleSelectRegistrar = (ianaId) => {
    if (selectedRegistrars.includes(ianaId)) {
      setSelectedRegistrars(selectedRegistrars.filter(id => id !== ianaId));
    } else {
      setSelectedRegistrars([...selectedRegistrars, ianaId]);
    }
  };
  
  const generateEnrichmentScript = () => {
    const script = `#!/bin/bash
# Registrar Enrichment Script using ICANN API
# This script fetches contact information for registrars

OUTPUT_FILE="enriched_registrars.csv"
echo "iana_id,name,website,email,phone,abuse_email,whois_server,status" > $OUTPUT_FILE

# Array of IANA IDs to enrich
IANA_IDS=(${selectedRegistrars.join(' ')})

for ID in "\${IANA_IDS[@]}"; do
  echo "Fetching data for IANA ID: $ID"
  
  # Fetch from ICANN API
  RESPONSE=$(curl -s "https://lookup.icann.org/api/registrar/$ID")
  
  # Parse JSON response (requires jq)
  NAME=$(echo $RESPONSE | jq -r '.name // "N/A"')
  WEBSITE=$(echo $RESPONSE | jq -r '.url // "N/A"')
  EMAIL=$(echo $RESPONSE | jq -r '.email // "N/A"')
  PHONE=$(echo $RESPONSE | jq -r '.phone // "N/A"')
  ABUSE_EMAIL=$(echo $RESPONSE | jq -r '.abuseEmail // "N/A"')
  WHOIS_SERVER=$(echo $RESPONSE | jq -r '.whoisServer // "N/A"')
  STATUS=$(echo $RESPONSE | jq -r '.status // "N/A"')
  
  # Append to CSV
  echo "$ID,\\"$NAME\\",\\"$WEBSITE\\",\\"$EMAIL\\",\\"$PHONE\\",\\"$ABUSE_EMAIL\\",\\"$WHOIS_SERVER\\",\\"$STATUS\\"" >> $OUTPUT_FILE
  
  # Rate limiting
  sleep 1
done

echo "Enrichment complete! Results saved to $OUTPUT_FILE"`;

    return script;
  };
  
  const generatePythonScript = () => {
    const script = `import requests
import pandas as pd
import time
from typing import Dict, List

def enrich_registrar_data(iana_ids: List[int]) -> pd.DataFrame:
    """
    Fetch registrar contact information from ICANN API
    """
    enriched_data = []
    
    for iana_id in iana_ids:
        print(f"Fetching data for IANA ID: {iana_id}")
        
        try:
            # ICANN Registrar API endpoint
            response = requests.get(f"https://lookup.icann.org/api/registrar/{iana_id}")
            
            if response.status_code == 200:
                data = response.json()
                
                enriched_data.append({
                    'iana_id': iana_id,
                    'name': data.get('name', 'N/A'),
                    'website': data.get('url', 'N/A'),
                    'email': data.get('email', 'N/A'),
                    'phone': data.get('phone', 'N/A'),
                    'abuse_email': data.get('abuseEmail', 'N/A'),
                    'whois_server': data.get('whoisServer', 'N/A'),
                    'status': data.get('status', 'N/A'),
                    'address': data.get('address', {}).get('street', 'N/A'),
                    'city': data.get('address', {}).get('city', 'N/A'),
                    'country': data.get('address', {}).get('country', 'N/A')
                })
            else:
                print(f"Error fetching data for IANA ID {iana_id}: {response.status_code}")
                
        except Exception as e:
            print(f"Exception for IANA ID {iana_id}: {str(e)}")
            
        # Rate limiting
        time.sleep(1)
    
    return pd.DataFrame(enriched_data)

# Registry Gateway registrar IANA IDs
registry_gateway_ids = [${selectedRegistrars.join(', ')}]

# Fetch enriched data
df_enriched = enrich_registrar_data(registry_gateway_ids)

# Save to CSV
df_enriched.to_csv('enriched_registrars.csv', index=False)
print(f"\\nEnriched {len(df_enriched)} registrars and saved to enriched_registrars.csv")

# Display summary
print("\\nSample enriched data:")
print(df_enriched.head())`;

    return script;
  };
  
  return (
    <div className="w-full min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Registrar Data Enrichment Tool</h1>
          <p className="text-gray-600">Enrich Registry Gateway (LogicBoxes) registrar data with contact information from ICANN</p>
        </div>
        
        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <div className="flex items-start">
            <AlertCircle className="h-6 w-6 text-blue-600 mr-3 flex-shrink-0 mt-0.5" />
            <div>
              <h3 className="font-semibold text-blue-900 mb-2">How to Enrich Registrar Data</h3>
              <p className="text-sm text-blue-800 mb-3">
                Your Excel file contains IANA IDs for each registrar. We can use these to fetch additional information:
              </p>
              <ul className="list-disc list-inside text-sm text-blue-800 space-y-1">
                <li><strong>ICANN API:</strong> https://lookup.icann.org/api/registrar/{'{IANA_ID}'}</li>
                <li><strong>Available data:</strong> Website, email, phone, abuse contacts, WHOIS server, physical address</li>
                <li><strong>Rate limiting:</strong> Include delays between requests to avoid being blocked</li>
                <li><strong>Alternative:</strong> ICANN's bulk registrar data export (updated weekly)</li>
              </ul>
            </div>
          </div>
        </div>
        
        {/* Registrar Selection */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Select Registrars to Enrich</h2>
            <button
              onClick={handleSelectAll}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
            >
              {selectedRegistrars.length === registrarsToEnrich.length ? 'Deselect All' : 'Select All'}
            </button>
          </div>
          
          <div className="space-y-3">
            {registrarsToEnrich.map((registrar) => {
              const isSelected = selectedRegistrars.includes(registrar.ianaId);
              const enrichedData = enrichedDataSample[registrar.ianaId];
              
              return (
                <div 
                  key={registrar.ianaId}
                  className={`border rounded-lg p-4 cursor-pointer transition-all ${
                    isSelected ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'
                  }`}
                  onClick={() => handleSelectRegistrar(registrar.ianaId)}
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          checked={isSelected}
                          onChange={() => {}}
                          className="mr-3"
                        />
                        <div>
                          <p className="font-semibold">{registrar.name}</p>
                          <p className="text-sm text-gray-600">IANA ID: {registrar.ianaId} | Domains: {registrar.domains.toLocaleString()}</p>
                        </div>
                      </div>
                      
                      {enrichedData && (
                        <div className="mt-3 ml-7 grid grid-cols-2 gap-3 text-sm">
                          <div className="flex items-center text-gray-700">
                            <Globe className="h-4 w-4 mr-2 text-gray-400" />
                            <span>{enrichedData.website}</span>
                          </div>
                          <div className="flex items-center text-gray-700">
                            <Mail className="h-4 w-4 mr-2 text-gray-400" />
                            <span>{enrichedData.email}</span>
                          </div>
                          <div className="flex items-center text-gray-700">
                            <Phone className="h-4 w-4 mr-2 text-gray-400" />
                            <span>{enrichedData.phone}</span>
                          </div>
                          <div className="flex items-center text-gray-700">
                            <CheckCircle2 className="h-4 w-4 mr-2 text-green-500" />
                            <span>{enrichedData.status}</span>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
        
        {/* Enrichment Scripts */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Bash Script */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3 flex items-center">
              <Building2 className="h-5 w-5 mr-2 text-gray-600" />
              Bash Enrichment Script
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Use this script to enrich data via command line (requires curl and jq)
            </p>
            <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
              <pre className="text-green-400 text-xs font-mono whitespace-pre">
                {selectedRegistrars.length > 0 ? generateEnrichmentScript() : '# Select registrars to generate script'}
              </pre>
            </div>
            {selectedRegistrars.length > 0 && (
              <button 
                className="mt-3 w-full px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-gray-700 transition-colors text-sm flex items-center justify-center"
                onClick={() => {
                  const blob = new Blob([generateEnrichmentScript()], { type: 'text/plain' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = 'enrich_registrars.sh';
                  a.click();
                }}
              >
                <Download className="h-4 w-4 mr-2" />
                Download Bash Script
              </button>
            )}
          </div>
          
          {/* Python Script */}
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold mb-3 flex items-center">
              <Building2 className="h-5 w-5 mr-2 text-blue-600" />
              Python Enrichment Script
            </h3>
            <p className="text-sm text-gray-600 mb-4">
              Python script with pandas for data processing
            </p>
            <div className="bg-gray-900 rounded-lg p-4 overflow-x-auto">
              <pre className="text-blue-400 text-xs font-mono whitespace-pre">
                {selectedRegistrars.length > 0 ? generatePythonScript() : '# Select registrars to generate script'}
              </pre>
            </div>
            {selectedRegistrars.length > 0 && (
              <button 
                className="mt-3 w-full px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm flex items-center justify-center"
                onClick={() => {
                  const blob = new Blob([generatePythonScript()], { type: 'text/plain' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = 'enrich_registrars.py';
                  a.click();
                }}
              >
                <Download className="h-4 w-4 mr-2" />
                Download Python Script
              </button>
            )}
          </div>
        </div>
        
        {/* Additional Resources */}
        <div className="mt-8 bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Additional Resources</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a 
              href="https://www.icann.org/resources/pages/registrar-data-2012-02-25-en"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ExternalLink className="h-5 w-5 mr-3 text-gray-600" />
              <div>
                <p className="font-semibold text-sm">ICANN Registrar Data</p>
                <p className="text-xs text-gray-600">Official registrar information database</p>
              </div>
            </a>
            
            <a 
              href="https://www.icann.org/registrar-reports/accredited-list.html"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center p-3 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            >
              <ExternalLink className="h-5 w-5 mr-3 text-gray-600" />
              <div>
                <p className="font-semibold text-sm">Accredited Registrar List</p>
                <p className="text-xs text-gray-600">Weekly updated CSV export</p>
              </div>
            </a>
            
            <div className="flex items-center p-3 border border-gray-200 rounded-lg bg-yellow-50">
              <AlertCircle className="h-5 w-5 mr-3 text-yellow-600" />
              <div>
                <p className="font-semibold text-sm">LogicBoxes Information</p>
                <p className="text-xs text-gray-600">Contact LogicBoxes directly for Registry Gateway details</p>
              </div>
            </div>
            
            <div className="flex items-center p-3 border border-gray-200 rounded-lg bg-green-50">
              <CheckCircle2 className="h-5 w-5 mr-3 text-green-600" />
              <div>
                <p className="font-semibold text-sm">Bulk Processing Tip</p>
                <p className="text-xs text-gray-600">Use ICANN's bulk export for all 115 registrars</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegistrarEnrichmentTool;
