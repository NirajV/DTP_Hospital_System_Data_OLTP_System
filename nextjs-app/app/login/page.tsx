"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("dr.smith@mediflow.health");
  const [password, setPassword] = useState("demo-password");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    // Stub auth: anything works. Wire to /api/v1/auth/login when added.
    localStorage.setItem("user_id", "1");
    localStorage.setItem("user_role", "doctor");
    localStorage.setItem("user_email", email);
    router.push("/dashboard");
  }

  return (
    <main className="min-h-screen grid place-items-center bg-gradient-to-br from-slate-50 via-white to-blue-50">
      <div className="w-full max-w-md p-8 bg-white rounded-2xl ring-soft">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-brand-600 grid place-items-center text-white font-bold">M</div>
          <div>
            <div className="font-semibold text-slate-900">MediFlow</div>
            <div className="text-xs text-slate-500">Hospital Operations Suite</div>
          </div>
        </div>
        <h1 className="text-2xl font-semibold text-slate-900">Welcome back</h1>
        <p className="text-sm text-slate-500 mb-6">Sign in to your provider account</p>

        <form onSubmit={submit} className="space-y-4">
          <div>
            <label className="text-xs font-medium text-slate-600">Email</label>
            <input
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-1 w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
            />
          </div>
          <div>
            <label className="text-xs font-medium text-slate-600">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-1 w-full px-3 py-2 rounded-lg border border-slate-200 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none text-sm"
            />
          </div>
          <div className="flex items-center justify-between text-xs text-slate-500">
            <label className="flex items-center gap-2">
              <input type="checkbox" className="rounded" defaultChecked /> Remember me
            </label>
            <a href="#" className="text-brand-600 hover:underline">Forgot password?</a>
          </div>
          <button
            type="submit"
            className="w-full py-2.5 rounded-lg bg-brand-600 hover:bg-brand-700 text-white text-sm font-medium transition"
          >Sign in</button>
        </form>

        <div className="mt-6 text-xs text-slate-400 text-center">
          HIPAA-compliant · Audit-logged · v0.9 demo
        </div>
      </div>
    </main>
  );
}
