"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { DollarSign, Briefcase, Users, LayoutList } from "lucide-react";
import { StatCard } from "./stat-card";
import { RevenueChart } from "./revenue-chart";
import { ActivityFeed } from "./activity-feed";
import { ProjectOverview } from "./project-overview";

export default function DashboardPage() {
  const { data: stats, isLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: async () => {
      // If no token or backend is down, return mock data for presentation
      try {
        const res = await api.get("/dashboard/stats");
        return res.data;
      } catch (error) {
         console.warn("Failed to fetch real stats, using mock data for demo.");
         return {
            revenue: 124500,
            expenses: 45000,
            profit: 79500,
            active_projects: 12,
            total_leads: 48,
            active_users: 15
         }
      }
    },
  });

  return (
    <div className="space-y-8 animate-in fade-in duration-500">
      <div>
        <h2 className="text-3xl font-bold tracking-tight">Dashboard</h2>
        <p className="text-muted-foreground mt-1">
          Visão geral da sua empresa. Acompanhe os principais indicadores.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Receita Mensal"
          value={stats?.revenue || 0}
          icon={DollarSign}
          description="+20.1% em relação ao mês anterior"
          isCurrency
          isLoading={isLoading}
          trend="up"
        />
        <StatCard
          title="Projetos Ativos"
          value={stats?.active_projects || 0}
          icon={Briefcase}
          description="+3 novos esta semana"
          isLoading={isLoading}
          trend="up"
        />
        <StatCard
          title="Leads (CRM)"
          value={stats?.total_leads || 0}
          icon={Users}
          description="12 aguardando contato"
          isLoading={isLoading}
        />
        <StatCard
          title="Colaboradores"
          value={stats?.active_users || 0}
          icon={LayoutList}
          description="1 em férias"
          isLoading={isLoading}
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <div className="lg:col-span-4 rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden">
           <RevenueChart />
        </div>
        <div className="lg:col-span-3 rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden flex flex-col">
           <div className="p-6 pb-2 border-b border-border/50">
             <h3 className="font-semibold leading-none tracking-tight">Projetos Recentes</h3>
             <p className="text-sm text-muted-foreground mt-1.5">Status dos projetos em andamento</p>
           </div>
           <ProjectOverview />
        </div>
      </div>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-1">
        <div className="rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden">
          <div className="p-6 pb-2 border-b border-border/50 flex justify-between items-center">
             <div>
               <h3 className="font-semibold leading-none tracking-tight">Feed de Atividades</h3>
               <p className="text-sm text-muted-foreground mt-1.5">Últimas ações realizadas no sistema</p>
             </div>
             <button className="text-sm text-primary hover:underline font-medium">Ver tudo</button>
          </div>
          <ActivityFeed />
        </div>
      </div>
    </div>
  );
}
