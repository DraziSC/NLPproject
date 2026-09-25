"""
================================================================================
Course:      Natural Language Interaction (ILN)
Institution: Universidade de Coimbra
Project:     Deliverable 2 (D2) Integration - Intent Classifier & Agent Router
Authors:     Mohammed Abdelqader & Michael O'Shea
Date:        September 25, 2026

Description:
Unified Conversational Agent that intelligently routes incoming user utterances
between:
  - Deliverable 1 (D1): "The Optimist" Rule-based Chatbot (NLTK + spaCy)
    Specializing in emotional support, academic well-being, stress, and chit-chat.
  - Deliverable 2 (D2): NASA Space Exploration RAG Agent (ChromaDB + Ollama Qwen2.5:7b)
    Specializing in technical aerospace telemetry, planetary science, and astrophysics.

Classification Paradigm:
  - Feature Extractor: Dense Semantic Embeddings via 'all-MiniLM-L6-v2' (SBERT / 384-d).
    Reuses the exact transformer model cached for ChromaDB with zero extra memory overhead.
  - Classifier Head: Calibrated Linear Probe (Logistic Regression with probability output).
  - Also includes Cosine Centroid Distance as an ablation baseline.
================================================================================
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple

# Ensure localhost traffic bypasses any sandbox or corporate proxies
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold

# Import D1 and D2 agent subsystems
import D1rule
from D1rule import (
    extract_key_topics,
    generate_fallback_response,
    lemmatize_text,
    persona_chat,
)
import D2RAG
from D2RAG import (
    build_or_load_vector_db,
    generate_rag_response,
    get_ollama_client,
    extract_citations,
)

# -----------------------------------------------------------------------------
# Configuration & Paths
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
ROUTER_MODEL_PATH = DATA_DIR / "router_classifier.joblib"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

LABEL_D1_CHITCHAT = "CHIT_CHAT"
LABEL_D2_NASA = "NASA_EXPERT"
DEFAULT_CONFIDENCE_THRESHOLD = 0.60


# =============================================================================
# 1. Training & Cross-Validation Dataset
# =============================================================================
# Carefully curated dataset with balanced classes, including challenging
# polysemous and lexical overlap edge cases (e.g., emotional vs mechanical stress).

ROUTER_TRAINING_DATA: List[Tuple[str, str]] = [
    # --- D1: Greetings, Persona, Identity & Well-being ---
    ("hello there", LABEL_D1_CHITCHAT),
    ("hi, how are you doing today?", LABEL_D1_CHITCHAT),
    ("good morning", LABEL_D1_CHITCHAT),
    ("hey chatbot", LABEL_D1_CHITCHAT),
    ("what is your name?", LABEL_D1_CHITCHAT),
    ("who created you and what can you do?", LABEL_D1_CHITCHAT),
    ("my name is Sarah", LABEL_D1_CHITCHAT),
    ("I am 22 years old", LABEL_D1_CHITCHAT),
    ("I live in Coimbra, Portugal", LABEL_D1_CHITCHAT),
    ("my hobby is playing acoustic guitar", LABEL_D1_CHITCHAT),
    ("I like watching movies in my spare time", LABEL_D1_CHITCHAT),
    ("you are very kind and helpful", LABEL_D1_CHITCHAT),
    ("thank you so much for listening to me", LABEL_D1_CHITCHAT),
    ("goodbye, talk to you later", LABEL_D1_CHITCHAT),
    ("bye bye!", LABEL_D1_CHITCHAT),

    # --- D1: Academic Stress, Emotional Support & Motivation ---
    ("I am feeling so stressed about my master's degree", LABEL_D1_CHITCHAT),
    ("I have too many exams next week and I feel overwhelmed", LABEL_D1_CHITCHAT),
    ("I have an assignment due tomorrow and I haven't started", LABEL_D1_CHITCHAT),
    ("the deadlines are piling up and I feel anxious", LABEL_D1_CHITCHAT),
    ("I feel really sad and down today", LABEL_D1_CHITCHAT),
    ("I am not feeling happy at all", LABEL_D1_CHITCHAT),
    ("I feel completely unmotivated to study", LABEL_D1_CHITCHAT),
    ("everything is too hard, I want to give up", LABEL_D1_CHITCHAT),
    ("can you give me some advice on how to improve?", LABEL_D1_CHITCHAT),
    ("why do I feel worried all the time?", LABEL_D1_CHITCHAT),
    ("how can I manage my study time better?", LABEL_D1_CHITCHAT),
    ("I need some words of encouragement", LABEL_D1_CHITCHAT),
    ("I failed my midterm exam", LABEL_D1_CHITCHAT),
    ("I'm feeling burnt out and exhausted from university", LABEL_D1_CHITCHAT),
    ("can you help me calm down?", LABEL_D1_CHITCHAT),
    ("I feel happy today because I finished my project", LABEL_D1_CHITCHAT),
    ("what should I do when I feel like giving up?", LABEL_D1_CHITCHAT),
    ("I'm worried I won't pass my final presentation", LABEL_D1_CHITCHAT),
    ("just feeling lonely and wanted someone to talk to", LABEL_D1_CHITCHAT),
    ("thanks for the positive vibes", LABEL_D1_CHITCHAT),

    # --- D2: James Webb Space Telescope (JWST) ---
    ("What instruments are onboard the James Webb Space Telescope?", LABEL_D2_NASA),
    ("How does NIRCam observe in the near-infrared spectrum?", LABEL_D2_NASA),
    ("Explain the cooling mechanism and temperature of the MIRI instrument", LABEL_D2_NASA),
    ("What are the beryllium mirror segment wavefront error tolerances at 40 Kelvin?", LABEL_D2_NASA),
    ("How does the JWST sunshield deploy at the Sun-Earth L2 Lagrange point?", LABEL_D2_NASA),
    ("What is the aperture diameter and collecting area of JWST?", LABEL_D2_NASA),
    ("Tell me about the Integrated Science Instrument Module ISIM", LABEL_D2_NASA),
    ("What detectors does NIRSpec use for multi-object spectroscopy?", LABEL_D2_NASA),

    # --- D2: Mars Exploration (Perseverance & Curiosity) ---
    ("What is the function of SHERLOC and WATSON on Perseverance?", LABEL_D2_NASA),
    ("How does ChemCam use laser-induced breakdown spectroscopy LIBS on Mars?", LABEL_D2_NASA),
    ("Describe the Entry, Descent, and Landing EDL sky-crane sequence for Curiosity", LABEL_D2_NASA),
    ("What biosignatures is Perseverance looking for in Jezero Crater?", LABEL_D2_NASA),
    ("What did the sedimentary rock samples in Jezero delta reveal?", LABEL_D2_NASA),
    ("What is the atmospheric entry speed and parachute deployment altitude for Mars rovers?", LABEL_D2_NASA),
    ("How does the PIXL instrument examine Martian petrology?", LABEL_D2_NASA),

    # --- D2: Ingenuity Mars Helicopter ---
    ("How does the Ingenuity helicopter generate lift in the thin Martian atmosphere?", LABEL_D2_NASA),
    ("What are the rotor blade dimensions and RPM of the Mars helicopter?", LABEL_D2_NASA),
    ("Explain the low Reynolds number aerodynamic regime on Mars", LABEL_D2_NASA),
    ("What structural analysis was conducted on the Mars Science Helicopter blades?", LABEL_D2_NASA),
    ("How do the counter-rotating carbon fiber blades provide yaw control?", LABEL_D2_NASA),

    # --- D2: Artemis Lunar Program & Space Launch System (SLS) ---
    ("What engines power the Space Launch System SLS core stage?", LABEL_D2_NASA),
    ("How did the RS-25 liquid hydrogen engines perform during Artemis I?", LABEL_D2_NASA),
    ("What were the telemetry results for the core stage propellant mixture valves?", LABEL_D2_NASA),
    ("What is the role of the Orion spacecraft in the Artemis lunar missions?", LABEL_D2_NASA),
    ("Explain the Human Landing System HLS lunar surface descent architecture", LABEL_D2_NASA),
    ("What volatile water ice prospecting is planned for the lunar South Pole?", LABEL_D2_NASA),

    # --- D2: Planetary Defense (DART) & Historic Spacecraft ---
    ("How did the DART kinetic impactor change the orbital period of Dimorphos?", LABEL_D2_NASA),
    ("What was the momentum enhancement factor beta measured from the DART impact?", LABEL_D2_NASA),
    ("How did the DRACO camera and SMART Nav guide DART to target Dimorphos?", LABEL_D2_NASA),
    ("What servicing missions were conducted on the Hubble Space Telescope?", LABEL_D2_NASA),
    ("What were the technical specifications of the Saturn V Apollo 11 AS-506 launch vehicle?", LABEL_D2_NASA),
]


# =============================================================================
# 2. Embedding Intent Classifier Engine
# =============================================================================

class SBERTRouterClassifier:
    """
    Semantic Intent Classifier powered by 'all-MiniLM-L6-v2' dense embeddings
    coupled with a calibrated linear classification head.
    """

    def __init__(self, model_name: str = EMBEDDING_MODEL_NAME):
        self.model_name = model_name
        print(f"[Router] Initializing SBERT encoder: '{model_name}'...")
        self.encoder = SentenceTransformer(model_name)
        self.classifier = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
        self.is_fitted = False

        # Class prototypes for geometric centroid distance
        self.centroid_d1: np.ndarray = None
        self.centroid_d2: np.ndarray = None

    def fit(self, training_data: List[Tuple[str, str]] = ROUTER_TRAINING_DATA):
        """
        Embeds training examples and fits the linear classifier head and centroids.
        """
        texts = [item[0] for item in training_data]
        labels = [1 if item[1] == LABEL_D2_NASA else 0 for item in training_data]

        print(f"[Router] Embedding {len(texts)} training utterances with {self.model_name}...")
        t0 = time.time()
        embeddings = self.encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        t_embed = time.time() - t0

        print(f"[Router] Fitting calibrated linear probe (Logistic Regression)...")
        self.classifier.fit(embeddings, labels)
        self.is_fitted = True

        # Pre-calculate normalized class centroids for geometric baseline
        emb_d1 = embeddings[[i for i, y in enumerate(labels) if y == 0]]
        emb_d2 = embeddings[[i for i, y in enumerate(labels) if y == 1]]
        self.centroid_d1 = np.mean(emb_d1, axis=0)
        self.centroid_d1 /= np.linalg.norm(self.centroid_d1)
        self.centroid_d2 = np.mean(emb_d2, axis=0)
        self.centroid_d2 /= np.linalg.norm(self.centroid_d2)

        print(f"[Router] Training complete in {t_embed:.2f}s! Classes: D1 ({len(emb_d1)}), D2 ({len(emb_d2)})")

    def save(self, filepath: Path = ROUTER_MODEL_PATH):
        """Serializes the classifier head and centroids to disk."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "classifier": self.classifier,
            "centroid_d1": self.centroid_d1,
            "centroid_d2": self.centroid_d2,
            "is_fitted": self.is_fitted,
            "model_name": self.model_name,
        }
        joblib.dump(payload, filepath)
        print(f"[Router] Model weights saved to: {filepath}")

    def load(self, filepath: Path = ROUTER_MODEL_PATH) -> bool:
        """Loads serialized classifier head from disk if available."""
        if not filepath.exists():
            return False
        try:
            payload = joblib.load(filepath)
            self.classifier = payload["classifier"]
            self.centroid_d1 = payload["centroid_d1"]
            self.centroid_d2 = payload["centroid_d2"]
            self.is_fitted = payload["is_fitted"]
            print(f"[Router] Loaded cached classifier from: {filepath}")
            return True
        except Exception as e:
            print(f"[Router Warning] Could not load cached model ({e}). Retraining...", file=sys.stderr)
            return False

    def predict_intent(self, text: str) -> Dict[str, Any]:
        """
        Embeds the input query and returns class probabilities and routing decision.
        """
        if not self.is_fitted:
            raise RuntimeError("Classifier is not fitted. Call fit() or load() first.")

        t0 = time.time()
        # Encode query to 384-dimensional unit vector
        query_vec = self.encoder.encode([text], convert_to_numpy=True, normalize_embeddings=True)
        
        # Linear probe calibrated probabilities
        probs = self.classifier.predict_proba(query_vec)[0]
        prob_d1 = float(probs[0])
        prob_d2 = float(probs[1])

        # Centroid cosine distances (Paradigm 2 comparison)
        cos_d1 = float(np.dot(query_vec[0], self.centroid_d1))
        cos_d2 = float(np.dot(query_vec[0], self.centroid_d2))

        inference_time_ms = (time.time() - t0) * 1000

        predicted_label = LABEL_D2_NASA if prob_d2 >= prob_d1 else LABEL_D1_CHITCHAT
        confidence = max(prob_d1, prob_d2)

        return {
            "query": text,
            "predicted_label": predicted_label,
            "confidence": confidence,
            "prob_d1_chitchat": prob_d1,
            "prob_d2_nasa": prob_d2,
            "cos_sim_d1": cos_d1,
            "cos_sim_d2": cos_d2,
            "latency_ms": inference_time_ms,
        }


