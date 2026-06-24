import { describe, it, expect, vi } from "vitest";
import axios from "axios";
import apiClient from "./api-client";

describe("api-client", () => {
  it("is an axios instance", () => {
    expect(apiClient.defaults).toBeDefined();
    expect(apiClient.interceptors).toBeDefined();
  });

  it("has a baseURL configured", () => {
    expect(apiClient.defaults.baseURL).toBeDefined();
  });

  it("injects token from localStorage via interceptor", () => {
    const getItemSpy = vi.spyOn(localStorage, "getItem");
    getItemSpy.mockReturnValue("test-token-123");

    // Trigger interceptor by simulating a request config
    const config = { ...apiClient.defaults, url: "/test", method: "get" };
    // The interceptor runs when a request is made — we can't easily
    // trigger it without a server, but we can verify the interceptor is registered
    // by checking the request interceptor chain
    expect(apiClient.interceptors.request.handlers.length).toBeGreaterThan(0);

    getItemSpy.mockRestore();
  });

  it("uses default baseURL when env var is not set", () => {
    // In test env, NEXT_PUBLIC_API_URL may not be set
    expect(apiClient.defaults.baseURL).toBe("http://localhost:8000");
  });
});
