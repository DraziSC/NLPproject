#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
NASA Space Missions: Ground Truth RAG vs. Baseline Evaluation System
===============================================================================
Course: Natural Language Interaction (ILN) 2026/2027
Institution: Universidade de Coimbra - DEI-FCTUC
Authors: Mohammed Abdelqader & Michael O'Shea

Description:
  Standalone, non-intrusive evaluation harness that benchmarks the With-RAG
  system (ChromaDB `nasa_missions` vector store + Ollama local LLM) against
  a Without-RAG baseline (parametric internal memory) using the 20-question
  authoritative ground truth dataset (`nasa_eval_dataset.json`).

Key Capabilities:
  1. Automated retrieval from ChromaDB (1,600 chunks, 17 NASA PDF reports).
  2. Side-by-side response generation: With-RAG vs. Without-RAG.
  3. Deterministic scoring:
     - Ground Truth Fact Recall %
     - Telemetry Metric & Parameter Coverage %
     - Inline Citation Frequency & Document Relevance
     - End-to-End Latency (Retrieval vs. Generation)
  4. LLM-as-a-Judge Scoring (Qwen2.5:7b) across 4 dimensions (1-5 Likert scale):
     - Factual Accuracy
     - Completeness
     - Groundedness & Anti-Hallucination
     - Scientific Precision
  5. Multi-format export:
     - Machine-readable structured JSON: `data/nasa_eval_results.json`
     - Human-readable Markdown summary report: `data/nasa_eval_results.md`
     - Terminal interactive tabular summaries

Zero-Modification Guarantee:
  This script does NOT modify any existing codebase files (D2RAG.py,
  D2RAGfull.py, D1rule.py, D1D2classifierrouter.py, README.md).
===============================================================================
"""

import sys
import os
import re
import time
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple

# Reconfigure stdout/stderr to UTF-8 on Windows to prevent charmap encoding errors
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr is not None and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Third-party imports with clear diagnostic messages
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# =============================================================================
# Global Constants & Paths
# =============================================================================

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_CHROMA_DIR = PROJECT_DIR / "data" / "chroma_db"
DEFAULT_DATASET_PATH = PROJECT_DIR / "nasa_eval_dataset.json"
DEFAULT_RESULTS_JSON = PROJECT_DIR / "data" / "nasa_eval_results.json"
DEFAULT_RESULTS_MD = PROJECT_DIR / "data" / "nasa_eval_results.md"

COLLECTION_NAME = "nasa_missions"
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_LLM_MODEL = "qwen2.5:7b"
DEFAULT_JUDGE_LLM_MODEL = "mistral-small:24b"
DEFAULT_TOP_K = 6
OLLAMA_HOST = "http://127.0.0.1:11434"

RAG_SYSTEM_PROMPT = """You are an authoritative NASA Space Exploration and Astrophysics Technical Advisor.
Your objective is to provide precise, rigorous engineering and scientific answers grounded strictly in the provided official NASA technical documents.

CRITICAL INSTRUCTIONS:
1. Grounding: Answer ONLY based on the facts provided in the Context Excerpts. Do NOT extrapolate, speculate, or introduce external unverified claims.
2. Citations: You MUST substantiate every technical claim and metric with an inline bracketed citation citing the exact source file name and page number, in the exact format: [Document Name, Page X] (for example: [JWST_Mission_Overview_and_Status.pdf, Page 12]). You MUST use the exact file name given in "Source Document:", NEVER cite using excerpt numbers like [1, Page 12] or [Excerpt 1].
3. Transparency: If the provided excerpts do not contain enough information to answer any part of the query, explicitly state: "The provided NASA documentation does not contain sufficient data to address this aspect."
4. Tone: Technical, concise, professional, and fact-focused.
"""

BASELINE_SYSTEM_PROMPT = """You are an AI assistant answering questions about space exploration and NASA missions.
Provide an answer based solely on your internal training knowledge without access to external documents.
"""

JUDGE_SYSTEM_PROMPT = """You are an expert impartial NASA evaluation judge.
Your task is to evaluate a candidate answer against an authoritative ground truth reference answer for a technical aerospace question.

Scoring Criteria (1 to 5 scale):
1. Factual Accuracy (1-5): Are the technical facts, numbers, equations, and mission details strictly consistent with ground truth? (5 = 100% correct, 1 = serious errors/contradictions).
2. Completeness (1-5): Does the candidate answer all components and sub-questions asked? (5 = fully comprehensive, 1 = superficial or misses core points).
3. Groundedness (1-5): Is the answer free from hallucinations and unverified assumptions? Does it reflect authoritative documentation? (5 = strictly grounded, 1 = fabricated claims).
4. Clarity & Precision (1-5): Is the language technically rigorous, concise, and appropriate for aerospace engineering? (5 = exceptional, 1 = vague or confusing).

