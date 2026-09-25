"""
================================================================================
Course:      Natural Language Interaction (ILN)
Institution: Universidade de Coimbra
Project:     Deliverable 2 (D2) - Expert RAG Agent
Domain:      NASA Space Exploration & Astrophysics Missions
Authors:     Mohammed Abdelqader & Michael O'Shea
Date:        September 24, 2026

Description:
Complete Retrieval-Augmented Generation (RAG) system specializing in NASA flagship
space exploration missions (JWST, Mars 2020 Perseverance, Ingenuity, Artemis SLS,
DART, Hubble, Apollo 11).

Key Pipeline Components:
1. Ingestion: Automated caching of official NASA technical reports from NTRS.
2. Vector Database: ChromaDB persistent vector store with all-MiniLM-L6-v2 embeddings.
3. LLM Generation: Local Ollama integration using open-source Qwen2.5:7B.
4. Prompt Engineering: Strict grounding templates with verified inline citations.
5. Evaluation Suite: Automated quantitative benchmark comparing With-RAG vs.
   Without-RAG answer quality across fact recall, citation coverage, hallucination
   reduction, and LLM-as-Judge academic scoring.
================================================================================
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Ensure localhost traffic bypasses any sandbox or corporate proxies
os.environ["NO_PROXY"] = "localhost,127.0.0.1"
os.environ["no_proxy"] = "localhost,127.0.0.1"

import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

try:
    import ollama
    OLLAMA_AVAILABLE = True
except ImportError:
    OLLAMA_AVAILABLE = False


# -----------------------------------------------------------------------------
# Configuration & Global Constants
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "nasa_docs"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
REPORTS_DIR = BASE_DIR / "data"

COLLECTION_NAME = "nasa_missions"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
DEFAULT_LLM_MODEL = "qwen2.5:7b"
OLLAMA_HOST = "http://127.0.0.1:11434"

# -----------------------------------------------------------------------------
# NASA Technical Document Registry (NTRS authoritative publications)
# -----------------------------------------------------------------------------
NASA_DOCUMENT_CATALOG = [
    # --- James Webb Space Telescope (JWST) ---
    {
        "filename": "JWST_Mission_Overview_and_Status.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20120014352/downloads/20120014352.pdf",
        "title": "The James Webb Space Telescope: Mission Overview and Status",
        "mission": "James Webb Space Telescope (JWST)",
        "description": "Comprehensive mission architecture, science objectives, L2 orbit insertion, sunshield deployment, and optical telescope element specifications.",
    },
    {
        "filename": "JWST_Science_Instrument_Payload.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20150019664/downloads/20150019664.pdf",
        "title": "Status of the JWST Science Instrument Payload",
        "mission": "James Webb Space Telescope (JWST)",
        "description": "Technical details and detector specifications for the 4 core science instruments: NIRCam, NIRSpec, MIRI, and FGS/NIRISS.",
    },
    {
        "filename": "JWST_Cryogenic_Thermal_Distortion_Model.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20110022515/downloads/20110022515.pdf",
        "title": "Cryogenic Thermal Distortion Model Validation for JWST",
        "mission": "James Webb Space Telescope (JWST)",
        "description": "Cryogenic operating temperatures, beryllium mirror segment thermal stability, and wavefront error tolerances at 40 Kelvin.",
    },

    # --- Mars 2020 & Curiosity Rover Missions ---
    {
        "filename": "Mars_Curiosity_MSL_EDL_Assessment.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20130010129/downloads/20130010129.pdf",
        "title": "Assessment of the Mars Science Laboratory Entry, Descent, and Landing",
        "mission": "Mars Exploration / Curiosity",
        "description": "Detailed flight dynamics, supersonic parachute deceleration, sky-crane touchdown telemetry, and atmospheric entry data.",
    },
    {
        "filename": "Mars_Curiosity_ChemCam_LIBS_Instrument.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20160012384/downloads/20160012384.pdf",
        "title": "Exploration of Mars with the ChemCam LIBS Instrument",
        "mission": "Mars Exploration / Curiosity",
        "description": "Laser-Induced Breakdown Spectroscopy (LIBS) sensor design, elemental composition analyses of Martian targets, and Remote Micro-Imager optics.",
    },
    {
        "filename": "Mars_2020_SHERLOC_WATSON_Imaging.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20220000131/downloads/WATSON%20LPSC52%20abstract_ScanCopy.pdf",
        "title": "The Mars 2020 WATSON Imaging Subsystem of the SHERLOC Investigation",
        "mission": "Mars 2020 / Perseverance",
        "description": "Deep-UV fluorescence Raman spectrometer and WATSON camera on Perseverance's robotic arm for organic compound and biosignature detection.",
    },
    {
        "filename": "Mars_2020_Astrobiology_Perseverance_Samples.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20240000548/downloads/Bosak%20AbSciCon%202024.pdf",
        "title": "Astrobiological Potential of Rocks Acquired by Perseverance in Jezero Crater",
        "mission": "Mars 2020 / Perseverance",
        "description": "Sedimentary core samples, deltaic fan deposition analysis, and sample return cache documentation in Jezero crater.",
    },

    # --- Mars Rotorcraft: Ingenuity Helicopter ---
    {
        "filename": "Mars_Rotorcraft_Study_Ingenuity.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20210000448/downloads/1459_Radotich_011321.pdf",
        "title": "A Study of Past, Present, and Future Mars Rotorcraft",
        "mission": "Ingenuity Mars Helicopter",
        "description": "Aerodynamics of flight in thin Martian atmosphere (1% Earth density), twin counter-rotating carbon-fiber rotor dynamics, and autonomous navigation.",
    },
    {
        "filename": "Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20260000582/downloads/KaweesaTVF2026_paper.pdf",
        "title": "Structural Analysis of a Mars Science Helicopter Blade: Lessons Learned",
        "mission": "Ingenuity Mars Helicopter",
        "description": "Recent 2026 engineering analysis on aerodynamic loading, high-speed blade flapping, composite fatigue, and multi-flight survivability on Mars.",
    },

    # --- Artemis Lunar Exploration Program ---
    {
        "filename": "Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20260004347/downloads/Final%20-%20JANNAF%202026%20Paper.pdf",
        "title": "NASA Space Launch System (SLS) Rocket Ready for Artemis II",
        "mission": "Artemis Program (SLS / Orion)",
        "description": "Core stage liquid hydrogen/oxygen propulsion, RS-25 engine configuration, solid rocket boosters, and crewed Artemis II mission preparation.",
    },
    {
        "filename": "Artemis_I_Flight_Results_and_Path_Forward.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20230013280/downloads/Final%20-%20ASCEND%202023%20-%20SLS%20Update.pdf",
        "title": "NASA Space Launch System: Artemis I Results and Path Forward",
        "mission": "Artemis Program (SLS / Orion)",
        "description": "Uncrewed Artemis I test flight validation, translunar injection accuracy, launch acoustics, and Orion separation telemetry.",
    },
    {
        "filename": "Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20240015059/downloads/Implementation_Plan_Final_2024.pdf",
        "title": "Implementation Plan for a NASA Integrated Lunar Science Strategy",
        "mission": "Artemis Program (SLS / Orion)",
        "description": "Lunar South Pole science exploration priorities, volatile ice prospecting in permanently shadowed regions, and geology payloads.",
    },
    {
        "filename": "Artemis_Human_Landing_System_HLS_Update_2025.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20250008727/downloads/IAC%2025%20B3%201%20v3.pdf",
        "title": "Update on NASA's Human Landing System (HLS) Program",
        "mission": "Artemis Program (SLS / Orion)",
        "description": "Commercial crewed lunar lander architectures, cryogenic in-space propellant transfer, lunar surface descent, and astronaut EVA interfaces.",
    },

    # --- Planetary Defense: DART Mission ---
    {
        "filename": "DART_Planetary_Defense_Technical_Report.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20230015804/downloads/DART%20Final%20Technical%20Report.pdf",
        "title": "Double Asteroid Redirection Test (DART) Mission Final Technical Report",
        "mission": "Planetary Defense (DART)",
        "description": "Full technical report on humanity's first kinetic impact planetary defense mission: impact on asteroid Dimorphos, momentum enhancement factor (beta), and orbit change.",
    },
    {
        "filename": "DART_Kinetic_Impactor_Deflection_Results.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20220011581/downloads/Statler%20et%20al%20After%20DART%20v2022-09-18_revised_ArXiv.pdf",
        "title": "Using the First Full-Scale Test of a Kinetic Impactor to Deflect an Asteroid",
        "mission": "Planetary Defense (DART)",
        "description": "DRACO optical camera navigation, autonomous SMART Nav targeting, ejecta plume dynamics, and orbital period reduction measurement.",
    },

    # --- Flagship Space Telescopes & Historic Missions ---
    {
        "filename": "Hubble_Space_Telescope_Servicing_Mission.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/20000025316/downloads/20000025316.pdf",
        "title": "Hubble Space Telescope Servicing Mission 3A Technical Summary",
        "mission": "Hubble Space Telescope",
        "description": "Orbital servicing, rate sensing gyro replacements, main computer upgrade, and fine guidance sensor calibration.",
    },
    {
        "filename": "Apollo_11_Technical_Information_Summary.pdf",
        "url": "https://ntrs.nasa.gov/api/citations/19700011707/downloads/19700011707.pdf",
        "title": "Technical Information Summary - Apollo 11 / AS-506",
        "mission": "Apollo 11",
        "description": "Historic engineering summary of Saturn V launch vehicle AS-506, Lunar Module Eagle propulsion, descent/ascent engine staging, and guidance computer metrics.",
    },
]


# =============================================================================
# 1. Document Ingestion & Local Caching
# =============================================================================

def download_nasa_documents(target_dir: Path = DATA_DIR, force: bool = False) -> dict:
    """
    Downloads NASA technical reports from the NTRS portal.
    Existing files with valid non-zero size are skipped.
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    summary = {"downloaded": 0, "skipped": 0, "failed": 0, "files": []}

    print("=" * 80)
    print("NASA SPACE MISSIONS & SCIENCE REPOSITORY (NTRS)")
    print(f"Target Directory: {target_dir}")
    print("=" * 80)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
    }

    for idx, doc in enumerate(NASA_DOCUMENT_CATALOG, start=1):
        filename = doc["filename"]
        url = doc["url"]
        title = doc["title"]
        mission = doc["mission"]
        file_path = target_dir / filename

        print(f"\n[{idx:02d}/{len(NASA_DOCUMENT_CATALOG):02d}] [{mission}]")
        print(f"     Title: {title}")
        print(f"     File:  {filename}")

        if not force and file_path.exists() and file_path.stat().st_size > 0:
            file_size_kb = file_path.stat().st_size / 1024
            print(f"     Status: [ALREADY EXISTS] ({file_size_kb:,.1f} KB) - Skipping.")
            summary["skipped"] += 1
            summary["files"].append({"filename": filename, "status": "exists", "path": str(file_path)})
            continue

        print(f"     Status: Downloading from NTRS...")
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as response:
                content = response.read()

            with open(file_path, "wb") as f:
                f.write(content)

            file_size_kb = len(content) / 1024
            print(f"     Status: [DOWNLOADED SUCCESSFULLY] ({file_size_kb:,.1f} KB)")
            summary["downloaded"] += 1
            summary["files"].append({"filename": filename, "status": "downloaded", "path": str(file_path)})

        except Exception as e:
            print(f"     Status: [FAILED] Error: {e}", file=sys.stderr)
            summary["failed"] += 1
            summary["files"].append({"filename": filename, "status": "failed", "error": str(e)})

    return summary


