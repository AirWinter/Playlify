import { isExpired } from "@/utils";
import { expect, jest, test } from "@jest/globals";

jest.mock("axios", () => {});

describe("isExpired working as intended", () => {
  afterEach(() => {
    localStorage.clear();
  });

  test("Returns true when not set", () => {
    expect(localStorage.getItem("expires_at")).toBe(null);
    expect(isExpired()).toBe(true);
  });

  test("Returns true when expired", () => {
    localStorage.setItem("expires_at", (Date.now() / 1000).toString());
    expect(isExpired()).toBe(true);
  });

  test("Returns false when valid", () => {
    localStorage.setItem("expires_at", (Date.now() / 1000 + 2000).toString());
    expect(isExpired()).toBe(false);
  });
});
