"use client";

import { Landmark, TrendingUp, FileText, ArrowUpRight, DollarSign, PieChart, ShieldCheck, Download, ExternalLink } from "lucide-react";
import { Button } from "@/components/ui/button";
import { StatCard } from "../dashboard/stat-card";

type Investment = {
  id: string;
  name: string;
  type: string;
  amount: number;
  yieldPercent: number;
  yieldAmount: number;
  risk: "Baixo" | "Médio" | "Alto";
};

const mockInvestments: Investment[] = [
  { id: "1", name: "CDB Banco Guará - 120% CDI", type: "Renda Fixa", amount: 450000.00, yieldPercent: 1.15, yieldAmount: 5175.00, risk: "Baixo" },
  { id: "2", name: "Fundo Imobiliário G6 (FII)", type: "Renda Variável", amount: 150000.00, yieldPercent: 0.85, yieldAmount: 1275.00, risk: "Médio" },
  { id: "3", name: "Tesouro IPCA+ 2035", type: "Títulos Públicos", amount: 320500.00, yieldPercent: 0.92, yieldAmount: 2948.60, risk: "Baixo" },
  { id: "4", name: "Ações Corporativas (Tech)", type: "Renda Variável", amount: 80000.00, yieldPercent: 3.40, yieldAmount: 2720.00, risk: "Alto" },
];

export default function FinancePage() {
  const totalInvested = mockInvestments.reduce((acc, curr) => acc + curr.amount, 0);
  const totalYield = mockInvestments.reduce((acc, curr) => acc + curr.yieldAmount, 0);

  return (
    <div className="space-y-6 animate-in fade-in duration-500 pb-10">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">Financeiro e Investimentos</h2>
          <p className="text-muted-foreground mt-1">
            Gestão do patrimônio da conta, rendimentos e fluxo contábil.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" className="gap-2">
            <PieChart className="h-4 w-4" />
            Ver Relatório Completo
          </Button>
          <Button className="gap-2">
            <TrendingUp className="h-4 w-4" />
            Novo Aporte
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard
          title="Patrimônio Total Investido"
          value={`R$ ${totalInvested.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          icon={Landmark}
          description="Valor atualizado hoje"
          trend="up"
        />
        <StatCard
          title="Rendimento (Mês Atual)"
          value={`+ R$ ${totalYield.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}`}
          icon={TrendingUp}
          description="Consolidado de todas as carteiras"
          trend="up"
        />
        <StatCard
          title="Caixa Disponível"
          value="R$ 145.200,00"
          icon={DollarSign}
          description="Liquidez Diária"
          trend="neutral"
        />
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        
        {/* Left Side: Investments List */}
        <div className="md:col-span-2 space-y-6">
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h3 className="text-lg font-semibold">Carteira de Investimentos</h3>
                <p className="text-sm text-muted-foreground">Onde sua conta está investida atualmente.</p>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="bg-muted/50 text-muted-foreground text-xs uppercase border-b border-border">
                  <tr>
                    <th className="px-4 py-3 font-medium">Ativo / Fundo</th>
                    <th className="px-4 py-3 font-medium">Valor Aplicado</th>
                    <th className="px-4 py-3 font-medium">Rendimento Mês</th>
                    <th className="px-4 py-3 font-medium">Risco</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {mockInvestments.map((inv) => (
                    <tr key={inv.id} className="hover:bg-muted/30 transition-colors">
                      <td className="px-4 py-4">
                        <div className="font-semibold text-foreground">{inv.name}</div>
                        <div className="text-xs text-muted-foreground">{inv.type}</div>
                      </td>
                      <td className="px-4 py-4 font-medium">
                        R$ {inv.amount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-4 py-4">
                        <div className="text-emerald-500 font-medium">
                          +R$ {inv.yieldAmount.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}
                        </div>
                        <div className="text-xs text-muted-foreground">+{inv.yieldPercent}%</div>
                      </td>
                      <td className="px-4 py-4">
                        <span className={`px-2 py-1 rounded-md text-xs font-medium ${
                          inv.risk === "Baixo" ? "bg-emerald-500/10 text-emerald-500" :
                          inv.risk === "Médio" ? "bg-orange-500/10 text-orange-500" :
                          "bg-destructive/10 text-destructive"
                        }`}>
                          {inv.risk}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Right Side: Accounting Routing */}
        <div className="space-y-6">
          <div className="rounded-xl border bg-card text-card-foreground shadow-sm p-6 flex flex-col h-full relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute top-[-20%] right-[-20%] w-[60%] h-[60%] rounded-full bg-primary/10 blur-[60px] pointer-events-none" />
            
            <div className="mb-6 relative z-10">
              <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <ShieldCheck className="h-5 w-5 text-primary" />
              </div>
              <h3 className="text-lg font-semibold">Direcionamento Contábil</h3>
              <p className="text-sm text-muted-foreground mt-1">
                Integração e envio de dados para a contabilidade externa.
              </p>
            </div>

            <div className="space-y-4 relative z-10 flex-1">
              <Button variant="outline" className="w-full justify-between h-12 bg-background/50 hover:bg-accent border-border/50">
                <div className="flex items-center gap-3">
                  <FileText className="h-4 w-4 text-primary" />
                  <span>Enviar Notas Fiscais</span>
                </div>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground" />
              </Button>

              <Button variant="outline" className="w-full justify-between h-12 bg-background/50 hover:bg-accent border-border/50">
                <div className="flex items-center gap-3">
                  <Download className="h-4 w-4 text-primary" />
                  <span>Baixar Balancete (Mês)</span>
                </div>
                <ArrowUpRight className="h-4 w-4 text-muted-foreground" />
              </Button>

              <div className="pt-4 mt-4 border-t border-border">
                <p className="text-xs text-muted-foreground mb-3 font-medium uppercase tracking-wider">Acesso do Contador</p>
                <div className="bg-muted p-3 rounded-lg flex items-center justify-between">
                  <div className="text-sm">
                    <p className="font-medium">Portal do Contador</p>
                    <p className="text-xs text-muted-foreground mt-0.5">Status: Conectado</p>
                  </div>
                  <Button size="sm" className="h-8 w-8 p-0">
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>

          </div>
        </div>

      </div>
    </div>
  );
}
