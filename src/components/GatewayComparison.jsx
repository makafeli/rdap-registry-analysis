import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { Download, TrendingUp, Users, Globe, Server } from 'lucide-react';

const GatewayComparison = () => {
  const [data, setData] = useState(null);
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        // Load comprehensive analysis
        const analysisResponse = await fetch('/data/processed/comprehensive_gateway_analysis.json');
        if (!analysisResponse.ok) {
          throw new Error(`Failed to load gateway analysis: ${analysisResponse.status} ${analysisResponse.statusText}`);
        }
        const analysisData = await analysisResponse.json();
        setData(analysisData);

        // Load gateway provider summary
        const summaryResponse = await fetch('/data/processed/gateway_provider_summary.json');
        if (!summaryResponse.ok) {
          throw new Error(`Failed to load gateway summary: ${summaryResponse.status} ${summaryResponse.statusText}`);
        }
        const summary = await summaryResponse.json();
        setSummaryData(summary);
        
      } catch (err) {
        console.error('Error loading data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">Loading gateway analysis...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
        Error loading data: {error}
      </div>
    );
  }

  if (!data || !data.dataset_summary) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">No data available</div>
      </div>
    );
  }

  // Prepare data for charts
  const gatewayProviders = data.gateway_providers ? Object.entries(data.gateway_providers).map(([name, info]) => ({
    name: name.replace(' (Potential Gateway)', ''),
    registrars: info.registrar_count,
    domains: info.total_domains,
    marketShare: info.market_share_percent,
    isPotential: name.includes('Potential Gateway')
  })) : [];

  // Sort by market share
  const sortedProviders = [...gatewayProviders].sort((a, b) => b.marketShare - a.marketShare);

  // Colors for charts
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4', '#84CC16'];

  // Pie chart data for market share
  const pieData = data.gateway_analysis ? [
    {
      name: 'Self-Hosted RDAP',
      value: data.gateway_analysis.self_hosted_market_share_percent,
      domains: data.gateway_analysis.total_self_hosted_domains
    },
    ...sortedProviders.map(provider => ({
      name: provider.name,
      value: provider.marketShare,
      domains: provider.domains
    }))
  ] : [];

  const formatNumber = (num) => {
    if (num >= 1000000) {
      return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
      return (num / 1000).toFixed(1) + 'K';
    }
    return num.toString();
  };

  const formatPercent = (num) => `${num.toFixed(1)}%`;

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      return (
        <div className="bg-white p-3 border border-gray-200 rounded shadow-lg">
          <p className="font-medium">{label}</p>
          <p className="text-blue-600">
            Market Share: {formatPercent(data.marketShare)}
          </p>
          <p className="text-green-600">
            Domains: {formatNumber(data.domains)}
          </p>
          <p className="text-purple-600">
            Registrars: {(data.registrars || 0).toLocaleString()}
          </p>
        </div>
      );
    }
    return null;
  };

  const exportData = () => {
    const csvContent = [
      ['Provider', 'Market Share (%)', 'Domains', 'Registrars', 'Type'],
      ...sortedProviders.map(provider => [
        provider.name,
        provider.marketShare.toFixed(2),
        provider.domains,
        provider.registrars,
        provider.isPotential ? 'Potential Gateway' : 'Known Gateway'
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'rdap_gateway_analysis.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Comprehensive RDAP Analysis Dashboard</h2>
            <p className="text-gray-600 mt-1">
              Complete analysis of RDAP adoption and gateway solutions across {(data.dataset_summary?.total_registrars || 0).toLocaleString()} registrars managing {formatNumber(data.dataset_summary?.total_domains || 0)} domains
            </p>
            {summaryData && Array.isArray(summaryData) && (
              <p className="text-sm text-blue-600 mt-1">
                Gateway adoption: {summaryData.reduce((sum, provider) => sum + (provider.registrar_count || 0), 0).toLocaleString()} registrars ({((summaryData.reduce((sum, provider) => sum + (provider.registrar_count || 0), 0) / (data.dataset_summary?.total_registrars || 1)) * 100).toFixed(1)}%) managing {formatNumber(summaryData.reduce((sum, provider) => sum + (provider.total_domains || 0), 0))} domains
              </p>
            )}
          </div>
          <button
            onClick={exportData}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download size={16} />
            Export Data
          </button>
        </div>

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Globe className="text-blue-600" size={20} />
              <span className="text-sm font-medium text-blue-600">Total Domains</span>
            </div>
            <div className="text-2xl font-bold text-blue-900">
              {formatNumber(data.dataset_summary?.total_domains || 0)}
            </div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Server className="text-green-600" size={20} />
              <span className="text-sm font-medium text-green-600">Gateway Adoption</span>
            </div>
            <div className="text-2xl font-bold text-green-900">
              {formatPercent(data.gateway_analysis?.gateway_market_share_percent || 0)}
            </div>
          </div>

          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <Users className="text-purple-600" size={20} />
              <span className="text-sm font-medium text-purple-600">Gateway Providers</span>
            </div>
            <div className="text-2xl font-bold text-purple-900">
              {Object.keys(data.gateway_providers || {}).length}
            </div>
          </div>

          <div className="bg-orange-50 p-4 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="text-orange-600" size={20} />
              <span className="text-sm font-medium text-orange-600">Gateway Domains</span>
            </div>
            <div className="text-2xl font-bold text-orange-900">
              {formatNumber(data.gateway_analysis?.total_gateway_domains || 0)}
            </div>
          </div>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Market Share Pie Chart */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold mb-4">RDAP Market Share Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${formatPercent(value)}`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                formatter={(value, name, props) => [
                  `${formatPercent(value)} (${formatNumber(props.payload.domains)} domains)`,
                  name
                ]}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {/* Gateway Provider Comparison */}
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h3 className="text-lg font-semibold mb-4">Gateway Provider Market Share</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sortedProviders} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="name" 
                angle={-45}
                textAnchor="end"
                height={100}
                interval={0}
              />
              <YAxis tickFormatter={formatPercent} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="marketShare" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Detailed Provider Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="p-6 border-b">
          <h3 className="text-lg font-semibold">Gateway Provider Details</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Provider
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Market Share
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Domains
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Registrars
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Type
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Top Registrar
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {sortedProviders.map((provider, index) => {
                const providerData = data.gateway_providers?.[provider.isPotential ? `${provider.name} (Potential Gateway)` : provider.name];
                const topRegistrar = providerData?.top_registrars?.[0];
                
                return (
                  <tr key={provider.name} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div className={`w-3 h-3 rounded-full mr-3`} style={{ backgroundColor: COLORS[index % COLORS.length] }}></div>
                        <div className="font-medium text-gray-900">{provider.name}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900 font-medium">
                      {formatPercent(provider.marketShare)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatNumber(provider.domains)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {(provider.registrars || 0).toLocaleString()}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        provider.isPotential 
                          ? 'bg-yellow-100 text-yellow-800'
                          : 'bg-green-100 text-green-800'
                      }`}>
                        {provider.isPotential ? 'Potential Gateway' : 'Known Gateway'}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {topRegistrar ? (
                        <div>
                          <div className="font-medium">{topRegistrar.name}</div>
                          <div className="text-gray-500">{formatNumber(topRegistrar.domains)} domains</div>
                        </div>
                      ) : (
                        <div className="text-gray-400">—</div>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Analysis Insights */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold mb-4">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Market Leadership</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• <strong>Tucows</strong> dominates with 9.4% market share and 66 registrars</li>
              <li>• <strong>Network Solutions</strong> serves 476 registrars as a potential gateway</li>
              <li>• <strong>NameBright</strong> has the highest registrar count (1,252)</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-gray-900 mb-2">Gateway Adoption</h4>
            <ul className="text-sm text-gray-600 space-y-1">
              <li>• Gateway solutions serve 20.6% of total domains</li>
              <li>• Traditional known gateways handle 10.5% of domains</li>
              <li>• Emerging potential gateways serve 10.1% of domains</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GatewayComparison;