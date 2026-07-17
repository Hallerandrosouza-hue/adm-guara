"use client";

import { CheckCircle2, MessageSquare, FileEdit, UserPlus } from "lucide-react";

const activities = [
  {
    id: 1,
    user: "Ana Silva",
    action: "concluiu a tarefa",
    target: "Revisão do Contrato",
    project: "Projeto Alpha",
    timeLabel: "há 15 minutos",
    icon: CheckCircle2,
    color: "text-emerald-500",
    bg: "bg-emerald-500/10",
  },
  {
    id: 2,
    user: "Carlos Mendes",
    action: "comentou em",
    target: "Mockups Iniciais",
    project: "Projeto Beta",
    timeLabel: "há 2 horas",
    icon: MessageSquare,
    color: "text-blue-500",
    bg: "bg-blue-500/10",
  },
  {
    id: 3,
    user: "Você",
    action: "atualizou o status do cliente",
    target: "Tech Solutions Inc.",
    project: "CRM",
    timeLabel: "há 5 horas",
    icon: FileEdit,
    color: "text-orange-500",
    bg: "bg-orange-500/10",
  },
  {
    id: 4,
    user: "Juliana Costa",
    action: "adicionou um novo membro",
    target: "Roberto Almeida",
    project: "RH",
    timeLabel: "há 1 dia",
    icon: UserPlus,
    color: "text-primary",
    bg: "bg-primary/10",
  },
];

export function ActivityFeed() {
  return (
    <div className="p-0">
      <ul className="divide-y divide-border">
        {activities.map((activity) => (
          <li
            key={activity.id}
            className="p-4 hover:bg-muted/30 transition-colors"
          >
            <div className="flex items-start space-x-4">
              <div
                className={`flex-shrink-0 rounded-full p-2 ${activity.bg}`}
              >
                <activity.icon className={`h-4 w-4 ${activity.color}`} />
              </div>
              <div className="min-w-0 flex-1">
                <p className="text-sm text-foreground">
                  <span className="font-semibold">{activity.user}</span>{" "}
                  {activity.action}{" "}
                  <span className="font-medium text-primary">
                    {activity.target}
                  </span>
                </p>
                <div className="mt-1 flex items-center gap-2 text-xs text-muted-foreground">
                  <span>{activity.project}</span>
                  <span>•</span>
                  <span>{activity.timeLabel}</span>
                </div>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
