import { int, mysqlEnum, mysqlTable, text, timestamp, varchar } from "drizzle-orm/mysql-core";

export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export const profiles = mysqlTable("profiles", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  displayName: varchar("displayName", { length: 160 }).notNull(),
  course: varchar("course", { length: 160 }),
  year: varchar("year", { length: 32 }),
  preferredLanguage: varchar("preferredLanguage", { length: 64 }).default("English").notNull(),
  avatarUrl: text("avatarUrl"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export const chats = mysqlTable("chats", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  title: varchar("title", { length: 240 }).notNull(),
  subject: varchar("subject", { length: 120 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export const messages = mysqlTable("messages", {
  id: int("id").autoincrement().primaryKey(),
  chatId: int("chatId").notNull(),
  userId: int("userId").notNull(),
  role: mysqlEnum("role", ["user", "assistant", "system"]).notNull(),
  content: text("content").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const learningFlows = mysqlTable("learningFlows", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  topic: varchar("topic", { length: 160 }).notNull(),
  understandingLevel: int("understandingLevel").default(0).notNull(),
  confidenceScore: int("confidenceScore").default(0).notNull(),
  preferredLanguage: varchar("preferredLanguage", { length: 64 }).default("English").notNull(),
  weakTopics: text("weakTopics"),
  lastStudiedAt: timestamp("lastStudiedAt").defaultNow().notNull(),
});

export const topics = mysqlTable("topics", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  name: varchar("name", { length: 160 }).notNull(),
  subject: varchar("subject", { length: 120 }),
  understandingLevel: int("understandingLevel").default(0).notNull(),
  mistakes: text("mistakes"),
  completedQuestions: int("completedQuestions").default(0).notNull(),
  confidenceScore: int("confidenceScore").default(0).notNull(),
  lastStudiedAt: timestamp("lastStudiedAt").defaultNow().notNull(),
});

export const quizQuestions = mysqlTable("quizQuestions", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  topic: varchar("topic", { length: 160 }).notNull(),
  subject: varchar("subject", { length: 120 }).notNull(),
  type: mysqlEnum("type", ["mcq", "true_false", "short_answer"]).notNull(),
  difficulty: mysqlEnum("difficulty", ["easy", "medium", "hard"]).default("medium").notNull(),
  prompt: text("prompt").notNull(),
  options: text("options"),
  answer: text("answer").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const quizAttempts = mysqlTable("quizAttempts", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  questionId: int("questionId").notNull(),
  answer: text("answer").notNull(),
  score: int("score").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const challenges = mysqlTable("challenges", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  chatId: int("chatId"),
  topic: varchar("topic", { length: 160 }).notNull(),
  prompt: text("prompt").notNull(),
  answer: text("answer"),
  correctAnswer: text("correctAnswer"),
  status: mysqlEnum("status", ["active", "completed", "expired"]).default("active").notNull(),
  score: int("score").default(0).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const challengeAttempts = mysqlTable("challengeAttempts", {
  id: int("id").autoincrement().primaryKey(),
  challengeId: int("challengeId").notNull(),
  userId: int("userId").notNull(),
  answer: text("answer").notNull(),
  score: int("score").default(0).notNull(),
  feedback: text("feedback"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const credits = mysqlTable("credits", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  amount: int("amount").notNull(),
  reason: varchar("reason", { length: 160 }).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const teams = mysqlTable("teams", {
  id: int("id").autoincrement().primaryKey(),
  ownerId: int("ownerId").notNull(),
  name: varchar("name", { length: 160 }).notNull(),
  inviteCode: varchar("inviteCode", { length: 80 }).notNull().unique(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const teamMembers = mysqlTable("teamMembers", {
  id: int("id").autoincrement().primaryKey(),
  teamId: int("teamId").notNull(),
  userId: int("userId").notNull(),
  isOnline: int("isOnline").default(1).notNull(),
  joinedAt: timestamp("joinedAt").defaultNow().notNull(),
});

export const teamMessages = mysqlTable("teamMessages", {
  id: int("id").autoincrement().primaryKey(),
  teamId: int("teamId").notNull(),
  userId: int("userId").notNull(),
  content: text("content").notNull(),
  attachmentUrl: text("attachmentUrl"),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const vaultFiles = mysqlTable("vaultFiles", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  name: varchar("name", { length: 240 }).notNull(),
  category: varchar("category", { length: 80 }).default("Documents").notNull(),
  fileKey: text("fileKey").notNull(),
  url: text("url").notNull(),
  mimeType: varchar("mimeType", { length: 120 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export const progress = mysqlTable("progress", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  totalCredits: int("totalCredits").default(0).notNull(),
  currentStreak: int("currentStreak").default(0).notNull(),
  questionsSolved: int("questionsSolved").default(0).notNull(),
  accuracy: int("accuracy").default(0).notNull(),
  learningLevel: varchar("learningLevel", { length: 80 }).default("Beginner").notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export const userPreferences = mysqlTable("userPreferences", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  theme: mysqlEnum("theme", ["light", "dark"]).default("dark").notNull(),
  language: varchar("language", { length: 64 }).default("English").notNull(),
  notificationsEnabled: int("notificationsEnabled").default(1).notNull(),
  antiCheatingEnabled: int("antiCheatingEnabled").default(1).notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;
