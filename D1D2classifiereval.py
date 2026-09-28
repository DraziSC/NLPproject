#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
Course:      Natural Language Interaction (ILN)
Institution: Universidade de Coimbra - DEI-FCTUC
Project:     Deliverable 2 / Deliverable 3 - Standalone Intent Classifier Evaluation
Authors:     Mohammed Abdelqader & Michael O'Shea
Date:        September 2026

Description:
Standalone evaluation harness for the D1/D2 Intent Router Classifier.
This script evaluates the few-shot semantic transfer learning classifier
(SBERT 'all-MiniLM-L6-v2' dense embeddings + Calibrated Logistic Regression probe)
without requiring ChromaDB, vector database re-indexing, or Ollama LLM generation.

Evaluation Capabilities:
  1. 5-Fold Stratified Cross-Validation (Accuracy, Precision, Recall, F1, Confusion Matrix).
  2. Baseline Architecture Ablation: Calibrated Linear Probe vs. Nearest Centroid Distance.
  3. Polysemy & Semantic Boundary Stress-Testing (e.g., emotional vs. mechanical stress).
  4. Latency & CPU Throughput Benchmarking.
  5. Interactive / Single-Query Live Classification Testing.
================================================================================
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Ensure localhost bypasses any proxy settings
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold

# Import classifier architecture and training data from D1D2classifierrouter
try:
    from D1D2classifierrouter import (
        EMBEDDING_MODEL_NAME,
        LABEL_D1_CHITCHAT,
        LABEL_D2_NASA,
        ROUTER_MODEL_PATH,
        ROUTER_TRAINING_DATA,
        SBERTRouterClassifier,
    )
except ImportError as e:
    print(f"[ERROR] Could not import from D1D2classifierrouter.py: {e}", file=sys.stderr)
    sys.exit(1)

PROJECT_DIR = Path(__file__).resolve().parent
DEFAULT_REPORT_JSON = PROJECT_DIR / "data" / "classifier_eval_results.json"
DEFAULT_REPORT_MD = PROJECT_DIR / "data" / "classifier_eval_report.md"

# =============================================================================
# Polysemy and Ambiguity Challenge Test Suite
# =============================================================================
STRESS_TEST_CASES: List[Tuple[str, str, str]] = [
    # (Utterance, Expected Label, Polysemous Focus)
    ("I feel an immense amount of stress about my exams tomorrow", LABEL_D1_CHITCHAT, "Emotional Stress"),
    ("What aerodynamic stress does the rocket core stage experience at Max-Q?", LABEL_D2_NASA, "Mechanical / Aerodynamic Stress"),
    ("I need to work on my motivation and daily study habits", LABEL_D1_CHITCHAT, "Study Work / Personal Effort"),
    ("How does the ChemCam laser work on Mars soil targets?", LABEL_D2_NASA, "Physical / Functional Mechanism"),
    ("Can you help me feel less lonely today?", LABEL_D1_CHITCHAT, "Emotional / Social Support"),
    ("Can you help explain the cryogenic sunshield of the James Webb telescope?", LABEL_D2_NASA, "Technical Explanation Request"),
    ("My laptop crashed and I am so upset", LABEL_D1_CHITCHAT, "Daily Frustration / Venting"),
    ("What caused the Apollo 11 computer to trigger 1201 and 1202 alarms?", LABEL_D2_NASA, "Spacecraft Avionics Fault"),
    ("Do you like pizza or coffee?", LABEL_D1_CHITCHAT, "Casual Preference / Chit-chat"),
    ("What are the propellant types for the SLS core stage?", LABEL_D2_NASA, "Chemical Rocket Propulsion"),
    ("I am feeling really tired and burned out from school", LABEL_D1_CHITCHAT, "Academic Fatigue"),
    ("What is the battery recharge cycle of the Ingenuity Mars helicopter?", LABEL_D2_NASA, "Rotorcraft Telemetry"),
]


# =============================================================================
# 1. Stratified K-Fold Cross-Validation
# =============================================================================

