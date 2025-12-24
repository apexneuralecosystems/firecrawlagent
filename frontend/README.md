# FireCrawl Agent Frontend

<div align="center">

**Modern React + TypeScript frontend for the FireCrawl Agent RAG Application**

[![React](https://img.shields.io/badge/React-18.2+-61dafb.svg)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2+-3178c6.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646cff.svg)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-3.3+-38bdf8.svg)](https://tailwindcss.com/)

</div>

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Components](#components)
- [Pages](#pages)
- [Services](#services)
- [Development](#development)
- [Building for Production](#building-for-production)
- [Styling](#styling)
- [State Management](#state-management)
- [Routing](#routing)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

The FireCrawl Agent Frontend is a modern, responsive web application built with React and TypeScript. It provides an intuitive interface for interacting with the FireCrawl Agentic RAG Workflow, including document upload, chat interactions, user authentication, and payment processing.

### Key Capabilities

- **Document Management**: Upload and manage PDF documents
- **Chat Interface**: Real-time chat with the RAG agent
- **User Authentication**: Complete auth flow with protected routes
- **Payment Processing**: PayPal integration for subscriptions
- **Newsletter Subscription**: Email subscription functionality
- **Responsive Design**: Mobile-friendly interface with dark mode support
- **Modern UI**: Beautiful, intuitive interface with animations

## ✨ Features

### Core Features
- ✅ **PDF Document Upload**: Drag-and-drop or file picker for PDF uploads
- ✅ **Real-time Chat**: Interactive chat interface for querying documents
- ✅ **Session Management**: View and manage document sessions
- ✅ **Process Details**: View detailed processing information
- ✅ **Welcome Screen**: User-friendly onboarding experience

### User Features
- ✅ **User Authentication**: Sign up, login, password reset
- ✅ **Protected Routes**: Secure access to dashboard
- ✅ **Landing Page**: Beautiful landing page with features showcase
- ✅ **Newsletter Subscription**: Email subscription with confirmation
- ✅ **Payment Integration**: PayPal payment processing
- ✅ **Responsive Design**: Works on desktop, tablet, and mobile
- ✅ **Dark Mode**: Automatic dark mode support

### Developer Features
- ✅ **TypeScript**: Full type safety throughout the application
- ✅ **Hot Reload**: Fast development with Vite HMR
- ✅ **Component Library**: Reusable React components
- ✅ **API Service**: Centralized API client with Axios
- ✅ **Context API**: Global state management with React Context
- ✅ **React Router**: Client-side routing with protected routes

## 🛠️ Tech Stack

### Core Framework
- **React 18.2+** - Modern UI framework with hooks
- **TypeScript 5.2+** - Type-safe development
- **Vite 5.0+** - Fast build tool and dev server

### UI & Styling
- **TailwindCSS 3.3+** - Utility-first CSS framework
- **Framer Motion 12+** - Animation library
- **Lucide React** - Icon library
- **clsx & tailwind-merge** - Conditional class utilities

### Routing & HTTP
- **React Router 7+** - Client-side routing
- **Axios 1.6+** - HTTP client for API communication

### Additional Libraries
- **react-pdf 7.6+** - PDF viewer component (if needed)

## 📦 Prerequisites

- **Node.js 18+** or **Bun 1.0+** (recommended)
- **npm**, **yarn**, or **bun** package manager
- Backend API running at `http://localhost:8000` (or configured URL)

## 🚀 Installation

### 1. Navigate to Frontend Directory
```bash
cd frontend
```

### 2. Install Dependencies

**Option A: Using Bun (Recommended)**
```bash
bun install
```

**Option B: Using npm**
```bash
npm install
```

**Option C: Using yarn**
```bash
yarn install
```

### 3. Set Up Environment Variables

Create a `.env` file in the `frontend/` directory:
```env
VITE_API_URL=http://localhost:8000
```

**Note**: Vite requires the `VITE_` prefix for environment variables to be exposed to the client.

### 4. Verify Installation

Check that all dependencies are installed:
```bash
bun run dev
# Or: npm run dev
```

The application should start at `http://localhost:3000` (or the port shown in terminal).

## ⚙️ Configuration

### Environment Variables

Create `.env` file in the `frontend/` directory:

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API base URL | `http://localhost:8000` |

### API Configuration

The API client is configured in `src/services/api.ts`. Update the base URL if needed:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

### Build Configuration

Build settings are configured in `vite.config.ts`:

```typescript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

## 🏃 Running the Application

### Development Mode

**Using Bun (Recommended):**
```bash
bun run dev
```

**Using npm:**
```bash
npm run dev
```

**Using yarn:**
```bash
yarn dev
```

The application will be available at `http://localhost:3000` (or the port shown in terminal).

### Production Build

**Build the application:**
```bash
bun run build
# Or: npm run build
```

**Preview production build:**
```bash
bun run preview
# Or: npm run preview
```

The built files will be in the `dist/` directory.

### Serve Production Build

After building, serve the `dist/` directory with a web server:

**Using a simple HTTP server:**
```bash
# Python
python -m http.server 3000 -d dist

# Node.js
npx serve -s dist -l 3000
```

**Using nginx:**
```nginx
server {
    listen 3000;
    root /path/to/frontend/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/           # React components
│   │   ├── AuthLayout.tsx   # Authentication layout wrapper
│   │   ├── ChatInterface.tsx # Main chat interface
│   │   ├── DashboardLayout.tsx # Dashboard layout
│   │   ├── MessageBubble.tsx # Chat message component
│   │   ├── ProcessDetails.tsx # Process details viewer
│   │   ├── ProtectedRoute.tsx # Route protection component
│   │   ├── Sidebar.tsx      # Sidebar navigation
│   │   ├── WelcomeScreen.tsx # Welcome/onboarding screen
│   │   └── PaymentComponent.tsx # Payment component
│   ├── pages/               # Page components
│   │   ├── LandingPage.tsx  # Landing/home page
│   │   ├── LoginPage.tsx    # Login page
│   │   ├── SignupPage.tsx   # Signup page
│   │   ├── ForgotPasswordPage.tsx # Password reset page
│   │   └── PaymentPage.tsx  # Payment page
│   ├── services/            # API services
│   │   └── api.ts           # API client with Axios
│   ├── context/             # React context
│   │   └── AuthContext.tsx  # Authentication context
│   ├── App.tsx              # Main app component with routes
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── public/                  # Static assets
├── dist/                    # Production build output
├── node_modules/            # Dependencies
├── package.json             # Dependencies and scripts
├── tsconfig.json            # TypeScript configuration
├── tsconfig.node.json       # TypeScript config for Vite
├── tailwind.config.js       # TailwindCSS configuration
├── postcss.config.js        # PostCSS configuration
├── vite.config.ts           # Vite configuration
└── README.md                # This file
```

## 🧩 Components

### Core Components

#### `AuthLayout`
Wrapper component for authentication pages (login, signup, forgot password).

#### `DashboardLayout`
Main layout for the dashboard with sidebar navigation.

#### `ChatInterface`
Main chat interface component for interacting with documents.

#### `MessageBubble`
Individual chat message component with user/assistant styling.

#### `WelcomeScreen`
Welcome/onboarding screen shown when no document is uploaded.

#### `ProcessDetails`
Component for displaying document processing details.

#### `Sidebar`
Sidebar navigation component with session management.

#### `ProtectedRoute`
Route protection component that requires authentication.

#### `PaymentComponent`
PayPal payment integration component.

## 📄 Pages

### `LandingPage`
Public landing page with features showcase, hero section, and newsletter subscription.

### `LoginPage`
User login page with email/password form.

### `SignupPage`
User registration page with signup form.

### `ForgotPasswordPage`
Password reset request page.

### `PaymentPage`
Payment processing page (if implemented).

## 🔌 Services

### API Service (`src/services/api.ts`)

Centralized API client using Axios:

```typescript
import api from './services/api';

// Upload document
const response = await api.uploadDocument(file);

// Send chat message
const response = await api.chat(sessionId, message);

// Authentication
const response = await api.login(email, password);
```

**Available Methods:**
- `uploadDocument(file)` - Upload PDF document
- `chat(sessionId, message)` - Send chat message
- `getSessions()` - Get all sessions
- `getSession(sessionId)` - Get session details
- `deleteSession(sessionId)` - Delete session
- `login(email, password)` - User login
- `signup(data)` - User registration
- `forgotPassword(email)` - Request password reset
- `resetPassword(token, newPassword)` - Reset password
- `subscribeNewsletter(email)` - Subscribe to newsletter

## 💻 Development

### Development Workflow

1. **Start Development Server:**
```bash
bun run dev
```

2. **Make Changes:**
   - Edit files in `src/`
   - Changes are automatically reflected (HMR)

3. **Check for Errors:**
   - TypeScript errors shown in terminal
   - Browser console for runtime errors

### Adding New Components

1. Create component file in `src/components/`:
```typescript
// src/components/MyComponent.tsx
import React from 'react';

interface MyComponentProps {
  title: string;
}

const MyComponent: React.FC<MyComponentProps> = ({ title }) => {
  return <div>{title}</div>;
};

export default MyComponent;
```

2. Import and use in your pages:
```typescript
import MyComponent from '../components/MyComponent';
```

### Adding New Pages

1. Create page file in `src/pages/`:
```typescript
// src/pages/MyPage.tsx
import React from 'react';

const MyPage: React.FC = () => {
  return <div>My Page</div>;
};

export default MyPage;
```

2. Add route in `src/App.tsx`:
```typescript
import MyPage from './pages/MyPage';

<Route path="/my-page" element={<MyPage />} />
```

### Code Quality

**Linting:**
```bash
bun run lint
# Or: npm run lint
```

**Type Checking:**
```bash
# TypeScript will check types automatically
# Or manually:
npx tsc --noEmit
```

**Formatting:**
Consider using Prettier (if configured):
```bash
npx prettier --write "src/**/*.{ts,tsx}"
```

## 🏗️ Building for Production

### Build Process

1. **Build the Application:**
```bash
bun run build
# Or: npm run build
```

2. **Verify Build:**
```bash
bun run preview
# Or: npm run preview
```

3. **Deploy:**
   - Upload `dist/` directory to your web server
   - Configure server to serve `index.html` for all routes (SPA routing)

### Build Optimization

Vite automatically optimizes the build:
- Code splitting
- Tree shaking
- Minification
- Asset optimization

### Environment-Specific Builds

Create environment-specific `.env` files:
- `.env.development` - Development variables
- `.env.production` - Production variables

## 🎨 Styling

### TailwindCSS

The project uses TailwindCSS for styling. Configure in `tailwind.config.js`:

```javascript
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      // Custom theme extensions
    },
  },
  plugins: [],
}
```

### Global Styles

Global styles are in `src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

/* Custom global styles */
```

### Component Styling

Use Tailwind classes directly in components:

```tsx
<div className="flex items-center justify-center p-4 bg-blue-500 text-white">
  Content
</div>
```

### Dark Mode

Dark mode is automatically supported via Tailwind's dark mode:

```tsx
<div className="bg-white dark:bg-gray-800">
  Content
</div>
```

## 🔄 State Management

### React Context

Authentication state is managed with React Context (`src/context/AuthContext.tsx`):

```typescript
import { useAuth } from '../context/AuthContext';

const MyComponent = () => {
  const { user, login, logout, isAuthenticated } = useAuth();
  
  // Use auth state
};
```

### Local State

Use React hooks for component-local state:

```typescript
const [count, setCount] = useState(0);
const [data, setData] = useState(null);
```

## 🧭 Routing

### Route Configuration

Routes are configured in `src/App.tsx`:

```typescript
<Routes>
  <Route path="/" element={<LandingPage />} />
  <Route path="/login" element={<LoginPage />} />
  <Route path="/dashboard" element={
    <ProtectedRoute>
      <DashboardLayout />
    </ProtectedRoute>
  } />
</Routes>
```

### Protected Routes

Use `ProtectedRoute` component to protect routes:

```typescript
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <DashboardLayout />
    </ProtectedRoute>
  }
/>
```

### Navigation

Use React Router's `Link` or `useNavigate`:

```typescript
import { Link, useNavigate } from 'react-router-dom';

// Using Link
<Link to="/dashboard">Dashboard</Link>

// Using navigate
const navigate = useNavigate();
navigate('/dashboard');
```

## 🐛 Troubleshooting

### Common Issues

1. **Port Already in Use**
   - Change port in `vite.config.ts`:
   ```typescript
   server: {
     port: 3001,
   }
   ```

2. **API Connection Errors**
   - Verify backend is running at `VITE_API_URL`
   - Check CORS configuration in backend
   - Verify network connectivity

3. **Build Errors**
   - Clear `node_modules` and reinstall:
   ```bash
   rm -rf node_modules
   bun install
   ```
   - Clear Vite cache:
   ```bash
   rm -rf node_modules/.vite
   ```

4. **TypeScript Errors**
   - Run type check: `npx tsc --noEmit`
   - Check `tsconfig.json` configuration
   - Ensure all types are properly defined

5. **Styling Issues**
   - Verify TailwindCSS is properly configured
   - Check `tailwind.config.js` content paths
   - Ensure PostCSS is configured

6. **Hot Reload Not Working**
   - Restart dev server
   - Clear browser cache
   - Check file watcher limits (Linux)

### Debug Tips

1. **Browser DevTools**
   - Use React DevTools extension
   - Check Network tab for API calls
   - Use Console for debugging

2. **Vite DevTools**
   - Check terminal for build errors
   - Use Vite's error overlay in browser

3. **TypeScript**
   - Enable strict mode in `tsconfig.json`
   - Use type assertions carefully
   - Check for `any` types

## 📚 Additional Resources

- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/)
- [Vite Documentation](https://vitejs.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/)
- [React Router Documentation](https://reactrouter.com/)
- [Axios Documentation](https://axios-http.com/)

## 🚀 Deployment

### Static Hosting

The frontend can be deployed to any static hosting service:

- **Vercel**: Connect GitHub repo, auto-deploy
- **Netlify**: Drag and drop `dist/` folder
- **GitHub Pages**: Deploy `dist/` to gh-pages branch
- **AWS S3 + CloudFront**: Upload to S3, serve via CloudFront
- **Firebase Hosting**: Use Firebase CLI to deploy

### Deployment Steps

1. **Build the application:**
```bash
bun run build
```

2. **Upload `dist/` directory** to your hosting service

3. **Configure routing:**
   - Ensure all routes serve `index.html` (SPA routing)
   - Configure redirects if needed

4. **Set environment variables:**
   - Update `VITE_API_URL` to production API URL
   - Rebuild if environment variables changed

---

<div align="center">

**Built with React, TypeScript, and TailwindCSS**

[Back to Main README](../README.md) • [Backend README](../backend/README.md)

</div>
