import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAtom } from 'jotai';
import { tokenTypeAtom, accessTokenAtom } from '@atoms/authAtoms';
import { googleCallback } from '@api/authApi';
import { Logo, BackgroundElements } from '@components';
import '@styles/pages/Auth.css';

const GoogleCallback = () => {
  const [, setTokenType] = useAtom(tokenTypeAtom);
  const [, setAccessToken] = useAtom(accessTokenAtom);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const handleCallback = async () => {
      try {
        const urlParams = new URLSearchParams(location.search);
        const code = urlParams.get('code');
        const error = urlParams.get('error');

        if (error) {
          throw new Error('Google authentication was cancelled or failed');
        }

        if (!code) {
          throw new Error('No authorization code received from Google');
        }

        const res = await googleCallback(code);
        setTokenType( res.data.token_type);
        setAccessToken(res.data.access_token);

        navigate('/dashboard', { replace: true });

      } catch (err) {
        console.error('Google callback error:', err);
        setError(err.response?.data?.err || err.message || 'Authentication failed');
        setLoading(false);
        
        setTimeout(() => {
          navigate('/login', { replace: true });
        }, 3000);
      }
    };

    handleCallback();
  }, [location.search, navigate, setTokenType, setAccessToken]);

  return (
    <div className="auth-container">
      <BackgroundElements />
      
      <div className="glassmorphic-card w-xl">
        {/* Logo/Title */}
        <div className="auth-header mb-8">
          <Logo size={3} />
          <p className='text-center text-silver-blue-950'>Secure Image Steganography Platform</p>
        </div>

        <div className="auth-form text-center">
          {loading && !error && (
            <>
              <div className="flex justify-center mb-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
              </div>
              <h2>Completing Google Sign In...</h2>
              <p className="text-gray-600">Please wait while we complete your authentication.</p>
            </>
          )}

          {error && (
            <>
              <div className="text-red-500 mb-4">
                <svg className="w-12 h-12 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z" />
                </svg>
              </div>
              <h2 className="text-red-500">Authentication Failed</h2>
              <p className="text-gray-600 mb-4">{error}</p>
              <p className="text-sm text-gray-500">Redirecting to login page...</p>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default React.memo(GoogleCallback);