# =============================================================================
# 3. Model Cross-Validation & Polysemy Stress-Testing
# =============================================================================

def run_classifier_cross_validation(training_data: List[Tuple[str, str]] = ROUTER_TRAINING_DATA):
    """
    Executes a 5-fold Stratified Cross-Validation on the router dataset
    and stress-tests polysemous edge cases ("mechanical stress" vs "exam stress").
    """
    print("\n" + "=" * 80)
    print("INTENT ROUTER EVALUATION: 5-FOLD STRATIFIED CROSS-VALIDATION")
    print("=" * 80)

    encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    texts = [item[0] for item in training_data]
    y = np.array([1 if item[1] == LABEL_D2_NASA else 0 for item in training_data])

    print(f"Vectorizing {len(texts)} samples with '{EMBEDDING_MODEL_NAME}'...")
    X = encoder.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    y_true_all = []
    y_pred_all = []

    fold = 1
    for train_idx, test_idx in skf.split(X, y):
        clf = LogisticRegression(C=1.0, max_iter=1000)
        clf.fit(X[train_idx], y[train_idx])
        preds = clf.predict(X[test_idx])
        acc = np.mean(preds == y[test_idx]) * 100
        print(f"  Fold {fold}: Accuracy = {acc:.1f}% ({len(test_idx)} test samples)")
        y_true_all.extend(y[test_idx])
        y_pred_all.extend(preds)
        fold += 1

    print("\n" + "-" * 80)
    print("CLASSIFICATION REPORT ACROSS ALL 5 FOLDS:")
    print("-" * 80)
    target_names = [f"D1 ({LABEL_D1_CHITCHAT})", f"D2 ({LABEL_D2_NASA})"]
    print(classification_report(y_true_all, y_pred_all, target_names=target_names, digits=3))

    cm = confusion_matrix(y_true_all, y_pred_all)
    print("CONFUSION MATRIX:")
    print(f"                Predicted D1    Predicted D2")
    print(f"  Actual D1:    {cm[0][0]:>12}    {cm[0][1]:>12}")
    print(f"  Actual D2:    {cm[1][0]:>12}    {cm[1][1]:>12}")

    # Stress testing tricky polysemy and edge cases
    print("\n" + "=" * 80)
    print("POLYSEMY & AMBIGUITY STRESS TESTS (THE 'STRESS' & 'WORK' PROBLEM)")
    print("=" * 80)

    # Train full model for demonstration
    router = SBERTRouterClassifier()
    router.fit(training_data)

    stress_test_cases = [
        # Ambiguous word "stress":
        ("I feel an immense amount of stress about my exams tomorrow", LABEL_D1_CHITCHAT),
        ("What aerodynamic stress does the rocket core stage experience at Max-Q?", LABEL_D2_NASA),
        # Ambiguous word "work":
        ("I need to work on my motivation and daily study habits", LABEL_D1_CHITCHAT),
        ("How does the ChemCam laser work on Mars soil targets?", LABEL_D2_NASA),
        # Ambiguous word "help":
        ("Can you help me feel less lonely today?", LABEL_D1_CHITCHAT),
        ("Can you help explain the cryogenic sunshield of the James Webb telescope?", LABEL_D2_NASA),
        # Out-of-domain / Conversational:
        ("Do you like pizza or coffee?", LABEL_D1_CHITCHAT),
        ("What is the Apollo 11 Saturn V thrust?", LABEL_D2_NASA),
    ]

    for utterance, expected in stress_test_cases:
        res = router.predict_intent(utterance)
        status = "PASSED" if res["predicted_label"] == expected else "FAILED"
        print(f"\nUtterance: \"{utterance}\"")
        print(f"  Expected:    {expected}")
        print(f"  Predicted:   {res['predicted_label']} (Confidence: {res['confidence']*100:.1f}%) | Latency: {res['latency_ms']:.2f}ms")
        print(f"  Status:      [{status}]")
    print("=" * 80)


