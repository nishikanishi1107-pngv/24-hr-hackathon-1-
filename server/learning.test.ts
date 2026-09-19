import { describe, expect, it } from "vitest";
import { capOfflineResponse, scoreChallengeAnswer } from "../shared/learning";

describe("learning utilities", () => {
  it("scores a concept challenge using understanding signals", () => {
    expect(scoreChallengeAnswer("The base case stops the recursive calls.")).toBe("correct");
    expect(scoreChallengeAnswer("It returns a value after several nested calls are made.")).toBe("partial");
    expect(scoreChallengeAnswer("I am not sure.")).toBe("wrong");
  });

  it("caps offline responses at the requested word limit", () => {
    const content = Array.from({ length: 125 }, (_, index) => `word${index}`).join(" ");
    const result = capOfflineResponse(content);
    expect(result.split(" ")).toHaveLength(100);
    expect(result.endsWith("word99")).toBe(true);
  });
});
