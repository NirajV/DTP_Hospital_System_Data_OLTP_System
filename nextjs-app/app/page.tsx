"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Root() {
  const router = useRouter();
  useEffect(() => {
    const signedIn = typeof window !== "undefined" && localStorage.getItem("user_id");
    router.replace(signedIn ? "/dashboard" : "/login");
  }, [router]);
  return null;
}
