'use client'

import { useEffect, useRef, useState } from 'react'

export default function LoginPage() {
  const bgRef = useRef<HTMLDivElement>(null)
  const vantaRef = useRef<any>(null)
  const [isLogin, setIsLogin] = useState(true)

  useEffect(() => {
    if (typeof window === 'undefined' || !bgRef.current || vantaRef.current) return

    const initVanta = async () => {
      const THREE = await import('three')
      // @ts-ignore
      window.THREE = THREE

      const vantaModule = await import('vanta/dist/vanta.birds.min')
      const BIRDS = vantaModule.default || vantaModule

      vantaRef.current = BIRDS({
        el: bgRef.current,
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00,
        scale: 1.00,
        scaleMobile: 1.00,
        backgroundColor: 0x0,
        birdSize: 1.50,
        wingSpan: 20.00,
        speedLimit: 4.00,
        separation: 60.00,
        alignment: 40.00,
        cohesion: 40.00,
        quantity: 3.00,
      })
    }

    initVanta()

    return () => {
      if (vantaRef.current) {
        vantaRef.current.destroy()
      }
    }
  }, [])

  return (
    <div className="relative min-h-screen overflow-hidden">
      <div
        ref={bgRef}
        className="fixed top-0 left-0 w-full h-full -z-10"
      />

      <div className="flex items-center justify-center min-h-screen">
        <div className="bg-white/10 backdrop-blur-md p-8 rounded-2xl shadow-2xl w-80 border border-white/20">
          <h2 className="text-white text-2xl mb-6 font-bold text-center">
            {isLogin ? '登录' : '注册'}
          </h2>

          <input
            className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
            type="email"
            placeholder="邮箱"
          />

          {!isLogin && (
            <input
              className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
              type="text"
              placeholder="用户名"
            />
          )}

          <input
            className="w-full p-3 mb-4 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
            type="password"
            placeholder="密码"
          />

          {!isLogin && (
            <input
              className="w-full p-3 mb-6 rounded-lg bg-transparent border border-white/30 text-white placeholder-white/60 outline-none focus:border-white/80 transition"
              type="password"
              placeholder="确认密码"
            />
          )}

          {isLogin && <div className="mb-2" />}

          <button className="w-full bg-blue-500/80 hover:bg-blue-500 text-white p-3 rounded-lg font-medium transition duration-200 mb-4">
            {isLogin ? '登录' : '注册'}
          </button>

          <div className="text-center">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-white/60 hover:text-white text-sm transition"
            >
              {isLogin ? '没有账号？去注册' : '已有账号？去登录'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
