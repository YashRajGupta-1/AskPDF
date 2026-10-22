from pipeline.retrieve import retrieve

# Write 5 questions whose answers you KNOW are in test.pdf
questions = [
    "What are the five key themes the 17 SDGs are built around?",
    "Which SDGs address the environmental dimension?",
    "What Indian government programs support girls' education?",
    "What are the root causes of gender-based education disparity in India?",
    "How does education support SDGs beyond Goal 4 and Goal 5?",
    "What strategies are suggested to prevent gender disparity in education?",
    "When were the SDGs adopted and what did they replace?",
]

for q in questions:
    print(f"\n{'='*60}\nQ: {q}\n{'='*60}")
    for r in retrieve("test", q, k=5):
        print(f"[page {r['page']}, dist {r['score']:.3f}] {r['text']}...")