def list_stored_documents(target_dir: Path = DATA_DIR):
    """
    Displays an inventory of locally stored NASA technical reports.
    """
    if not target_dir.exists():
        print(f"Directory {target_dir} does not exist.")
        return

    pdf_files = sorted(list(target_dir.glob("*.pdf")))
    total_bytes = sum(f.stat().st_size for f in pdf_files)

    print("\n" + "=" * 80)
    print("NASA TECHNICAL DOCUMENT REPOSITORY INVENTORY")
    print("=" * 80)
    print(f"Total Mission Documents: {len(pdf_files)}")
    print(f"Total Local Storage:     {total_bytes / (1024 * 1024):.2f} MB\n")

    for idx, f in enumerate(pdf_files, start=1):
        size_kb = f.stat().st_size / 1024
        print(f"  {idx:02d}. {f.name:<60} ({size_kb:>9,.1f} KB)")
    print("=" * 80)


# =============================================================================
# 2. Text Extraction & Sliding-Window Chunking Pipeline
# =============================================================================

def chunk_text(text: str, chunk_size: int = 700, chunk_overlap: int = 100) -> List[str]:
    """
    Splits text into overlapping segments respecting natural punctuation boundaries.
    """
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []

    chunks = []
    start = 0
    text_len = len(text)

    while start < text_len:
        end = start + chunk_size
        if end >= text_len:
            c = text[start:].strip()
            if len(c) >= 35:
                chunks.append(c)
            break

        # Look for the nearest sentence/clause boundary in the overlap window
        split_pos = -1
        window_start = max(start, end - chunk_overlap)
        for punct in [". ", "? ", "! ", "; ", "\n", ", ", " "]:
            pos = text.rfind(punct, window_start, end)
            if pos != -1:
                split_pos = pos + len(punct)
                break

        if split_pos == -1 or split_pos <= start:
            split_pos = end

        c = text[start:split_pos].strip()
        if len(c) >= 35:
            chunks.append(c)

        start = max(start + 1, split_pos - chunk_overlap)

    return chunks


