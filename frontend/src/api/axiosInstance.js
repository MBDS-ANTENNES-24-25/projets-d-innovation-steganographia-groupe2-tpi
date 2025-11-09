import axios from 'axios';
import { getDefaultStore } from 'jotai';
import { tokenTypeAtom, accessTokenAtom, userInfoAtom, authHeaderAtom, logoutAtom } from '@atoms/authAtoms';
import { refreshToken, getMe } from './authApi';


const store = getDefaultStore();

const createAxiosInstance = (interceptRes = true) => {
    const axiosInstance = axios.create({
        baseURL: `${import.meta.env.VITE_API_BASE_URL}`,
        withCredentials: true,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
    });

    // Request interceptor to add auth token
    axiosInstance.interceptors.request.use(
        (config) => {
            const authHeader = store.get(authHeaderAtom);
            if (authHeader) {
                config.headers.Authorization = authHeader;
            }
            return config;
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    if (interceptRes) {

        // Response interceptor to handle token expiration
        axiosInstance.interceptors.response.use(
            (response) => response,
            async (error) => {
                const originalRequest = error.config;

                if (error.response?.status === 401 && !originalRequest._retry) {
                    originalRequest._retry = true;

                    try {
                        const tokenRes = await refreshToken();
                        store.set(accessTokenAtom, tokenRes.data.access_token);
                        store.set(tokenTypeAtom, tokenRes.data.token_type);
                        
                        const userRes = await getMe();
                        const newUser = userRes.data;
                        store.set(userInfoAtom, newUser);

                        if (originalRequest.url === '/auth/me') {
                            return Promise.resolve({ data: newUser });
                        } else {
                            const authHeader = store.get(authHeaderAtom);
                            originalRequest.headers.Authorization = authHeader;
                            return axiosInstance(originalRequest);
                        }
                        

                    } catch (tokenRefreshError) {
                        store.set(logoutAtom);
                        return Promise.reject(tokenRefreshError);
                    }
                }

                return Promise.reject(error);
            }
        );
    }

    return axiosInstance;
};

const axiosInstance = createAxiosInstance();

const axiosInstanceWithoutResponseIntercept = createAxiosInstance(false);

export { axiosInstance, axiosInstanceWithoutResponseIntercept };
