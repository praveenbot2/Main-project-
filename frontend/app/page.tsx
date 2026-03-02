"use client";

import { useRouter } from "next/navigation";
import { HeartPulse, Activity, Brain, Bell } from "lucide-react";
import { HealthHero } from "@/components/ui/health-hero";

export default function LandingPage() {
  const router = useRouter();

  return (
    <HealthHero
      logo="AI Health Monitor"
      navigation={[
        { label: "Features", href: "#features" },
        { label: "Dashboard", href: "/dashboard" },
        { label: "Health Check", href: "/health-check" },
        { label: "Live Monitor", href: "/live-monitor" },
      ]}
      contactButton={{
        label: "Open Chat",
        onClick: () => router.push("/chat"),
      }}
      title="Your Health, Powered by"
      highlightedText="Artificial Intelligence"
      subtitle="Monitor vitals in real-time, get AI-powered health predictions, receive instant alerts, and chat with an intelligent health assistant — all in one platform."
      ctaButton={{
        label: "Go to Dashboard",
        onClick: () => router.push("/dashboard"),
      }}
      secondaryCtaButton={{
        label: "Try Health Check",
        onClick: () => router.push("/health-check"),
      }}
      floatingIcons={[
        {
          icon: <HeartPulse className="h-8 w-8 text-teal-400" />,
          label: "Vitals",
          position: { x: "8%", y: "25%" },
        },
        {
          icon: <Brain className="h-8 w-8 text-teal-400" />,
          label: "AI Prediction",
          position: { x: "12%", y: "62%" },
        },
        {
          icon: <Activity className="h-8 w-8 text-sky-400" />,
          label: "Monitoring",
          position: { x: "82%", y: "22%" },
        },
        {
          icon: <Bell className="h-8 w-8 text-amber-400" />,
          label: "Alerts",
          position: { x: "85%", y: "60%" },
        },
      ]}
      trustedByText="Built With"
      brands={[
        {
          name: "Next.js",
          logo: (
            <svg width="80" height="24" viewBox="0 0 80 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Next.js
              </text>
            </svg>
          ),
        },
        {
          name: "Flask",
          logo: (
            <svg width="60" height="24" viewBox="0 0 60 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Flask
              </text>
            </svg>
          ),
        },
        {
          name: "TailwindCSS",
          logo: (
            <svg width="100" height="24" viewBox="0 0 100 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Tailwind
              </text>
            </svg>
          ),
        },
        {
          name: "Scikit-learn",
          logo: (
            <svg width="100" height="24" viewBox="0 0 100 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Scikit-learn
              </text>
            </svg>
          ),
        },
        {
          name: "Framer Motion",
          logo: (
            <svg width="120" height="24" viewBox="0 0 120 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Framer Motion
              </text>
            </svg>
          ),
        },
        {
          name: "Recharts",
          logo: (
            <svg width="80" height="24" viewBox="0 0 80 24" fill="none">
              <text
                x="0"
                y="18"
                fill="rgba(255,255,255,0.5)"
                fontSize="16"
                fontWeight="600"
              >
                Recharts
              </text>
            </svg>
          ),
        },
      ]}
    />
  );
}
