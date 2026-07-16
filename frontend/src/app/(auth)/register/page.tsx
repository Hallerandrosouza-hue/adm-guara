"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { z } from "zod";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { api } from "@/lib/api";
import { useAuth } from "@/providers/auth-provider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Loader2 } from "lucide-react";

const registerSchema = z.object({
  company_name: z.string().min(2, "Nome da empresa muito curto"),
  company_slug: z.string().min(2, "URL muito curta").regex(/^[a-z0-9-]+$/, "Apenas letras minúsculas, números e hifens"),
  first_name: z.string().min(2, "Nome muito curto"),
  last_name: z.string().min(2, "Sobrenome muito curto"),
  email: z.string().email("Email inválido"),
  password: z.string().min(8, "A senha deve ter no mínimo 8 caracteres"),
});

type RegisterFormValues = z.infer<typeof registerSchema>;

export default function RegisterPage() {
  const router = useRouter();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const form = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      company_name: "",
      company_slug: "",
      first_name: "",
      last_name: "",
      email: "",
      password: "",
    },
  });

  // Auto-generate slug from company name
  const handleCompanyNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const name = e.target.value;
    form.setValue("company_name", name);
    if (!form.formState.touchedFields.company_slug) {
      const slug = name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)+/g, "");
      form.setValue("company_slug", slug);
    }
  };

  const onSubmit = async (data: RegisterFormValues) => {
    try {
      setError(null);
      const response = await api.post("/auth/register", data);
      login(response.data.access_token);
    } catch (err: any) {
      setError(err.response?.data?.detail || "Erro ao registrar. Tente novamente.");
    }
  };

  return (
    <Card className="w-full shadow-lg border-primary/10">
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold tracking-tight">Criar Conta</CardTitle>
        <CardDescription>
          Cadastre sua empresa e comece a usar o Guará Manager.
        </CardDescription>
      </CardHeader>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <CardContent className="space-y-4">
          {error && (
            <div className="p-3 text-sm rounded-md bg-destructive/15 text-destructive font-medium">
              {error}
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="first_name">Nome</Label>
              <Input id="first_name" {...form.register("first_name")} />
              {form.formState.errors.first_name && (
                <p className="text-xs text-destructive">{form.formState.errors.first_name.message}</p>
              )}
            </div>
            <div className="space-y-2">
              <Label htmlFor="last_name">Sobrenome</Label>
              <Input id="last_name" {...form.register("last_name")} />
              {form.formState.errors.last_name && (
                <p className="text-xs text-destructive">{form.formState.errors.last_name.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="email">Email de Trabalho</Label>
            <Input id="email" type="email" placeholder="m@suaempresa.com" {...form.register("email")} />
            {form.formState.errors.email && (
              <p className="text-xs text-destructive">{form.formState.errors.email.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="company_name">Nome da Empresa</Label>
            <Input id="company_name" onChange={handleCompanyNameChange} />
            {form.formState.errors.company_name && (
              <p className="text-xs text-destructive">{form.formState.errors.company_name.message}</p>
            )}
          </div>

          <div className="space-y-2">
            <Label htmlFor="company_slug">URL da Empresa</Label>
            <div className="flex flex-col">
              <div className="flex rounded-md shadow-sm">
                <span className="inline-flex items-center rounded-l-md border border-r-0 border-input bg-muted px-3 text-sm text-muted-foreground">
                  guara.com/
                </span>
                <Input 
                  id="company_slug" 
                  className="rounded-l-none focus-visible:ring-offset-0" 
                  {...form.register("company_slug")} 
                />
              </div>
              {form.formState.errors.company_slug && (
                <p className="text-xs text-destructive mt-1">{form.formState.errors.company_slug.message}</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="password">Senha</Label>
            <Input id="password" type="password" {...form.register("password")} />
            {form.formState.errors.password && (
              <p className="text-xs text-destructive">{form.formState.errors.password.message}</p>
            )}
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button 
            type="submit" 
            className="w-full" 
            disabled={form.formState.isSubmitting}
          >
            {form.formState.isSubmitting ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Criando conta...
              </>
            ) : (
              "Criar Conta"
            )}
          </Button>
          <div className="text-center text-sm text-muted-foreground">
            Já tem uma conta?{" "}
            <Link href="/login" className="text-primary hover:underline font-medium">
              Fazer login
            </Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  );
}
