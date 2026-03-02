"use client";

import React from "react";
import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface FloatingIcon {
  icon: React.ReactNode;
  label: string;
  position: { x: string; y: string };
}

interface HealthHeroProps {
  logo?: string;
  navigation?: Array<{
    label: string;
    href?: string;
    onClick?: () => void;
  }>;
  contactButton?: {
    label: string;
    onClick: () => void;
  };
  title: string;
  highlightedText?: string;
  subtitle: string;
  ctaButton?: {
    label: string;
    onClick: () => void;
  };
  secondaryCtaButton?: {
    label: string;
    onClick: () => void;
  };
  floatingIcons?: FloatingIcon[];
  trustedByText?: string;
  brands?: Array<{
    name: string;
    logo: React.ReactNode;
  }>;
  className?: string;
  children?: React.ReactNode;
}

export function HealthHero({
  logo = "AI Health Monitor",
  navigation = [
    { label: "Features" },
    { label: "Monitor" },
    { label: "About" },
  ],
  contactButton,
  title,
  highlightedText = "AI Health Monitor",
  subtitle,
  ctaButton,
  secondaryCtaButton,
  floatingIcons = [],
  trustedByText = "Powered by",
  brands = [],
  className,
  children,
}: HealthHeroProps) {
  return (
    <section
      className={cn(
        "relative w-full min-h-screen flex flex-col overflow-hidden",
        className,
      )}
      style={{
        background:
          "linear-gradient(180deg, #021a17 0%, #04302a 50%, #053d34 100%)",
      }}
      role="banner"
      aria-label="Hero section"
    >
      {/* Radial Glow Background */}
      <div className="absolute inset-0 pointer-events-none" aria-hidden="true">
        <div
          className="absolute"
          style={{
            width: "1200px",
            height: "1200px",
            left: "50%",
            top: "50%",
            transform: "translate(-50%, -50%)",
            background:
              "radial-gradient(circle, rgba(20,184,166,0.25) 0%, rgba(20,184,166,0) 70%)",
            filter: "blur(100px)",
          }}
        />
        {/* Secondary subtle glow */}
        <div
          className="absolute"
          style={{
            width: "600px",
            height: "600px",
            left: "20%",
            top: "30%",
            background:
              "radial-gradient(circle, rgba(56,189,248,0.12) 0%, transparent 70%)",
            filter: "blur(80px)",
          }}
        />
      </div>

      {/* Grid pattern overlay */}
      <div
        className="absolute inset-0 pointer-events-none opacity-[0.03]"
        aria-hidden="true"
        style={{
          backgroundImage:
            "linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
      />

      {/* Header */}
      <motion.header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="relative z-20 flex flex-row justify-between items-center px-6 lg:px-16"
        style={{ paddingTop: "24px", paddingBottom: "24px" }}
      >
        {/* Logo */}
        <div className="flex items-center gap-2.5">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-br from-teal-400 to-teal-600 flex items-center justify-center">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
            </svg>
          </div>
          <span
            style={{
              fontFamily: "Inter, system-ui, sans-serif",
              fontWeight: 700,
              fontSize: "18px",
              color: "#FFFFFF",
            }}
          >
            {logo}
          </span>
        </div>

        {/* Navigation */}
        <nav
          className="hidden lg:flex flex-row items-center gap-8"
          aria-label="Main navigation"
        >
          {navigation.map((item, index) => (
            <a
              key={index}
              href={item.href || "#"}
              onClick={item.onClick}
              className="hover:text-teal-300 transition-colors"
              style={{
                fontFamily: "Inter, system-ui, sans-serif",
                fontSize: "14px",
                fontWeight: 500,
                color: "rgba(255,255,255,0.7)",
              }}
            >
              {item.label}
            </a>
          ))}
        </nav>

        {/* Contact Button */}
        {contactButton && (
          <button
            onClick={contactButton.onClick}
            className="px-5 py-2 rounded-full transition-all hover:scale-105 hover:border-teal-400/60"
            style={{
              background: "transparent",
              border: "1px solid rgba(255,255,255,0.2)",
              fontFamily: "Inter, system-ui, sans-serif",
              fontSize: "14px",
              fontWeight: 500,
              color: "#FFFFFF",
            }}
          >
            {contactButton.label}
          </button>
        )}
      </motion.header>

      {/* Main Content */}
      {children ? (
        <div className="relative z-10 flex-1 flex items-center justify-center w-full">
          {children}
        </div>
      ) : (
        <div className="relative z-10 flex-1 flex flex-col items-center justify-center px-4">
          {/* Floating Health Icons */}
          {floatingIcons.map((item, index) => (
            <motion.div
              key={index}
              className="absolute hidden lg:flex flex-col items-center gap-2"
              style={{
                left: item.position.x,
                top: item.position.y,
              }}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{
                opacity: 1,
                scale: 1,
                y: [0, -15, 0],
              }}
              transition={{
                opacity: { duration: 0.6, delay: 0.3 + index * 0.1 },
                scale: { duration: 0.6, delay: 0.3 + index * 0.1 },
                y: {
                  duration: 3 + index * 0.5,
                  repeat: Infinity,
                  ease: "easeInOut",
                },
              }}
            >
              <div
                style={{
                  width: "72px",
                  height: "72px",
                  borderRadius: "50%",
                  background: "rgba(20,184,166,0.1)",
                  backdropFilter: "blur(10px)",
                  border: "1px solid rgba(20,184,166,0.25)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: "0 0 40px rgba(20,184,166,0.3)",
                }}
              >
                {item.icon}
              </div>
              <span
                style={{
                  fontFamily: "Inter, system-ui, sans-serif",
                  fontSize: "11px",
                  fontWeight: 600,
                  color: "rgba(255,255,255,0.6)",
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                {item.label}
              </span>
            </motion.div>
          ))}

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="flex flex-col items-center text-center max-w-4xl"
            style={{ gap: "28px" }}
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="flex items-center gap-2 px-4 py-1.5 rounded-full"
              style={{
                background: "rgba(20,184,166,0.1)",
                border: "1px solid rgba(20,184,166,0.25)",
              }}
            >
              <div className="h-2 w-2 rounded-full bg-teal-400 animate-pulse" />
              <span
                style={{
                  fontFamily: "Inter, system-ui, sans-serif",
                  fontSize: "12px",
                  fontWeight: 500,
                  color: "rgba(255,255,255,0.7)",
                  letterSpacing: "0.05em",
                }}
              >
                AI-Powered Health Intelligence
              </span>
            </motion.div>

            {/* Title */}
            <h1
              style={{
                fontFamily: "Inter, system-ui, sans-serif",
                fontWeight: 600,
                fontSize: "clamp(32px, 5vw, 68px)",
                lineHeight: "1.1",
                color: "#FFFFFF",
                letterSpacing: "-0.03em",
              }}
            >
              {title}
              <br />
              <span
                style={{
                  background:
                    "linear-gradient(90deg, #14B8A6 0%, #38BDF8 50%, #14B8A6 100%)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                  fontWeight: 700,
                }}
              >
                {highlightedText}
              </span>
            </h1>

            {/* Subtitle */}
            <p
              style={{
                fontFamily: "Inter, system-ui, sans-serif",
                fontWeight: 400,
                fontSize: "clamp(15px, 2vw, 18px)",
                lineHeight: "1.7",
                color: "rgba(255,255,255,0.6)",
                maxWidth: "560px",
              }}
            >
              {subtitle}
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row items-center gap-4 mt-2">
              {ctaButton && (
                <motion.button
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: 0.6 }}
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={ctaButton.onClick}
                  className="px-8 py-3.5 rounded-xl transition-all font-semibold text-[15px]"
                  style={{
                    background:
                      "linear-gradient(135deg, #14B8A6 0%, #0D9488 100%)",
                    color: "#FFFFFF",
                    boxShadow:
                      "0 4px 24px rgba(20,184,166,0.4), 0 1px 3px rgba(0,0,0,0.2)",
                  }}
                >
                  {ctaButton.label}
                </motion.button>
              )}

              {secondaryCtaButton && (
                <motion.button
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.6, delay: 0.7 }}
                  whileHover={{ scale: 1.04 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={secondaryCtaButton.onClick}
                  className="px-8 py-3.5 rounded-xl transition-all font-medium text-[15px]"
                  style={{
                    background: "transparent",
                    border: "1px solid rgba(255,255,255,0.2)",
                    color: "#FFFFFF",
                  }}
                >
                  {secondaryCtaButton.label}
                </motion.button>
              )}
            </div>
          </motion.div>
        </div>
      )}

      {/* Brand / Tech Slider */}
      {brands.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.8 }}
          className="relative z-10 w-full overflow-hidden"
          style={{ paddingTop: "48px", paddingBottom: "48px" }}
        >
          {/* "Powered by" Text */}
          <div className="text-center mb-6">
            <span
              style={{
                fontFamily: "Inter, system-ui, sans-serif",
                fontSize: "11px",
                fontWeight: 500,
                color: "rgba(255,255,255,0.4)",
                letterSpacing: "0.12em",
                textTransform: "uppercase",
              }}
            >
              {trustedByText}
            </span>
          </div>

          {/* Gradient Overlays */}
          <div
            className="absolute left-0 top-0 bottom-0 z-10 pointer-events-none"
            style={{
              width: "200px",
              background:
                "linear-gradient(90deg, #021a17 0%, rgba(2,26,23,0) 100%)",
            }}
          />
          <div
            className="absolute right-0 top-0 bottom-0 z-10 pointer-events-none"
            style={{
              width: "200px",
              background:
                "linear-gradient(270deg, #021a17 0%, rgba(2,26,23,0) 100%)",
            }}
          />

          {/* Scrolling Brands */}
          <motion.div
            className="flex items-center"
            animate={{
              x: [0, -(brands.length * 200)],
            }}
            transition={{
              x: {
                repeat: Infinity,
                repeatType: "loop",
                duration: brands.length * 5,
                ease: "linear",
              },
            }}
            style={{ gap: "80px", paddingLeft: "80px" }}
          >
            {[...brands, ...brands].map((brand, index) => (
              <div
                key={index}
                className="flex-shrink-0 flex items-center justify-center opacity-40 hover:opacity-60 transition-opacity"
                style={{ width: "120px", height: "40px" }}
              >
                {brand.logo}
              </div>
            ))}
          </motion.div>
        </motion.div>
      )}
    </section>
  );
}
