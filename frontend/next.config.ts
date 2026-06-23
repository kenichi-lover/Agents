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
    ];
  },
};

export default nextConfig;
