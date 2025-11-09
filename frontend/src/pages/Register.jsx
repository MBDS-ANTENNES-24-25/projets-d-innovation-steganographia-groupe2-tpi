import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { Link } from 'react-router-dom';
import { Logo, BackgroundElements, GoogleIcon, Input, LoadingButton } from '@components';
import { zodResolver } from '@hookform/resolvers/zod';
import { register as registerApi, googleLogin } from '@api/authApi';
import { registerSchema } from '@schemas/registerSchema';
import '@styles/pages/Auth.css';

const Register = () => {
  const [loading, setLoading] = useState(false);
  const [googleAuthLoading, setGoogleAuthLoading] = useState(false);
  const [registerError, setRegisterError] = useState('');
  const [registerSuccess, setRegisterSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(registerSchema),
    mode: 'onBlur'
  });

  const onRegisterSubmit = async (data) => {
    document.activeElement?.blur();
    setRegisterError('');
    setLoading(true);
    
    try {
      await registerApi(data.firstname, data.lastname, data.username, data.email, data.password);

      setRegisterSuccess(true);
    } catch (error) {
      setRegisterError(error.response?.data?.err || 'An error occurred during registration');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleRegister = async () => {
    setGoogleAuthLoading(true);
    setRegisterError('');
    
    try {
      const res = await googleLogin();
      window.location.href = res.data.auth_url;
    } catch (error) {
      setRegisterError(error.response?.data?.err || 'Failed to initiate Google registration');
      setGoogleAuthLoading(false);
    }
  };

  const googleAuthButtonDefaultText = (
    <>
      <div className="google-icon">
        <GoogleIcon width={20} height={20} />
      </div>
      Continue with Google
    </>
  );

  if (registerSuccess) {
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
              <h2 className="!text-green-600 mb-4">Registration Successful!</h2>
              <div className='text-sm'>
                <p className="mb-4">A confirmation email has been sent to your email address.</p>
                <p className="mb-6">Please check your inbox and confirm your account to complete the registration process.</p>
                <p className="mb-4">If your account is already confirmed, you can now sign in.</p>
              </div>
              
              <Link to="/login" className="link">
                Go to Login
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
          <h2>Create Account</h2>
          <p className="auth-subtitle">Join us to start securing your images</p>

          {/* Google Register Button Start */}
          <LoadingButton 
            type="button"
            className="google-auth-btn" 
            defaultText={googleAuthButtonDefaultText}
            loadingText="Connecting to Google..."
            loading={googleAuthLoading}
            spinnerSize={4}
            onClick={handleGoogleRegister}
          />
          {/* Google Register Button End */}

          {/* Divider Start */}
          <div className="divider !my-8">
            <span>or</span>
          </div>
          {/* Divider End */}

          {/* Register Form Start */}
          <form 
            className="text-left" 
            onSubmit={handleSubmit(onRegisterSubmit)}
          >
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <Input 
                type="text" 
                label="First Name" 
                placeholder="First Name" 
                {...register('firstname')}
                errorMessage={errors.firstname?.message} 
              />
              <Input 
                type="text" 
                label="Last Name" 
                placeholder="Last Name" 
                {...register('lastname')}
                errorMessage={errors.lastname?.message} 
              />
            </div>

            <Input 
              type="text" 
              label="Username" 
              placeholder="Username" 
              {...register('username')}
              errorMessage={errors.username?.message} 
              className="mb-4" 
            />

            <Input 
              type="email" 
              label="Email" 
              placeholder="Email" 
              {...register('email')}
              errorMessage={errors.email?.message} 
              className="mb-4" 
            />

            <Input 
              type="password" 
              label="Password" 
              placeholder="Password" 
              {...register('password')}
              errorMessage={errors.password?.message} 
              className="mb-4" 
            />

            <Input 
              type="password" 
              label="Confirm Password" 
              placeholder="Confirm Password" 
              {...register('confirmPassword')}
              errorMessage={errors.confirmPassword?.message} 
              className="mb-6" 
            />

            {registerError && (
              <div className="p-4 mb-4 text-sm text-red-500 border border-red-500 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                {registerError}
              </div>
            )}

            <LoadingButton 
              type="submit" 
              className="btn btn-primary w-full !py-3" 
              defaultText="Create Account"
              loadingText="Creating Account..."
              loading={loading}
              spinnerSize={4}
            />

          </form>
          {/* Register Form End */}

          <br />

          {/* Footer Links Start */}
          <div className="auth-footer">
            <p>Already have an account? <Link to="/login" className="link">Sign in</Link></p>
          </div>
          {/* Footer Links End */}
        </div>
      </div>
    </div>
  );
};

export default React.memo(Register);
