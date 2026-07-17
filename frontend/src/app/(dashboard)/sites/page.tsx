"use client";

import { useState } from "react";
import { Search, Plus, Globe, Github, ExternalLink, Filter, MoreHorizontal } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type Site = {
  id: string;
  name: string;
  client: string;
  url: string;
  gitRepo: string;
  status: "Online" | "Em Desenvolvimento" | "Manutenção";
};

const mockSites: Site[] = [
  {
    id: "1",
    name: "Acme Institucional",
    client: "Acme Corp",
    url: "https://acme.com.br",
    gitRepo: "https://github.com/guarasix/acme-website",
    status: "Online",
  },
  {
    id: "2",
    name: "E-Commerce Tech",
    client: "Tech Store",
    url: "https://techstore.exemplo.com",
    gitRepo: "https://github.com/guarasix/tech-ecommerce",
    status: "Online",
  },
  {
    id: "3",
    name: "Landing Page Evento",
    client: "Marketing Pro",
    url: "https://evento.marketingpro.com",
    gitRepo: "https://github.com/guarasix/lp-evento",
    status: "Em Desenvolvimento",
  },
];

export default function SitesPage() {
  const [search, setSearch] = useState("");

  const filtered = mockSites.filter(site => 
    site.name.toLowerCase().includes(search.toLowerCase()) || 
    site.client.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Sites Entregues</h2>
          <p className="text-muted-foreground mt-1">
            Repositório central de todos os sites e projetos web desenvolvidos.
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Registrar Novo Site
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card p-4 rounded-xl border shadow-sm">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar por nome ou cliente..."
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

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((site) => (
          <div
            key={site.id}
            className="group relative rounded-xl border bg-card p-6 shadow-sm hover:shadow-md transition-all hover:border-primary/50 flex flex-col"
          >
            <div className="flex justify-between items-start mb-4">
              <div
                className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  site.status === "Online"
                    ? "bg-emerald-500/10 text-emerald-500"
                    : site.status === "Em Desenvolvimento"
                    ? "bg-orange-500/10 text-orange-500"
                    : "bg-muted text-muted-foreground"
                }`}
              >
                {site.status}
              </div>
              <button className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                <MoreHorizontal className="h-5 w-5" />
              </button>
            </div>
            
            <h3 className="font-semibold text-lg leading-tight mb-1">
              {site.name}
            </h3>
            <p className="text-sm text-muted-foreground mb-6">
              Cliente: <span className="font-medium text-foreground">{site.client}</span>
            </p>

            <div className="space-y-3 mt-auto">
              {/* Site URL */}
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1 uppercase tracking-wider">URL do Site</p>
                <a 
                  href={site.url} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-2 rounded-md bg-accent/50 hover:bg-accent border border-border/50 transition-colors group/link"
                >
                  <div className="flex items-center gap-2 overflow-hidden">
                    <Globe className="h-4 w-4 text-primary shrink-0" />
                    <span className="text-sm truncate text-muted-foreground group-hover/link:text-foreground transition-colors">{site.url.replace('https://', '')}</span>
                  </div>
                  <ExternalLink className="h-3.5 w-3.5 text-muted-foreground shrink-0 ml-2" />
                </a>
              </div>

              {/* Git Repo */}
              <div>
                <p className="text-xs font-medium text-muted-foreground mb-1 uppercase tracking-wider">Repositório Git</p>
                <a 
                  href={site.gitRepo} 
                  target="_blank" 
                  rel="noopener noreferrer"
                  className="flex items-center justify-between p-2 rounded-md bg-accent/50 hover:bg-accent border border-border/50 transition-colors group/link"
                >
                  <div className="flex items-center gap-2 overflow-hidden">
                    <Github className="h-4 w-4 text-foreground shrink-0" />
                    <span className="text-sm truncate text-muted-foreground group-hover/link:text-foreground transition-colors">{site.gitRepo.replace('https://github.com/', '')}</span>
                  </div>
                  <ExternalLink className="h-3.5 w-3.5 text-muted-foreground shrink-0 ml-2" />
                </a>
              </div>
            </div>
            
          </div>
        ))}

        {filtered.length === 0 && (
          <div className="col-span-full py-12 text-center border border-dashed rounded-xl">
            <Globe className="h-8 w-8 text-muted-foreground mx-auto mb-3 opacity-50" />
            <p className="text-muted-foreground">Nenhum site encontrado na sua busca.</p>
          </div>
        )}
      </div>
    </div>
  );
}
