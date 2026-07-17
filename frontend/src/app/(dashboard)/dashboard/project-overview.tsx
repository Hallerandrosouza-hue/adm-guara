"use client";

import { AlertCircle, Clock } from "lucide-react";

const projects = [
  {
    id: "1",
    name: "Website Redesign",
    client: "Acme Corp",
    progress: 75,
    dueDateLabel: "5 dias",
    status: "on_track",
  },
  {
    id: "2",
    name: "Mobile App MVP",
    client: "StartupZ",
    progress: 32,
    dueDateLabel: "14 dias",
    status: "at_risk",
  },
  {
    id: "3",
    name: "Brand Identity",
    client: "Nova Bakery",
    progress: 90,
    dueDateLabel: "2 dias",
    status: "on_track",
  },
  {
    id: "4",
    name: "SEO Optimization",
    client: "TechBlog",
    progress: 15,
    dueDateLabel: "30 dias",
    status: "delayed",
  },
];

export function ProjectOverview() {
  return (
    <div className="flex-1 overflow-y-auto">
      <ul className="divide-y divide-border">
        {projects.map((project) => (
          <li
            key={project.id}
            className="p-4 hover:bg-muted/30 transition-colors"
          >
            <div className="flex justify-between items-start mb-2">
              <div>
                <h4 className="text-sm font-semibold">{project.name}</h4>
                <p className="text-xs text-muted-foreground">{project.client}</p>
              </div>
              <div className="flex items-center text-xs text-muted-foreground">
                {project.status === "at_risk" && (
                  <AlertCircle className="w-3 h-3 text-orange-500 mr-1" />
                )}
                {project.status === "delayed" && (
                  <AlertCircle className="w-3 h-3 text-destructive mr-1" />
                )}
                <Clock className="w-3 h-3 mr-1" />
                {project.dueDateLabel}
              </div>
            </div>
            <div className="mt-3">
              <div className="flex justify-between text-xs mb-1">
                <span className="font-medium text-muted-foreground">
                  Progresso
                </span>
                <span className="font-medium">{project.progress}%</span>
              </div>
              <div className="w-full bg-secondary rounded-full h-1.5 overflow-hidden">
                <div
                  className={`h-1.5 rounded-full ${
                    project.status === "delayed"
                      ? "bg-destructive"
                      : project.status === "at_risk"
                      ? "bg-orange-500"
                      : "bg-primary"
                  }`}
                  style={{ width: `${project.progress}%` }}
                />
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
