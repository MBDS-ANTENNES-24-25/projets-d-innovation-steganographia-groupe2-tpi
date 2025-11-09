import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAtom } from 'jotai';
import { refreshToken, getMe } from '@api/authApi';
import { tokenTypeAtom, accessTokenAtom, userInfoAtom, isAuthenticatedAtom, logoutAtom  } from '../../atoms/authAtoms';

const ProtectedRoute = ({ children }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [isAuthenticated] = useAtom(isAuthenticatedAtom);
  const [, setLogout] = useAtom(logoutAtom);
  const [, setTokenType] = useAtom(tokenTypeAtom);
  const [, setAccessToken] = useAtom(accessTokenAtom);
  const [, setUserInfo] = useAtom(userInfoAtom);
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {   
        if (!isAuthenticated) {
          const tokenRes = await refreshToken();
          setTokenType(tokenRes.data.token_type);
          setAccessToken(tokenRes.data.access_token);
        }
        
        const userRes = await getMe();
        setUserInfo(userRes.data);

        setIsLoading(false);
      } catch (error) {
        setLogout();
        navigate('/login');
      }
    };

    checkAuth();
  }, [navigate]);

  return (
    <>
      {isLoading ? (
        <div className="min-h-screen flex items-center justify-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-silver-blue-800"></div>
        </div>
      ) : (
        children
      )}
    </>
  );
};

export default React.memo(ProtectedRoute);