# =============================================================================
# 4. Agent Handlers & Execution Routing
# =============================================================================

def handle_d1_request(user_input: str) -> Dict[str, Any]:
    """
    Executes Deliverable 1: The Optimist rule-based agent with spaCy pre-processing.
    Returns response string and sub-millisecond execution telemetry.
    """
    t0 = time.time()
    key_topics = extract_key_topics(user_input)
    lemmatized_input = lemmatize_text(user_input)

    clean_input = lemmatized_input.strip()
    while clean_input and clean_input[-1] in "!.?":
        clean_input = clean_input[:-1].strip()

    if not clean_input:
        response_text = "I am listening. What is on your mind today?"
    else:
        response_text = persona_chat.respond(clean_input)
        if response_text is None:
            response_text = generate_fallback_response(key_topics)

    latency_ms = (time.time() - t0) * 1000
    return {
        "agent": "D1 (The Optimist - Rule & spaCy Bot)",
        "response": response_text,
        "latency_ms": latency_ms,
        "citations": [],
    }


def handle_d2_request(user_input: str, chroma_collection, ollama_client, top_k: int = 8) -> Dict[str, Any]:
    """
    Executes Deliverable 2: Expert NASA RAG Agent with ChromaDB retrieval and Qwen2.5:7b.
    Returns grounded technical answer with citations and retrieval latency.
    """
    res = generate_rag_response(
        query=user_input,
        collection=chroma_collection,
        client=ollama_client,
        top_k=top_k
    )
    citations = extract_citations(res["answer"])
    return {
        "agent": "D2 (NASA Space Missions Expert RAG Agent)",
        "response": res["answer"],
        "latency_ms": res["total_latency"] * 1000,
        "citations": citations,
        "retrieved_chunks": len(res.get("retrieved_chunks", [])),
    }


