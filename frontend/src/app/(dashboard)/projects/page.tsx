"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { Plus, Search, Filter, MoreHorizontal, Calendar, Folder } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

type ProjectLink = {
  title: string;
  url: string;
};

type Project = {
  id: string;
  name: string;
  description?: string;
  status: string;
  end_date?: string;
  links?: ProjectLink[];
};

export default function ProjectsPage() {
  const [search, setSearch] = useState("");

  const { data: projects, isLoading } = useQuery({
    queryKey: ["projects", search],
    queryFn: async (): Promise<Project[]> => {
      try {
        const res = await api.get(`/projects?search=${search}`);
        return res.data.items;
      } catch {
        // Return mock data if backend is not available
        return [
          {
            id: "1",
            name: "Website Redesign",
            description: "Redesign completo do site institucional da empresa.",
            status: "IN_PROGRESS",
            end_date: new Date(Date.now() + 1000 * 60 * 60 * 24 * 15).toISOString(),
            links: [
              { title: "Prévia de Design", url: "https://figma.com/preview-xyz" },
              { title: "Staging URL", url: "https://staging.acme.com" }
            ]
          },
          {
            id: "2",
            name: "App Mobile MVP",
            description: "Desenvolvimento do MVP do aplicativo mobile.",
            status: "PLANNING",
            end_date: new Date(Date.now() + 1000 * 60 * 60 * 24 * 45).toISOString(),
            links: []
          },
          {
            id: "3",
            name: "E-Commerce Integrado",
            description: "Nova loja online integrada com ERP.",
            status: "COMPLETED",
            end_date: new Date(Date.now() - 1000 * 60 * 60 * 24 * 5).toISOString(),
            links: [
              { title: "Site Final Entregue", url: "https://lojanova.exemplo.com.br" },
              { title: "Documentação API", url: "https://docs.exemplo.com.br" }
            ]
          },
        ];
      }
    },
  });

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Projetos</h2>
          <p className="text-muted-foreground mt-1">
            Gerencie todos os projetos da sua empresa.
          </p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          Novo Projeto
        </Button>
      </div>

      <div className="flex flex-col sm:flex-row gap-4 items-center justify-between bg-card p-4 rounded-xl border shadow-sm">
        <div className="relative w-full sm:w-96">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            placeholder="Buscar projetos..."
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

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map((i) => (
            <div
              key={i}
              className="h-48 rounded-xl bg-card border shadow-sm animate-pulse"
            />
          ))}
        </div>
      ) : !projects || projects.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-24 px-4 text-center border rounded-xl bg-card border-dashed">
          <div className="h-20 w-20 bg-primary/10 rounded-full flex items-center justify-center mb-4">
            <Folder className="h-10 w-10 text-primary" />
          </div>
          <h3 className="text-xl font-semibold">Nenhum projeto encontrado</h3>
          <p className="text-muted-foreground mt-2 max-w-sm">
            Você ainda não possui projetos cadastrados ou nenhum corresponde à
            sua busca.
          </p>
          <Button className="mt-6 gap-2">
            <Plus className="h-4 w-4" />
            Criar Primeiro Projeto
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {projects.map((project) => (
            <div
              key={project.id}
              className="group relative rounded-xl border bg-card p-6 shadow-sm hover:shadow-md transition-all hover:border-primary/50"
            >
              <div className="flex justify-between items-start mb-4">
                <div
                  className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                    project.status === "IN_PROGRESS"
                      ? "bg-primary/10 text-primary"
                      : project.status === "COMPLETED"
                      ? "bg-emerald-500/10 text-emerald-600"
                      : "bg-muted text-muted-foreground"
                  }`}
                >
                  {project.status === "IN_PROGRESS"
                    ? "Em Andamento"
                    : project.status === "COMPLETED"
                    ? "Concluído"
                    : "Planejamento"}
                </div>
                <button className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                  <MoreHorizontal className="h-5 w-5" />
                </button>
              </div>
              <h3 className="font-semibold text-lg leading-tight mb-2">
                {project.name}
              </h3>
              <p className="text-sm text-muted-foreground line-clamp-2 mb-4">
                {project.description || "Sem descrição."}
              </p>
              
              {project.links && project.links.length > 0 && (
                <div className="mb-4 space-y-2">
                  <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">Links / Entregas</h4>
                  <div className="flex flex-wrap gap-2">
                    {project.links.map((link, idx) => (
                      <a 
                        key={idx} 
                        href={link.url} 
                        target="_blank" 
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1.5 px-2.5 py-1.5 bg-accent text-accent-foreground text-xs rounded-md hover:bg-primary/10 hover:text-primary transition-colors border border-border"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                        {link.title}
                      </a>
                    ))}
                  </div>
                </div>
              )}

              <div className="pt-4 border-t flex items-center justify-between text-sm text-muted-foreground mt-auto">
                <div className="flex items-center gap-1.5">
                  <Calendar className="h-4 w-4" />
                  <span>
                    {project.end_date
                      ? new Date(project.end_date).toLocaleDateString("pt-BR")
                      : "Sem prazo"}
                  </span>
                </div>
                <div className="flex -space-x-2">
                  <div className="h-6 w-6 rounded-full border-2 border-background bg-primary/20" />
                  <div className="h-6 w-6 rounded-full border-2 border-background bg-muted" />
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
