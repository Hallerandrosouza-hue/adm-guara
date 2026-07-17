"use client";

import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

// Fixed data (no Math.random to avoid hydration mismatch)
const data = [
  { name: "Jan", total: 3200 },
  { name: "Fev", total: 4100 },
  { name: "Mar", total: 2800 },
  { name: "Abr", total: 5100 },
  { name: "Mai", total: 4700 },
  { name: "Jun", total: 6200 },
  { name: "Jul", total: 5800 },
  { name: "Ago", total: 7100 },
  { name: "Set", total: 6400 },
  { name: "Out", total: 5500 },
  { name: "Nov", total: 7800 },
  { name: "Dez", total: 9200 },
];

export function RevenueChart() {
  return (
    <div className="p-6 h-[350px] w-full flex flex-col">
      <div className="mb-4">
        <h3 className="font-semibold leading-none tracking-tight">
          Evolução Financeira
        </h3>
        <p className="text-sm text-muted-foreground mt-1.5">
          Receita gerada nos últimos 12 meses
        </p>
      </div>
      <div className="flex-1">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <XAxis
              dataKey="name"
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
            />
            <YAxis
              stroke="#888888"
              fontSize={12}
              tickLine={false}
              axisLine={false}
              tickFormatter={(value) => `R$${value}`}
            />
            <Tooltip
              cursor={{ fill: "rgba(249, 115, 22, 0.08)" }}
              contentStyle={{
                borderRadius: "8px",
                border: "1px solid hsl(var(--border))",
                backgroundColor: "hsl(var(--background))",
                color: "hsl(var(--foreground))",
              }}
              formatter={(value: number) => [`R$ ${value}`, "Receita"]}
            />
            <Bar
              dataKey="total"
              fill="hsl(24 95% 53%)"
              radius={[4, 4, 0, 0]}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
