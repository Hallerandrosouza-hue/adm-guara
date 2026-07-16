import { ThemeProvider } from "@/providers/theme-provider";
import { QueryProvider } from "@/providers/query-provider";
import { AuthProvider } from "@/providers/auth-provider";

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem disableTransitionOnChange>
        <QueryProvider>
            {/* We still need AuthProvider here for logic, though layout is different */}
            <AuthProvider>
                <div className="min-h-screen flex items-center justify-center bg-muted/40 p-4 relative overflow-hidden">
                    {/* Decorative background elements */}
                    <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px] mix-blend-multiply" />
                    <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-indigo-500/20 blur-[120px] mix-blend-multiply" />
                    
                    <div className="w-full max-w-md relative z-10">
                        <div className="mb-8 text-center">
                            <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-indigo-500">
                                Guará Manager
                            </h1>
                            <p className="text-muted-foreground mt-2">Enterprise SaaS Platform</p>
                        </div>
                        {children}
                    </div>
                </div>
            </AuthProvider>
        </QueryProvider>
    </ThemeProvider>
  );
}
