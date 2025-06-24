import React, { useState, useMemo, useEffect } from 'react';
import { Search, Download, SortAsc, SortDesc, X } from 'lucide-react';

const RegistryGatewayUsers = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortConfig, setSortConfig] = useState({ key: 'domain_count', direction: 'desc' });
  const [filters, setFilters] = useState({
    gatewayProvider: '',
    domainCountRange: '',
    category: ''
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(50);

  // Load all gateway registrars data
  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch('/data/processed/all_gateway_registrars.json');
        if (!response.ok) {
          throw new Error(`Failed to load gateway registrars: ${response.status} ${response.statusText}`);
        }
        const registrars = await response.json();
        setData(registrars);
      } catch (err) {
        console.error('Error loading data:', err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  // Filter and search data
  const filteredData = useMemo(() => {
    let filtered = data;

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(registrar =>
        registrar.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        registrar.iana_id.toString().includes(searchTerm) ||
        (registrar.rdap_url && registrar.rdap_url.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (registrar.gateway_provider && registrar.gateway_provider.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Apply gateway provider filter
    if (filters.gatewayProvider) {
      filtered = filtered.filter(registrar => registrar.gateway_provider === filters.gatewayProvider);
    }

    // Apply domain count range filter
    if (filters.domainCountRange) {
      filtered = filtered.filter(registrar => {
        const count = registrar.domain_count || 0;
        switch (filters.domainCountRange) {
          case 'small': return count < 1000;
          case 'medium': return count >= 1000 && count < 100000;
          case 'large': return count >= 100000 && count < 1000000;
          case 'enterprise': return count >= 1000000;
          default: return true;
        }
      });
    }

    // Apply category filter
    if (filters.category) {
      if (filters.category === 'null') {
        filtered = filtered.filter(registrar => !registrar.category);
      } else {
        filtered = filtered.filter(registrar => registrar.category === filters.category);
      }
    }

    return filtered;
  }, [data, searchTerm, filters]);

  // Sort data
  const sortedData = useMemo(() => {
    if (!sortConfig.key) return filteredData;

    return [...filteredData].sort((a, b) => {
      let aVal = a[sortConfig.key];
      let bVal = b[sortConfig.key];

      // Handle null/undefined values
      if (aVal === null || aVal === undefined) aVal = sortConfig.key === 'domain_count' ? 0 : '';
      if (bVal === null || bVal === undefined) bVal = sortConfig.key === 'domain_count' ? 0 : '';

      // Convert to numbers for domain_count
      if (sortConfig.key === 'domain_count') {
        aVal = Number(aVal);
        bVal = Number(bVal);
      }

      if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [filteredData, sortConfig]);

  // Paginate data
  const paginatedData = useMemo(() => {
    const startIndex = (currentPage - 1) * pageSize;
    return sortedData.slice(startIndex, startIndex + pageSize);
  }, [sortedData, currentPage, pageSize]);

  // Get unique values for filters
  const gatewayProviders = useMemo(() => {
    return [...new Set(data.map(r => r.gateway_provider))].filter(Boolean).sort();
  }, [data]);

  const categories = useMemo(() => {
    const cats = [...new Set(data.map(r => r.category))].filter(Boolean);
    return [...cats.sort(), 'null']; // Add option for null categories
  }, [data]);

  // Handle sorting
  const handleSort = (key) => {
    setSortConfig(prev => ({
      key,
      direction: prev.key === key && prev.direction === 'desc' ? 'asc' : 'desc'
    }));
  };

  // Handle filter changes
  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({ ...prev, [filterType]: value }));
    setCurrentPage(1); // Reset to first page when filtering
  };

  // Clear all filters
  const clearFilters = () => {
    setFilters({ gatewayProvider: '', domainCountRange: '', category: '' });
    setSearchTerm('');
    setCurrentPage(1);
  };

  // Export to CSV
  const exportToCSV = () => {
    const headers = ['IANA ID', 'Name', 'Domain Count', 'Gateway Provider', 'Category', 'RDAP URL'];
    const csvContent = [
      headers.join(','),
      ...sortedData.map(registrar => [
        registrar.iana_id,
        `"${registrar.name}"`,
        registrar.domain_count || 0,
        `"${registrar.gateway_provider || ''}"`,
        `"${registrar.category || ''}"`,
        `"${registrar.rdap_url || ''}"`
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'all_gateway_registrars.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  // Format numbers
  const formatNumber = (num) => {
    if (!num) return '0';
    return new Intl.NumberFormat().format(num);
  };

  // Calculate totals
  const totalDomains = useMemo(() => {
    return filteredData.reduce((sum, registrar) => sum + (registrar.domain_count || 0), 0);
  }, [filteredData]);

  // Get provider color
  const getProviderColor = (provider) => {
    const colors = {
      'Tucows': 'bg-blue-100 text-blue-800',
      'Network Solutions': 'bg-green-100 text-green-800',
      'RDAP Server': 'bg-purple-100 text-purple-800',
      'NameBright': 'bg-orange-100 text-orange-800',
      'RRPProxy/CentralNic': 'bg-red-100 text-red-800'
    };
    return colors[provider] || 'bg-gray-100 text-gray-800';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-lg">Loading registry gateway users...</div>
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

  const totalPages = Math.ceil(sortedData.length / pageSize);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex justify-between items-center mb-4">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Registry Gateway Users</h2>
            <p className="text-gray-600 mt-1">
              {filteredData.length.toLocaleString()} of {data.length.toLocaleString()} registrars • {formatNumber(totalDomains)} total domains
            </p>
          </div>
          <button
            onClick={exportToCSV}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            <Download size={16} />
            Export CSV
          </button>
        </div>

        {/* Provider Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
          {gatewayProviders.map(provider => {
            const providerData = data.filter(r => r.gateway_provider === provider);
            const providerDomains = providerData.reduce((sum, r) => sum + (r.domain_count || 0), 0);
            
            return (
              <div key={provider} className="text-center p-3 bg-gray-50 rounded-lg">
                <div className="text-sm font-medium text-gray-600">{provider}</div>
                <div className="text-lg font-bold text-gray-900">{providerData.length}</div>
                <div className="text-xs text-gray-500">{formatNumber(providerDomains)} domains</div>
              </div>
            );
          })}
        </div>

        {/* Search and Filters */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" size={16} />
            <input
              type="text"
              placeholder="Search registrars..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Gateway Provider Filter */}
          <select
            value={filters.gatewayProvider}
            onChange={(e) => handleFilterChange('gatewayProvider', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Gateway Providers</option>
            {gatewayProviders.map(provider => (
              <option key={provider} value={provider}>{provider}</option>
            ))}
          </select>

          {/* Domain Count Range Filter */}
          <select
            value={filters.domainCountRange}
            onChange={(e) => handleFilterChange('domainCountRange', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Domain Counts</option>
            <option value="small">Small (&lt; 1K domains)</option>
            <option value="medium">Medium (1K - 100K domains)</option>
            <option value="large">Large (100K - 1M domains)</option>
            <option value="enterprise">Enterprise (1M+ domains)</option>
          </select>

          {/* Category Filter */}
          <select
            value={filters.category}
            onChange={(e) => handleFilterChange('category', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>
                {category === 'null' ? 'No Category' : category}
              </option>
            ))}
          </select>
        </div>

        {/* Clear Filters */}
        {(searchTerm || filters.gatewayProvider || filters.domainCountRange || filters.category) && (
          <div className="mt-4">
            <button
              onClick={clearFilters}
              className="flex items-center gap-2 text-gray-600 hover:text-gray-800 transition-colors"
            >
              <X size={16} />
              Clear all filters
            </button>
          </div>
        )}
      </div>

      {/* Table */}
      <div className="bg-white rounded-lg shadow-sm border overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('iana_id')}
                >
                  <div className="flex items-center gap-2">
                    IANA ID
                    {sortConfig.key === 'iana_id' && (
                      sortConfig.direction === 'desc' ? <SortDesc size={14} /> : <SortAsc size={14} />
                    )}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('name')}
                >
                  <div className="flex items-center gap-2">
                    Registrar Name
                    {sortConfig.key === 'name' && (
                      sortConfig.direction === 'desc' ? <SortDesc size={14} /> : <SortAsc size={14} />
                    )}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('domain_count')}
                >
                  <div className="flex items-center gap-2">
                    Domain Count
                    {sortConfig.key === 'domain_count' && (
                      sortConfig.direction === 'desc' ? <SortDesc size={14} /> : <SortAsc size={14} />
                    )}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('gateway_provider')}
                >
                  <div className="flex items-center gap-2">
                    Gateway Provider
                    {sortConfig.key === 'gateway_provider' && (
                      sortConfig.direction === 'desc' ? <SortDesc size={14} /> : <SortAsc size={14} />
                    )}
                  </div>
                </th>
                <th 
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                  onClick={() => handleSort('category')}
                >
                  <div className="flex items-center gap-2">
                    Category
                    {sortConfig.key === 'category' && (
                      sortConfig.direction === 'desc' ? <SortDesc size={14} /> : <SortAsc size={14} />
                    )}
                  </div>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  RDAP URL
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {paginatedData.map((registrar) => (
                <tr key={registrar.iana_id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                    {registrar.iana_id}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <div className="max-w-xs">
                      <div className="font-medium">{registrar.name}</div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {registrar.domain_count ? (
                      <span className="font-medium">{formatNumber(registrar.domain_count)}</span>
                    ) : (
                      <span className="text-gray-400">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                      getProviderColor(registrar.gateway_provider)
                    }`}>
                      {registrar.gateway_provider || 'Unknown'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {registrar.category ? (
                      <span className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        registrar.category === 'DROPCATCH' 
                          ? 'bg-yellow-100 text-yellow-800'
                          : registrar.category === 'REGISTRAR'
                          ? 'bg-indigo-100 text-indigo-800'
                          : registrar.category === 'SUBSIDIARY'
                          ? 'bg-purple-100 text-purple-800'
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {registrar.category}
                      </span>
                    ) : (
                      <span className="text-gray-400">—</span>
                    )}
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-900">
                    <code className="text-xs bg-gray-100 px-2 py-1 rounded">
                      {registrar.rdap_url}
                    </code>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        {totalPages > 1 && (
          <div className="bg-white px-4 py-3 border-t border-gray-200 sm:px-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <select
                  value={pageSize}
                  onChange={(e) => {
                    setPageSize(Number(e.target.value));
                    setCurrentPage(1);
                  }}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm"
                >
                  <option value={25}>25 per page</option>
                  <option value={50}>50 per page</option>
                  <option value={100}>100 per page</option>
                  <option value={200}>200 per page</option>
                </select>
                
                <span className="text-sm text-gray-700">
                  Showing {((currentPage - 1) * pageSize) + 1} to {Math.min(currentPage * pageSize, sortedData.length)} of {sortedData.length.toLocaleString()} results
                </span>
              </div>

              <div className="flex items-center gap-2">
                <button
                  onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
                  disabled={currentPage === 1}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Previous
                </button>
                
                <span className="text-sm text-gray-700">
                  Page {currentPage} of {totalPages}
                </span>
                
                <button
                  onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
                  disabled={currentPage === totalPages}
                  className="px-3 py-1 border border-gray-300 rounded-md text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  Next
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default RegistryGatewayUsers;