# =============================================================================
# 5. Unified Conversational Assistant Orchestrator
# =============================================================================

class UnifiedConversationalAssistant:
    """
    Orchestrates the entire natural language interaction pipeline, integrating
    the SBERT router, D1 rule-based agent, and D2 expert RAG agent into a single
    seamless interface.
    """

    def __init__(self, threshold: float = DEFAULT_CONFIDENCE_THRESHOLD, force_retrain: bool = False):
        self.threshold = threshold
        self.router = SBERTRouterClassifier()

        # Initialize or train router classifier
        if force_retrain or not self.router.load(ROUTER_MODEL_PATH):
            self.router.fit(ROUTER_TRAINING_DATA)
            self.router.save(ROUTER_MODEL_PATH)

        # Lazy initialization for D2 RAG components
        print("\n[Unified Assistant] Connecting to ChromaDB vector store...")
        self.chroma_collection = build_or_load_vector_db()
        self.ollama_client = get_ollama_client()

    def process_message(self, user_query: str, top_k: int = 8) -> Dict[str, Any]:
        """
        Processes a user utterance through the classification router and dispatches
        to the appropriate deliverable.
        """
        # Step 1: Semantic Intent Classification
        routing_info = self.router.predict_intent(user_query)
        pred_label = routing_info["predicted_label"]
        confidence = routing_info["confidence"]

        # Step 2: Dispatch Logic
        if pred_label == LABEL_D1_CHITCHAT and confidence >= self.threshold:
            result = handle_d1_request(user_query)
            result["routed_to"] = "D1"
        elif pred_label == LABEL_D2_NASA and confidence >= self.threshold:
            result = handle_d2_request(user_query, self.chroma_collection, self.ollama_client, top_k=top_k)
            result["routed_to"] = "D2"
        else:
            # Ambiguity / Low-confidence fallback
            result = {
                "agent": "Router Disambiguation",
                "routed_to": "AMBIGUOUS",
                "response": (
                    "I noticed your question could relate to how you are feeling, or to NASA space exploration. "
                    "If you are looking for encouragement and support, I am here to chat! "
                    "Or if you have a technical question about NASA missions (JWST, Artemis, Mars, DART), "
                    "please specify and I will look up the technical reports for you."
                ),
                "latency_ms": routing_info["latency_ms"],
                "citations": [],
            }

        result["routing"] = routing_info
        return result


