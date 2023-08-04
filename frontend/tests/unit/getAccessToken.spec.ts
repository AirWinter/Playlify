import * as utilsFunc from "@/utils";
import { expect, jest, test } from "@jest/globals";

jest.mock("axios", () => ({
  get: jest.fn(() =>
    Promise.resolve({
      data: {
        access_token: "test_access_token",
        refresh_token: "test_refresh_token",
        expires_at: Date.now() / 1000 + 3600,
      },
    })
  ),
}));

describe("getAccessToken", () => {
  afterEach(() => {
    localStorage.clear();
  });

  test("should return an empty string if there is no refresh token", async () => {
    jest.spyOn(utilsFunc, "isExpired").mockImplementation(() => false);

    const result = await utilsFunc.getAccessToken();

    expect(result).toBe("");
  });

  test("should fetch new access token if token is expired", async () => {
    jest.spyOn(utilsFunc, "isExpired").mockImplementation(() => true);

    // Set the refresh token in local storage
    localStorage.setItem("refresh_token", "");
    const result = await utilsFunc.getAccessToken();
    expect(result).toBe("test_access_token");

    // Ensure that the access token, refresh token, and expiration time are stored in local storage
    expect(localStorage.getItem("access_token")).toBe("test_access_token");
    expect(localStorage.getItem("refresh_token")).toBe("test_refresh_token");
    expect(Number(localStorage.getItem("expires_at"))).toBeCloseTo(
      Date.now() / 1000 + 3600,
      -2
    );
  });

  test("should return the existing access token if it is not expired", async () => {
    jest.spyOn(utilsFunc, "isExpired").mockImplementation(() => false);

    // Set a test access token in local storage
    localStorage.setItem("access_token", "test_access_token");
    debugger;
    const result = await utilsFunc.getAccessToken();

    expect(result).toBe("test_access_token");
  });
});
