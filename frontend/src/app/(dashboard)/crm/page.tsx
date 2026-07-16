"use client";

import { useState } from "react";
import { Plus, Search, Filter, Phone, Mail, Building } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export default function CRMPage() {
  const [search, setSearch] = useState("");

  const mockClients = [
    { id: 1, contact: "João Silva", company: "TechCorp", email: "joao@techcorp.com", phone: "(11) 98765-4321", stage: "Proposta", value: "R$ 15.000" },
    { id: 2, contact: "Maria Oliveira", company: "Inova Marketing", email: "maria@inova.com", phone: "(11) 91234-5678", stage: "Lead", value: "R$ 8.500" },
    { id: 3, contact: "Pedro Santos", company: "Construtora Alfa", email: "pedro@alfa.com", phone: "(21) 99999-8888", stage: "Negociação", value: "R$ 45.000" },
    { id: 4, contact: "Ana Costa", company: "Retail Plus", email: "ana@retail.com", phone: "(31) 97777-6666", stage: "Fechado", value: "R$ 12.000" },
  ];

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">CRM</h2>
          <p className="text-muted-foreground mt-1">Gerencie seus leads, clientes e oportunidades.</p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Novo Contato
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card p-4 rounded-xl border shadow-sm">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Buscar contatos ou empresas..." 
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

      <div className="bg-card rounded-xl border shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground bg-muted/50 uppercase border-b border-border">
              <tr>
                <th className="px-6 py-4 font-medium">Contato / Empresa</th>
                <th className="px-6 py-4 font-medium">Informações</th>
                <th className="px-6 py-4 font-medium">Estágio</th>
                <th className="px-6 py-4 font-medium">Valor</th>
                <th className="px-6 py-4 font-medium text-right">Ações</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {mockClients.map((client) => (
                <tr key={client.id} className="hover:bg-muted/30 transition-colors">
                  <td className="px-6 py-4">
                    <div className="font-medium text-foreground">{client.contact}</div>
                    <div className="flex items-center text-muted-foreground mt-1 gap-1.5 text-xs">
                      <Building className="h-3 w-3" />
                      {client.company}
                    </div>
                  </td>
                  <td className="px-6 py-4 space-y-1">
                    <div className="flex items-center text-muted-foreground gap-2">
                      <Mail className="h-3.5 w-3.5" />
                      {client.email}
                    </div>
                    <div className="flex items-center text-muted-foreground gap-2">
                      <Phone className="h-3.5 w-3.5" />
                      {client.phone}
                    </div>
                  </td>
                  <td className="px-6 py-4">
                    <span className={`px-2.5 py-1 rounded-full text-xs font-medium
                      ${client.stage === 'Fechado' ? 'bg-emerald-500/10 text-emerald-600' : 
                        client.stage === 'Negociação' ? 'bg-orange-500/10 text-orange-600' : 
                        client.stage === 'Proposta' ? 'bg-blue-500/10 text-blue-600' : 
                        'bg-primary/10 text-primary'}`}>
                      {client.stage}
                    </span>
                  </td>
                  <td className="px-6 py-4 font-medium">
                    {client.value}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <Button variant="ghost" size="sm" className="text-primary hover:text-primary">
                      Ver detalhes
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
