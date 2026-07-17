"use client";

import { useState } from "react";
import { Search, Plus, Filter, FileText, Download, UserPlus, MoreVertical, Briefcase, GraduationCap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { StatCard } from "../dashboard/stat-card";

type Employee = {
  id: string;
  name: string;
  role: string;
  department: string;
  status: "Ativo" | "Férias" | "Afastado";
  email: string;
  joinDate: string;
};

const mockEmployees: Employee[] = [
  { id: "1", name: "Ana Silva", role: "Desenvolvedora Senior", department: "Engenharia", status: "Ativo", email: "ana.silva@teste.com", joinDate: "12/05/2022" },
  { id: "2", name: "Carlos Mendes", role: "Designer UX/UI", department: "Design", status: "Ativo", email: "carlos.mendes@teste.com", joinDate: "03/11/2023" },
  { id: "3", name: "Roberto Almeida", role: "Gerente de Contas", department: "Vendas", status: "Férias", email: "roberto.a@teste.com", joinDate: "15/01/2021" },
  { id: "4", name: "Juliana Costa", role: "Especialista de RH", department: "Recursos Humanos", status: "Ativo", email: "juliana.c@teste.com", joinDate: "20/08/2023" },
  { id: "5", name: "Marcos Vinicius", role: "Analista de Suporte", department: "Atendimento", status: "Afastado", email: "marcos.v@teste.com", joinDate: "05/02/2024" },
];

export default function HRPage() {
  const [search, setSearch] = useState("");

  const filtered = mockEmployees.filter(emp => emp.name.toLowerCase().includes(search.toLowerCase()) || emp.role.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Recursos Humanos</h2>
          <p className="text-muted-foreground mt-1">
            Gestão completa de colaboradores, currículos e documentações.
          </p>
        </div>
        <Button className="gap-2">
          <UserPlus className="h-4 w-4" />
          Adicionar Funcionário
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard
          title="Total de Funcionários"
          value={124}
          icon={Briefcase}
          description="+4 contratados este mês"
          trend="up"
        />
        <StatCard
          title="Em Férias / Afastados"
          value={8}
          icon={UserPlus}
          description="3 retornam na próxima semana"
          trend="neutral"
        />
        <StatCard
          title="Vagas Abertas"
          value={5}
          icon={GraduationCap}
          description="Entrevistas em andamento"
          trend="up"
        />
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card p-4 rounded-xl border shadow-sm">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por nome ou cargo..."
            className="pl-9"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Button variant="outline" className="gap-2">
            <Filter className="h-4 w-4" />
            Filtros
          </Button>
        </div>
      </div>

      <div className="rounded-xl border bg-card text-card-foreground shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted/50 text-muted-foreground text-xs uppercase border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Nome / Email</th>
                <th className="px-6 py-4 font-medium">Cargo / Departamento</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Arquivos (CV/Docs)</th>
                <th className="px-6 py-4 font-medium text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filtered.map((emp) => (
                <tr key={emp.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-4">
                    <div className="font-semibold text-foreground">{emp.name}</div>
                    <div className="text-xs text-muted-foreground">{emp.email}</div>
                  </td>
                  <td className="px-6 py-4">
                    <div className="font-medium">{emp.role}</div>
                    <div className="text-xs text-muted-foreground">{emp.department}</div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium ${
                      emp.status === "Ativo" ? "bg-emerald-500/10 text-emerald-500" :
                      emp.status === "Férias" ? "bg-orange-500/10 text-orange-500" :
                      "bg-destructive/10 text-destructive"
                    }`}>
                      {emp.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex items-center gap-2">
                      <Button variant="outline" size="sm" className="h-8 gap-1.5 text-xs bg-background">
                        <FileText className="h-3.5 w-3.5 text-primary" />
                        Currículo
                      </Button>
                      <Button variant="outline" size="sm" className="h-8 gap-1.5 text-xs bg-background">
                        <Download className="h-3.5 w-3.5" />
                        Contrato
                      </Button>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-foreground">
                      <MoreVertical className="h-4 w-4" />
                    </Button>
                  </td>
                </tr>
              ))}
              
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={5} className="px-6 py-12 text-center text-muted-foreground">
                    Nenhum funcionário encontrado com essa busca.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
