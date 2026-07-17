"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import { api } from "@/lib/api";

type User = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  avatar_url: string | null;
  tenant_name: string;
};

type AuthContextType = {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        if (token === "demo-token") {
          // Mock user for presentation mode
          setUser({
            id: "1",
            email: "admin@teste.com",
            first_name: "Admin",
            last_name: "Teste",
            role: "admin",
            avatar_url: null,
            tenant_name: "Teste SaaS",
          });
        } else {
          try {
            const response = await api.get("/auth/me");
            setUser(response.data);
          } catch {
            localStorage.removeItem("token");
            setUser(null);
          }
        }
      } else {
        setUser(null);
      }
      setIsLoading(false);
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (!isLoading) {
      const isAuthPage =
        pathname.startsWith("/login") || pathname.startsWith("/register");
      if (!user && !isAuthPage) {
        router.push("/login");
      }
    }
  }, [user, isLoading, pathname, router]);

  const login = (token: string) => {
    localStorage.setItem("token", token);
    window.location.href = "/dashboard";
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    router.push("/login");
  };

  return (
    <AuthContext.Provider
      value={{ user, isAuthenticated: !!user, isLoading, login, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
