import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';

// Mock scrollIntoView in jsdom
if (!HTMLElement.prototype.scrollIntoView) {
  HTMLElement.prototype.scrollIntoView = vi.fn();
}

// Mock next/navigation
vi.mock('next/navigation', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    prefetch: vi.fn(),
    pathname: '/',
    query: {},
    asPath: '/',
  }),
  usePathname: () => '/',
  useSearchParams: () => ({
    get: vi.fn(),
  }),
}));

// Mock next/three-js components (SSR-safe)
vi.mock('next/dynamic', () => ({
  default: (fn: () => Promise<any>) => fn,
}));
