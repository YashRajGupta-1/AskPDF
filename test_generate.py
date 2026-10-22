from pipeline.retrieve import retrieve
from pipeline.generate import build_prompt, ask_llm

# Test 1: answer IS in the document
q1 = "What strategies are suggested to prevent gender disparity in education?"
chunks = retrieve("test", q1, k=5)
print("--- PROMPT (first 600 chars) ---")
print(build_prompt(q1, chunks)[:600])
print("\n--- ANSWER ---")
print(ask_llm(build_prompt(q1, chunks)))

# Test 2: answer is NOT in the document — the leash test
q2 = "What is the capital of France?"
print("\n--- ANSWER 2 ---")
print(ask_llm(build_prompt(q2, retrieve("test", q2, k=5))))