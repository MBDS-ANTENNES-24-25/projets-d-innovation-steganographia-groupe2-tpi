import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { useParams, useNavigate } from 'react-router-dom';
import { Logo, BackgroundElements, Input, LoadingButton } from '@components';
import { zodResolver } from '@hookform/resolvers/zod';
import { resetPassword } from '@api/authApi';
import { z } from 'zod';
import '@styles/pages/Auth.css';

const resetPasswordSchema = z.object({
  new_password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/, 
      'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character'),
  confirm_password: z.string()
}).refine((data) => data.new_password === data.confirm_password, {
  message: "Passwords don't match",
  path: ["confirm_password"],
});

const ResetPassword = () => {
  const { token } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(resetPasswordSchema),
    mode: 'onBlur'
  });

  useEffect(() => {
    // Extract email from JWT token if possible
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload.email) {
          setUserEmail(payload.email);
        }
      } catch (error) {
        console.log('Could not extract email from token');
      }
    }
  }, [token]);

  const onSubmit = async (data) => {
    document.activeElement?.blur();
    setError('');
    setLoading(true);
    
    try {
      await resetPassword(token, data.new_password);
      setSuccess(true);
    } catch (error) {
      setError(error.response?.data?.err || 'Failed to reset password');
    } finally {
      setLoading(false);
    }
  };

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
              <h2 className="!text-green-600 mb-4">Password Reset Successful!</h2>
              <div className='text-sm'>
                <p className="mb-4">Your password has been successfully reset.</p>
                <p className="mb-6">You can now sign in with your new password.</p>
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
        {/* Logo/Title */}
        <div className="auth-header mb-8">
          <Logo size={3} />
          <p className='text-center text-silver-blue-950'>Secure Image Steganography Platform</p>
        </div>

        <div className="auth-form">
          <h2>Reset Password</h2>
          {userEmail && (
            <p className="auth-subtitle mb-4">
              Reset password for: <span className="font-semibold text-gray-700">{userEmail}</span>
            </p>
          )}
          <p className="auth-subtitle">Enter your new password below</p>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <Input
                type="password"
                placeholder="New password"
                {...register('new_password')}
                error={errors.new_password?.message}
              />
            </div>

            <div>
              <Input
                type="password"
                placeholder="Confirm new password"
                {...register('confirm_password')}
                error={errors.confirm_password?.message}
              />
            </div>

            {error && (
              <div className="text-red-500 text-sm text-center">
                {error}
              </div>
            )}

            <LoadingButton
              type="submit"
              className="w-full"
              defaultText="Reset Password"
              loadingText="Resetting..."
              loading={loading}
              spinnerSize={4}
            />
          </form>

          <div className="auth-footer">
            <p>Remember your password?</p>
            <button 
              onClick={() => navigate('/login')}
              className="link"
            >
              Sign in here
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword; 