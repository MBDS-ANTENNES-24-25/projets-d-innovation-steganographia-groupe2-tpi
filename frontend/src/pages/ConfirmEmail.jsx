import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Logo, BackgroundElements } from '@components';
import { confirmEmail } from '@api/authApi';
import '@styles/pages/Auth.css';

const ConfirmEmail = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const confirmUserEmail = async () => {
      if (!token) {
        setError('Invalid confirmation link');
        setLoading(false);
        return;
      }

      try {
        await confirmEmail(token);
        setSuccess(true);
      } catch (error) {
        setError(error.response?.data?.err || 'Failed to confirm email');
      } finally {
        setLoading(false);
      }
    };

    confirmUserEmail();
  }, [token]);

  if (loading) {
    return (
      <div className="auth-container">
        <BackgroundElements />
        
        <div className="glassmorphic-card w-xl">
          <div className="auth-header mb-8">
            <Logo size={3} />
            <p className='text-center text-silver-blue-950'>Secure Image Steganography Platform</p>
          </div>

          <div className="auth-form text-center">
            <div className="p-6 text-gray-600">
              <h2 className="mb-4">Confirming your email...</h2>
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900 mx-auto"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (success) {
    return (
      <div className="auth-container">
        <BackgroundElements />
        
        <div className="glassmorphic-card w-xl">
          <div className="auth-header mb-8">
            <Logo size={3} />
            <p className='text-center text-silver-blue-950'>Secure Image Steganography Platform</p>
          </div>

          <div className="auth-form text-center">
            <div className="p-6 text-gray-600">
              <h2 className="!text-green-600 mb-4">Email Confirmed Successfully!</h2>
              <div className='text-sm'>
                <p className="mb-4">Your email has been confirmed and your account is now active.</p>
                <p className="mb-6">You can now sign in to your account.</p>
              </div>
              
              <button 
                onClick={() => navigate('/login')}
                className="btn btn-primary"
              >
                Go to Login
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-container">
      <BackgroundElements />
      
      <div className="glassmorphic-card w-xl">
        <div className="auth-header mb-8">
          <Logo size={3} />
          <p className='text-center text-silver-blue-950'>Secure Image Steganography Platform</p>
        </div>

        <div className="auth-form text-center">
          <div className="p-6 text-gray-600">
            <h2 className="!text-red-600 mb-4">Email Confirmation Failed</h2>
            <div className='text-sm'>
              <p className="mb-4">{error}</p>
              <p className="mb-6">Please try again or contact support if the problem persists.</p>
            </div>
            
            <button 
              onClick={() => navigate('/login')}
              className="btn btn-primary"
            >
              Go to Login
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ConfirmEmail; 