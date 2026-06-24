import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/auth/:path*",
        destination: "http://localhost:8000/api/auth/:path*",
      },
      {
        source: "/api/parties/:path*",
        destination: "http://localhost:8000/api/parties/:path*",
      },
      {
        source: "/api/agents/:path*",
        destination: "http://localhost:8000/api/agents/:path*",
      },
      {
        source: "/api/presence/:path*",
        destination: "http://localhost:8000/api/presence/:path*",
      },
    ];
  },
};

export default nextConfig;
