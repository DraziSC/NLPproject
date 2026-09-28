#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
NASA Space Missions: Ground Truth RAG vs. Baseline Evaluation System (Refactored)
===============================================================================
Course: Natural Language Interaction (ILN) 2026/2027
Institution: Universidade de Coimbra - DEI-FCTUC
Authors: Mohammed Abdelqader & Michael O'Shea

Description:
  Automated evaluation harness that benchmarks the With-RAG system against a
  Without-RAG parametric baseline using the 20-question authoritative ground
  truth dataset ('nasa_eval_dataset.json').

Architecture:
  - Reuses canonical RAG pipelines directly from 'D2RAG.py' (single source of truth):
      * Vector Database: ChromaDB persistent collection 'nasa_missions'
      * Retrieval: Semantic-chunked top-k retrieval with metadata tracking
      * Generation: Ollama LLM with strict grounding & inline citation attribution
  - Deterministic Scoring:
      * Ground Truth Fact Recall %
      * Telemetry Metric & Quantitative Parameter Coverage %
      * Inline Citation Frequency and Source Relevance
      * Retrieval vs. Generation Latency
  - LLM-as-a-Judge Scoring:
      * Independent evaluation judge (e.g., 'mistral-small:24b' or 'qwen2.5:14b')
      * Evaluates Factual Accuracy, Completeness, Groundedness, and Scientific Precision
  - Multi-format Reporting:
      * Structured machine-readable JSON: 'data/nasa_eval_results.json'
      * Comprehensive Markdown executive report: 'data/nasa_eval_results.md'
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

# Ensure localhost traffic bypasses any sandbox or corporate proxies
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

# Reconfigure stdout/stderr to UTF-8 on Windows
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr is not None and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# =============================================================================
# Import Core RAG Subsystems directly from D2RAG (Single Source of Truth)
# =============================================================================
try:
    import D2RAG
    from D2RAG import (
        CHROMA_DIR as DEFAULT_CHROMA_DIR,
        COLLECTION_NAME,
        DEFAULT_LLM_MODEL,
        DEFAULT_TOP_K,
        OLLAMA_HOST,
        build_or_load_vector_db,
        extract_citations,
        generate_baseline_response,
        generate_rag_response,
        get_ollama_client,
        resolve_inline_citations,
    )
    D2RAG_AVAILABLE = True
except ImportError as e:
    D2RAG_AVAILABLE = False
    D2RAG_IMPORT_ERROR = e

# =============================================================================
# Global Constants & Paths
# =============================================================================

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET_PATH = PROJECT_DIR / "nasa_eval_dataset.json"
DEFAULT_RESULTS_JSON = PROJECT_DIR / "data" / "nasa_eval_results.json"
DEFAULT_RESULTS_MD = PROJECT_DIR / "data" / "nasa_eval_results.md"

# Evaluator Judge Model: Recommended larger or independent model to eliminate self-preference bias
DEFAULT_JUDGE_LLM_MODEL = "mistral-small:24b"

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
# Evaluation Metrics & Automated Judges
# =============================================================================

