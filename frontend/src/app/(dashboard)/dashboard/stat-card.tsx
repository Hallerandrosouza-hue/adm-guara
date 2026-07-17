import { LucideIcon, TrendingUp, TrendingDown, Minus } from "lucide-react";
import { formatCurrency } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  description?: string;
  isCurrency?: boolean;
  isLoading?: boolean;
  trend?: "up" | "down" | "neutral";
}

export function StatCard({
  title,
  value,
  icon: Icon,
  description,
  isCurrency,
  isLoading,
  trend,
}: StatCardProps) {
  return (
    <Card className="overflow-hidden relative group hover:shadow-md transition-all duration-300 border-primary/5">
      <div className="absolute right-0 top-0 w-24 h-24 bg-primary/5 rounded-bl-full -mr-4 -mt-4 transition-transform group-hover:scale-110" />
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2 relative z-10">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <div className="h-8 w-8 rounded-md bg-primary/10 flex items-center justify-center text-primary">
            <Icon className="h-4 w-4" />
        </div>
      </CardHeader>
      <CardContent className="relative z-10">
        {isLoading ? (
          <div className="h-8 w-1/2 animate-pulse bg-muted rounded mt-1" />
        ) : (
          <div className="text-2xl font-bold tracking-tight">
            {isCurrency ? formatCurrency(value) : value}
          </div>
        )}
        {description && (
          <div className="flex items-center mt-1 text-xs text-muted-foreground">
            {trend === "up" && <TrendingUp className="h-3 w-3 text-emerald-500 mr-1" />}
            {trend === "down" && <TrendingDown className="h-3 w-3 text-destructive mr-1" />}
            {trend === "neutral" && <Minus className="h-3 w-3 text-muted-foreground mr-1" />}
            <span className={cn(
                trend === "up" && "text-emerald-500 font-medium",
                trend === "down" && "text-destructive font-medium"
            )}>
                {description}
            </span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