# =============================================================================
# 6. Interactive Unified Shell
# =============================================================================

def interactive_unified_shell(assistant: UnifiedConversationalAssistant):
    """
    Terminal loop demonstrating real-time classification routing and seamless
    hand-offs between Deliverable 1 and Deliverable 2.
    """
    banner = r"""
===============================================================================
       UNIVERSIDADE DE COIMBRA - NATURAL LANGUAGE INTERACTION (ILN)
             UNIFIED CONVERSATIONAL SYSTEM (D1 + D2 INTEGRATION)
===============================================================================
  • Router:   all-MiniLM-L6-v2 Semantic Embedding Linear Probe (< 10ms)
  • Agent 1:  D1 'The Optimist' (NLTK + spaCy Academic Well-being & Chit-Chat)
  • Agent 2:  D2 NASA Flagship RAG (ChromaDB 1,600 chunks + Ollama Qwen2.5:7b)
-------------------------------------------------------------------------------
Type any message: chat, share how you feel, or ask NASA technical questions.
Type 'eval' to run classifier cross-validation, or 'quit' / 'exit' to end.
===============================================================================
"""
    print(banner)

    while True:
        try:
            user_input = input("\nUser > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting unified assistant. Have a wonderful day!")
                break
            if user_input.lower() in ["eval", "evaluate", "test"]:
                run_classifier_cross_validation()
                continue

            print("[Thinking: Routing utterance through semantic classifier...]")
            res = assistant.process_message(user_input)

            routing = res["routing"]
            dest = res["routed_to"]
            conf = routing["confidence"] * 100
            r_lat = routing["latency_ms"]

            # Visual dispatch indicator
            print("\n" + "-" * 80)
            if dest == "D1":
                print(f"[ROUTER DISPATCH] -> D1: The Optimist (Well-being & Support)")
            elif dest == "D2":
                print(f"[ROUTER DISPATCH] -> D2: NASA Expert RAG (Technical Deep-Dive)")
            else:
                print(f"[ROUTER DISPATCH] -> AMBIGUOUS (Clarification Prompt)")
            print(f"                  Intent: {routing['predicted_label']} | Confidence: {conf:.1f}% | Routing Latency: {r_lat:.2f}ms")
            print("-" * 80)

            print(f"\n{res['agent']}:")
            print(res["response"])

            if res.get("citations"):
                print(f"\n[Attributed Citations ({len(res['citations'])}): {', '.join(res['citations'][:3])}]")
            print(f"[Total Response Latency: {res['latency_ms']:.2f}ms]")
            print("=" * 80)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting unified assistant. Goodbye!")
            break