def run_cross_validation(
    training_data: List[Tuple[str, str]] = ROUTER_TRAINING_DATA,
    n_splits: int = 5,
    random_state: int = 42
) -> Dict[str, Any]:
    """
    Executes an N-fold Stratified Cross-Validation on the router dataset.
    Evaluates both the Logistic Regression linear probe and the Nearest Centroid baseline.
    """
    print("\n" + "=" * 80)
    print(f"INTENT CLASSIFIER EVALUATION: {n_splits}-FOLD STRATIFIED CROSS-VALIDATION")
    print("=" * 80)

    encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [item[0] for item in training_data]
    y = np.array([1 if item[1] == LABEL_D2_NASA else 0 for item in training_data])

    print(f"Vectorizing {len(texts)} samples with '{EMBEDDING_MODEL_NAME}' (384-dimensional dense vectors)...")
    t0 = time.time()
    X = encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    t_embed = time.time() - t0
    print(f"Embedding completed in {t_embed:.2f}s ({len(texts)/(t_embed if t_embed>0 else 1):.1f} samples/sec).")

    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)

    # Tracking for Logistic Regression (Linear Probe)
    lr_y_true = []
    lr_y_pred = []
    lr_fold_accuracies = []

    # Tracking for Nearest-Centroid Baseline
    nc_y_pred = []
    nc_fold_accuracies = []

    print("\n--- Running Fold Splits ---")
    fold = 1
    for train_idx, test_idx in skf.split(X, y):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Model 1: Logistic Regression Linear Probe
        clf = LogisticRegression(C=1.0, max_iter=1000, random_state=random_state)
        clf.fit(X_train, y_train)
        preds_lr = clf.predict(X_test)
        acc_lr = accuracy_score(y_test, preds_lr) * 100.0
        lr_fold_accuracies.append(acc_lr)

        lr_y_true.extend(y_test)
        lr_y_pred.extend(preds_lr)

        # Model 2: Nearest-Centroid Baseline (Geometric Prototypical)
        c0 = np.mean(X_train[y_train == 0], axis=0)
        c0 /= np.linalg.norm(c0)
        c1 = np.mean(X_train[y_train == 1], axis=0)
        c1 /= np.linalg.norm(c1)

        sim_c0 = np.dot(X_test, c0)
        sim_c1 = np.dot(X_test, c1)
        preds_nc = (sim_c1 >= sim_c0).astype(int)
        acc_nc = accuracy_score(y_test, preds_nc) * 100.0
        nc_fold_accuracies.append(acc_nc)
        nc_y_pred.extend(preds_nc)

        print(f"  Fold {fold}: Linear Probe Acc = {acc_lr:5.1f}% | Nearest-Centroid Acc = {acc_nc:5.1f}%  ({len(test_idx)} samples)")
        fold += 1

    # Aggregate Metrics for Linear Probe
    lr_precision, lr_recall, lr_f1, _ = precision_recall_fscore_support(lr_y_true, lr_y_pred, average="weighted")
    nc_precision, nc_recall, nc_f1, _ = precision_recall_fscore_support(lr_y_true, nc_y_pred, average="weighted")

    target_names = [f"D1 ({LABEL_D1_CHITCHAT})", f"D2 ({LABEL_D2_NASA})"]
    report_dict = classification_report(lr_y_true, lr_y_pred, target_names=target_names, output_dict=True)
    report_str = classification_report(lr_y_true, lr_y_pred, target_names=target_names, digits=3)

    cm = confusion_matrix(lr_y_true, lr_y_pred)

    print("\n" + "=" * 80)
    print("CLASSIFICATION REPORT: LOGISTIC REGRESSION LINEAR PROBE")
    print("=" * 80)
    print(report_str)

    print("CONFUSION MATRIX:")
    print(f"                    Predicted D1 (Chat)    Predicted D2 (NASA)")
    print(f"  Actual D1 (Chat):      {cm[0][0]:>12}             {cm[0][1]:>12}")
    print(f"  Actual D2 (NASA):      {cm[1][0]:>12}             {cm[1][1]:>12}")

    print("\n" + "=" * 80)
    print("ARCHITECTURAL ABLATION: PROBE VS. CENTROID BASELINE")
    print("=" * 80)
    print(f"{'Classifier Architecture':<36} | {'Mean Accuracy':<14} | {'Weighted F1':<12}")
    print("-" * 80)
    print(f"{'SBERT + Logistic Regression (Probe)':<36} | {np.mean(lr_fold_accuracies):>12.2f}% | {lr_f1:>10.4f}")
    print(f"{'SBERT + Cosine Centroids (Baseline)':<36} | {np.mean(nc_fold_accuracies):>12.2f}% | {nc_f1:>10.4f}")
    print("=" * 80)

    return {
        "n_samples": len(texts),
        "n_splits": n_splits,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "linear_probe": {
            "mean_accuracy_pct": round(float(np.mean(lr_fold_accuracies)), 2),
            "fold_accuracies": [round(a, 2) for a in lr_fold_accuracies],
            "weighted_precision": round(float(lr_precision), 4),
            "weighted_recall": round(float(lr_recall), 4),
            "weighted_f1": round(float(lr_f1), 4),
            "confusion_matrix": cm.tolist(),
            "classification_report": report_dict,
        },
        "centroid_baseline": {
            "mean_accuracy_pct": round(float(np.mean(nc_fold_accuracies)), 2),
            "fold_accuracies": [round(a, 2) for a in nc_fold_accuracies],
            "weighted_f1": round(float(nc_f1), 4),
        }
    }


