import { axiosInstance, axiosInstanceWithoutResponseIntercept } from './axiosInstance';

export const login = (email, password) => {
  return axiosInstanceWithoutResponseIntercept.post('/auth/login', { 
    email: email, 
    password: password 
  });
};

export const register = (firstname, lastname, username, email, password) => {
  return axiosInstanceWithoutResponseIntercept.post('/auth/register', {
    firstname: firstname,
    lastname: lastname,
    username: username,
    email: email,
    password: password
  });
};

export const refreshToken = () => axiosInstanceWithoutResponseIntercept.post('/auth/refresh');

export const logout = () => axiosInstanceWithoutResponseIntercept.post('/auth/logout');

export const getMe = () => axiosInstance.get('/auth/me');

export const googleLogin = () => axiosInstance.get("/auth/google/login");

export const googleCallback = (code) => axiosInstance.get(`/auth/google/callback?code=${code}`);

export const confirmEmail = (token) => {
  return axiosInstanceWithoutResponseIntercept.post('/auth/confirm-email', null, {
    params: { token }
  });
};

export const forgotPassword = (email) => {
  return axiosInstanceWithoutResponseIntercept.post('/auth/forgot-password', {
    email: email
  });
};

export const resetPassword = (token, newPassword) => {
  return axiosInstanceWithoutResponseIntercept.post('/auth/reset-password', {
    token: token,
    new_password: newPassword
  });
};