# =============================================================================
# Main Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Unified NLP Assistant Router (D1 Rule Bot + D2 NASA RAG Agent)"
    )
    parser.add_argument(
        "--eval",
        action="store_true",
        help="Run 5-fold Stratified Cross-Validation on the router dataset",
    )
    parser.add_argument(
        "--retrain",
        action="store_true",
        help="Force re-embedding and re-training of the router classifier head",
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        default=None,
        help="Process a single utterance through the router and print dispatch decision",
    )
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=DEFAULT_CONFIDENCE_THRESHOLD,
        help=f"Confidence threshold for routing (default: {DEFAULT_CONFIDENCE_THRESHOLD})",
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=8,
        help="Top-k chunks to retrieve if routed to D2 (default: 8)",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch the interactive unified conversational shell",
    )

    args = parser.parse_args()

    if args.eval:
        run_classifier_cross_validation()
        return

    # Initialize the unified assistant
    assistant = UnifiedConversationalAssistant(threshold=args.threshold, force_retrain=args.retrain)

    if args.query:
        print(f"\n[Utterance]: \"{args.query}\"")
        res = assistant.process_message(args.query, top_k=args.top_k)
        routing = res["routing"]
        print(f"[Routing Decision]: Routed to {res['routed_to']} ({res['agent']})")
        print(f"                   Confidence: {routing['confidence']*100:.1f}% | Routing Latency: {routing['latency_ms']:.2f}ms")
        print(f"[Response]:\n{res['response']}")
        if res.get("citations"):
            print(f"[Citations]: {res['citations']}")
        return

    # Default action: launch interactive shell
    interactive_unified_shell(assistant)


if __name__ == "__main__":
    main()

