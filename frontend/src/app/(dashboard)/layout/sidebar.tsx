"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, FolderKanban, CheckSquare, Users, Settings, LogOut, ChevronLeft, ChevronRight, UserCircle, Landmark, Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/providers/auth-provider";
import { useState } from "react";

const navItems = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Projetos", href: "/projects", icon: FolderKanban },
  { name: "Tarefas", href: "/tasks", icon: CheckSquare },
  { name: "CRM", href: "/crm", icon: Users },
  { name: "Recursos Humanos", href: "/hr", icon: UserCircle },
  { name: "Financeiro", href: "/finance", icon: Landmark },
  { name: "Sites", href: "/sites", icon: Globe },
  { name: "Configurações", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuth();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside
      className={cn(
        "bg-card border-r border-border h-screen sticky top-0 flex flex-col transition-all duration-300 z-20",
        collapsed ? "w-20" : "w-64"
      )}
    >
      <div className="flex h-16 items-center justify-between px-4 border-b border-border">
        {!collapsed && (
          <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-orange-500 truncate">
            Guará Manager
          </span>
        )}
        {collapsed && (
          <span className="text-xl font-bold text-primary mx-auto">GM</span>
        )}
      </div>

      <div className="flex-1 overflow-y-auto py-4">
        <nav className="space-y-1 px-3">
          {navItems.map((item) => {
            const isActive = pathname.startsWith(item.href);
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  "flex items-center rounded-md px-3 py-2.5 text-sm font-medium transition-colors group relative",
                  isActive
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-accent hover:text-accent-foreground"
                )}
                title={collapsed ? item.name : undefined}
              >
                <item.icon className={cn("flex-shrink-0", collapsed ? "h-6 w-6 mx-auto" : "h-5 w-5 mr-3")} />
                {!collapsed && <span>{item.name}</span>}
                {isActive && !collapsed && (
                  <span className="absolute right-2 w-1.5 h-1.5 rounded-full bg-primary" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      <div className="p-4 border-t border-border space-y-2">
         <button
            onClick={() => setCollapsed(!collapsed)}
            className={cn(
              "flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-muted-foreground hover:bg-accent hover:text-accent-foreground transition-colors",
               collapsed && "justify-center"
            )}
          >
            {collapsed ? <ChevronRight className="h-5 w-5" /> : <><ChevronLeft className="h-5 w-5 mr-3" /> Recolher</>}
          </button>
        <button
          onClick={logout}
          className={cn(
            "flex w-full items-center rounded-md px-3 py-2 text-sm font-medium text-destructive hover:bg-destructive/10 transition-colors",
             collapsed && "justify-center"
          )}
          title={collapsed ? "Sair" : undefined}
        >
          <LogOut className={cn("flex-shrink-0", collapsed ? "h-5 w-5" : "h-5 w-5 mr-3")} />
          {!collapsed && <span>Sair</span>}
        </button>
      </div>
    </aside>
  );
}
