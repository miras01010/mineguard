import json
from answer import client, LLM_MODEL, DOC_NAMES, page_label
from search import search_with_neighbours

def search_regulations(query):
    passages = search_with_neighbours(query, k=5)
    blocks=[]
    for p in passages:
        name = DOC_NAMES.get(p["source"], p["source"])
        blocks.append(f"({name}, {page_label(p)})\n{p['text']}")
    return "\n\n".join(blocks)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_regulations",
            "description": (
                "Searches the Mines Act 1952, the Coal Mines Regulations 2017, "
                "the Metalliferous Mines Regulations 1961 and the Mines Rescue Rules 1985, "
                "and returns relevant passages, each labelled with its document name and pages. "
                "Use this whenever the user asks about Indian mining safety law, duties, limits or procedures."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": (
                            "A short search query about ONE topic, for example 'inflammable gas withdrawal' "
                            "or 'qualifications of a mine manager'. For questions with several parts, "
                            "call this tool once per part."
                        ),
                    }
                },
                "required": ["query"],
            },
        },
    }
]

AGENT_PROMPT = """You are MineGuard, an assistant for Indian mining safety law.
Rules:
1. Always use the search_regulations tool before answering. Never answer from memory.
2. For questions with several parts, search once for each part.
3. Use ONLY information from the search results.
4. Cite every fact with its document and pages, like (Coal Mines Regulations, 2017, pages 250-251).
5. Include exact numbers, percentages, time limits and conditions. Never make up numbers.
6. If coal mines and metal mines have DIFFERENT rules on the same point, give them in separate sections. If one law applies to all mines, state it once.
7. If the search results do not contain the answer, say "I could not find this in the regulations."
8. After each search, check whether the results answer exactly what was asked. A definition is not the same as an operating rule (for example, how a seam is CLASSIFIED is different from the limit at which gas counts as DETECTED). If the results don't match, search again with different words.
"""

MAX_STEPS = 5

def run_agent(question):
    messages = [
        {"role": "system", "content": AGENT_PROMPT},
        {"role": "user", "content": question},
    ]
    for step in range(MAX_STEPS):
        response = client.chat.completions.create(
            model=LLM_MODEL, messages=messages, tools=TOOLS, temperature=0,
        )
        msg = response.choices[0].message

        if not msg.tool_calls:
            return msg.content

        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {"id": tc.id, "type": "function",
                 "function": {"name": tc.function.name, "arguments": tc.function.arguments}}
                for tc in msg.tool_calls
            ],
        })

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"  [search] {args['query']}")
            result = search_regulations(args["query"])
            for block in result.split("\n\n"):
                print("      found:", block.split("\n")[0])
            messages.append({"role": "tool", "tool_call_id": tc.id, "content": result})

    return "I could not complete this within the step limit."

if __name__ == "__main__":
    question = input("Ask a question: ")
    print("\n" + run_agent(question))