# =============================================================================
# 2. Polysemy & Semantic Boundary Stress Testing
# =============================================================================

def run_stress_tests(router: SBERTRouterClassifier) -> List[Dict[str, Any]]:
    """
    Evaluates how the classifier handles ambiguous polysemous words ('stress', 'work', 'help')
    where lexical matching fails but dense contextual semantic embeddings succeed.
    """
    print("\n" + "=" * 80)
    print("POLYSEMY & AMBIGUITY STRESS TESTING (THE 'STRESS' & 'WORK' PROBLEM)")
    print("=" * 80)

    stress_results = []
    passed_count = 0

    for utterance, expected_label, focus_topic in STRESS_TEST_CASES:
        pred = router.predict_intent(utterance)
        actual_label = pred["predicted_label"]
        confidence = pred["confidence"]
        latency = pred["latency_ms"]
        is_correct = (actual_label == expected_label)

        if is_correct:
            passed_count += 1
            status_str = "PASSED"
        else:
            status_str = "FAILED"

        print(f"\n[{focus_topic}]")
        print(f"  Utterance:  \"{utterance}\"")
        print(f"  Expected:   {expected_label}")
        print(f"  Predicted:  {actual_label} (Confidence: {confidence * 100:.1f}%) | Latency: {latency:.2f}ms")
        print(f"  Result:     [{status_str}]")

        stress_results.append({
            "focus_topic": focus_topic,
            "utterance": utterance,
            "expected_label": expected_label,
            "predicted_label": actual_label,
            "confidence": round(confidence, 4),
            "prob_d1": round(pred["prob_d1_chitchat"], 4),
            "prob_d2": round(pred["prob_d2_nasa"], 4),
            "latency_ms": round(latency, 2),
            "passed": is_correct
        })

    pass_rate = (passed_count / len(STRESS_TEST_CASES)) * 100.0
    print("\n" + "-" * 80)
    print(f"Polysemy Stress Test Summary: {passed_count}/{len(STRESS_TEST_CASES)} passed ({pass_rate:.1f}% accuracy)")
    print("=" * 80)

    return stress_results


# =============================================================================
# 3. Latency & Throughput Benchmarking
# =============================================================================

def benchmark_inference_latency(router: SBERTRouterClassifier, n_iterations: int = 100) -> Dict[str, float]:
    """Measures single-utterance CPU inference latency and throughput."""
    sample_queries = [
        "How are you feeling today?",
        "What is the orbital period change of Dimorphos from the DART impact?",
        "I am so worried about my final grade",
        "Explain the cryocooler loop on the JWST MIRI instrument."
    ]

    latencies = []
    for i in range(n_iterations):
        q = sample_queries[i % len(sample_queries)]
        t0 = time.perf_counter()
        _ = router.predict_intent(q)
        latencies.append((time.perf_counter() - t0) * 1000.0)

    lat_arr = np.array(latencies)
    mean_lat = float(np.mean(lat_arr))
    p50 = float(np.percentile(lat_arr, 50))
    p95 = float(np.percentile(lat_arr, 95))
    p99 = float(np.percentile(lat_arr, 99))
    qps = 1000.0 / mean_lat if mean_lat > 0 else 0.0

    print("\n" + "=" * 80)
    print(f"CPU INFERENCE LATENCY & THROUGHPUT BENCHMARK ({n_iterations} Iterations)")
    print("=" * 80)
    print(f"  Mean Latency:    {mean_lat:6.2f} ms")
    print(f"  Median (P50):    {p50:6.2f} ms")
    print(f"  95th Percentile: {p95:6.2f} ms")
    print(f"  99th Percentile: {p99:6.2f} ms")
    print(f"  Throughput:      {qps:6.1f} queries/sec (Single CPU thread)")
    print("=" * 80)

    return {
        "mean_latency_ms": round(mean_lat, 2),
        "median_p50_ms": round(p50, 2),
        "p95_ms": round(p95, 2),
        "p99_ms": round(p99, 2),
        "throughput_qps": round(qps, 1)
    }


