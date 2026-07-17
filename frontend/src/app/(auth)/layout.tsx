// Auth layout — server component (no 'use client')
// Providers are already at root layout, so no need to wrap again
export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/40 p-4 relative overflow-hidden">
      {/* Decorative background gradient blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[120px]" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-orange-500/20 blur-[120px]" />

      <div className="w-full max-w-md relative z-10">
        <div className="mb-8 text-center">
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-orange-500">
            Guará Manager
          </h1>
          <p className="text-muted-foreground mt-2">Enterprise SaaS Platform</p>
        </div>
        {children}
      </div>
    </div>
  );
}
