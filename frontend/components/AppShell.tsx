"use client";

import React, { useState } from "react";
import { usePathname } from "next/navigation";
import { Sidebar, SidebarBody, SidebarLink } from "@/components/ui/sidebar";
import {
  LayoutDashboard,
  HeartPulse,
  Activity,
  MessageSquare,
  Bell,
  Settings,
} from "lucide-react";
import Link from "next/link";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

const NAV_LINKS = [
  {
    label: "Dashboard",
    href: "/dashboard",
    icon: <LayoutDashboard className="h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Health Check",
    href: "/health-check",
    icon: <HeartPulse className="h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Live Monitor",
    href: "/live-monitor",
    icon: <Activity className="h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Chat",
    href: "/chat",
    icon: <MessageSquare className="h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Alerts",
    href: "/alerts",
    icon: <Bell className="h-5 w-5 flex-shrink-0" />,
  },
  {
    label: "Settings",
    href: "/settings",
    icon: <Settings className="h-5 w-5 flex-shrink-0" />,
  },
];

const Logo = () => (
  <Link
    href="/"
    className="relative z-20 flex items-center space-x-2 py-1 text-sm font-normal"
  >
    <div className="h-6 w-7 flex-shrink-0 rounded-br-lg rounded-tl-lg rounded-tr-sm rounded-bl-sm bg-gradient-to-br from-teal-400 to-teal-600" />
    <motion.span
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="whitespace-pre font-semibold text-white"
    >
      AI Health Monitor
    </motion.span>
  </Link>
);

const LogoIcon = () => (
  <Link
    href="/"
    className="relative z-20 flex items-center space-x-2 py-1 text-sm font-normal"
  >
    <div className="h-6 w-7 flex-shrink-0 rounded-br-lg rounded-tl-lg rounded-tr-sm rounded-bl-sm bg-gradient-to-br from-teal-400 to-teal-600" />
  </Link>
);

export default function AppShell({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  // Landing page renders full-screen without the sidebar shell
  if (pathname === "/") {
    return <>{children}</>;
  }

  return (
    <div
      className={cn(
        "flex w-full flex-1 flex-col overflow-hidden md:flex-row",
        "h-screen",
      )}
      style={{
        background:
          "linear-gradient(180deg, #021a17 0%, #04302a 50%, #053d34 100%)",
      }}
    >
      <Sidebar open={open} setOpen={setOpen}>
        <SidebarBody className="justify-between gap-10 border-r border-white/[0.08] bg-[#031f1b]">
          <div className="flex flex-1 flex-col overflow-y-auto overflow-x-hidden">
            {open ? <Logo /> : <LogoIcon />}
            <div className="mt-8 flex flex-col gap-2">
              {NAV_LINKS.map((link) => (
                <SidebarLink
                  key={link.href}
                  link={link}
                  active={pathname === link.href}
                />
              ))}
            </div>
          </div>
          <div>
            <SidebarLink
              link={{
                label: "Health Monitor v1.0",
                href: "#",
                icon: (
                  <div className="flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-full bg-teal-900/50 text-xs font-bold text-teal-300">
                    AI
                  </div>
                ),
              }}
            />
          </div>
        </SidebarBody>
      </Sidebar>

      {/* Main content */}
      <main className="flex flex-1 flex-col overflow-y-auto">
        <div className="flex-1 p-4 md:p-8">{children}</div>
      </main>
    </div>
  );
}
