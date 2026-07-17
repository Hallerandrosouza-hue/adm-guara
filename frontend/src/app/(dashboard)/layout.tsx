// Dashboard layout — server component (no 'use client')
import { DashboardLayoutClient } from "./dashboard-layout-client";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return <DashboardLayoutClient>{children}</DashboardLayoutClient>;
}