You MUST respond strictly with a valid JSON object formatted as follows, with no text outside the JSON:
{
  "factual_accuracy": <int 1-5>,
  "completeness": <int 1-5>,
  "groundedness": <int 1-5>,
  "clarity": <int 1-5>,
  "overall_score": <float 1.0-5.0>,
  "strengths": "<short string summarizing key strengths>",
  "weaknesses": "<short string summarizing errors, omissions, or hallucinations>"
}
"""


# =============================================================================
# Vector Database & Retrieval Utilities
# =============================================================================

def load_vector_store(chroma_dir: Path = DEFAULT_CHROMA_DIR, collection_name: str = COLLECTION_NAME):
    """Loads existing ChromaDB persistent collection."""
    if not CHROMADB_AVAILABLE:
        raise RuntimeError("The 'chromadb' package is not installed. Install via: pip install chromadb")

    if not chroma_dir.exists():
        raise FileNotFoundError(f"ChromaDB directory not found: {chroma_dir}. Please run D2RAG.py first to build vector store.")

    client = chromadb.PersistentClient(path=str(chroma_dir))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL_NAME)
    collection = client.get_collection(name=collection_name, embedding_function=emb_fn)
    return collection


def retrieve_context(
    collection,
    query: str,
    top_k: int = DEFAULT_TOP_K,
    mission_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieves top-k context chunks from ChromaDB."""
    query_kwargs = {"query_texts": [query], "n_results": top_k}
    if mission_filter:
        query_kwargs["where"] = {"mission": {"$eq": mission_filter}}

    results = collection.query(**query_kwargs)

    retrieved = []
    if results and "documents" in results and results["documents"]:
        docs = results["documents"][0]
        metas = results["metadatas"][0] if "metadatas" in results else [{}] * len(docs)
        dists = results["distances"][0] if "distances" in results else [0.0] * len(docs)

        for doc, meta, dist in zip(docs, metas, dists):
            sim = 1.0 - dist if dist <= 1.0 else 1.0 / (1.0 + dist)
            retrieved.append({
                "document": doc,
                "source": meta.get("source", "Unknown.pdf"),
                "title": meta.get("title", "NASA Document"),
                "mission": meta.get("mission", "NASA"),
                "page": meta.get("page", 1),
                "distance": dist,
                "similarity": sim
            })
    return retrieved


def format_context_blocks(chunks: List[Dict[str, Any]]) -> str:
    """Formats retrieved chunks into clean structured prompt context."""
    blocks = []
    for idx, c in enumerate(chunks, start=1):
        block = (
            f"--- EXCERPT {idx} ---\n"
            f"Source Document: {c.get('source', 'Unknown')} (Page {c.get('page', 1)})\n"
            f"Mission Category: {c.get('mission', 'NASA')}\n"
            f"Content: {c.get('document', '').strip()}\n"
        )
        blocks.append(block)
    return "\n".join(blocks)


def extract_citations(text: str, chunks: Optional[List[Dict[str, Any]]] = None) -> List[str]:
    """Extracts citation references like [Document.pdf, Page X] from text."""
    pattern = r"\[([^\]]+?),\s*(?:Page|p\.?)\s*(\d+)\]"
    matches = re.findall(pattern, text, re.IGNORECASE)
    resolved = []
    for doc_ref, page in matches:
        doc_clean = doc_ref.strip()
        idx_match = re.search(r"^(?:excerpt\s*|source\s*|#\s*)?(\d+)$", doc_clean, re.IGNORECASE)
        if idx_match and chunks:
            idx = int(idx_match.group(1)) - 1
            if 0 <= idx < len(chunks):
                doc_clean = chunks[idx].get("source", doc_clean)
        citation = f"{doc_clean}, Page {page}"
        if citation not in resolved:
            resolved.append(citation)
    return resolved


def resolve_inline_citations(text: str, chunks: List[Dict[str, Any]]) -> str:
    """Replaces numerical citations [7, Page 1] with actual file names."""
    if not chunks:
        return text

    def _replace_cite(match):
        doc_ref = match.group(1).strip()
        page = match.group(2)
        idx_match = re.search(r"^(?:excerpt\s*|source\s*|#\s*)?(\d+)$", doc_ref, re.IGNORECASE)
        if idx_match:
            idx = int(idx_match.group(1)) - 1
            if 0 <= idx < len(chunks):
                doc_name = chunks[idx].get("source", doc_ref)
                return f"[{doc_name}, Page {page}]"
        return match.group(0)

    pattern = r"\[([^\]]+?),\s*(?:Page|p\.?)\s*(\d+)\]"
    return re.sub(pattern, _replace_cite, text, flags=re.IGNORECASE)


