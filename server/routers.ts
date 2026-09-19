import { z } from "zod";
import { invokeLLM } from "./_core/llm";
import { getLearningFlowsForUser, getProgressForUser, getTopicsForUser } from "./db";
import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { protectedProcedure, publicProcedure, router } from "./_core/trpc";

const messageSchema = z.object({
  role: z.enum(["user", "assistant", "system"]),
  content: z.string().min(1),
});

function contentToText(content: unknown) {
  if (typeof content === "string") return content;
  if (Array.isArray(content)) {
    return content
      .map((part) => (typeof part === "string" ? part : (part as { text?: string }).text ?? ""))
      .join("");
  }
  return "I’m ready to help you learn. Try asking about a concept, example, or project doubt.";
}

export const appRouter = router({
  system: systemRouter,
  auth: router({
    me: publicProcedure.query((opts) => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
  }),
  dashboard: router({
    snapshot: protectedProcedure.query(async ({ ctx }) => {
      const [progress, flows, topics] = await Promise.all([
        getProgressForUser(ctx.user.id),
        getLearningFlowsForUser(ctx.user.id),
        getTopicsForUser(ctx.user.id),
      ]);
      return {
        progress: progress ?? { totalCredits: 0, currentStreak: 0, questionsSolved: 0, accuracy: 0, learningLevel: "Beginner" },
        flows,
        topics,
      };
    }),
  }),
  ai: router({
    chat: publicProcedure
      .input(z.object({ messages: z.array(messageSchema).min(1), topic: z.string().optional() }))
      .mutation(async ({ input }) => {
        const response = await invokeLLM({
          messages: [
            {
              role: "system",
              content: "You are LearnFlow AI, a warm and natural personal tutor. Have a real conversation, not an exam-only interaction. Answer normal greetings, casual messages, follow-up questions, simple doubts, definitions, translations, and academic questions. Detect the language of the user's latest message and write BOTH the answer and any challenge in that exact language. If the user writes Tamil, reply fully in Tamil; if Malayalam, reply fully in Malayalam; likewise for Telugu, Kannada, Hindi, Bengali, Gujarati, Marathi, or any other language. If the user writes Tanglish or another mixed-language style, mirror that same style naturally. Never switch to English merely because the topic is technical, and do not mix languages unless the user mixed them. For coding questions, explain the code line by line using short inline comments such as // this line creates the loop, then give a clean corrected example when useful. For mathematics, solve step by step, show the formula, substitute values, and state the final answer clearly; never skip intermediate reasoning. For project questions, suggest a practical approach with recommended steps, tools, risks, and a small next action. Keep simple questions simple, ask a brief clarifying question only when truly needed, and be encouraging. Use examples only when helpful. Generate a Concept Challenge only when the user is clearly asking to learn, practice, revise, or understand an academic topic; for greetings, casual conversation, meanings, quick doubts, or follow-ups, return an empty challenge string. Return JSON with answer and challenge fields.",
            },
            ...input.messages,
          ],
          response_format: {
            type: "json_schema",
            json_schema: {
              name: "learning_response",
              strict: true,
              schema: {
                type: "object",
                properties: {
                  answer: { type: "string" },
                  challenge: { type: "string", description: "A practice question only when useful; otherwise an empty string." },
                },
                required: ["answer", "challenge"],
                additionalProperties: false,
              },
            },
          },
        });
        const raw = contentToText(response.choices?.[0]?.message?.content);
        try {
          const parsed = JSON.parse(raw) as { answer: string; challenge: string };
          return parsed;
        } catch {
          return {
            answer: raw,
            challenge: "In one sentence, explain the main idea using your own words.",
          };
        }
      }),
    personalize: protectedProcedure
      .input(z.object({ topic: z.string(), level: z.number().min(0).max(100) }))
      .mutation(async ({ input }) => {
        const response = await invokeLLM({
          messages: [
            { role: "system", content: "Give concise, encouraging study recommendations for a college student." },
            { role: "user", content: `The student is at ${input.level}% confidence in ${input.topic}. Recommend one next step.` },
          ],
        });
        return { recommendation: contentToText(response.choices?.[0]?.message?.content) };
      }),
  }),
  challenges: router({
    evaluate: protectedProcedure
      .input(z.object({ prompt: z.string(), answer: z.string().min(1) }))
      .mutation(async ({ input }) => {
        const response = await invokeLLM({
          messages: [
            { role: "system", content: "Evaluate the student's answer gently. Return JSON with score from 0 to 10, correct boolean, and feedback string." },
            { role: "user", content: `Challenge: ${input.prompt}\nStudent answer: ${input.answer}` },
          ],
          response_format: {
            type: "json_schema",
            json_schema: {
              name: "challenge_evaluation",
              strict: true,
              schema: {
                type: "object",
                properties: {
                  score: { type: "integer" },
                  correct: { type: "boolean" },
                  feedback: { type: "string" },
                },
                required: ["score", "correct", "feedback"],
                additionalProperties: false,
              },
            },
          },
        });
        try {
          return JSON.parse(contentToText(response.choices?.[0]?.message?.content));
        } catch {
          return { score: 5, correct: false, feedback: "Good attempt. Compare your answer with the concept recap and try once more." };
        }
      }),
  }),
  practice: router({
    generate: protectedProcedure
      .input(z.object({ topic: z.string(), subject: z.string(), difficulty: z.enum(["easy", "medium", "hard"]) }))
      .mutation(async ({ input }) => {
        const response = await invokeLLM({
          messages: [
            { role: "system", content: "Create one clear educational multiple-choice question. Return JSON with question, options array, answer, and explanation." },
            { role: "user", content: `${input.subject} / ${input.topic} / ${input.difficulty}` },
          ],
          response_format: {
            type: "json_schema",
            json_schema: {
              name: "practice_question",
              strict: true,
              schema: {
                type: "object",
                properties: {
                  question: { type: "string" },
                  options: { type: "array", items: { type: "string" } },
                  answer: { type: "string" },
                  explanation: { type: "string" },
                },
                required: ["question", "options", "answer", "explanation"],
                additionalProperties: false,
              },
            },
          },
        });
        return JSON.parse(contentToText(response.choices?.[0]?.message?.content));
      }),
  }),
});

export type AppRouter = typeof appRouter;
