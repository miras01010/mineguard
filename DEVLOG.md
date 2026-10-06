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