# =============================================================================
# Response Generation Pipelines
# =============================================================================

def generate_rag_response(
    query: str,
    collection,
    client,
    model: str = DEFAULT_LLM_MODEL,
    top_k: int = DEFAULT_TOP_K,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """Generates an authoritative answer grounded in retrieved ChromaDB context."""
    t0 = time.time()
    retrieved = retrieve_context(collection, query, top_k=top_k)
    retrieval_latency = time.time() - t0

    context_str = format_context_blocks(retrieved)
    user_prompt = (
        f"Context Excerpts from Official NASA Technical Reports:\n"
        f"================================================================================\n"
        f"{context_str}\n"
        f"================================================================================\n\n"
        f"User Technical Query: {query}\n\n"
        f"Instructions: Provide a detailed, technically rigorous response to the query using ONLY "
        f"the excerpts above. Include exact inline citations [Document Name, Page X] for every key fact, "
        f"parameter, and specification (e.g. [JWST_Mission_Overview_and_Status.pdf, Page 4]). Use the exact "
        f"filename from 'Source Document:', not excerpt numbers."
    )

    t_gen_start = time.time()
    try:
        resp = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature}
        )
        raw_text = resp["message"]["content"]
        answer_text = resolve_inline_citations(raw_text, retrieved)
    except Exception as e:
        answer_text = f"[ERROR: RAG generation failed: {e}]"

    generation_latency = time.time() - t_gen_start
    total_latency = time.time() - t0
    citations = extract_citations(answer_text, retrieved)

    return {
        "mode": "with_rag",
        "answer": answer_text,
        "retrieved_chunks": retrieved,
        "citations": citations,
        "retrieval_latency": round(retrieval_latency, 3),
        "generation_latency": round(generation_latency, 3),
        "total_latency": round(total_latency, 3)
    }


def generate_baseline_response(
    query: str,
    client,
    model: str = DEFAULT_LLM_MODEL,
    temperature: float = 0.1
) -> Dict[str, Any]:
    """Generates a baseline answer relying purely on internal LLM parametric memory."""
    t0 = time.time()
    user_prompt = (
        f"User Technical Query: {query}\n\n"
        f"Instructions: Provide a detailed, technical response based on your general knowledge."
    )

    try:
        resp = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature}
        )
        answer_text = resp["message"]["content"]
    except Exception as e:
        answer_text = f"[ERROR: Baseline generation failed: {e}]"

    total_latency = time.time() - t0
    citations = extract_citations(answer_text, None)

    return {
        "mode": "without_rag",
        "answer": answer_text,
        "retrieved_chunks": [],
        "citations": citations,
        "retrieval_latency": 0.0,
        "generation_latency": round(total_latency, 3),
        "total_latency": round(total_latency, 3)
    }


# =============================================================================
# Evaluation Metrics & Automated Judges
# =============================================================================

