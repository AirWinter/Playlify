import { getAllTracksFromLibrary } from "@/services/songs";
import { expect, jest, test } from "@jest/globals";

const mockGet = jest.fn(() =>
  Promise.resolve({
    data: {
      all_songs: "test_all_songs",
      all_artists: "test_all_artists",
      all_genres: "test_all_genres",
    },
  })
);
jest.mock("axios", () => ({
  get: () => mockGet(),
}));

describe("Songs Service", () => {
  afterEach(() => {
    jest.clearAllMocks();
    sessionStorage.clear();
  });
  test("GetAllTracksFromLibrary already set don't call axios", async () => {
    sessionStorage.setItem("all_songs", "");
    sessionStorage.setItem("all_artists", "");
    await getAllTracksFromLibrary();
    expect(mockGet).toBeCalledTimes(0);
  });

  test("GetAllTracksFromLibrary not set should call axios", async () => {
    await getAllTracksFromLibrary();
    expect(mockGet).toBeCalledTimes(1);
    expect(sessionStorage.getItem("all_songs")).toBe(
      JSON.stringify("test_all_songs")
    );
    expect(sessionStorage.getItem("all_artists")).toBe(
      JSON.stringify("test_all_artists")
    );
  });
});
