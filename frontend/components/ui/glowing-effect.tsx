"use client";

import React from "react";
import { cn } from "@/lib/utils";

export const GlowingEffect = ({
  children,
  className,
  glowColor = "rgba(14, 165, 233, 0.15)",
}: {
  children: React.ReactNode;
  className?: string;
  glowColor?: string;
}) => {
  return (
    <div className={cn("relative group", className)}>
      <div
        className="absolute -inset-0.5 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 blur-xl"
        style={{ background: glowColor }}
      />
      <div className="relative">{children}</div>
    </div>
  );
};
