"use client";

import { useState } from "react";
import { Plus, GripVertical, Clock, MessageSquare, Paperclip } from "lucide-react";
import { Button } from "@/components/ui/button";

// Mock data for the initial Kanban representation
const columns = [
  { id: "todo", title: "A Fazer" },
  { id: "in_progress", title: "Em Andamento" },
  { id: "review", title: "Em Revisão" },
  { id: "done", title: "Concluído" },
];

const mockTasks = [
  { id: "1", title: "Definir arquitetura do BD", column: "todo", tags: ["Design"], comments: 2 },
  { id: "2", title: "Implementar autenticação JWT", column: "in_progress", tags: ["Backend", "Segurança"], comments: 5, attachments: 1 },
  { id: "3", title: "Criar layout do Dashboard", column: "in_progress", tags: ["Frontend", "UI/UX"], comments: 1 },
  { id: "4", title: "Configurar CI/CD", column: "review", tags: ["DevOps"], comments: 0 },
  { id: "5", title: "Setup Inicial do Projeto", column: "done", tags: ["Setup"], comments: 3 },
];

export default function TasksPage() {
  return (
    <div className="h-full flex flex-col space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Tarefas</h2>
          <p className="text-muted-foreground mt-1">Quadro Kanban para gestão de atividades.</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="flex -space-x-2 mr-4">
            <div className="h-8 w-8 rounded-full border-2 border-background bg-primary/20 flex items-center justify-center text-xs font-medium text-primary">AS</div>
            <div className="h-8 w-8 rounded-full border-2 border-background bg-blue-500/20 flex items-center justify-center text-xs font-medium text-blue-500">CM</div>
            <div className="h-8 w-8 rounded-full border-2 border-background bg-muted flex items-center justify-center text-xs font-medium">+3</div>
          </div>
          <Button className="gap-2">
            <Plus className="h-4 w-4" />
            Nova Tarefa
          </Button>
        </div>
      </div>

      {/* Kanban Board Placeholder */}
      <div className="flex-1 flex gap-6 overflow-x-auto pb-4">
        {columns.map((column) => (
          <div key={column.id} className="flex-shrink-0 w-80 flex flex-col bg-muted/40 rounded-xl">
            <div className="p-4 flex items-center justify-between border-b border-border/50">
              <h3 className="font-semibold text-sm">{column.title}</h3>
              <span className="bg-muted text-muted-foreground text-xs font-medium px-2 py-0.5 rounded-full">
                {mockTasks.filter((t) => t.column === column.id).length}
              </span>
            </div>
            <div className="flex-1 p-3 space-y-3 overflow-y-auto">
              {mockTasks
                .filter((t) => t.column === column.id)
                .map((task) => (
                  <div key={task.id} className="bg-card p-4 rounded-lg shadow-sm border cursor-pointer hover:border-primary/50 transition-colors group">
                    <div className="flex flex-wrap gap-1.5 mb-3">
                      {task.tags.map(tag => (
                         <span key={tag} className="text-[10px] font-medium px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                           {tag}
                         </span>
                      ))}
                    </div>
                    <h4 className="text-sm font-medium leading-snug mb-4">{task.title}</h4>
                    <div className="flex items-center justify-between text-muted-foreground">
                       <GripVertical className="h-4 w-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                       <div className="flex items-center gap-3 text-xs">
                          {task.comments > 0 && (
                            <div className="flex items-center gap-1">
                              <MessageSquare className="h-3.5 w-3.5" />
                              <span>{task.comments}</span>
                            </div>
                          )}
                          {task.attachments && task.attachments > 0 && (
                            <div className="flex items-center gap-1">
                              <Paperclip className="h-3.5 w-3.5" />
                              <span>{task.attachments}</span>
                            </div>
                          )}
                       </div>
                    </div>
                  </div>
                ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
