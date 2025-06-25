import React, { useState } from 'react';
import GatewayComparison from './components/GatewayComparison';
import RegistryGatewayUsers from './components/RegistryGatewayUsers';
import LoginScreen from './components/LoginScreen';
import Header from './components/Header';
import useAuth from './hooks/useAuth';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const { isAuthenticated, isLoading, login, logout } = useAuth();

  // Show loading spinner while checking authentication
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  // Show login screen if not authenticated
  if (!isAuthenticated) {
    return <LoginScreen onLogin={login} />;
  }

  // Show main dashboard if authenticated
  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header with logout */}
      <Header onLogout={logout} />
      
      {/* Navigation */}
      <div className="bg-white shadow-sm border-t">
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
          <div className="max-w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <RegistryGatewayUsers />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