def evaluate_deterministic_metrics(answer_text: str, ground_truth_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes lexical fact recall, telemetry parameter coverage, and citation alignment
    against the annotated ground truth item.
    """
    answer_lower = answer_text.lower()

    # 1. Fact Recall
    gt_facts = ground_truth_item.get("ground_truth_facts", [])
    matched_facts = []
    missing_facts = []
    for fact in gt_facts:
        f_clean = fact.strip().lower()
        if f_clean in answer_lower:
            matched_facts.append(fact)
        else:
            missing_facts.append(fact)

    fact_recall = (len(matched_facts) / len(gt_facts) * 100.0) if gt_facts else 100.0

    # 2. Telemetry Metric Coverage
    telemetry_metrics = ground_truth_item.get("telemetry_metrics", [])
    matched_metrics = []
    missing_metrics = []
    for metric in telemetry_metrics:
        m_clean = metric.strip().lower().replace("μm", "um")
        ans_norm = answer_lower.replace("μm", "um")
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
    model: str = DEFAULT_JUDGE_LLM_MODEL
) -> Dict[str, Any]:
    """
    Invokes LLM-as-a-judge (decoupled model) to evaluate candidate answer against ground truth.
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
    lines.append(f"**Generator Model:** `{evaluation_results.get('model', DEFAULT_LLM_MODEL)}`  ")
    lines.append(f"**Judge Model:** `{evaluation_results.get('judge_model', DEFAULT_JUDGE_LLM_MODEL)}`  ")
    lines.append(f"**Total Questions Evaluated:** {len(records)}\n")
    lines.append("---\n")

    # Executive Summary Table
    lines.append("## 1. Executive Performance Comparison\n")
    lines.append("| Metric Dimension | With-RAG (Augmented) | Without-RAG (Parametric) | Delta (Δ) |")
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
    chroma_dir: Path = DEFAULT_CHROMA_DIR,
    model: str = DEFAULT_LLM_MODEL,
    judge_model: str = DEFAULT_JUDGE_LLM_MODEL,
    top_k: int = DEFAULT_TOP_K,
    limit: Optional[int] = None,
    target_id: Optional[str] = None,
    enable_judge: bool = True,
    dry_run: bool = False,
    out_json: Path = DEFAULT_RESULTS_JSON,
    out_md: Path = DEFAULT_RESULTS_MD
):
    """Executes the full evaluation benchmark reusing D2RAG pipelines."""
    if not D2RAG_AVAILABLE:
        raise RuntimeError(f"Could not import D2RAG module: {D2RAG_IMPORT_ERROR}")

    print("=" * 80)
    print("NASA SPACE MISSIONS: GROUND TRUTH RAG EVALUATOR (D2RAG Integrated)")
    print(f"Dataset Path:    {dataset_path}")
    print(f"Vector Database: {chroma_dir} (Collection: {COLLECTION_NAME})")
    print(f"Generator Model: {model} (Host: {OLLAMA_HOST})")
    print(f"Judge Model:     {judge_model if enable_judge else 'Disabled'}")
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

    # 2. Connect Vector Database via D2RAG
    collection = None
    if not dry_run:
        try:
            collection = build_or_load_vector_db(
                chroma_dir=chroma_dir,
                collection_name=COLLECTION_NAME,
                force_reindex=False
            )
            print(f"[VectorDB] [OK] Successfully connected via D2RAG. Collection chunk count: {collection.count():,}")
        except Exception as e:
            print(f"[VectorDB] [ERROR] Failed to load vector database: {e}", file=sys.stderr)
            return

    # 3. Check Ollama Client via D2RAG
    client = None
    if not dry_run:
        try:
            client = get_ollama_client(OLLAMA_HOST)
            models_resp = client.list()
            avail = [m.model for m in models_resp.models] if hasattr(models_resp, 'models') else []
            if not any(model in name for name in avail):
                print(f"[Ollama] [WARNING] Generator model '{model}' not found in available models: {avail}", file=sys.stderr)
            else:
                print(f"[Ollama] [OK] Generator model '{model}' verified on server.")
            if enable_judge and not any(judge_model in name for name in avail):
                print(f"[Ollama] [WARNING] Judge model '{judge_model}' not found in available models: {avail}", file=sys.stderr)
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

        # Step A: With-RAG Generation (Calling canonical D2RAG pipeline)
        print("  -> Generating With-RAG response...", end="", flush=True)
        rag_res = generate_rag_response(
            query=query,
            collection=collection,
            client=client,
            model=model,
            top_k=top_k
        )
        print(f" done ({rag_res['total_latency']:.2f}s, {len(rag_res['citations'])} citations)")

        # Step B: Baseline Generation (Without-RAG)
        print("  -> Generating Without-RAG response...", end="", flush=True)
        base_res = generate_baseline_response(
            query=query,
            client=client,
            model=model
        )
        print(f" done ({base_res['total_latency']:.2f}s)")

        # Step C: Deterministic Metric Computation
        rag_metrics = evaluate_deterministic_metrics(rag_res["answer"], q_item)
        base_metrics = evaluate_deterministic_metrics(base_res["answer"], q_item)
        rag_res["metrics"] = rag_metrics
        base_res["metrics"] = base_metrics

        print(f"  [Metrics] Fact Recall: With-RAG {rag_metrics['fact_recall_pct']:.0f}% vs. No-RAG {base_metrics['fact_recall_pct']:.0f}%")
        print(f"  [Metrics] Telemetry:   With-RAG {rag_metrics['telemetry_coverage_pct']:.0f}% vs. No-RAG {base_metrics['telemetry_coverage_pct']:.0f}%")

        # Step D: Optional LLM-as-a-Judge Evaluation
        if enable_judge:
            print(f"  -> Running LLM-as-a-Judge evaluation (model: {judge_model})...", end="", flush=True)
            rag_judge = judge_answer_with_llm(query, gt_answer, rag_res["answer"], client, model=judge_model)
            base_judge = judge_answer_with_llm(query, gt_answer, base_res["answer"], client, model=judge_model)
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
            "judge_model": judge_model if enable_judge else "None",
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
        description="NASA Space Missions RAG vs. Baseline Benchmark Evaluator (D2RAG Integrated)"
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
        help="Generator Ollama model name (default: qwen2.5:7b)"
    )
    parser.add_argument(
        "--judge-model",
        type=str,
        default=DEFAULT_JUDGE_LLM_MODEL,
        help=f"Judge Ollama model name (default: {DEFAULT_JUDGE_LLM_MODEL})"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=DEFAULT_TOP_K,
        help=f"Number of retrieved chunks for RAG (default: {DEFAULT_TOP_K})"
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
        judge_model=args.judge_model,
        top_k=args.top_k,
        limit=args.limit,
        target_id=args.id,
        enable_judge=not args.no_judge,
        dry_run=args.dry_run,
        out_json=args.out_json,
        out_md=args.out_md
    )
