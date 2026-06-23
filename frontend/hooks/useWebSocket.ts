"use client";

import { useEffect, useRef, useState, useCallback } from "react";

interface WebSocketMessage {
  type: string;
  [key: string]: any;
}

export function useWebSocket(partyId: string, token: string) {
  const ws = useRef<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [messages, setMessages] = useState<WebSocketMessage[]>([]);
  const reconnectTimeout = useRef<ReturnType<typeof setTimeout>>(undefined as any);

  const connect = useCallback(() => {
    const wsUrl = `${process.env.NEXT_PUBLIC_WS_URL}/ws/party/${partyId}?token=${token}`;
    ws.current = new WebSocket(wsUrl);

    ws.current.onopen = () => {
      setIsConnected(true);
      console.log("🎉 Connected to party:", partyId);
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMessages((prev) => [...prev, data]);
      
      // 处理特殊消息类型
      if (data.type === "chat:thinking") {
        // 显示 Agent 思考动画
      }
    };

    ws.current.onclose = () => {
      setIsConnected(false);
      // 自动重连
      reconnectTimeout.current = setTimeout(connect, 3000);
    };

    ws.current.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  }, [partyId, token]);

  const sendMessage = useCallback((message: WebSocketMessage) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(message));
    }
  }, []);

  useEffect(() => {
    connect();
    return () => {
      clearTimeout(reconnectTimeout.current);
      ws.current?.close();
    };
  }, [connect]);

  return { isConnected, messages, sendMessage };
}
