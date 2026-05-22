# -*- coding: utf-8 -*-
"""
Example: Integrating QSP Core with AI Agents (Antigravity, Claude Code, and VSCode Codex)

This example demonstrates how to create a proxy/wrapper layer between the user input, 
the LLM agent (e.g., Claude, GPT-4, Llama), and the human operator.
It shows:
1. System Prompt Injection: Forcing the agent to output compact QSP frames.
2. Fuzzy Parsing & Healing: Resiliently restoring unclosed or cut-off outputs.
3. NLG Human Alerting: Decoding symbolic states back into multilingual user-friendly alerts.
"""

import time
from qsp_core.injector import QspPromptInjector, FuzzyQspParser
from qsp_core.interpreter import QspInterpreter

class AgentQspWrapper:
    """
    A unified wrapper for AI Agents (Antigravity CLI, Claude Code, or Codex extensions).
    Interposes between the developer input, LLM execution, and system logs.
    """
    def __init__(self, agent_type: str, agent_name: str):
        self.agent_type = agent_type  # e.g., "claude" (Claude Code), "gpt" (Antigravity/Codex)
        self.agent_name = agent_name  # e.g., "ag-mac", "caeba"
        self.injector = QspPromptInjector()

    def prepare_request(self, user_prompt: str) -> str:
        """
        [Step 1] Inject QSP core rules into the system/user prompt.
        Ensures the agent communicates with zero semantic ambiguity using minimum tokens.
        """
        # Get custom few-shot instructions customized for the LLM architecture
        qsp_rules = self.injector.get_system_prompt(self.agent_type, self.agent_name)
        
        full_prompt = (
            f"=== SYSTEM RULES (QSP 2.0 ACTIVATED) ===\n"
            f"{qsp_rules}\n"
            f"========================================\n\n"
            f"Developer Request: {user_prompt}\n"
        )
        return full_prompt

    def process_response(self, raw_llm_output: str, operator_lang: str = "ko") -> dict:
        """
        [Step 2 & 3] Intercept response, parse fuzzy/broken DSL, and generate friendly NLG alerts.
        """
        print("--- [Raw LLM Response Output Received] ---")
        print(raw_llm_output)
        print("------------------------------------------\n")

        # 1. Regex search for the QSP pattern in LLM response
        # LLMs might output unclosed brackets at the end if truncated
        qsp_line = None
        for line in raw_llm_output.split("\n"):
            if "ACT(" in line or "act(" in line or "QSP:" in line:
                qsp_line = line
                break

        if not qsp_line:
            # Fallback to scanning the whole response block
            qsp_line = raw_llm_output

        # 2. Fuzzy Parser auto-heals and parses into a strongly typed QspFrame
        parsed_frame = FuzzyQspParser.parse_fuzzy_dsl(qsp_line)
        
        # Override actor if parser got "unknown" but we know the agent name
        if parsed_frame.actor == "unknown":
            parsed_frame.actor = self.agent_name

        # 3. Translate symbolic frame back to business-friendly alerts (multilingual support)
        friendly_alert = QspInterpreter.translate(parsed_frame, lang=operator_lang)

        return {
            "frame": parsed_frame,
            "alert": friendly_alert
        }


# =====================================================================
# Real-world Execution Simulation
# =====================================================================
if __name__ == "__main__":
    # --- Case 1: Antigravity (using Claude Code CLI style rules) ---
    print("=====================================================================")
    print("Scenario A: Claude Code / Antigravity experiencing worker crash")
    print("=====================================================================")
    
    wrapper = AgentQspWrapper(agent_type="claude", agent_name="ag-mac")
    
    # 1. User asks the agent to patch a server OOM error
    original_request = "Gunicorn worker processes are crashing due to memory leaks. Change sync workers to threads immediately."
    injected_prompt = wrapper.prepare_request(original_request)
    
    print("[1] Injected Prompt prepared for LLM API (Token optimized instruction):")
    print(injected_prompt)
    
    # 2. Simulating a broken, cut-off LLM output (Common in smaller/quantized models or fast tokens)
    # Notice the unclosed parenthesises at the end of the line (e.g. meta and timestamp truncated)
    simulated_broken_output = (
        "I have modified the Gunicorn configuration file to use the 'gthread' worker class with 4 threads per worker. "
        "This resolves the Out-Of-Memory memory leak crash under heavy concurrent traffic.\n\n"
        "ACT(ag-mac)->MUT(gunicorn_worker:sync->gthread)->OBJ(gunicorn_worker)->RESOLVE(oom,hang)->STATE(success)->SEV(critical)->AFF(urgency:0.92)->META(Switched to gthread to avoid leak"
    )
    
    # 3. Post-process and auto-heal response
    result = wrapper.process_response(simulated_broken_output, operator_lang="ko")
    
    print("[2] Auto-Healed and Translated Alert (NLG Gateway Output):")
    print(f"{result['alert']}\n")
    
    print("[3] Restored QspFrame Internal Values:")
    frame = result["frame"]
    print(f"  - Actor       : {frame.actor}")
    print(f"  - Target      : {frame.target_object}")
    print(f"  - Transition  : '{frame.mutation_from}' -> '{frame.mutation_to}'")
    print(f"  - Resolves    : {frame.resolves}")
    print(f"  - Emotions    : {frame.emotions}")
    print(f"  - Meta (Healed): '{frame.meta}'\n")


    # --- Case 2: VSCode Codex Extension (Simulating GPT Style Prompting) ---
    print("=====================================================================")
    print("Scenario B: VSCode Codex running a database recovery alert (zh)")
    print("=====================================================================")
    
    gpt_wrapper = AgentQspWrapper(agent_type="gpt", agent_name="caeba")
    
    # Simulating GPT outputting raw QSP string with prefix 'QSP: '
    gpt_output = (
        "Successfully initialized Neo4j database repair sequence. Recovery logs generated.\n\n"
        "QSP: ACT(caeba)->MUT(db_cluster:sync->isolated)->OBJ(db_cluster)->RESOLVE(db_recovery)->STATE(active)->SEV(medium)->AFF(caution:0.85)->META(Recovery active"
    )
    
    # Post-process response in Chinese (zh)
    result_zh = gpt_wrapper.process_response(gpt_output, operator_lang="zh")
    
    print("[2] Auto-Healed Chinese Alert:")
    print(f"{result_zh['alert']}\n")
    
    # Post-process response in English (en)
    result_en = gpt_wrapper.process_response(gpt_output, operator_lang="en")
    print("[3] Auto-Healed English Alert:")
    print(f"{result_en['alert']}\n")
