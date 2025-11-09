import { z } from 'zod';

export const registerSchema = z.object({
  firstname: z.string()
    .min(1, 'First name is required')
    .min(2, 'First name must be at least 2 characters')
    .max(100, 'First name must be less than 100 characters'),

  lastname: z.string()
    .min(1, 'Last name is required')
    .min(2, 'Last name must be at least 2 characters')
    .max(100, 'Last name must be less than 100 characters'),

  username: z.string()
    .min(1, 'Username is required')
    .min(3, 'Username must be at least 3 characters')
    .max(30, 'Username must be less than 30 characters')
    .regex(/^[a-zA-Z0-9_]+$/, 'Username can only contain letters, numbers, and underscores'),
  
  email: z.string()
    .min(1, 'Email is required')
    .email('Please enter a valid email address'),
  
  password: z.string()
    .min(1, 'Password is required')
    .min(8, 'Password must be at least 8 characters')
    .regex(/(?=.*[a-z])/, 'Password must contain at least one lowercase letter')
    .regex(/(?=.*[A-Z])/, 'Password must contain at least one uppercase letter')
    .regex(/(?=.*\d)/, 'Password must contain at least one number')
    .regex(/(?=.*[@$!%*?&])/, 'Password must contain at least one special character'),
  
  confirmPassword: z.string()
    .min(1, 'Please confirm your password')
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword']
});
