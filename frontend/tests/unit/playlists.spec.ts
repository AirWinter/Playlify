import { getPlaylists } from "@/services/playlists";
import { expect, jest, test } from "@jest/globals";
import * as utilsFunc from "@/utils";

const mockGet = jest.fn(() =>
  Promise.resolve({
    data: {},
  })
);
jest.mock("axios", () => ({
  get: () => mockGet(),
}));

describe("Playlist Service", () => {
  test("No token string doesn't call axios", async () => {
    jest.spyOn(utilsFunc, "getAccessToken").mockImplementation(async () => "");
    await getPlaylists();
    expect(mockGet).toBeCalledTimes(0);
  });

  test("Valid token string calls axios", async () => {
    jest
      .spyOn(utilsFunc, "getAccessToken")
      .mockImplementation(async () => "valid token");
    var result = await getPlaylists();
    expect(mockGet).toBeCalledTimes(1);
    expect(result).not.toBeUndefined();
  });
});