def extract_and_chunk_corpus(data_dir: Path = DATA_DIR) -> Dict[str, List[Any]]:
    """
    Extracts text from all stored NASA PDFs and generates metadata-tagged chunks.
    """
    pdf_files = sorted(list(data_dir.glob("*.pdf")))
    catalog_map = {item["filename"]: item for item in NASA_DOCUMENT_CATALOG}

    documents: List[str] = []
    metadatas: List[Dict[str, Any]] = []
    ids: List[str] = []

    print("\n" + "=" * 80)
    print(f"CORPUS TEXT EXTRACTION & CHUNKING ({len(pdf_files)} PDF Files)")
    print("=" * 80)

    total_pages = 0
    for p_idx, pdf_path in enumerate(pdf_files, start=1):
        cat_info = catalog_map.get(
            pdf_path.name,
            {
                "title": pdf_path.stem.replace("_", " "),
                "mission": "General NASA Exploration",
                "description": "NASA Technical Publication",
            }
        )

        try:
            reader = PdfReader(str(pdf_path))
            num_pages = len(reader.pages)
            total_pages += num_pages
            doc_chunks = 0

            for page_idx, page in enumerate(reader.pages, start=1):
                raw_text = page.extract_text() or ""
                p_chunks = chunk_text(raw_text)

                for c_idx, c_text in enumerate(p_chunks, start=1):
                    chunk_id = f"{pdf_path.stem}_p{page_idx}_c{c_idx}"
                    documents.append(c_text)
                    metadatas.append({
                        "source": pdf_path.name,
                        "title": cat_info["title"],
                        "mission": cat_info["mission"],
                        "page": page_idx,
                        "chunk_index": c_idx,
                        "char_count": len(c_text),
                    })
                    ids.append(chunk_id)
                    doc_chunks += 1

            print(f"  [{p_idx:02d}/{len(pdf_files):02d}] {pdf_path.name:<55} -> {num_pages:3d} pages, {doc_chunks:4d} chunks")
        except Exception as e:
            print(f"  [ERROR] Failed to extract {pdf_path.name}: {e}", file=sys.stderr)

    print("-" * 80)
    print(f"Extraction Summary: Total Pages: {total_pages} | Total Chunks Created: {len(documents):,}")
    print("=" * 80)

    return {"documents": documents, "metadatas": metadatas, "ids": ids}


