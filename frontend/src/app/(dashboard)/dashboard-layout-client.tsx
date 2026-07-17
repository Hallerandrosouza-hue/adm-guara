"use client";

import { useState } from "react";
import { Sidebar } from "./layout/sidebar";
import { Header } from "./layout/header";

export function DashboardLayoutClient({
  children,
}: {
  children: React.ReactNode;
}) {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Suppress unused warning — will be used with mobile drawer
  void mobileMenuOpen;

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      {/* Sidebar desktop */}
      <div className="hidden lg:flex">
        <Sidebar />
      </div>

      {/* Main content */}
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header setMobileMenuOpen={setMobileMenuOpen} />

        <main className="flex-1 overflow-y-auto bg-muted/30 p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl h-full">{children}</div>
        </main>
      </div>
    </div>
  );
}
