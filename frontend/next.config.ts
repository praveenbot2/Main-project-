import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // In local dev, proxy /api/* requests to the Flask backend on :5000.
  // On Vercel this is handled by vercel.json routes instead.
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "http://127.0.0.1:5000/:path*",
      },
    ];
  },
};

export default nextConfig;