# =============================================================================
# 4. Report Exporters
# =============================================================================

def export_markdown_report(results: Dict[str, Any], output_path: Path):
    """Exports a formatted markdown evaluation report for project deliverables."""
    cv = results.get("cross_validation", {}).get("linear_probe", {})
    ablation = results.get("cross_validation", {})
    stress = results.get("stress_tests", [])
    perf = results.get("latency_benchmark", {})

    lines = [
        "# D1/D2 Intent Router: Standalone Classification Evaluation Report",
        "",
        "**Course:** Natural Language Interaction (ILN) 2026/2027  ",
        "**Institution:** Universidade de Coimbra (DEI-FCTUC)  ",
        "**Authors:** Mohammed Abdelqader & Michael O'Shea  ",
        f"**Evaluation Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Encoder Model:** `{results.get('embedding_model', EMBEDDING_MODEL_NAME)}` (384-dimensional dense embeddings)  ",
        f"**Dataset Size:** {results.get('dataset_size', 0)} annotated utterances  ",
        "",
        "---",
        "",
        "## 1. Stratified 5-Fold Cross-Validation Performance",
        "",
        "| Metric Dimension | Linear Probe (Logistic Regression) | Nearest Centroid Baseline | Delta (Δ) |",
        "| :--- | :---: | :---: | :---: |",
        f"| **Mean Accuracy** | **{cv.get('mean_accuracy_pct', 0):.2f}%** | {ablation.get('centroid_baseline', {}).get('mean_accuracy_pct', 0):.2f}% | `+{cv.get('mean_accuracy_pct', 0) - ablation.get('centroid_baseline', {}).get('mean_accuracy_pct', 0):.2f}%` |",
        f"| **Weighted Precision** | **{cv.get('weighted_precision', 0):.4f}** | — | — |",
        f"| **Weighted Recall** | **{cv.get('weighted_recall', 0):.4f}** | — | — |",
        f"| **Weighted F1-Score** | **{cv.get('weighted_f1', 0):.4f}** | {ablation.get('centroid_baseline', {}).get('weighted_f1', 0):.4f} | `+{cv.get('weighted_f1', 0) - ablation.get('centroid_baseline', {}).get('weighted_f1', 0):.4f}` |",
        "",
        "### Fold-by-Fold Breakdown",
        "",
        f"- **Fold Accuracies:** `{cv.get('fold_accuracies', [])}`",
        "",
        "---",
        "",
        "## 2. Polysemy & Semantic Boundary Stress Test Results",
        "",
        "| Polysemous Context | Test Utterance | Expected | Predicted | Confidence | Status |",
        "| :--- | :--- | :---: | :---: | :---: | :---: |",
    ]

    for item in stress:
        status_icon = "✅ PASS" if item["passed"] else "❌ FAIL"
        lines.append(
            f"| **{item['focus_topic']}** | \"{item['utterance']}\" | `{item['expected_label']}` | `{item['predicted_label']}` | {item['confidence']*100:.1f}% | {status_icon} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Execution Latency & CPU Throughput",
        "",
        f"- **Mean Single-Query Latency:** `{perf.get('mean_latency_ms', 0)} ms`",
        f"- **95th Percentile Latency (P95):** `{perf.get('p95_ms', 0)} ms`",
        f"- **Single-Thread CPU Throughput:** `{perf.get('throughput_qps', 0)} queries/second`",
        "",
        "> **Architectural Insight:** Running the few-shot linear probe on the CPU achieves sub-10ms response times with zero GPU VRAM consumption, allowing the GPU to remain 100% dedicated to the large 7B/24B RAG models.",
    ])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Saved Markdown evaluation report to: {output_path}")


# =============================================================================
# 5. Interactive Testing Shell
# =============================================================================

