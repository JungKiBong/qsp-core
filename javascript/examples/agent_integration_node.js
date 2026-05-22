/**
 * Example: Integrating QSP Core with AI Agents in Node.js (Antigravity, Claude Code, and VSCode Codex)
 *
 * This example demonstrates how to create a proxy/wrapper layer in JavaScript/TypeScript
 * between the developer input, the LLM agent, and the operator.
 * 
 * To run this example, first build the package:
 * $ npm run build
 * $ node examples/agent_integration_node.js
 */

const { QspPromptInjector, FuzzyQspParser, QspInterpreter } = require('../dist/index');

class AgentQspWrapper {
  /**
   * @param {string} agentType - e.g., "claude" (Claude Code), "gpt" (Antigravity/Codex)
   * @param {string} agentName - e.g., "ag-mac", "caeba"
   */
  constructor(agentType, agentName) {
    this.agentType = agentType;
    this.agentName = agentName;
    this.injector = new QspPromptInjector();
  }

  /**
   * [Step 1] Inject QSP core rules into the system/user prompt.
   * Ensures the agent communicates with zero semantic ambiguity using minimum tokens.
   * @param {string} userPrompt
   * @returns {string}
   */
  prepareRequest(userPrompt) {
    const qspRules = this.injector.getSystemPrompt(this.agentType, this.agentName);
    return (
      `=== SYSTEM RULES (QSP 2.0 ACTIVATED) ===\n` +
      `${qspRules}\n` +
      `========================================\n\n` +
      `Developer Request: ${userPrompt}\n` +
      `Output ONLY the response and the final QSP frame string.`
    );
  }

  /**
   * [Step 2 & 3] Intercept response, parse fuzzy/broken DSL, and generate friendly NLG alerts.
   * @param {string} rawLlmOutput
   * @param {string} operatorLang
   * @returns {object}
   */
  processResponse(rawLlmOutput, operatorLang = 'ko') {
    console.log("--- [Raw LLM Response Output Received] ---");
    console.log(rawLlmOutput);
    console.log("------------------------------------------\n");

    // 1. Search for the QSP pattern in LLM response
    let qspLine = null;
    const lines = rawLlmOutput.split('\n');
    for (const line of lines) {
      if (line.includes('ACT(') || line.includes('act(') || line.includes('QSP:')) {
        qspLine = line;
        break;
      }
    }

    if (!qspLine) {
      // Fallback
      qspLine = rawLlmOutput;
    }

    // 2. Fuzzy Parser auto-heals and parses into a strongly typed QspFrame
    const parsedFrame = FuzzyQspParser.parseFuzzyDsl(qspLine);

    if (parsedFrame.actor === 'unknown') {
      parsedFrame.actor = this.agentName;
    }

    // 3. Translate symbolic frame back to business-friendly alerts (multilingual support)
    const friendlyAlert = QspInterpreter.translate(parsedFrame, operatorLang);

    return {
      frame: parsedFrame,
      alert: friendlyAlert
    };
  }
}

// =====================================================================
// Real-world Execution Simulation
// =====================================================================
function runSimulation() {
  console.log("=====================================================================");
  console.log("Scenario A: Claude Code / Antigravity (Node.js) worker crash");
  console.log("=====================================================================");

  const wrapper = new AgentQspWrapper('claude', 'ag-mac');

  // 1. User request
  const originalRequest = "Gunicorn worker processes are crashing due to memory leaks. Change sync workers to threads immediately.";
  const injectedPrompt = wrapper.prepareRequest(originalRequest);

  console.log("[1] Injected Prompt prepared for LLM API (Token optimized instruction):");
  console.log(injectedPrompt);
  console.log("\n");

  // 2. Simulating a broken, cut-off LLM output (Common in smaller/quantized models or fast tokens)
  // Notice the unclosed parenthesises at the end of the line (e.g. meta and timestamp truncated)
  const simulatedBrokenOutput = 
    "I have modified the Gunicorn configuration file to use the 'gthread' worker class with 4 threads per worker. " +
    "This resolves the Out-Of-Memory memory leak crash under heavy concurrent traffic.\n\n" +
    "ACT(ag-mac)->MUT(gunicorn_worker:sync->gthread)->OBJ(gunicorn_worker)->RESOLVE(oom,hang)->STATE(success)->SEV(critical)->AFF(urgency:0.92)->META(Switched to gthread to avoid leak";

  // 3. Post-process and auto-heal response
  const result = wrapper.processResponse(simulatedBrokenOutput, 'ko');

  console.log("[2] Auto-Healed and Translated Alert (NLG Gateway Output):");
  console.log(`${result.alert}\n`);

  console.log("[3] Restored QspFrame Internal Values:");
  const frame = result.frame;
  console.log(`  - Actor       : ${frame.actor}`);
  console.log(`  - Target      : ${frame.targetObject}`);
  console.log(`  - Transition  : '${frame.mutationFrom}' -> '${frame.mutationTo}'`);
  console.log(`  - Resolves    : ${frame.resolves.join(', ')}`);
  console.log(`  - Emotions    : ${JSON.stringify(frame.emotions)}`);
  console.log(`  - Meta (Healed): '${frame.meta}'\n`);

  console.log("=====================================================================");
  console.log("Scenario B: VSCode Codex running a database recovery alert (zh)");
  console.log("=====================================================================");

  const gptWrapper = new AgentQspWrapper('gpt', 'caeba');

  const gptOutput = 
    "Successfully initialized Neo4j database repair sequence. Recovery logs generated.\n\n" +
    "QSP: ACT(caeba)->MUT(db_cluster:sync->isolated)->OBJ(db_cluster)->RESOLVE(db_recovery)->STATE(active)->SEV(medium)->AFF(caution:0.85)->META(Recovery active";

  // Chinese
  const resultZh = gptWrapper.processResponse(gptOutput, 'zh');
  console.log("[2] Auto-Healed Chinese Alert:");
  console.log(`${resultZh.alert}\n`);

  // English
  const resultEn = gptWrapper.processResponse(gptOutput, 'en');
  console.log("[3] Auto-Healed English Alert:");
  console.log(`${resultEn.alert}\n`);
}

// Execute simulation
try {
  runSimulation();
} catch (e) {
  console.error("Please build the package first by running: npm run build");
  console.error(e);
}
