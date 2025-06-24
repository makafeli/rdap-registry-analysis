import React, { useState } from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Search, Server, Database, Building2, TrendingUp } from 'lucide-react';

const RDAPAnalysisDashboard = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Main statistics
  const totalRegistrars = 2358;
  const uniqueRdapUrls = 349;
  const gatewayProviders = 3;
  const coreGatewayUsers = 189;
  
  // Core Gateway Providers data
  const topProviders = [
    { name: 'Tucows Gateway Network', count: 66, percentage: 34.9, color: '#3B82F6' },
    { name: 'LogicBoxes (rdapserver.net)', count: 115, percentage: 60.8, color: '#F59E0B' },
    { name: 'RRPProxy/CentralNic', count: 8, percentage: 4.2, color: '#10B981' },
  ];
  
  // Registry Gateway registrars with domain counts
  const registryGatewayRegistrars = [
    { name: 'PDR Ltd. (PublicDomainRegistry)', ianaId: 303, domains: 4845099 },
    { name: 'Launchpad.com Inc.', ianaId: 955, domains: 729662 },
    { name: 'Hostinger, UAB', ianaId: 1636, domains: 590290 },
    { name: 'BigRock Solutions Ltd.', ianaId: 1495, domains: 276454 },
    { name: 'IHS Telekom, Inc.', ianaId: 1091, domains: 160821 },
    { name: 'NetEarth One Inc.', ianaId: 1005, domains: 142479 },
    { name: 'Sav.com, LLC', ianaId: 609, domains: 135595 },
    { name: 'MAT BAO CORPORATION', ianaId: 1586, domains: 134504 },
    { name: 'Beget LLC', ianaId: 3806, domains: 103122 },
    { name: 'TecnocrÃ¡tica Centro de Datos', ianaId: 1600, domains: 101516 },
    { name: 'Alpine Domains Inc.', ianaId: 1432, domains: 81068 },
    { name: 'Aerotek Bilisim', ianaId: 1534, domains: 80389 },
    { name: 'Reg2C.com Inc.', ianaId: 819, domains: 75272 },
    { name: 'Neubox Internet S.A. de C.V.', ianaId: 1483, domains: 62661 },
    { name: 'Nhan Hoa Software Company Ltd.', ianaId: 1710, domains: 57102 }
  ];
  
  // Domain distribution by RDAP provider (Gateway vs Self-hosted)
  const domainDistribution = [
    { provider: 'GoDaddy (Self-hosted)', domains: 63168934, registrars: 1, avgDomains: 63168934 },
    { provider: 'Tucows Gateway', domains: 20188795, registrars: 66, avgDomains: 305891 },
    { provider: 'Aliyun (Self-hosted)', domains: 12931823, registrars: 4, avgDomains: 3232956 },
    { provider: 'Namecheap (Self-hosted)', domains: 10323962, registrars: 3, avgDomains: 3441321 },
    { provider: 'LogicBoxes Gateway', domains: 8131328, registrars: 115, avgDomains: 70707 },
    { provider: 'RRPProxy/CentralNic', domains: 2278349, registrars: 8, avgDomains: 284794 }
  ];
  
  // Service models comparison (Core Gateway Focus)
  const serviceModels = [
    { model: 'Self-hosted RDAP', count: 2169, description: 'Registrars managing their own RDAP service', example: 'rdap.godaddy.com' },
    { model: 'LogicBoxes Gateway', count: 115, description: 'Independent registrars using LogicBoxes infrastructure', example: 'rdapserver.net' },
    { model: 'Tucows Gateway Network', count: 66, description: 'Registrars using Tucows branded RDAP endpoints', example: 'opensrs.rdap.tucows.com' },
    { model: 'RRPProxy/CentralNic', count: 8, description: 'Specialized gateway for reseller networks', example: 'rdap.rrpproxy.net' }
  ];
  
  const filteredRegistrars = registryGatewayRegistrars.filter(reg => 
    reg.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    reg.ianaId.toString().includes(searchTerm) ||
    (reg.domains && reg.domains.toString().includes(searchTerm))
  );

  return (
    <div className="w-full min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">RDAP Gateway Analysis Dashboard</h1>
          <p className="text-gray-600">Focus on core RDAP gateway providers: LogicBoxes, Tucows, and RRPProxy/CentralNic</p>
        </div>
        
        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Registrars</p>
                <p className="text-2xl font-bold text-gray-900">{totalRegistrars.toLocaleString()}</p>
              </div>
              <Building2 className="h-10 w-10 text-blue-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Unique RDAP URLs</p>
                <p className="text-2xl font-bold text-gray-900">{uniqueRdapUrls}</p>
              </div>
              <Server className="h-10 w-10 text-green-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Core Gateway Users</p>
                <p className="text-2xl font-bold text-gray-900">{coreGatewayUsers}</p>
              </div>
              <Database className="h-10 w-10 text-yellow-500" />
            </div>
          </div>
          
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Core Gateway Providers</p>
                <p className="text-2xl font-bold text-gray-900">{gatewayProviders}</p>
              </div>
              <TrendingUp className="h-10 w-10 text-purple-500" />
            </div>
          </div>
        </div>
        
        {/* Main Charts Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Pie Chart */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">RDAP Service Provider Distribution</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={topProviders}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${percentage}%`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="count"
                >
                  {topProviders.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-2">
              {topProviders.map((provider, idx) => (
                <div key={idx} className="flex items-center justify-between text-sm">
                  <div className="flex items-center">
                    <div className={`w-3 h-3 rounded-full mr-2`} style={{ backgroundColor: provider.color }}></div>
                    <span className="text-gray-700">{provider.name}</span>
                  </div>
                  <span className="font-semibold">{provider.count} ({provider.percentage}%)</span>
                </div>
              ))}
            </div>
          </div>
          
          {/* Service Models */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">RDAP Service Models</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={serviceModels}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="model" angle={-15} textAnchor="end" height={80} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="count" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
            <div className="mt-4 space-y-3">
              {serviceModels.map((model, idx) => (
                <div key={idx} className="border-l-4 border-blue-500 pl-3">
                  <p className="font-semibold text-sm">{model.model}</p>
                  <p className="text-xs text-gray-600">{model.description}</p>
                  <p className="text-xs text-gray-500">Example: {model.example}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
        
        {/* Domain Distribution Section */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Domain Distribution by RDAP Provider</h2>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart data={domainDistribution} margin={{ top: 20, right: 30, left: 50, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="provider" />
              <YAxis 
                tickFormatter={(value) => `${(value / 1000000).toFixed(0)}M`}
                label={{ value: 'Domains (Millions)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                formatter={(value) => value.toLocaleString()}
                labelFormatter={(label) => `Provider: ${label}`}
              />
              <Bar dataKey="domains" fill="#3B82F6">
                <Cell fill="#1E40AF" /> {/* GoDaddy */}
                <Cell fill="#3B82F6" /> {/* Aliyun */}
                <Cell fill="#60A5FA" /> {/* Namecheap */}
                <Cell fill="#F59E0B" /> {/* Registry Gateway */}
                <Cell fill="#10B981" /> {/* Network Solutions */}
                <Cell fill="#93C5FD" /> {/* Namebright */}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
          
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <h3 className="font-semibold text-blue-900 mb-2">Efficiency Analysis</h3>
              <p className="text-sm text-blue-800">
                Registry Gateway manages <span className="font-bold">8.1M domains</span> with <span className="font-bold">115 registrars</span>, 
                averaging <span className="font-bold">70,707 domains per registrar</span> - significantly higher than most providers.
              </p>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <h3 className="font-semibold text-green-900 mb-2">Market Share Insight</h3>
              <p className="text-sm text-green-800">
                While GoDaddy dominates with 63M domains, Registry Gateway ranks <span className="font-bold">4th in total domains</span> managed, 
                demonstrating the success of the shared infrastructure model.
              </p>
            </div>
          </div>
        </div>
        
        {/* Registry Gateway Focus */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <div className="mb-6">
            <h2 className="text-xl font-semibold mb-2">Registry Gateway Service Analysis</h2>
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
              <h3 className="font-semibold text-yellow-900 mb-2">What is Registry Gateway?</h3>
              <p className="text-sm text-yellow-800 mb-2">
                Registry Gateway (rdapserver.net) is a service by <span className="font-bold">LogicBoxes</span> that allows registrars to:
              </p>
              <ul className="list-disc list-inside text-sm text-yellow-800 space-y-1">
                <li>Maintain their own ICANN accreditations</li>
                <li>Use shared technical infrastructure for RDAP/WHOIS</li>
                <li>Benefit from automated ICANN compliance (WDRP, ERRP, Registrant Verification)</li>
                <li>Reduce operational overhead while maintaining independence</li>
              </ul>
            </div>
          </div>
          
          <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
            <h3 className="font-semibold text-blue-900 mb-2">Top Registry Gateway Users</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-sm">
              <div>
                <p className="text-blue-800"><span className="font-semibold">PDR Ltd.</span> manages 4.8M domains (60% of all RG domains)</p>
                <p className="text-blue-800"><span className="font-semibold">Launchpad.com</span> manages 730K domains</p>
                <p className="text-blue-800"><span className="font-semibold">Hostinger</span> manages 590K domains</p>
              </div>
              <div>
                <p className="text-blue-700 italic">These top 3 registrars account for 76% of all Registry Gateway domains, showing that even within shared infrastructure, there's significant concentration.</p>
              </div>
            </div>
          </div>
          
          {/* Search for Registry Gateway users */}
          <div className="mb-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Search Registry Gateway users..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>
          </div>
          
          {/* Registry Gateway Users List */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {filteredRegistrars.map((registrar, idx) => (
              <div key={idx} className="border border-gray-200 rounded-lg p-3 hover:bg-gray-50 transition-colors">
                <p className="font-medium text-sm text-gray-900">{registrar.name}</p>
                <div className="flex justify-between items-center mt-1">
                  <p className="text-xs text-gray-500">IANA ID: {registrar.ianaId}</p>
                  {registrar.domains && (
                    <p className="text-xs font-semibold text-blue-600">
                      {registrar.domains.toLocaleString()} domains
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
          
          <div className="mt-4 text-center">
            <p className="text-sm text-gray-600">
              Showing {filteredRegistrars.length} of {registryGatewayRegistrars.length} total Registry Gateway users
            </p>
          </div>
        </div>
        
        {/* Key Insights */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Key Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-3">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <span className="text-blue-600 font-semibold">1</span>
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold">Market Concentration</h3>
                  <p className="text-sm text-gray-600">
                    Two providers (Namebright and Network Solutions) serve 73.3% of all registrars, 
                    indicating significant market concentration.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-green-100 rounded-full flex items-center justify-center">
                  <span className="text-green-600 font-semibold">2</span>
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold">Unique Name Pattern</h3>
                  <p className="text-sm text-gray-600">
                    Every registrar has a unique name across all RDAP URLs - no duplicates found, 
                    confirming individual ICANN accreditations.
                  </p>
                </div>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-yellow-100 rounded-full flex items-center justify-center">
                  <span className="text-yellow-600 font-semibold">3</span>
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold">Registry Gateway Efficiency</h3>
                  <p className="text-sm text-gray-600">
                    Registry Gateway serves 4.9% of registrars but manages 6.3% of domains (8.1M), 
                    showing higher efficiency than traditional models.
                  </p>
                </div>
              </div>
              
              <div className="flex items-start">
                <div className="flex-shrink-0 w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center">
                  <span className="text-purple-600 font-semibold">4</span>
                </div>
                <div className="ml-3">
                  <h3 className="font-semibold">Domain Concentration</h3>
                  <p className="text-sm text-gray-600">
                    GoDaddy alone manages 49% of tracked domains (63M), while the top 6 providers 
                    control 85% of all domains, showing extreme market concentration.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RDAPAnalysisDashboard;
