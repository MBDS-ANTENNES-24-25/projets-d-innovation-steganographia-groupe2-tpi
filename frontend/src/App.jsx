import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import { Login, Register, Dashboard, SignImage, VerifyImage, MySignatures, MyVerifications, Profile, GoogleCallback, ConfirmEmail, ForgotPassword, ResetPassword } from '@pages';
import { ProtectedRoute } from '@components';

function App() {
  return (
    <Router>
      <Routes>
        {/* Public routes */}
        <Route path="/" element={<Navigate to="/login" replace />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:token" element={<ResetPassword />} />
        <Route path="/confirm-email/:token" element={<ConfirmEmail />} />
        <Route path="/google/callback" element={<GoogleCallback />} />
        
        {/* Protected routes */}
        <Route path="/dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
        <Route path="/sign-image" element={
          <ProtectedRoute>
            <SignImage />
          </ProtectedRoute>
        } />
        <Route path="/verify-image" element={
          <ProtectedRoute>
            <VerifyImage />
          </ProtectedRoute>
        } />
        <Route path="/my-signatures" element={
          <ProtectedRoute>
            <MySignatures />
          </ProtectedRoute>
        } />
        <Route path="/my-verifications" element={
          <ProtectedRoute>
            <MyVerifications />
          </ProtectedRoute>
        } />
        <Route path="/profile" element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

export default App;