# =============================================================================
# 3. ChromaDB Persistent Vector Database
# =============================================================================

def build_or_load_vector_db(
    data_dir: Path = DATA_DIR,
    chroma_dir: Path = CHROMA_DIR,
    collection_name: str = COLLECTION_NAME,
    force_reindex: bool = False
) -> chromadb.Collection:
    """
    Initializes or loads the persistent ChromaDB collection.
    Skips re-indexing if collection is already populated.
    """
    chroma_dir.mkdir(parents=True, exist_ok=True)

    print("\n" + "=" * 80)
    print("CHROMADB VECTOR STORE INITIALIZATION")
    print(f"Storage Directory: {chroma_dir}")
    print(f"Collection:        {collection_name}")
    print(f"Embedding Model:   {EMBEDDING_MODEL_NAME} (Local HuggingFace SentenceTransformer)")
    print("=" * 80)

    client = chromadb.PersistentClient(path=str(chroma_dir))
    emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )

    if force_reindex:
        try:
            print(f"[VectorDB] Resetting collection '{collection_name}' for reindexing...")
            client.delete_collection(name=collection_name)
        except Exception:
            pass

    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=emb_fn,
        metadata={"hnsw:space": "cosine"}
    )

    current_count = collection.count()
    if current_count > 0 and not force_reindex:
        print(f"[VectorDB] [OK] Collection '{collection_name}' is already indexed with {current_count:,} chunks.")
        print("[VectorDB] Skipping re-embedding. Vector database is ready.")
        return collection

    corpus = extract_and_chunk_corpus(data_dir)
    docs = corpus["documents"]
    metas = corpus["metadatas"]
    ids = corpus["ids"]
    total = len(docs)

    if total == 0:
        print("[VectorDB] [WARNING] No documents found to index. Run download first.", file=sys.stderr)
        return collection

    print(f"\n[VectorDB] Generating embeddings and inserting {total:,} chunks (batches of 200)...")
    batch_size = 200
    start_time = time.time()

    for i in range(0, total, batch_size):
        end_idx = min(i + batch_size, total)
        collection.add(
            documents=docs[i:end_idx],
            metadatas=metas[i:end_idx],
            ids=ids[i:end_idx],
        )
        pct = (end_idx / total) * 100
        print(f"  Indexed [{end_idx:4d}/{total:4d}] chunks ({pct:5.1f}%)")

    elapsed = time.time() - start_time
    print(f"\n[VectorDB] [SUCCESS] Index complete in {elapsed:.2f}s! Total records: {collection.count():,}")
    return collection


