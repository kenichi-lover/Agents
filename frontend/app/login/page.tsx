"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function LoginPage() {
  const bgRef = useRef<HTMLDivElement>(null);
  const vantaRef = useRef<any>(null);
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  // VANTA init — keep existing logic
  useEffect(() => {
    if (typeof window === "undefined" || !bgRef.current || vantaRef.current)
      return;

    const initVanta = async () => {
      const THREE = await import("three");
      window.THREE = THREE;
      const vantaModule = await import("vanta/dist/vanta.birds.min");
      const BIRDS = vantaModule.default || vantaModule;
      vantaRef.current = BIRDS({
        el: bgRef.current,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200,
        minWidth: 200,
        scale: 1,
        scaleMobile: 1,
        backgroundColor: 0x0,
        birdSize: 1.5,
        wingSpan: 20,
        speedLimit: 4,
        separation: 60,
        alignment: 40,
        cohesion: 40,
        quantity: 3,
      });
    };

    initVanta();
    return () => {
      if (vantaRef.current) vantaRef.current.destroy();
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (!isLogin && password !== confirmPassword) {
        setError("Passwords do not match");
        setLoading(false);
        return;
      }

      const body: Record<string, string> = { email, password };
      if (!isLogin) body.username = username;

      const url = isLogin ? "/api/auth/login" : "/api/auth/register";
      const resp = await axios.post(url, body, {
        headers: { "Content-Type": "application/json" },
      });

      if (isLogin && resp.data.access_token) {
        localStorage.setItem("access_token", resp.data.access_token);
        router.push("/party/demo");
      } else if (!isLogin) {
        setIsLogin(true);
        setError("Registration successful, please login");
        // Clear form
        setEmail("");
        setUsername("");
        setPassword("");
        setConfirmPassword("");
      }
    } catch (err: unknown) {
      const detail =
        err instanceof axios.AxiosError && err.response?.data?.detail
          ? err.response.data.detail
          : "Request failed";
      setError(String(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div ref={bgRef} className="fixed inset-0 -z-10" />
      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-white/10 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-80 border border-white/20">
          <h2 className="text-white text-2xl mb-6 font-bold text-center">
            {isLogin ? "Login" : "Register"}
          </h2>

          <form onSubmit={handleSubmit}>
            <input
              className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            {!isLogin && (
              <input
                className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            )}

            <input
              className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

            {!isLogin && (
              <input
                className="w-full p-3 mb-6 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
                type="password"
                placeholder="Confirm Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
              />
            )}

            {isLogin && <div className="mb-2" />}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-500/80 hover:bg-blue-500 text-white p-3 rounded-lg font-medium transition duration-200 mb-4 disabled:opacity-50"
            >
              {loading ? "Loading..." : isLogin ? "Login" : "Register"}
            </button>
          </form>

          {error && (
            <p className="text-red-300 text-sm text-center mb-2">{error}</p>
          )}

          <div className="text-center">
            <button
              type="button"
              onClick={() => setIsLogin(!isLogin)}
              className="text-white/60 hover:text-white text-sm transition"
            >
              {isLogin
                ? "No account? Register"
                : "Have an account? Login"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
