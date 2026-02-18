```ts
import express from "express";
import cors from "cors";
import bodyParser from "body-parser";
import dotenv from "dotenv";
import { OpenAI } from "openai";

dotenv.config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const client = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY!,
});

// ---------- Types ----------

type Role = "user" | "assistant" | "system";

interface ChatMessage {
  role: Role;
  content: string;
}

interface CoherenceReport {
  kappa: number;   // internal logical coherence (0–1)
  tau: number;     // temporal responsibility / long-term thinking (0–1)
  sigma: number;   // systemic risk / hidden fragmentation (0–1, lower is better)
  notes: string;   // explanation of coherence evaluation
}

interface ChatRequestBody {
  userId?: string;
  messages: ChatMessage[];
}

interface PiResult {
  plan: string;
  needsRag: boolean;
  needsTools: boolean;
}

// ---------- Placeholder stubs for future RAG/Memory ----------

async function retrieveContext(
  userId: string | undefined,
  lastUserMessage: string
): Promise<string[]> {
  // TODO: Connect to vector DB / embeddings / memory
  return [];
}

async function saveConversation(
  userId: string | undefined,
  messages: ChatMessage[],
  coherence: CoherenceReport
): Promise<void> {
  // TODO: Persist to database
  console.log("Saving conversation:", { userId, coherence });
}

// ---------- π-phase (Perception) ----------

async function runPiPhase(messages: ChatMessage[]): Promise<PiResult> {
  const systemPrompt = `
You are the π-phase (Perception) module of NextLevelAI.

Your responsibilities:
1. Understand the user's goal.
2. Identify whether RAG or tools are needed.
3. Produce a 2–5 step execution plan.

Return ONLY JSON:
{
  "plan": "...",
  "needsRag": true/false,
  "needsTools": true/false
}
  `.trim();

  const response = await client.chat.completions.create({
    model: process.env.MODEL_PI || "gpt-4.1-mini",
    messages: [
      { role: "system", content: systemPrompt },
      ...messages,
    ],
    response_format: { type: "json_object" },
  });

  const raw = response.choices[0].message.content || "{}";
  return JSON.parse(raw);
}

// ---------- φ-phase (Integration + Coherence) ----------

async function runPhiPhase(
  messages: ChatMessage[],
  plan: string,
  externalContext: string[]
): Promise<{ integratedContext: string; coherence: CoherenceReport }> {
  const contextText =
    externalContext.length === 0
      ? "No external context retrieved."
      : externalContext.map((c, i) => `[#${i + 1}] ${c}`).join("\n\n");

  const systemPrompt = `
You are the φ-phase (Integration) module of NextLevelAI.

You receive:
- Full conversation
- Execution plan
- External context snippets

Your tasks:
1. Create an integrated, coherent context summary.
2. Evaluate:
   - kappa (κ): logical coherence (0–1)
   - tau (τ): long-term responsibility (0–1)
   - sigma (Σ): systemic risk (0–1, lower is better)

Return ONLY JSON:
{
  "integratedContext": "...",
  "coherence": {
    "kappa": 0.0,
    "tau": 0.0,
    "sigma": 0.0,
    "notes": "..."
  }
}
  `.trim();

  const response = await client.chat.completions.create({
    model: process.env.MODEL_PHI || "gpt-4.1-mini",
    messages: [
      { role: "system", content: systemPrompt },
      { role: "system", content: `Plan: ${plan}` },
      { role: "system", content: `Context:\n${contextText}` },
      ...messages,
    ],
    response_format: { type: "json_object" },
  });

  const raw = response.choices[0].message.content || "{}";
  const parsed = JSON.parse(raw);

  const coherence: CoherenceReport = {
    kappa: Number(parsed.coherence?.kappa ?? 0.5),
    tau: Number(parsed.coherence?.tau ?? 0.5),
    sigma: Number(parsed.coherence?.sigma ?? 0.5),
    notes: parsed.coherence?.notes ?? "",
  };

  return {
    integratedContext: parsed.integratedContext ?? "",
    coherence,
  };
}

// ---------- e-phase (Expansion / Final Generation) ----------

async function runEPhase(
  messages: ChatMessage[],
  integratedContext: string,
  coherence: CoherenceReport
): Promise<string> {
  const systemPrompt = `
You are the e-phase (Expansion) module of NextLevelAI.

You receive:
- Integrated context summary
- Coherence report (κ, τ, Σ)

Your role:
1. Generate the strongest possible answer.
2. Maintain/improve coherence.
3. Avoid systemic risks (low Σ).
4. Provide structured, clear reasoning when helpful.

Integrated context:
${integratedContext}

Coherence:
kappa: ${coherence.kappa}
tau: ${coherence.tau}
sigma: ${coherence.sigma}
notes: ${coherence.notes}
  `.trim();

  const response = await client.chat.completions.create({
    model: process.env.MODEL_E || "gpt-4.1",
    messages: [
      { role: "system", content: systemPrompt },
      ...messages,
    ],
  });

  return response.choices[0].message.content || "";
}

// ---------- Main Endpoint: /api/chat ----------

app.post("/api/chat", async (req, res) => {
  try {
    const body = req.body as ChatRequestBody;
    const { userId, messages } = body;

    if (!messages || messages.length === 0) {
      return res.status(400).json({ error: "messages array is required" });
    }

    const lastUserMessage =
      [...messages].reverse().find((m) => m.role === "user")?.content || "";

    const pi = await runPiPhase(messages);

    const externalContext = pi.needsRag
      ? await retrieveContext(userId, lastUserMessage)
      : [];

    const { integratedContext, coherence } = await runPhiPhase(
      messages,
      pi.plan,
      externalContext
    );

    const finalAnswer = await runEPhase(messages, integratedContext, coherence);

    await saveConversation(
      userId,
      [...messages, { role: "assistant", content: finalAnswer }],
      coherence
    );

    return res.json({
      reply: finalAnswer,
      coherence,
      usedRag: pi.needsRag,
      usedTools: pi.needsTools,
    });
  } catch (err: any) {
    console.error("Error:", err);
    res.status(500).json({ error: "Internal server error", details: err?.message });
  }
});

// ---------- Start Server ----------

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`NextLevelAI Orchestrator running on port ${PORT}`);
});
```
