import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthLayout } from './components/AuthLayout';
import DashboardLayout from './components/DashboardLayout';
import { ProtectedRoute } from './components/ProtectedRoute';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import OpenSourceLicensePage from './pages/OpenSourceLicensePage';
import PrivacyPolicyPage from './pages/PrivacyPolicyPage';
import SecurityPage from './pages/SecurityPage';
import TermsPage from './pages/TermsPage';

function App() {
  return (
    <Routes>
      {/* Public Landing Page */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/terms" element={<TermsPage />} />
      <Route path="/privacy" element={<PrivacyPolicyPage />} />
      <Route path="/open-source-license" element={<OpenSourceLicensePage />} />
      <Route path="/security" element={<SecurityPage />} />

      {/* Auth Routes */}
      <Route element={<AuthLayout />}>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
      </Route>

      {/* Protected Dashboard Route */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      />

      {/* Protected Payment Route */}
      {/* <Route
        path="/payment"
        element={
          <ProtectedRoute>
            <PaymentPage />
          </ProtectedRoute>
        }
      /> */}

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;

