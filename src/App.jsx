import React, { useState } from 'react';
import GatewayComparison from './components/GatewayComparison';
import RegistryGatewayUsers from './components/RegistryGatewayUsers';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Navigation */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`py-4 px-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'dashboard'
                  ? 'text-blue-600 border-blue-600'
                  : 'text-gray-500 border-transparent hover:text-gray-700'
              }`}
            >
              RDAP Analysis Dashboard
            </button>
            <button
              onClick={() => setActiveTab('registrars')}
              className={`py-4 px-2 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'registrars'
                  ? 'text-blue-600 border-blue-600'
                  : 'text-gray-500 border-transparent hover:text-gray-700'
              }`}
            >
              Registry Gateway Users
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-full">
        {activeTab === 'dashboard' && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <GatewayComparison />
          </div>
        )}
        {activeTab === 'registrars' && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <RegistryGatewayUsers />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
