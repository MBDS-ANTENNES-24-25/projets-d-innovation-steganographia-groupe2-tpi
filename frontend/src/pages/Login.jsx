import React, { useState } from 'react';
import { useForm } from 'react-hook-form';
import { useNavigate, Link } from 'react-router-dom';
import { Logo, BackgroundElements, GoogleIcon, Input, LoadingButton } from '@components';
import { tokenTypeAtom, accessTokenAtom } from '@atoms/authAtoms';
import { zodResolver } from '@hookform/resolvers/zod';
import { login, googleLogin } from '@api/authApi';
import { loginSchema } from '@schemas/loginSchema';
import { useAtom } from 'jotai';
import '@styles/pages/Auth.css';

const Login = () => {
  const [, setTokenType] = useAtom(tokenTypeAtom);
  const [, setAccessToken] = useAtom(accessTokenAtom);

  const [loading, setLoading] = useState(false);
  const [googleAuthLoading, setGoogleAuthLoading] = useState(false);
  const [loginError, setLoginError] = useState('');
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(loginSchema)
  });

  const onLoginSubmit = async (data) => {
    document.activeElement?.blur();
    setLoginError('');
    setLoading(true);
    
    try {
      let res = await login(data.email, data.password);
      setTokenType(res.data.token_type);
      setAccessToken(res.data.access_token);

      navigate('/dashboard');

    } catch (error) {
      setLoginError(error.response?.data?.err || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    setGoogleAuthLoading(true);
    setLoginError('');
    
    try {
      const res = await googleLogin();
      window.location.href = res.data.auth_url;
    } catch (error) {
      setLoginError(error.response?.data?.err || 'Failed to initiate Google login');
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
          <h2>Welcome Back</h2>
          <p className="auth-subtitle">Sign in to continue to your dashboard</p>

          {/* Google Login Button Start */}
          <LoadingButton 
            type="button"
            className="google-auth-btn" 
            defaultText={googleAuthButtonDefaultText}
            loadingText="Connecting to Google..."
            loading={googleAuthLoading}
            spinnerSize={4}
            onClick={handleGoogleLogin}
          />
          {/* Google Login Button End */}


          {/* Divider Start */}
          <div className="divider !my-12">
            <span>or</span>
          </div>
          {/* Divider End */}


          {/* Login Form Start */}
          <form 
            className="text-left" 
            onSubmit={handleSubmit(onLoginSubmit)}
          >

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
              className="mb-6" 
            />

            {loginError && (
              <div className="p-4 mb-4 text-sm text-red-500 border border-red-500 rounded-lg bg-red-50 dark:bg-gray-800 dark:text-red-400" role="alert">
                {loginError}
              </div>
            )}

            <LoadingButton 
              type="submit" 
              className="btn btn-primary w-full !py-3" 
              defaultText="Sign In"
              loadingText="Signing In..."
              loading={loading}
              spinnerSize={4}
            />

          </form>
          {/* Login Form End */}

          <br />

          {/* Footer Links Start */}
          <div className="auth-footer">
            <p>Don't have an account? <Link to="/register" className="link">Sign up</Link></p>
            <p><Link to="/forgot-password" className="link">Forgot password?</Link></p>
          </div>
          {/* Footer Links End */}
        </div>
      </div>
    </div>
  );
};

export default React.memo(Login);
