import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { RoundTable } from "./RoundTable";

// Shared mutable mock state
const mockStore: Record<string, any> = {
  roundTableMode: false,
  arrangeRoundTable: vi.fn(),
  scatterAgents: vi.fn(),
};

// vi.mock is hoisted — returns the selector result
vi.mock("@/stores/partyStore", () => ({
  usePartyStore: vi.fn((selector: (s: typeof mockStore) => any) => selector(mockStore)),
}));

describe("RoundTable", () => {
  beforeEach(() => {
    mockStore.roundTableMode = false;
    mockStore.arrangeRoundTable.mockClear();
    mockStore.scatterAgents.mockClear();
  });

  it("shows Activate button when not in round table mode", () => {
    render(<RoundTable partyId="test-party" />);
    expect(screen.getByText("Activate")).toBeInTheDocument();
  });

  it("switches to Active when roundTableMode changes", () => {
    render(<RoundTable partyId="test-party" />);
    expect(screen.getByText("Activate")).toBeInTheDocument();

    // Mutate the shared mock state to simulate store update
    mockStore.roundTableMode = true;

    // Re-render picks up the new state from the mock
    render(<RoundTable partyId="test-party" />);
    expect(screen.getByText("Active")).toBeInTheDocument();
  });

  it("calls arrangeRoundTable on Activate click", () => {
    render(<RoundTable partyId="test-party" />);
    fireEvent.click(screen.getByText("Activate"));
    expect(mockStore.arrangeRoundTable).toHaveBeenCalledWith(2.5, 0, 0);
  });

  it("calls scatterAgents when toggling off", () => {
    mockStore.roundTableMode = true;
    render(<RoundTable partyId="test-party" />);
    fireEvent.click(screen.getByText("Active"));
    expect(mockStore.scatterAgents).toHaveBeenCalledWith("test-party", 8);
  });

  it("displays contextual description text", () => {
    render(<RoundTable partyId="test-party" />);
    expect(screen.getByText("Round Table")).toBeInTheDocument();
    expect(screen.getByText("🍽️")).toBeInTheDocument();
    expect(screen.getByText(/Click Activate/i)).toBeInTheDocument();
  });
});
