"use client";

import { Sidebar } from "./sidebar";
import { Header } from "./header";
import { useState } from "react";
import { AuthProvider } from "@/providers/auth-provider";
import { QueryProvider } from "@/providers/query-provider";
import { ThemeProvider } from "@/providers/theme-provider";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
      <QueryProvider>
        <AuthProvider>
          <div className="flex h-screen bg-background text-foreground overflow-hidden">
            <div className="hidden lg:flex">
                <Sidebar />
            </div>
            
            {/* Mobile menu could be implemented here using a Dialog/Drawer */}
            
            <div className="flex flex-1 flex-col overflow-hidden">
              <Header setMobileMenuOpen={setMobileMenuOpen} />
              
              <main className="flex-1 overflow-y-auto bg-muted/30 p-4 sm:p-6 lg:p-8">
                <div className="mx-auto max-w-7xl h-full">
                    {children}
                </div>
              </main>
            </div>
          </div>
        </AuthProvider>
      </QueryProvider>
    </ThemeProvider>
  );
}
