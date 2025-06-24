import { useState, useEffect } from 'react';

const useAuth = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already authenticated on app load
  useEffect(() => {
    const checkAuth = () => {
      try {
        const authStatus = localStorage.getItem('rdap_dashboard_auth');
        const authTime = localStorage.getItem('rdap_dashboard_auth_time');
        
        if (authStatus === 'true' && authTime) {
          const sessionTime = parseInt(authTime);
          const currentTime = Date.now();
          const sessionHours = parseInt(process.env.REACT_APP_SESSION_DURATION_HOURS) || 0;
          
          // Check if session is unlimited (0) or still valid
          if (sessionHours === 0) {
            // Unlimited session
            setIsAuthenticated(true);
          } else {
            const sessionDuration = sessionHours * 60 * 60 * 1000; // Convert hours to milliseconds
            
            // Check if session is still valid
            if (currentTime - sessionTime < sessionDuration) {
              setIsAuthenticated(true);
            } else {
              // Session expired, clear storage
              localStorage.removeItem('rdap_dashboard_auth');
              localStorage.removeItem('rdap_dashboard_auth_time');
            }
          }
        }
      } catch (error) {
        console.error('Error checking authentication:', error);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  const login = () => {
    try {
      localStorage.setItem('rdap_dashboard_auth', 'true');
      localStorage.setItem('rdap_dashboard_auth_time', Date.now().toString());
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error storing authentication:', error);
    }
  };

  const logout = () => {
    try {
      localStorage.removeItem('rdap_dashboard_auth');
      localStorage.removeItem('rdap_dashboard_auth_time');
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Error clearing authentication:', error);
    }
  };

  return {
    isAuthenticated,
    isLoading,
    login,
    logout
  };
};

export default useAuth;