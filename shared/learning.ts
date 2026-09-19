export type ChallengeResult = "correct" | "partial" | "wrong";

export function scoreChallengeAnswer(answer: string): ChallengeResult {
  const normalized = answer.toLowerCase();
  if (normalized.includes("base") || normalized.includes("smaller")) return "correct";
  if (answer.trim().length > 24) return "partial";
  return "wrong";
}

export function capOfflineResponse(content: string, maxWords = 100) {
  return content.trim().split(/\s+/).filter(Boolean).slice(0, maxWords).join(" ");
}
