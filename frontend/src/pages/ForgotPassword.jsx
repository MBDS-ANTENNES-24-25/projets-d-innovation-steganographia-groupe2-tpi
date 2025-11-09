import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { Logo, BackgroundElements, Input, LoadingButton } from '@components';
import { zodResolver } from '@hookform/resolvers/zod';
import { forgotPassword } from '@api/authApi';
import { z } from 'zod';
import '@styles/pages/Auth.css';

const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address')
});

const ForgotPassword = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(forgotPasswordSchema),
    mode: 'onBlur'
  });

  const onSubmit = async (data) => {
    document.activeElement?.blur();
    setError('');
    setLoading(true);
    
    try {
      await forgotPassword(data.email);
      setSuccess(true);
    } catch (error) {
      setError(error.response?.data?.err || 'An error occurred while sending the reset email');
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
              <h2 className="!text-green-600 mb-4">Reset Email Sent!</h2>
              <div className='text-sm'>
                <p className="mb-4">A password reset link has been sent to your email address.</p>
                <p className="mb-6">Please check your inbox and click on the reset link to create a new password.</p>
                <p className="mb-4">If you don't see the email, please check your spam folder.</p>
              </div>
              
              <Link to="/login" className="link">
                Back to Login
              </Link>
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
          <h2>Forgot Password</h2>
          <p className="auth-subtitle">Enter your email to receive a password reset link</p>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
            <div>
              <Input
                type="email"
                placeholder="Enter your email address"
                {...register('email')}
                error={errors.email?.message}
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
              defaultText="Send Reset Email"
              loadingText="Sending..."
              loading={loading}
              spinnerSize={4}
            />
          </form>

          <div className="auth-footer">
            <p>Remember your password?</p>
            <Link to="/login" className="link">
              Sign in here
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword; 