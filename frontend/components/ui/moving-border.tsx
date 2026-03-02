"use client";

import React from "react";
import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";

export function MovingBorder({
  children,
  duration = 2000,
  className,
  containerClassName,
  borderClassName,
  as: Component = "div",
  ...otherProps
}: {
  children: React.ReactNode;
  duration?: number;
  className?: string;
  containerClassName?: string;
  borderClassName?: string;
  as?: React.ElementType;
} & HTMLMotionProps<"div">) {
  return (
    <Component
      className={cn(
        "bg-transparent relative text-xl p-[1px] overflow-hidden rounded-xl",
        containerClassName,
      )}
      {...otherProps}
    >
      <div className="absolute inset-0" style={{ borderRadius: "inherit" }}>
        <motion.div
          className={cn("absolute inset-[-100%] rounded-full", borderClassName)}
          style={{
            background:
              "conic-gradient(from 0deg, transparent 0 340deg, #0ea5e9 360deg)",
          }}
          animate={{ rotate: 360 }}
          transition={{
            duration: duration / 1000,
            repeat: Infinity,
            ease: "linear",
          }}
        />
      </div>
      <div
        className={cn(
          "relative bg-white dark:bg-neutral-900 border border-transparent rounded-[inherit] z-10",
          className,
        )}
      >
        {children}
      </div>
    </Component>
  );
}