def evaluate_deterministic_metrics(answer_text: str, ground_truth_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes lexical fact recall and telemetry parameter coverage against ground truth.
    """
    answer_lower = answer_text.lower()
    
    # 1. Fact Recall
    gt_facts = ground_truth_item.get("ground_truth_facts", [])
    matched_facts = []
    missing_facts = []
    for fact in gt_facts:
        f_clean = fact.strip().lower()
        # Substring or token match
        if f_clean in answer_lower:
            matched_facts.append(fact)
        else:
            missing_facts.append(fact)

    fact_recall = (len(matched_facts) / len(gt_facts) * 100.0) if gt_facts else 100.0

    # 2. Telemetry Coverage
    telemetry_metrics = ground_truth_item.get("telemetry_metrics", [])
    matched_metrics = []
    missing_metrics = []
    for metric in telemetry_metrics:
        # Check standard variation (e.g., um vs μm, K, m/s)
        m_clean = metric.strip().lower().replace("μm", "um")
        ans_norm = answer_lower.replace("μm", "um")
        # Split tokens for flexible numeric checking
        tokens = [t.strip() for t in m_clean.split() if len(t.strip()) > 1]
        if m_clean in ans_norm or (tokens and all(tok in ans_norm for tok in tokens)):
            matched_metrics.append(metric)
        else:
            missing_metrics.append(metric)

    telemetry_coverage = (len(matched_metrics) / len(telemetry_metrics) * 100.0) if telemetry_metrics else 100.0

    # 3. Source Groundedness & Alignment
    primary = ground_truth_item.get("primary_source", "")
    supporting = ground_truth_item.get("supporting_sources", [])
    expected_docs = [primary] + supporting

    citations = extract_citations(answer_text)
    aligned_citations = []
    for cite in citations:
        if any(doc.lower() in cite.lower() for doc in expected_docs if doc):
            aligned_citations.append(cite)

    return {
        "fact_recall_pct": round(fact_recall, 1),
        "facts_matched": matched_facts,
        "facts_missing": missing_facts,
        "telemetry_coverage_pct": round(telemetry_coverage, 1),
        "telemetry_matched": matched_metrics,
        "telemetry_missing": missing_metrics,
        "citation_count": len(citations),
        "aligned_citation_count": len(aligned_citations),
        "citations": citations
    }


def judge_answer_with_llm(
    question: str,
    ground_truth_answer: str,
    candidate_answer: str,
    client,
    #model: str = DEFAULT_LLM_MODEL
    model: str = DEFAULT_JUDGE_LLM_MODEL
) -> Dict[str, Any]:
    """
    Invokes LLM-as-a-judge to evaluate the candidate answer against the ground truth.
    """
    prompt = (
        f"Question:\n{question}\n\n"
        f"Authoritative Ground Truth Answer:\n{ground_truth_answer}\n\n"
        f"Candidate Answer to Evaluate:\n{candidate_answer}\n\n"
        f"Please output your evaluation as a strict JSON object according to your system prompt."
    )

    try:
        resp = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": JUDGE_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            options={"temperature": 0.0}
        )
        content = resp["message"]["content"].strip()

        # Parse JSON from response (handling potential markdown wrapper)
        json_match = re.search(r"\{.*\}", content, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return {
                "factual_accuracy": int(data.get("factual_accuracy", 3)),
                "completeness": int(data.get("completeness", 3)),
                "groundedness": int(data.get("groundedness", 3)),
                "clarity": int(data.get("clarity", 3)),
                "overall_score": float(data.get("overall_score", 3.0)),
                "strengths": str(data.get("strengths", "")),
                "weaknesses": str(data.get("weaknesses", ""))
            }
        else:
            return {
                "factual_accuracy": 3, "completeness": 3, "groundedness": 3, "clarity": 3,
                "overall_score": 3.0, "strengths": "Parsing fallback", "weaknesses": "Could not parse JSON"
            }
    except Exception as e:
        return {
            "factual_accuracy": 1, "completeness": 1, "groundedness": 1, "clarity": 1,
            "overall_score": 1.0, "strengths": "Error", "weaknesses": f"Judge invocation failed: {e}"
        }


# =============================================================================
# Markdown & JSON Report Generators
# =============================================================================

def generate_markdown_report(evaluation_results: Dict[str, Any], output_path: Path):
    """Writes an executive markdown report comparing With-RAG and Without-RAG."""
    summary = evaluation_results.get("summary", {})
    records = evaluation_results.get("evaluations", [])

    lines = []
    lines.append("# NASA Space Missions: RAG vs. Without-RAG Benchmark Evaluation Report\n")
    lines.append(f"**Course:** Natural Language Interaction (ILN) 2026/2027  ")
    lines.append(f"**Institution:** Universidade de Coimbra (DEI-FCTUC)  ")
    lines.append(f"**Authors:** Mohammed Abdelqader & Michael O'Shea  ")
    lines.append(f"**Evaluation Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ")
    lines.append(f"**Evaluated Model:** `{evaluation_results.get('model', DEFAULT_LLM_MODEL)}`  ")
    lines.append(f"**Total Questions Evaluated:** {len(records)}\n")
    lines.append("---\n")

    # Executive Summary Table
    lines.append("## 1. Executive Performance Comparison\n")
    lines.append("| Metric Dimension | With-RAG (Augmented) | Without-RAG (Parametric) | Delta (\u0394) |")
    lines.append("|:---|:---:|:---:|:---:|")

    rag_sum = summary.get("with_rag", {})
    base_sum = summary.get("without_rag", {})

    fact_delta = rag_sum.get("avg_fact_recall_pct", 0) - base_sum.get("avg_fact_recall_pct", 0)
    telem_delta = rag_sum.get("avg_telemetry_coverage_pct", 0) - base_sum.get("avg_telemetry_coverage_pct", 0)
    cite_delta = rag_sum.get("avg_citations", 0) - base_sum.get("avg_citations", 0)
    lat_delta = rag_sum.get("avg_total_latency_sec", 0) - base_sum.get("avg_total_latency_sec", 0)

    lines.append(f"| **Fact Recall %** | **{rag_sum.get('avg_fact_recall_pct', 0):.1f}%** | {base_sum.get('avg_fact_recall_pct', 0):.1f}% | `{fact_delta:+.1f}%` |")
    lines.append(f"| **Telemetry Metric Coverage %** | **{rag_sum.get('avg_telemetry_coverage_pct', 0):.1f}%** | {base_sum.get('avg_telemetry_coverage_pct', 0):.1f}% | `{telem_delta:+.1f}%` |")
    lines.append(f"| **Average Citations / Answer** | **{rag_sum.get('avg_citations', 0):.2f}** | {base_sum.get('avg_citations', 0):.2f} | `{cite_delta:+.2f}` |")
    lines.append(f"| **Average Latency (s)** | {rag_sum.get('avg_total_latency_sec', 0):.2f}s | {base_sum.get('avg_total_latency_sec', 0):.2f}s | `{lat_delta:+.2f}s` |")

    if "avg_judge_overall" in rag_sum:
        judge_delta = rag_sum.get("avg_judge_overall", 0) - base_sum.get("avg_judge_overall", 0)
        lines.append(f"| **LLM Judge Score (1-5)** | **{rag_sum.get('avg_judge_overall', 0):.2f} / 5.0** | {base_sum.get('avg_judge_overall', 0):.2f} / 5.0 | `{judge_delta:+.2f}` |")
        lines.append(f"| **Judge: Factual Accuracy** | **{rag_sum.get('avg_judge_accuracy', 0):.2f}** | {base_sum.get('avg_judge_accuracy', 0):.2f} | `{rag_sum.get('avg_judge_accuracy', 0) - base_sum.get('avg_judge_accuracy', 0):+.2f}` |")
        lines.append(f"| **Judge: Groundedness** | **{rag_sum.get('avg_judge_groundedness', 0):.2f}** | {base_sum.get('avg_judge_groundedness', 0):.2f} | `{rag_sum.get('avg_judge_groundedness', 0) - base_sum.get('avg_judge_groundedness', 0):+.2f}` |")

    lines.append("\n---\n")

    # Question-by-Question Breakdown
    lines.append("## 2. Granular Question-by-Question Results\n")
    lines.append("| ID | Domain | With-RAG Recall | No-RAG Recall | With-RAG Telem | No-RAG Telem | With-RAG Cites | RAG Latency |")
    lines.append("|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")

    for rec in records:
        q_id = rec["id"]
        domain = rec["domain"]
        wr = rec["with_rag"]["metrics"]
        nr = rec["without_rag"]["metrics"]
        lat = rec["with_rag"]["total_latency"]
        lines.append(
            f"| **{q_id}** | {domain} | {wr['fact_recall_pct']:.0f}% | {nr['fact_recall_pct']:.0f}% | "
            f"{wr['telemetry_coverage_pct']:.0f}% | {nr['telemetry_coverage_pct']:.0f}% | {wr['citation_count']} | {lat:.2f}s |"
        )

    lines.append("\n---\n")

    # Detailed Evidence & Sample Analyses
    lines.append("## 3. Case Studies & Verification Evidence\n")
    for rec in records:
        lines.append(f"### {rec['id']}: {rec['domain']} — {rec['subdomain']}\n")
        lines.append(f"**Question:** {rec['question']}\n")
        lines.append(f"**Primary Source Document:** `{rec['primary_source']}`\n")
        
        lines.append("<details>\n<summary><b>View Ground Truth Answer</b></summary>\n\n")
        lines.append(f"{rec['ground_truth_answer']}\n")
        lines.append("</details>\n\n")

        lines.append("<details>\n<summary><b>View With-RAG Answer (Grounded)</b></summary>\n\n")
        lines.append(f"**Latency:** {rec['with_rag']['total_latency']}s | **Fact Recall:** {rec['with_rag']['metrics']['fact_recall_pct']}% | **Telemetry:** {rec['with_rag']['metrics']['telemetry_coverage_pct']}%\n")
        lines.append(f"**Citations:** `{rec['with_rag']['metrics']['citations']}`\n\n")
        lines.append(f"{rec['with_rag']['answer']}\n")
        lines.append("</details>\n\n")

        lines.append("<details>\n<summary><b>View Without-RAG Answer (Baseline)</b></summary>\n\n")
        lines.append(f"**Latency:** {rec['without_rag']['total_latency']}s | **Fact Recall:** {rec['without_rag']['metrics']['fact_recall_pct']}% | **Telemetry:** {rec['without_rag']['metrics']['telemetry_coverage_pct']}%\n\n")
        lines.append(f"{rec['without_rag']['answer']}\n")
        lines.append("</details>\n\n")

        if "judge" in rec["with_rag"]:
            lines.append("**Judge Analysis:**\n")
            lines.append(f"- **With-RAG Overall Score:** {rec['with_rag']['judge']['overall_score']} / 5.0 | *Strengths:* {rec['with_rag']['judge']['strengths']}\n")
            lines.append(f"- **Without-RAG Overall Score:** {rec['without_rag']['judge']['overall_score']} / 5.0 | *Weaknesses:* {rec['without_rag']['judge']['weaknesses']}\n")

        lines.append("\n---\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Exported Markdown report to: {output_path}")


# =============================================================================
# Main Evaluation Orchestrator
# =============================================================================

def run_evaluation(
    dataset_path: Path,
    chroma_dir: Path,
    model: str = DEFAULT_LLM_MODEL,
    top_k: int = DEFAULT_TOP_K,
    limit: Optional[int] = None,
    target_id: Optional[str] = None,
    enable_judge: bool = True,
    dry_run: bool = False,
    out_json: Path = DEFAULT_RESULTS_JSON,
    out_md: Path = DEFAULT_RESULTS_MD
):
    """Executes the full evaluation benchmark."""
    print("=" * 80)
    print("NASA SPACE MISSIONS: GROUND TRUTH RAG EVALUATOR")
    print(f"Dataset Path:    {dataset_path}")
    print(f"Vector Database: {chroma_dir} (Collection: {COLLECTION_NAME})")
    print(f"Ollama Model:    {model} (Host: {OLLAMA_HOST})")
    print(f"Top-K Chunks:    {top_k}")
    print(f"Judge Mode:      {'Enabled (LLM-as-a-judge)' if enable_judge else 'Disabled (Deterministic only)'}")
    print("=" * 80)

    # 1. Load Dataset
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at {dataset_path}. Run build_nasa_eval_system.py first.")

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    questions = dataset.get("questions", [])
    if target_id:
        questions = [q for q in questions if q.get("id") == target_id]
        if not questions:
            print(f"[ERROR] Question ID '{target_id}' not found in dataset.", file=sys.stderr)
            return
    elif limit and limit > 0:
        questions = questions[:limit]

    print(f"[Dataset] Loaded {len(questions)} question(s) for evaluation.")

    # 2. Check Vector DB
    collection = None
    if not dry_run:
        try:
            collection = load_vector_store(chroma_dir=chroma_dir, collection_name=COLLECTION_NAME)
            print(f"[VectorDB] [OK] Successfully connected. Collection chunk count: {collection.count():,}")
        except Exception as e:
            print(f"[VectorDB] [ERROR] Failed to load vector database: {e}", file=sys.stderr)
            return

    # 3. Check Ollama Client
    client = None
    if not dry_run:
        try:
            client = ollama.Client(host=OLLAMA_HOST)
            models_resp = client.list()
            avail = [m.model for m in models_resp.models] if hasattr(models_resp, 'models') else []
            if not any(model in name for name in avail):
                print(f"[Ollama] [WARNING] Target model '{model}' not found in available models: {avail}", file=sys.stderr)
            else:
                print(f"[Ollama] [OK] Server active and model '{model}' verified.")
        except Exception as e:
            print(f"[Ollama] [ERROR] Could not connect to Ollama: {e}", file=sys.stderr)
            return

    # Dry-run exit
    if dry_run:
        print("\n[DRY RUN SUMMARY]")
        print(f"Questions to evaluate ({len(questions)}):")
        for q in questions:
            print(f"  - [{q['id']}] {q['domain']}: {q['question'][:75]}...")
        print("\nDry-run completed successfully. No LLM calls were made.")
        return

    # 4. Evaluation Loop
    eval_records = []
    total_q = len(questions)

    print("\n" + "=" * 80)
    print(f"STARTING BENCHMARK EXECUTION ({total_q} Questions)")
    print("=" * 80)

    for idx, q_item in enumerate(questions, start=1):
        q_id = q_item["id"]
        query = q_item["question"]
        domain = q_item.get("domain", "NASA")
        subdomain = q_item.get("subdomain", "")
        gt_answer = q_item.get("ground_truth_answer", "")

        print(f"\n[{idx:02d}/{total_q:02d}] Evaluating {q_id}: {domain} - {subdomain}")
        print(f"  Q: \"{query[:80]}...\"")

        # Step A: With-RAG Generation
        print("  -> Generating With-RAG response...", end="", flush=True)
        rag_res = generate_rag_response(
            query=query,
            collection=collection,
            client=client,
            model=model,
            top_k=top_k
        )
        print(f" done ({rag_res['total_latency']}s, {len(rag_res['citations'])} citations)")

        # Step B: Baseline Generation (Without-RAG)
        print("  -> Generating Without-RAG response...", end="", flush=True)
        base_res = generate_baseline_response(
            query=query,
            client=client,
            model=model
        )
        print(f" done ({base_res['total_latency']}s)")

        # Step C: Deterministic Metric Computation
        rag_metrics = evaluate_deterministic_metrics(rag_res["answer"], q_item)
        base_metrics = evaluate_deterministic_metrics(base_res["answer"], q_item)
        rag_res["metrics"] = rag_metrics
        base_res["metrics"] = base_metrics

        print(f"  [Metrics] Fact Recall: With-RAG {rag_metrics['fact_recall_pct']:.0f}% vs. No-RAG {base_metrics['fact_recall_pct']:.0f}%")
        print(f"  [Metrics] Telemetry:   With-RAG {rag_metrics['telemetry_coverage_pct']:.0f}% vs. No-RAG {base_metrics['telemetry_coverage_pct']:.0f}%")

        # Step D: Optional LLM-as-a-Judge Evaluation
        if enable_judge:
            print("  -> Running LLM-as-a-Judge evaluation...", end="", flush=True)
            rag_judge = judge_answer_with_llm(query, gt_answer, rag_res["answer"], client, model)
            base_judge = judge_answer_with_llm(query, gt_answer, base_res["answer"], client, model)
            rag_res["judge"] = rag_judge
            base_res["judge"] = base_judge
            print(f" done (RAG: {rag_judge['overall_score']:.1f}/5.0 | No-RAG: {base_judge['overall_score']:.1f}/5.0)")

        record = {
            "id": q_id,
            "domain": domain,
            "subdomain": subdomain,
            "primary_source": q_item.get("primary_source", ""),
            "supporting_sources": q_item.get("supporting_sources", []),
            "question": query,
            "ground_truth_answer": gt_answer,
            "ground_truth_facts": q_item.get("ground_truth_facts", []),
            "telemetry_metrics": q_item.get("telemetry_metrics", []),
            "with_rag": rag_res,
            "without_rag": base_res
        }
        eval_records.append(record)

    # 5. Compute Aggregate Summary Statistics
    def _avg(lst):
        return round(sum(lst) / len(lst), 2) if lst else 0.0

    summary = {
        "with_rag": {
            "avg_fact_recall_pct": _avg([r["with_rag"]["metrics"]["fact_recall_pct"] for r in eval_records]),
            "avg_telemetry_coverage_pct": _avg([r["with_rag"]["metrics"]["telemetry_coverage_pct"] for r in eval_records]),
            "avg_citations": _avg([r["with_rag"]["metrics"]["citation_count"] for r in eval_records]),
            "avg_aligned_citations": _avg([r["with_rag"]["metrics"]["aligned_citation_count"] for r in eval_records]),
            "avg_retrieval_latency_sec": _avg([r["with_rag"]["retrieval_latency"] for r in eval_records]),
            "avg_generation_latency_sec": _avg([r["with_rag"]["generation_latency"] for r in eval_records]),
            "avg_total_latency_sec": _avg([r["with_rag"]["total_latency"] for r in eval_records]),
        },
        "without_rag": {
            "avg_fact_recall_pct": _avg([r["without_rag"]["metrics"]["fact_recall_pct"] for r in eval_records]),
            "avg_telemetry_coverage_pct": _avg([r["without_rag"]["metrics"]["telemetry_coverage_pct"] for r in eval_records]),
            "avg_citations": _avg([r["without_rag"]["metrics"]["citation_count"] for r in eval_records]),
            "avg_aligned_citations": 0.0,
            "avg_retrieval_latency_sec": 0.0,
            "avg_generation_latency_sec": _avg([r["without_rag"]["generation_latency"] for r in eval_records]),
            "avg_total_latency_sec": _avg([r["without_rag"]["total_latency"] for r in eval_records]),
        }
    }

    if enable_judge:
        summary["with_rag"]["avg_judge_overall"] = _avg([r["with_rag"]["judge"]["overall_score"] for r in eval_records])
        summary["with_rag"]["avg_judge_accuracy"] = _avg([r["with_rag"]["judge"]["factual_accuracy"] for r in eval_records])
        summary["with_rag"]["avg_judge_groundedness"] = _avg([r["with_rag"]["judge"]["groundedness"] for r in eval_records])
        summary["with_rag"]["avg_judge_completeness"] = _avg([r["with_rag"]["judge"]["completeness"] for r in eval_records])

        summary["without_rag"]["avg_judge_overall"] = _avg([r["without_rag"]["judge"]["overall_score"] for r in eval_records])
        summary["without_rag"]["avg_judge_accuracy"] = _avg([r["without_rag"]["judge"]["factual_accuracy"] for r in eval_records])
        summary["without_rag"]["avg_judge_groundedness"] = _avg([r["without_rag"]["judge"]["groundedness"] for r in eval_records])
        summary["without_rag"]["avg_judge_completeness"] = _avg([r["without_rag"]["judge"]["completeness"] for r in eval_records])

    final_payload = {
        "metadata": {
            "dataset_title": dataset.get("title", ""),
            "course": dataset.get("course", ""),
            "institution": dataset.get("institution", ""),
            "authors": dataset.get("authors", []),
            "evaluation_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": model,
            "top_k": top_k,
            "total_questions_evaluated": len(eval_records),
        },
        "summary": summary,
        "evaluations": eval_records
    }

    # 6. Save JSON & Markdown
    out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(final_payload, f, indent=2, ensure_ascii=False)
    print(f"\n[OK] Saved complete evaluation results to: {out_json}")

    generate_markdown_report(final_payload, out_md)

    # 7. Print Terminal Summary
    print("\n" + "=" * 80)
    print("BENCHMARK EVALUATION SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Metric':<30} | {'With-RAG':<15} | {'Without-RAG':<15} | {'Delta':<10}")
    print("-" * 80)
    w_sum = summary["with_rag"]
    b_sum = summary["without_rag"]
    print(f"{'Fact Recall %':<30} | {w_sum['avg_fact_recall_pct']:>13.1f}% | {b_sum['avg_fact_recall_pct']:>13.1f}% | {w_sum['avg_fact_recall_pct'] - b_sum['avg_fact_recall_pct']:>+9.1f}%")
    print(f"{'Telemetry Metric Coverage %':<30} | {w_sum['avg_telemetry_coverage_pct']:>13.1f}% | {b_sum['avg_telemetry_coverage_pct']:>13.1f}% | {w_sum['avg_telemetry_coverage_pct'] - b_sum['avg_telemetry_coverage_pct']:>+9.1f}%")
    print(f"{'Average Citations':<30} | {w_sum['avg_citations']:>14.2f} | {b_sum['avg_citations']:>14.2f} | {w_sum['avg_citations'] - b_sum['avg_citations']:>+9.2f}")
    print(f"{'Average Total Latency (s)':<30} | {w_sum['avg_total_latency_sec']:>13.2f}s | {b_sum['avg_total_latency_sec']:>13.2f}s | {w_sum['avg_total_latency_sec'] - b_sum['avg_total_latency_sec']:>+9.2f}s")
    if enable_judge:
        print(f"{'Judge Overall Score (1-5)':<30} | {w_sum['avg_judge_overall']:>14.2f} | {b_sum['avg_judge_overall']:>14.2f} | {w_sum['avg_judge_overall'] - b_sum['avg_judge_overall']:>+9.2f}")
    print("=" * 80)


# =============================================================================
# CLI Entry Point
# =============================================================================

def parse_args():
    parser = argparse.ArgumentParser(
        description="NASA Space Missions RAG vs. Baseline Benchmark Evaluator"
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET_PATH,
        help="Path to 20-question ground truth JSON dataset"
    )
    parser.add_argument(
        "--chroma-dir",
        type=Path,
        default=DEFAULT_CHROMA_DIR,
        help="Path to ChromaDB persistent storage directory"
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_LLM_MODEL,
        help="Ollama model name (default: qwen2.5:7b)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help="Number of retrieved chunks for RAG"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit evaluation to first N questions"
    )
    parser.add_argument(
        "--id",
        type=str,
        default=None,
        help="Evaluate a single question by ID (e.g. NASA_Q01, NASA_Q04)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run evaluation on all 20 questions"
    )
    parser.add_argument(
        "--no-judge",
        action="store_true",
        help="Skip LLM-as-a-judge scoring for fast deterministic evaluation"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Inspect dataset and connection sanity without running LLM inference"
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=DEFAULT_RESULTS_JSON,
        help="Output path for results JSON"
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=DEFAULT_RESULTS_MD,
        help="Output path for results Markdown report"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_evaluation(
        dataset_path=args.dataset,
        chroma_dir=args.chroma_dir,
        model=args.model,
        top_k=args.top_k,
        limit=args.limit,
        target_id=args.id,
        enable_judge=not args.no_judge,
        dry_run=args.dry_run,
        out_json=args.out_json,
        out_md=args.out_md
    )
