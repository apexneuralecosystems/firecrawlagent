import { createContext, ReactNode, useContext, useEffect, useState } from 'react';
import { login as apiLogin, signup as apiSignup, getMe, User } from '../services/api';

interface AuthContextType {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    login: (credentials: any) => Promise<void>;
    signup: (data: any) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    // Initialize auth state from local storage
    useEffect(() => {
        const initAuth = async () => {
            const token = localStorage.getItem('access_token');
            if (token) {
                try {
                    const userData = await getMe();
                    setUser(userData);
                    setIsAuthenticated(true);
                } catch (error) {
                    console.error("Failed to fetch user on init", error);
                    logout();
                }
            }
            setIsLoading(false);
        };

        initAuth();
    }, []);

    const login = async (credentials: any) => {
        const data = await apiLogin(credentials);
        localStorage.setItem('access_token', data.access_token);
        // If backend returns user object in login response, use it, otherwise fetch me
        if (data.user) {
            setUser(data.user);
        } else {
            const userData = await getMe();
            setUser(userData);
        }
        setIsAuthenticated(true);
    };

    const signup = async (data: any) => {
        await apiSignup(data);
        // Auto login after signup? Or require manual login?
        // For now, let's require manual login or assume the caller handles redirect
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        setUser(null);
        setIsAuthenticated(false);
    };

    return (
        <AuthContext.Provider value={{ user, isAuthenticated, isLoading, login, signup, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
