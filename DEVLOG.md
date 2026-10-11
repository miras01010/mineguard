## Oct 5
- Coal Regulations PDF is bilingual; Hindi pages in legacy font extract as gibberish. Built a filter; verified it by checking skipped pages.
- Switched pypdf to PyMuPDF: fixed broken words ("reg ulation" → "regulation").
- Stripping garbled Hindi headers moved the correct chunk from rank 2 to rank 1.

## Oct 6
- Eval set: 12 questions. Baseline retrieval hit rate @5: 11/12.
- Prompt fix separated coal and metal rules, but the gas threshold was still missing.
- Root cause: chunk boundary split a 3-tier rule (0.1% / 0.5% / 1.25% by seam degree).
- Initial version gave a vague answer; diagnosed it as a chunk boundary splitting a tiered regulation; fixed it with neighbour expansion.
- Neighbour expansion retrieved the full regulation (page 250 now included), but the LLM still skipped the thresholds. The problem moved from retrieval to generation

# MineGuard Dev Log

## Oct 5: Data pipeline, search, first answer
- Coal Mines Regulations PDF is a bilingual Gazette; Hindi pages use a legacy font and extract as Latin gibberish.
- Built an English-page filter (common-word ratio). Verified it by checking skipped pages:
  - False negative: Rescue Rules Schedule I (table page) was dropped → switched from a fixed count to a percentage rule.
  - False positives: Hindi pages 156/158 slipped through because the English running header "THE GAZETTE OF INDIA" gave free hits → strip headers before filtering.
  - Final: Coal 121 kept / 159 skipped; boundary at page 160.
- Switched pypdf → PyMuPDF: fixed broken words ("reg ulation" → "regulation"). Chunks 1170 → 1141.
- Chunking: 200 words, 40 overlap, no crossing pages.
- Embeddings: all-MiniLM-L6-v2 + ChromaDB (cosine).
- Stripping garbled Hindi header lines moved the correct chunk (p.251) from rank 2 (0.363) to rank 1 (0.341).
- LLM via Groq. llama-3.3-70b was retired (404) → switched to openai/gpt-oss-120b.
- First cited answer. Issues: dropped the gas threshold, mixed coal/metal rules, duplicate sources.

## Oct 6: Evals and debugging answer quality
- Eval set: 12 questions across all 4 documents.
- Baseline retrieval hit rate @5: 11/12 (7 at rank 1).
  - Only failure (dust): answer spans pp.78–80, and the Coal Regs also cover dust → the answer key is too strict, not a search failure.
- Rewrote the system prompt (6 rules): coal/metal now separated ✅; fixed 【1†L3】 citation format ✅; threshold still missing ❌.
- Neighbour expansion (±1 chunk, same document only): p.250 now retrieved, but the threshold was still missing.
- Inspected the data: thresholds ARE in p.250. Regulation 166 is split across two passages, so the LLM never connected them → a generation problem, not retrieval.

## Oct 11: Fixed it, and milestone 1 done
- Merged consecutive chunks into continuous passages (overlap removed, page ranges kept).
- Result: all three thresholds now answered (0.1% / 0.5% / 1.25% by seam degree). Sources 13 fragments → 4 passages.
- Verified the Metalliferous 1.25% citation against p.89 ✅
- Streamlit web UI working → MILESTONE 1 COMPLETE.
- TODO: show only cited sources; harder casual eval questions; allow multiple correct pages per eval question.