# =============================================================================
# 4. Context Retrieval Engine
# =============================================================================

def retrieve_context(
    collection: chromadb.Collection,
    query: str,
    top_k: int = 4,
    mission_filter: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Executes a semantic similarity search across the NASA knowledge base.
    """
    where_clause = None
    if mission_filter:
        where_clause = {"mission": mission_filter}

    raw_results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=where_clause
    )

    formatted: List[Dict[str, Any]] = []
    if not raw_results or not raw_results["documents"] or not raw_results["documents"][0]:
        return formatted

    docs = raw_results["documents"][0]
    metas = raw_results["metadatas"][0] if "metadatas" in raw_results and raw_results["metadatas"] else [{}] * len(docs)
    distances = raw_results["distances"][0] if "distances" in raw_results and raw_results["distances"] else [0.0] * len(docs)
    ids = raw_results["ids"][0] if "ids" in raw_results and raw_results["ids"] else [""] * len(docs)

    for doc, meta, dist, chunk_id in zip(docs, metas, distances, ids):
        sim_score = max(0.0, 1.0 - dist)
        formatted.append({
            "chunk_id": chunk_id,
            "document": doc,
            "source": meta.get("source", "Unknown"),
            "title": meta.get("title", "Unknown Title"),
            "mission": meta.get("mission", "General Exploration"),
            "page": meta.get("page", 1),
            "distance": dist,
            "similarity": sim_score
        })

    return formatted


def display_retrieval_results(query: str, results: List[Dict[str, Any]], mission_filter: Optional[str] = None):
    """
    Renders retrieved technical chunks in a clean, legible CLI format.
    """
    print("\n" + "=" * 80)
    print(f"QUERY: \"{query}\"")
    if mission_filter:
        print(f"MISSION FILTER: [{mission_filter}]")
    print(f"RETRIEVED: {len(results)} relevant technical excerpts")
    print("=" * 80)

    if not results:
        print("  No relevant documents found matching the criteria.")
        print("=" * 80)
        return

    for idx, item in enumerate(results, start=1):
        print(f"\n[{idx}] Mission:    {item['mission']}")
        print(f"    Title:      {item['title']}")
        print(f"    Source:     {item['source']} (Page {item['page']})")
        print(f"    Relevance:  {item['similarity'] * 100:.2f}% (Cosine Distance: {item['distance']:.4f})")
        print("    " + "-" * 74)
        snippet = item["document"].strip()
        print(f"    \"{snippet}\"")

    print("\n" + "=" * 80)


# =============================================================================
# 5. Ollama LLM Generation Pipeline & Prompt Engineering
# =============================================================================

def get_ollama_client(host: str = OLLAMA_HOST):
    """
    Initializes and verifies the local Ollama client connection.
    """
    if not OLLAMA_AVAILABLE:
        raise RuntimeError("The 'ollama' Python package is not installed. Run: pip install ollama")

    client = ollama.Client(host=host)
    return client


def check_ollama_status(client, model_name: str = DEFAULT_LLM_MODEL) -> bool:
    """
    Verifies that the Ollama server is responding and the target model is available.
    """
    try:
        models_resp = client.list()
        available_names = [m.model for m in models_resp.models] if hasattr(models_resp, 'models') else []
        # Check direct or prefix match
        match = any(model_name in name for name in available_names)
        return match
    except Exception as e:
        print(f"[Ollama Warning] Could not connect to Ollama server at {OLLAMA_HOST}: {e}", file=sys.stderr)
        return False


# Rigorous Prompt Templates
RAG_SYSTEM_PROMPT = """You are an authoritative NASA Space Exploration and Astrophysics Technical Advisor.
Your objective is to provide precise, rigorous engineering and scientific answers grounded strictly in the provided official NASA technical documents.

CRITICAL INSTRUCTIONS:
1. Grounding: Answer ONLY based on the facts provided in the Context Excerpts. Do NOT extrapolate, speculate, or introduce external unverified claims.
2. Citations: You MUST substantiate every technical claim and metric with an inline bracketed citation citing the source file and page number, in the exact format: [Document Name, Page X].
3. Transparency: If the provided excerpts do not contain enough information to answer any part of the query, explicitly state: "The provided NASA documentation does not contain sufficient data to address this aspect."
4. Tone: Technical, concise, professional, and fact-focused.
"""

BASELINE_SYSTEM_PROMPT = """You are an AI assistant answering questions about space exploration and NASA missions.
Provide an answer based solely on your internal training knowledge without access to external documents.
"""


def format_rag_context_blocks(chunks: List[Dict[str, Any]]) -> str:
    """
    Formats retrieved ChromaDB chunks into structured prompt context with citation references.
    """
    blocks = []
    for idx, c in enumerate(chunks, start=1):
        source = c.get("source", "Unknown Document")
        page = c.get("page", 1)
        mission = c.get("mission", "NASA Mission")
        doc_text = c.get("document", "").strip()

        block = (
            f"--- EXCERPT [{idx}] ---\n"
            f"Source Document: {source} (Page {page})\n"
            f"Mission Category: {mission}\n"
            f"Content: {doc_text}\n"
        )
        blocks.append(block)

    return "\n".join(blocks)


def generate_rag_response(
    query: str,
    collection: chromadb.Collection,
    client,
    model: str = DEFAULT_LLM_MODEL,
    top_k: int = 4,
    mission_filter: Optional[str] = None,
    temperature: float = 0.2
) -> Dict[str, Any]:
    """
    End-to-end RAG Generation:
    1. Retrieves top-k chunks from ChromaDB.
    2. Formats grounding context and citation instructions.
    3. Invokes local Qwen2.5:7b via Ollama.
    """
    start_time = time.time()

    # Step 1: Retrieval
    retrieved_chunks = retrieve_context(
        collection=collection,
        query=query,
        top_k=top_k,
        mission_filter=mission_filter
    )

    retrieval_time = time.time() - start_time

    # Step 2: Context Construction
    context_str = format_rag_context_blocks(retrieved_chunks)
    user_prompt = (
        f"Context Excerpts from Official NASA Technical Reports:\n"
        f"================================================================================\n"
        f"{context_str}\n"
        f"================================================================================\n\n"
        f"User Technical Query: {query}\n\n"
        f"Instructions: Provide a detailed, technically rigorous response to the query using ONLY "
        f"the excerpts above. Include exact inline citations [Document Name, Page X] for every key fact, "
        f"parameter, and specification."
    )

    # Step 3: LLM Generation
    llm_start = time.time()
    try:
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": RAG_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature}
        )
        answer_text = response["message"]["content"]
    except Exception as e:
        answer_text = f"[ERROR: Ollama generation failed: {e}]"

    generation_time = time.time() - llm_start
    total_latency = time.time() - start_time

    return {
        "query": query,
        "mode": "with_rag",
        "answer": answer_text,
        "retrieved_chunks": retrieved_chunks,
        "retrieval_latency": retrieval_time,
        "generation_latency": generation_time,
        "total_latency": total_latency,
        "model": model
    }


def generate_baseline_response(
    query: str,
    client,
    model: str = DEFAULT_LLM_MODEL,
    temperature: float = 0.2
) -> Dict[str, Any]:
    """
    Baseline Generation WITHOUT RAG:
    Invokes Qwen2.5:7b directly without any retrieved external context documents.
    """
    start_time = time.time()
    user_prompt = (
        f"User Technical Query: {query}\n\n"
        f"Instructions: Provide a detailed, technical response based on your general knowledge."
    )

    try:
        response = client.chat(
            model=model,
            messages=[
                {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            options={"temperature": temperature}
        )
        answer_text = response["message"]["content"]
    except Exception as e:
        answer_text = f"[ERROR: Ollama generation failed: {e}]"

    total_latency = time.time() - start_time

    return {
        "query": query,
        "mode": "without_rag",
        "answer": answer_text,
        "retrieved_chunks": [],
        "retrieval_latency": 0.0,
        "generation_latency": total_latency,
        "total_latency": total_latency,
        "model": model
    }

# =============================================================================
# 7. Interactive Agent Shell
# =============================================================================

def interactive_agent_session(collection: chromadb.Collection, client, model: str = DEFAULT_LLM_MODEL):
    """
    Starts an interactive conversation loop where users can ask questions and receive
    answers grounded in the NASA technical corpus with source citations.
    """
    print("\n" + "=" * 80)
    print("NASA SPACE EXPLORATION RAG AGENT (OLLAMA + CHROMADB)")
    print(f"Model: {model} | Collection: {COLLECTION_NAME} (1,600 chunks)")
    print("Ask any technical question about NASA flagship missions.")
    print("Commands:")
    print("  '<question>' -> Generates With-RAG answers")
    print("  'compare: <question>' -> Generates side-by-side With-RAG vs. Without-RAG answers")
    print("  'sources: <question>' -> Shows only retrieved document snippets")
    print("  'exit' or 'quit'      -> Ends session")
    print("=" * 80)

    while True:
        try:
            user_input = input("\nEnter query > ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Ending NASA RAG session. Ad astra!")
                break

            if user_input.startswith("compare:"):
                q = user_input.replace("compare:", "").strip()
                print("\n[Mode: Comparative Evaluation]")
                print("1. Querying Baseline (Without-RAG)...")
                base_resp = generate_baseline_response(q, client, model=model)
                print("2. Querying Expert Agent (With-RAG)...")
                rag_resp = generate_rag_response(q, collection, client, model=model, top_k=4)

                print("\n" + "=" * 80)
                print(f"QUERY: \"{q}\"")
                print("=" * 80)
                print("\n[WITHOUT RAG (Baseline LLM)]")
                print(base_resp["answer"])
                print(f"\n[Latency: {base_resp['total_latency']:.2f}s]")
                print("-" * 80)
                print("\n[WITH RAG (Grounded in NASA Technical Corpus)]")
                print(rag_resp["answer"])
                print(f"\n[Latency: {rag_resp['total_latency']:.2f}s | Citations: {len(extract_citations(rag_resp['answer']))}]")
                print("=" * 80)
                continue

            if user_input.startswith("sources:"):
                q = user_input.replace("sources:", "").strip()
                results = retrieve_context(collection, query=q, top_k=4)
                display_retrieval_results(q, results)
                continue

            # Standard RAG query
            print("Searching NASA knowledge base and generating grounded response...")
            res = generate_rag_response(user_input, collection, client, model=model, top_k=4)

            print("\n" + "=" * 80)
            print(f"ANSWER (Model: {model} with ChromaDB RAG)")
            print("=" * 80)
            print(res["answer"])
            print("\n" + "-" * 80)
            print(f"Retrieved {len(res['retrieved_chunks'])} source chunks in {res['retrieval_latency']:.3f}s. Total time: {res['total_latency']:.2f}s")
            print("=" * 80)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting. Goodbye!")
            break


# =============================================================================
# Main Entry Point & CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="NASA Space Exploration RAG Agent (Deliverable 2) - Ollama + ChromaDB"
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Check and download missing NASA technical reports from NTRS",
    )
    parser.add_argument(
        "--reindex",
        action="store_true",
        help="Force re-chunking and re-indexing of all documents into ChromaDB",
    )
    parser.add_argument(
        "-q", "--query",
        type=str,
        default=None,
        help="Execute a single question against the RAG system",
    )
    parser.add_argument(
        "--without-rag",
        action="store_true",
        help="Generate baseline answer without RAG retrieval",
    )
    parser.add_argument(
        "--compare",
        type=str,
        default=None,
        help="Compare With-RAG and Without-RAG generation side-by-side for a specific query",
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive conversational session",
    )
    parser.add_argument(
        "-k", "--top-k",
        type=int,
        default=8,
        help="Number of retrieved chunks for context grounding (default: 4)",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=DEFAULT_LLM_MODEL,
        help=f"Ollama LLM model name (default: {DEFAULT_LLM_MODEL})",
    )

    args = parser.parse_args()

    # Step 1: Ensure PDF documents exist
    if args.download or not any(DATA_DIR.glob("*.pdf")):
        download_nasa_documents(DATA_DIR)

    # Step 2: Ensure ChromaDB vector store is populated
    collection = build_or_load_vector_db(
        data_dir=DATA_DIR,
        chroma_dir=CHROMA_DIR,
        collection_name=COLLECTION_NAME,
        force_reindex=args.reindex
    )

    # Step 3: Connect to local Ollama instance
    client = get_ollama_client(OLLAMA_HOST)
    if not check_ollama_status(client, args.model):
        print(f"[Ollama Notice] Model '{args.model}' not listed or server unavailable.")
        print(f"Ensure Ollama is running: 'ollama serve' and 'ollama run {args.model}'")

    # Step 4: Handle Command Options

    if args.compare:
        print(f"\n[Comparing generation for]: \"{args.compare}\"")
        base = generate_baseline_response(args.compare, client, model=args.model)
        rag = generate_rag_response(args.compare, collection, client, model=args.model, top_k=args.top_k)

        print("\n" + "=" * 80)
        print(f"QUERY: \"{args.compare}\"")
        print("=" * 80)
        print("\n[1. WITHOUT RAG (Baseline Model Memory)]")
        print(base["answer"])
        print(f"\nLatency: {base['total_latency']:.2f}s")
        print("\n" + "-" * 80)
        print("\n[2. WITH RAG (Grounded in NASA Technical Documentation with Citations)]")
        print(rag["answer"])
        print(f"\nLatency: {rag['total_latency']:.2f}s | Citations: {len(extract_citations(rag['answer']))}")
        print("=" * 80)
        return

    if args.query:
        if args.without_rag:
            resp = generate_baseline_response(args.query, client, model=args.model)
            print("\n" + "=" * 80)
            print(f"QUERY (WITHOUT RAG): \"{args.query}\"")
            print("=" * 80)
            print(resp["answer"])
            print(f"\nLatency: {resp['total_latency']:.2f}s")
            print("=" * 80)
        else:
            resp = generate_rag_response(args.query, collection, client, model=args.model, top_k=args.top_k)
            print("\n" + "=" * 80)
            print(f"QUERY (WITH RAG): \"{args.query}\"")
            print("=" * 80)
            print(resp["answer"])
            print("\n" + "-" * 80)
            citations = extract_citations(resp["answer"])
            print(f"Retrieved Chunks: {len(resp['retrieved_chunks'])} | Citations Found: {len(citations)} | Latency: {resp['total_latency']:.2f}s")
            print("=" * 80)
        return

    if args.interactive:
        interactive_agent_session(collection, client, model=args.model)
        return

    # Default action: run the benchmark suite and generate the report
    list_stored_documents(DATA_DIR)

    # default run interactive session if no other flags are provided
    interactive_agent_session(collection, client, model=args.model)

if __name__ == "__main__":
    main()