def interactive_eval_session(router: SBERTRouterClassifier):
    """Launches an interactive prompt to test custom user inputs live."""
    print("\n" + "=" * 80)
    print("D1/D2 INTENT ROUTER: INTERACTIVE CLASSIFICATION PROMPT")
    print("Type any utterance to view classification probabilities and dispatch destination.")
    print("Type 'quit', 'exit', or 'q' to stop.")
    print("=" * 80)

    while True:
        try:
            user_input = input("\nEnter query > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("quit", "exit", "q"):
                print("Exiting interactive test session.")
                break

            res = router.predict_intent(user_input)
            dest = res["predicted_label"]
            conf = res["confidence"]
            lat = res["latency_ms"]

            agent_name = "D1: The Optimist (Rule & spaCy)" if dest == LABEL_D1_CHITCHAT else "D2: NASA Expert RAG"

            print(f"  -> Predicted Intent:  [{dest}] -> {agent_name}")
            print(f"  -> Confidence:        {conf * 100:.1f}%")
            print(f"  -> Probabilities:     D1 (Chit-chat): {res['prob_d1_chitchat']:.4f} | D2 (NASA): {res['prob_d2_nasa']:.4f}")
            print(f"  -> Centroid Cos-Sim:  D1: {res['cos_sim_d1']:.4f} | D2: {res['cos_sim_d2']:.4f}")
            print(f"  -> Routing Latency:   {lat:.2f} ms")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting interactive test session.")
            break


# =============================================================================
# 6. CLI Main Function
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Standalone Intent Classifier Evaluation Suite (D1/D2 Router)"
    )
    parser.add_argument(
        "-k", "--k-folds",
        type=int,
        default=5,
        help="Number of folds for Stratified Cross-Validation (default: 5)"
    )
    parser.add_argument(
        "--test",
        type=str,
        default=None,
        help="Evaluate a single custom utterance and display its classification telemetry"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start an interactive test loop to classify queries live"
    )
    parser.add_argument(
        "--skip-stress",
        action="store_true",
        help="Skip the polysemy stress testing suite"
    )
    parser.add_argument(
        "--skip-bench",
        action="store_true",
        help="Skip the CPU latency benchmarking suite"
    )
    parser.add_argument(
        "--retrain",
        action="store_true",
        help="Force re-fitting the classifier head instead of loading cached weights"
    )
    parser.add_argument(
        "--out-json",
        type=Path,
        default=DEFAULT_REPORT_JSON,
        help=f"Path to export detailed JSON results (default: {DEFAULT_REPORT_JSON})"
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=DEFAULT_REPORT_MD,
        help=f"Path to export Markdown report (default: {DEFAULT_REPORT_MD})"
    )

    args = parser.parse_args()

    # Step 1: Initialize Router Classifier
    router = SBERTRouterClassifier()
    if args.retrain or not router.load(ROUTER_MODEL_PATH):
        router.fit(ROUTER_TRAINING_DATA)
        router.save(ROUTER_MODEL_PATH)

    # Mode A: Single query test
    if args.test:
        res = router.predict_intent(args.test)
        print(f"\nUtterance: \"{args.test}\"")
        print(f"  -> Predicted Label:  {res['predicted_label']}")
        print(f"  -> Confidence:       {res['confidence']*100:.1f}%")
        print(f"  -> Probabilities:    D1: {res['prob_d1_chitchat']:.4f} | D2: {res['prob_d2_nasa']:.4f}")
        print(f"  -> Latency:          {res['latency_ms']:.2f} ms")
        return

    # Mode B: Interactive test prompt
    if args.interactive:
        interactive_eval_session(router)
        return

    # Mode C: Full Standalone Evaluation Suite
    results = {
        "dataset_size": len(ROUTER_TRAINING_DATA),
        "embedding_model": EMBEDDING_MODEL_NAME,
        "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    # 1. 5-Fold Stratified Cross-Validation & Ablation
    cv_res = run_cross_validation(n_splits=args.k_folds)
    results["cross_validation"] = cv_res

    # 2. Polysemy Stress-Testing Suite
    if not args.skip_stress:
        stress_res = run_stress_tests(router)
        results["stress_tests"] = stress_res

    # 3. CPU Latency Benchmark
    if not args.skip_bench:
        bench_res = benchmark_inference_latency(router)
        results["latency_benchmark"] = bench_res

    # 4. Save Artifacts
    args.out_json.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[OK] Saved JSON evaluation metrics to: {args.out_json}")

    export_markdown_report(results, args.out_md)


if __name__ == "__main__":
    main()
