/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: process.env.BACKEND_INTERNAL_URL || "http://127.0.0.1:8000/api/:path*",
      },
      {
        source: "/metrics/:path*",
        destination: process.env.BACKEND_INTERNAL_URL ? `${process.env.BACKEND_INTERNAL_URL}/metrics/:path*` : "http://127.0.0.1:8000/metrics/:path*",
      },
      {
        source: "/docs",
        destination: process.env.BACKEND_INTERNAL_URL ? `${process.env.BACKEND_INTERNAL_URL}/docs` : "http://127.0.0.1:8000/docs",
      },
      {
        source: "/openapi.json",
        destination: process.env.BACKEND_INTERNAL_URL ? `${process.env.BACKEND_INTERNAL_URL}/openapi.json` : "http://127.0.0.1:8000/openapi.json",
      },
    ];
  },
};

export default nextConfig;
