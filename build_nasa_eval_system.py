"""
Builds the NASA 20-Question Ground Truth Dataset and Annotation Guide
for RAG and Without-RAG Evaluation.

Files created:
1. nasa_eval_dataset.json   (Machine-readable ground truth dataset)
2. nasa_annotation_guide.md (Human annotation handbook)

Zero modifications to existing project files.
"""

import json
import sys
from pathlib import Path

# Ensure UTF-8 output on Windows
if sys.stdout is not None and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent

DATASET_QUESTIONS = [
    {
        "id": "NASA_Q01",
        "domain": "James Webb Space Telescope (JWST)",
        "subdomain": "Science Instrument Payload & Cryogenic Architecture",
        "primary_source": "JWST_Science_Instrument_Payload.pdf",
        "supporting_sources": ["JWST_Mission_Overview_and_Status.pdf", "JWST_Cryogenic_Thermal_Distortion_Model.pdf"],
        "source_pages": "Payload Overview pp. 1-12; Thermal Architecture pp. 3-8",
        "question": "What are the four core science instruments housed in the JWST Integrated Science Instrument Module (ISIM), what wavelength ranges do they observe, what detector technologies are used, and what are their cryogenic operating temperatures?",
        "ground_truth_answer": (
            "The James Webb Space Telescope (JWST) Integrated Science Instrument Module (ISIM) houses four core scientific instruments "
            "engineered for infrared astrophysics across the 0.6 to 28.5 micrometer (μm) spectral regime:\n\n"
            "1. **NIRCam (Near-Infrared Camera)**: Serves as the primary imager from 0.6 to 5.0 μm and the principal wavefront sensor for telescope alignment. "
            "It utilizes ten 2048x2048 pixel Teledyne mercury-cadmium-telluride (HgCdTe) HAWAII-2RG (H2RG) focal plane detector arrays. "
            "It operates at a passive cryogenic temperature of ~37 to 40 Kelvin (K), cooled by radiation into deep space via dedicated thermal radiators.\n\n"
            "2. **NIRSpec (Near-Infrared Spectrograph)**: Operates over 0.6 to 5.0 μm, featuring multi-object spectroscopy capable of observing >100 simultaneous "
            "astronomical targets using a Micro-Shutter Array (MSA) containing ~250,000 individually addressable micro-shutters. It employs two 2048x2048 "
            "Teledyne HgCdTe H2RG detectors and operates at passive cryogenic temperatures around 37 to 40 K.\n\n"
            "3. **MIRI (Mid-Infrared Instrument)**: Covers the mid-infrared band from 4.9 to 28.5 (or 28.8) μm with imaging, coronagraphy, and medium/low-resolution "
            "spectroscopy. Because thermal emissions from the telescope at 40 K overwhelm mid-IR signals, MIRI uses arsenic-doped silicon (Si:As) Impurity Band "
            "Conduction (IBC) detector arrays (three 1024x1024 pixel FPAs) and requires an active closed-cycle helium loop cryocooler (pulse tube and Joule-Thomson "
            "refrigeration) to operate at an ultra-cold temperature of ~6.4 to 7.0 K.\n\n"
            "4. **FGS/NIRISS (Fine Guidance Sensor / Near-Infrared Imager and Slitless Spectrograph)**: A shared opto-mechanical package containing the FGS "
            "(two 2048x2048 HgCdTe guide channels operating at 0.6-5.0 μm for sub-milliarcsecond pointing precision) and NIRISS (0.6 to 5.0 μm slitless spectroscopy "
            "and aperture masking interferometry for exoplanet transit characterization), also cooled passively to ~37 to 40 K."
        ),
        "ground_truth_facts": [
            "NIRCam", "NIRSpec", "MIRI", "FGS/NIRISS", "ISIM", "infrared",
            "HgCdTe", "HAWAII-2RG", "Si:As IBC", "passive cooling", "cryocooler",
            "micro-shutter array"
        ],
        "telemetry_metrics": [
            "0.6 to 28.5 um", "0.6 to 5.0 um", "37 K", "40 K", "6.4 K", "7 K", "2048x2048", "1024x1024"
        ],
        "expected_rag_behavior": (
            "Must cite JWST_Science_Instrument_Payload.pdf and JWST_Mission_Overview_and_Status.pdf, accurately distinguish passive cooling (~37-40 K) "
            "for NIRCam/NIRSpec/NIRISS from active helium cryocooler cooling (~6.4-7.0 K) for MIRI, and specify HgCdTe vs Si:As IBC detector architectures."
        ),
        "expected_no_rag_failure_modes": (
            "Non-RAG baseline models frequently state that all instruments run at the same temperature, confuse MIRI's active cryocooler with "
            "liquid cryogen boil-off (e.g. expendable helium like Spitzer), hallucinate incorrect wavelength cutoffs, or omit NIRISS."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: All 4 instruments, detector materials, and temperature ranges are 100% correct; 3: Minor error in temperature or detector tech; 1: Significant hallucinations or missing instruments.",
            "completeness": "5: Addresses all 4 instruments with wavelengths, detectors, and cooling mechanisms; 3: Mentions instruments but misses detector types or cooling; 1: Barely lists names.",
            "groundedness": "5: Accurately reflects document figures without extrapolation; 1: Completely fabricates operating parameters."
        }
    },
    {
        "id": "NASA_Q02",
        "domain": "James Webb Space Telescope (JWST)",
        "subdomain": "Cryogenic Thermal Distortion & Wavefront Control",
        "primary_source": "JWST_Cryogenic_Thermal_Distortion_Model.pdf",
        "supporting_sources": ["JWST_Mission_Overview_and_Status.pdf"],
        "source_pages": "Cryogenic Structural Modeling pp. 1-14; Finite Element Validation pp. 15-28",
        "question": "How does NASA model and compensate for the cryogenic thermal distortion of JWST's 18 primary mirror segments as they cool from room temperature to deep cryogenic operational temperatures (~35-50 K)?",
        "ground_truth_answer": (
            "NASA addressed the primary mirror cryogenic distortion through an integrated engineering pipeline combining high-fidelity "
            "structural/thermal finite element modeling (FEM), optical ray-tracing, and active wavefront sensing and control (WFS&C):\n\n"
            "1. **Beryllium Substrate Selection**: The 18 hexagonal Primary Mirror Segment Assemblies (PMSAs) are machined from optical-grade O-30 beryllium, "
            "chosen for its superior stiffness-to-weight ratio, structural stability, and nearly zero coefficient of thermal expansion (CTE) at cryogenic "
            "temperatures below 100 K.\n\n"
            "2. **Cryo-Null Figuring**: Because beryllium undergoes non-uniform volumetric shrinkage when cooled from ambient polishing temperatures (~293 K) "
            "to operational temperatures (~35-50 K), NASA modeled this cryogenic deformation using detailed Nastran/SigFit structural finite element models "
            "and validated them inside cryogenic test chambers (e.g., NASA Marshall X-Ray and Cryogenic Facility - XRCF). The mirrors were manufactured with "
            "an inverse 'cryo-null' surface figure at room temperature so that thermal contraction warped them into the exact required aspheric prescription on orbit.\n\n"
            "3. **Active Hexapod & Radius of Curvature Actuation**: Each of the 18 segments is mounted on a mechanical hexapod providing six degrees of "
            "freedom (rigid body piston, tip, tilt, clocking, and lateral translation) driven by cryogenic stepper motor actuators capable of nanometer-scale "
            "step resolution. Furthermore, a 7th actuator mechanism attached to the rear ribs controls the Radius of Curvature (RoC) of each segment to match "
            "focal lengths across all 18 segments.\n\n"
            "4. **Wavefront Sensing & Control (WFS&C)**: During commissioning, NIRCam phase retrieval algorithms measured optical path differences (OPD) to "
            "iteratively align and co-phase the segments into a single monolithic 6.5-meter wavefront with less than 50 nanometers RMS wavefront error."
        ),
        "ground_truth_facts": [
            "beryllium", "O-30", "Primary Mirror Segment Assembly (PMSA)", "18 segments", "cryo-null figuring",
            "coefficient of thermal expansion (CTE)", "hexapod actuators", "Radius of Curvature (RoC)",
            "Wavefront Sensing and Control (WFS&C)", "phase retrieval", "nanometer precision", "6.5-meter"
        ],
        "telemetry_metrics": [
            "18 segments", "6.5 m", "35 to 50 K", "293 K", "6 degrees of freedom", "7th actuator", "<50 nm RMS"
        ],
        "expected_rag_behavior": (
            "Must cite JWST_Cryogenic_Thermal_Distortion_Model.pdf, explain the beryllium O-30 substrate choice, describe room-temperature cryo-null "
            "pre-distortion figuring, and detail the 6-DOF hexapod plus 7th Radius-of-Curvature actuator."
        ),
        "expected_no_rag_failure_modes": (
            "Generic models fail to mention cryo-null pre-shaping, confuse beryllium with glass/Zerodur, or omit the 7th Radius of Curvature actuator mechanism."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Mentions beryllium, cryo-null figuring, hexapods, and RoC mechanism; 3: Discusses actuators generally without cryo-null or beryllium details; 1: Completely incorrect.",
            "completeness": "5: Covers material, pre-shaping modeling, active actuation, and optical validation; 3: Covers only post-launch actuation; 1: Vague description.",
            "groundedness": "5: Rigorously matches NASA thermal distortion modeling reports; 1: Fabricated mechanics."
        }
    },
    {
        "id": "NASA_Q03",
        "domain": "James Webb Space Telescope (JWST)",
        "subdomain": "Sunshield Thermal Isolation Architecture",
        "primary_source": "JWST_Mission_Overview_and_Status.pdf",
        "supporting_sources": ["JWST_Cryogenic_Thermal_Distortion_Model.pdf"],
        "source_pages": "Sunshield Subsystem pp. 45-62",
        "question": "What is the mechanical design, material composition, and thermal gradient performance of JWST's five-layer deployable sunshield?",
        "ground_truth_answer": (
            "JWST's five-layer sunshield is a passive thermal isolation system measuring approximately 21.2 meters by 14.2 meters (~69.5 ft by 46.5 ft, "
            "comparable to the footprint of a regulation tennis court), engineered to protect the observatory from solar, terrestrial, and lunar infrared radiation:\n\n"
            "1. **Layer Composition & Coatings**: All five membranes are fabricated from lightweight Kapton E polyimide film. Layer 1 (sun-facing) is 0.05 mm "
            "(50 μm / 2 mil) thick, while Layers 2 through 5 are 0.025 mm (25 μm / 1 mil) thick to minimize launch mass. Layer 1 is coated on the sun-facing "
            "surface with a 100 nm vapor-deposited aluminum layer topped by a 50 nm silicon-doped coating for high solar reflectivity, low solar absorptance, "
            "and electrical conductivity to mitigate electrostatic discharge. All subsequent layers and the back of Layer 1 are vapor-deposited aluminum (100 nm).\n\n"
            "2. **V-Groove Geometric Thermal Isolation**: The five layers are arranged in a flared, kite-shaped geometry separated by varying vacuum gaps forming "
            "V-grooves that taper outward. Heat radiated from Layer 1 into Layer 2 is primarily reflected and channeled out into the vacuum of deep space "
            "through the open perimeter gaps between layers, rather than conducting to Layer 3, 4, or 5.\n\n"
            "3. **Thermal Telemetry & Gradient**: The sunshield achieves an effective Sun Protection Factor (SPF) of >1,000,000, dropping incoming solar power "
            "from approximately 200–300 kilowatts down to a fraction of a milliwatt on the telescope side. Telemetry records:\n"
            "   - **Sun-Facing Side (Layer 1)**: Reaches peak temperatures of +85°C to +109°C (~358 K to 382 K).\n"
            "   - **Cold Side (Telescope / Layer 5)**: Drops passively to approximately -233°C to -238°C (~35 K to 40 K), creating an extreme thermal gradient "
            "of roughly 320 to 340 Kelvin across a distance of only a few feet."
        ),
        "ground_truth_facts": [
            "Kapton polyimide", "5 layers", "vapor-deposited aluminum", "doped silicon coating", "V-groove isolation",
            "tennis court size", "SPF > 1,000,000", "passive cooling", "electrostatic discharge"
        ],
        "telemetry_metrics": [
            "21.2 m x 14.2 m", "0.05 mm", "0.025 mm", "+85 C to +109 C", "-233 C to -238 C", "35 K to 40 K", "300 K gradient"
        ],
        "expected_rag_behavior": (
            "Must cite JWST_Mission_Overview_and_Status.pdf, specify Kapton polyimide material, the V-groove heat-rejection geometry, "
            "and cite exact telemetry numbers (+85°C to -233°C / ~35-40 K cold side)."
        ),
        "expected_no_rag_failure_modes": (
            "Hallucinates materials like Mylar or Kevlar, confuses the number of layers, or fails to provide the exact temperature gradient values."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Correct materials (Kapton, aluminum, silicon dopant), dimensions, and temperature gradients; 3: Misses coating details or layer thicknesses; 1: Inaccurate.",
            "completeness": "5: Thoroughly details materials, V-groove physics, and thermal telemetry; 3: High-level overview; 1: Superficial.",
            "groundedness": "5: Directly grounded in NASA technical specs; 1: Extrapolated or fabricated."
        }
    },
    {
        "id": "NASA_Q04",
        "domain": "Planetary Defense (DART)",
        "subdomain": "Kinetic Impactor Performance & Orbital Period Change",
        "primary_source": "DART_Planetary_Defense_Technical_Report.pdf",
        "supporting_sources": ["DART_Kinetic_Impactor_Deflection_Results.pdf"],
        "source_pages": "Executive Summary pp. 1-12; Impact Telemetry pp. 35-50",
        "question": "On what date and target did the Double Asteroid Redirection Test (DART) execute its kinetic impact, what was the pre-impact vs. post-impact orbital period of Dimorphos, and how did the measured change compare to NASA's minimum mission success criterion?",
        "ground_truth_answer": (
            "NASA's Double Asteroid Redirection Test (DART)—humanity's first planetary defense technology demonstration—targeted the near-Earth binary asteroid "
            "system (65803) Didymos:\n\n"
            "1. **Impact Execution & Target**: On **September 26, 2022, at 23:14 UTC**, the DART spacecraft (approximate impact mass ~570-580 kg) intentionally "
            "impacted **Dimorphos**, the smaller 160-meter secondary moonlet orbiting the 780-meter primary asteroid Didymos, at a relative closing velocity "
            "of approximately **6.14 km/s** (~13,700 mph / 22,100 km/h).\n\n"
            "2. **Orbital Period Change**: Prior to the kinetic impact, Dimorphos orbited Didymos with an established mutual orbital period of **11 hours, "
            "55 minutes, and 17 seconds (11.921 hours / ~715.3 minutes)**. Following the impact, extensive worldwide optical lightcurve observations and "
            "planetary radar measurements (Goldstone and Green Bank) confirmed the new orbital period was shortened to **11 hours, 22 minutes, and 37 seconds "
            "(~11.372 hours)**, representing a net orbital period reduction of **32.6 minutes (± 1.9 minutes)**, or approximately **33 minutes**.\n\n"
            "3. **Comparison with Mission Success Criterion**: NASA's pre-mission Level 1 Requirement defined the minimum success criterion as causing a "
            "change in the orbital period of at least **73 seconds (1 minute and 13 seconds)**. The actual measured reduction of ~32 to 33 minutes exceeded "
            "the minimum threshold by a factor of more than **25 times (over 2,500%)**, demonstrating the immense efficiency of kinetic impact deflection."
        ),
        "ground_truth_facts": [
            "September 26, 2022", "Dimorphos", "Didymos", "binary asteroid", "kinetic impact",
            "orbital period reduction", "73 seconds", "success criterion", "worldwide telescope network", "radar"
        ],
        "telemetry_metrics": [
            "6.14 km/s", "570 kg", "11 hours 55 minutes", "11 hours 22 minutes", "32.6 minutes", "33 minutes", "73 seconds", ">25x"
        ],
        "expected_rag_behavior": (
            "Must cite DART_Planetary_Defense_Technical_Report.pdf or DART_Kinetic_Impactor_Deflection_Results.pdf, provide the exact impact date "
            "(September 26, 2022), initial period (~11h 55m), final period (~11h 22m), delta (32-33 min), and the Level 1 success threshold (73 s)."
        ),
        "expected_no_rag_failure_modes": (
            "Commonly hallucinates the target as Didymos rather than Dimorphos, confuses the period change with asteroid travel velocity, "
            "or fails to recall the exact 73-second Level 1 requirement."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Exactly names Dimorphos, Sept 26 2022, 11h55m -> 11h22m, 32-33 min change, 73s threshold; 3: Minor precision gap; 1: Confuses asteroids or metrics.",
            "completeness": "5: Answers date, target, pre/post periods, delta, and success criterion; 3: Omits baseline period or criterion; 1: Incomplete.",
            "groundedness": "5: Fully verified against NASA DART reports; 1: Unsubstantiated."
        }
    },
    {
        "id": "NASA_Q05",
        "domain": "Planetary Defense (DART)",
        "subdomain": "Momentum Enhancement Factor (Beta) & Ejecta Dynamics",
        "primary_source": "DART_Planetary_Defense_Technical_Report.pdf",
        "supporting_sources": ["DART_Kinetic_Impactor_Deflection_Results.pdf"],
        "source_pages": "Momentum Transfer Analysis pp. 60-84; Ejecta Plume Evolution pp. 85-110",
        "question": "How is the momentum enhancement factor (beta, beta) defined and calculated for the DART impact on Dimorphos, and what physical role did cratering ejecta recoil play in the deflection?",
        "ground_truth_answer": (
            "The momentum enhancement factor, denoted by the Greek letter beta (β), quantifies the efficiency of momentum transfer in a hypervelocity "
            "kinetic impact:\n\n"
            "1. **Mathematical Formulation**: When an impactor of mass $m$ strikes an asteroid of mass $M$ at velocity $\\mathbf{v}_{imp}$, the total momentum "
            "imparted to the asteroid $\\Delta \\mathbf{P}$ consists of the direct momentum of the spacecraft plus the additional reaction force imparted by "
            "material ejected backwards into space:\n"
            "$$\\Delta \\mathbf{P} = m \\mathbf{v}_{imp} + \\mathbf{p}_{ejecta} = \\beta m \\mathbf{v}_{imp}$$\n"
            "Thus, $\\beta$ is defined as:\n"
            "$$\\beta = \\frac{\\Delta P}{m v_{imp}} = 1 + \\frac{p_{ejecta}}{m v_{imp}}$$\n"
            "   - If $\\beta = 1$: The impact is completely inelastic with zero ejecta recoil (pure momentum capture).\n"
            "   - If $\\beta > 1$: High-speed ejecta particles escaping opposite the impact direction act like a rocket thruster, boosting the deflection momentum.\n\n"
            "2. **Physical Role of Ejecta Recoil**: High-speed imagery from DART's DRACO camera, LICIACube, and the Hubble/Webb space telescopes revealed that "
            "the hypervelocity impact at 6.14 km/s blasted thousands of metric tons of shattered rocky debris and dust away from Dimorphos at speeds exceeding "
            "the asteroid's escape velocity (~9 cm/s). This fast-moving ejecta plume created an immense backward thrust (recoil impulse) that pushed Dimorphos "
            "significantly harder than the direct kinetic blow of the spacecraft alone.\n\n"
            "3. **Measured β Value**: Based on Dimorphos mass estimates derived from Didymos binary dynamics, NASA calculated that **$\\beta$ ranged between "
            "approximately 2.2 and 4.9** (nominal consensus $\\beta \\approx 3.6$ assuming bulk density ~2,400 kg/m³). This proves that ejecta recoil "
            "contributed more than double to triple the deflection momentum imparted by the spacecraft body itself, demonstrating that rubble-pile asteroids "
            "are exceptionally receptive to kinetic deflection."
        ),
        "ground_truth_facts": [
            "momentum enhancement factor", "beta (β)", "ejecta recoil", "momentum transfer",
            "inelastic collision", "reaction force", "rocket effect", "escape velocity",
            "rubble-pile asteroid", "DRACO", "LICIACube"
        ],
        "telemetry_metrics": [
            "beta = 1 + p_ejecta / (m*v)", "beta between 2.2 and 4.9", "nominal beta ~ 3.6", "6.14 km/s", "escape velocity ~9 cm/s"
        ],
        "expected_rag_behavior": (
            "Must cite DART_Planetary_Defense_Technical_Report.pdf, give the formula $\\Delta P = \\beta m v$, explain the rocket-like recoil impulse "
            "of back-blown ejecta, and cite the measured empirical range $\\beta \\approx 2.2$ to $4.9$ (nominal ~3.6)."
        ),
        "expected_no_rag_failure_modes": (
            "Fails to write or explain the beta formula, assumes beta cannot exceed 1.0 (violating momentum conservation if recoil is ignored), "
            "or hallucinates values like beta = 0.5 or beta = 100."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Clear equation, physical recoil explanation, and empirical range 2.2 to 4.9; 3: Explains ejecta concept but lacks math or exact range; 1: Conceptually invalid.",
            "completeness": "5: Covers definition, equation, physical mechanics, and numerical results; 3: Missing one key aspect; 1: Incomplete.",
            "groundedness": "5: Rigorously faithful to NASA kinetic impact physics; 1: Hallucinatory."
        }
    },
    {
        "id": "NASA_Q06",
        "domain": "Planetary Defense (DART)",
        "subdomain": "Autonomous Guidance & Optical Targeting (SMART Nav / DRACO)",
        "primary_source": "DART_Planetary_Defense_Technical_Report.pdf",
        "supporting_sources": ["DART_Kinetic_Impactor_Deflection_Results.pdf"],
        "source_pages": "Terminal Guidance pp. 15-34; DRACO Imaging pp. 95-115",
        "question": "How did the Small-body Maneuvering Autonomous Real-Time Navigation (SMART Nav) system and the DRACO optical imaging camera guide DART to target Dimorphos during the final hours before impact?",
        "ground_truth_answer": (
            "Because DART was approximately 11 million kilometers from Earth at impact, round-trip radio signal latency was approximately **38 to 40 seconds** "
            "(~19 seconds one-way). Ground controllers could not pilot the spacecraft in real-time. Instead, NASA employed an autonomous terminal navigation suite:\n\n"
            "1. **DRACO Imaging Sensor**: The Didymos Reconnaissance and Asteroid Camera for Optical navigation (DRACO) was a high-resolution Ritchey-Chrétien "
            "telescopic imager (20.8 cm aperture, f/12.6) with a 2048x2048 CMOS detector. It captured visible-light streaming frames of the Didymos system at "
            "up to 1 Hz during the terminal approach, providing optical data down to millimeters per pixel just seconds before impact.\n\n"
            "2. **SMART Nav Software Pipeline**: Developed by Johns Hopkins Applied Physics Laboratory (JPL/APL), SMART Nav ran directly on the spacecraft's "
            "radiation-hardened flight computer:\n"
            "   - **Detection & Centroiding (T-4 hours to T-1 hour)**: At 4 hours out, Didymos and Dimorphos appeared as a single unresolved sub-pixel point of light. "
            "SMART Nav performed scene segmentation, background suppression, and center-of-light tracking.\n"
            "   - **Target Discrimination (T-1 hour / ~60-90 minutes)**: At approximately 65 minutes before impact, Dimorphos resolved into a distinct point separated "
            "from Didymos by ~4 pixels. SMART Nav autonomously recognized Dimorphos based on orbital ephemeris models, rejected the much brighter Didymos parent asteroid, "
            "and shifted its guidance solution entirely to Dimorphos.\n"
            "   - **Terminal Precision Maneuvers (T-50 minutes to impact)**: SMART Nav fed line-of-sight pointing errors directly into the guidance, navigation, and "
            "control (GNC) thruster manager, firing 12 hydrazine reaction control system (RCS) thrusters in closed-loop pulses to steer the spacecraft to impact within "
            "17 meters of Dimorphos's center-of-figure."
        ),
        "ground_truth_facts": [
            "SMART Nav", "DRACO", "Didymos Reconnaissance and Asteroid Camera for Optical navigation",
            "autonomous guidance", "speed-of-light latency", "38 seconds round-trip", "closed-loop thrusters",
            "hydrazine RCS", "target discrimination", "centroiding", "center of figure"
        ],
        "telemetry_metrics": [
            "38-40 seconds latency", "11 million km", "2048x2048 CMOS", "T-4 hours", "T-60 to 90 min", "17 meters center-of-figure"
        ],
        "expected_rag_behavior": (
            "Must cite DART technical reports, explain why autonomy was mandatory due to speed-of-light delay (~38s round-trip), describe DRACO's optical characteristics, "
            "and detail the SMART Nav target discrimination step at ~60-90 minutes before impact."
        ),
        "expected_no_rag_failure_modes": (
            "Claims humans were joy-sticking the craft from Mission Control, invents radar/lidar guidance (DART had no lidar), or fails to explain how Dimorphos was separated from Didymos."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Accurately explains optical autonomy, DRACO, SMART Nav algorithms, time-delay necessity, and 65-min separation; 3: General description without optical specifics; 1: Completely wrong.",
            "completeness": "5: Covers sensor, latency, algorithms, and maneuver execution; 3: Omits hardware or timelines; 1: Minimal.",
            "groundedness": "5: Exact engineering match to NASA/APL DART reports; 1: Unsubstantiated."
        }
    },
    {
        "id": "NASA_Q07",
        "domain": "Mars Exploration (Curiosity MSL)",
        "subdomain": "Entry, Descent, and Landing (EDL) Architecture",
        "primary_source": "Mars_Curiosity_MSL_EDL_Assessment.pdf",
        "supporting_sources": ["Mars_Curiosity_ChemCam_LIBS_Instrument.pdf"],
        "source_pages": "EDL Architecture pp. 1-25; Sky Crane Maneuver pp. 45-70",
        "question": "What were the sequential phases of the Mars Science Laboratory (Curiosity) Entry, Descent, and Landing (EDL) architecture, and how did the Sky Crane maneuver execute the rover's surface touchdown?",
        "ground_truth_answer": (
            "Because the Mars Science Laboratory (Curiosity) weighed nearly 900 kg—far too massive for previous airbag landing systems—NASA engineered "
            "the groundbreaking 'Seven Minutes of Terror' Entry, Descent, and Landing (EDL) sequence consisting of four synchronized phases:\n\n"
            "1. **Guided Hypersonic Entry**: Entering the Martian atmosphere at ~5,900 m/s (~13,200 mph) at an altitude of ~125 km inside a 4.5-meter aeroshell, "
            "the craft ejected two 75-kg tungsten balance masses to offset its center of mass, generating an aerodynamic lift-to-drag ratio ($L/D \\approx 0.24$). "
            "Active RCS hydrazine thrusters performed bank-angle reversals to steer through Martian atmospheric density variations, reducing landing error "
            "from hundreds of kilometers to a 20x7 km landing ellipse.\n\n"
            "2. **Supersonic Parachute Deceleration**: At Mach ~2.05 (~405 m/s) and ~10 km altitude, the world's largest supersonic Disk-Gap-Band (DGB) parachute "
            "(21.5 meters diameter) deployed via mortar. Twenty seconds later, the ablative heat shield was pyrotechnically jettisoned, exposing the rover, "
            "its downward-looking cameras (MARDI), and the Terminal Descent Sensor (TDS) pulse-Doppler landing radar.\n\n"
            "3. **Powered Descent & Divert**: At ~1.8 km altitude and ~80 m/s, the rover and descent stage separated from the backshell and parachute. "
            "Eight throttleable Mars Landing Engines (MLE) running on hydrazine fired to execute an autonomous divert maneuver, flying hundreds of meters "
            "horizontally away from the falling backshell, then establishing a steady vertical descent rate of ~0.75 m/s (1.7 mph).\n\n"
            "4. **The Sky Crane Maneuver**: At an altitude of ~20 meters above the floor of Gale Crater, the descent stage engaged the Sky Crane:\n"
            "   - Three nylon-bridle cords and an electrical umbilical line unwound from a central spool, lowering the 899-kg rover 7.5 meters below the descent stage.\n"
            "   - Curiosity deployed its mobility system (six-wheel rocker-bogie chassis and wheels) in mid-air to act as landing gear.\n"
            "   - Upon ground touchdown, load sensors in the bridle slackened, triggering pyrotechnic guillotine cutters to sever all bridle cables in <0.5 seconds.\n"
            "   - The descent stage throttled up its MLE thrusters to 100%, executing a pitched flyaway climb to crash-land at a safe distance (>650 meters away)."
        ),
        "ground_truth_facts": [
            "Seven Minutes of Terror", "guided lifting entry", "tungsten ballast masses", "supersonic disk-gap-band parachute",
            "heat shield separation", "Terminal Descent Sensor (radar)", "powered descent stage", "Mars Landing Engines (MLE)",
            "Sky Crane", "bridle cables", "rocker-bogie deployment", "pyrotechnic guillotine cutters", "flyaway maneuver"
        ],
        "telemetry_metrics": [
            "5,900 m/s", "Mach 2.05", "21.5 m parachute", "1.8 km separation", "20 m altitude", "7.5 m bridle", "0.75 m/s touchdown", "899 kg"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_Curiosity_MSL_EDL_Assessment.pdf, outline all 4 EDL phases (guided entry, supersonic parachute, powered descent, Sky Crane), "
            "and detail the 7.5 m bridle lowering, weight-on-wheels trigger, guillotine severance, and flyaway burn."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses Curiosity with airbag landings (Pathfinder/MER), claims thrusters landed directly on the rover belly, or misses the guided entry and ballast ejection."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Masterfully describes all 4 phases, metrics, and Sky Crane touchdown mechanisms; 3: Mentions Sky Crane but omits guided entry or parachute details; 1: Confuses with airbags.",
            "completeness": "5: Complete technical sequence from atmospheric entry to flyaway; 3: Brief overview; 1: Minimal.",
            "groundedness": "5: Perfectly matches NASA MSL EDL assessment; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q08",
        "domain": "Mars Exploration (Curiosity MSL)",
        "subdomain": "ChemCam Remote Geochemical Sensing & LIBS Spectroscopy",
        "primary_source": "Mars_Curiosity_ChemCam_LIBS_Instrument.pdf",
        "supporting_sources": ["Mars_Curiosity_MSL_EDL_Assessment.pdf"],
        "source_pages": "LIBS Operational Principles pp. 1-18; Calibration & Spectra pp. 30-55",
        "question": "How does the ChemCam Laser-Induced Breakdown Spectroscopy (LIBS) instrument on Curiosity determine rock and soil elemental composition from standoff distances, and what complementary role does the Remote Micro-Imager (RMI) play?",
        "ground_truth_answer": (
            "ChemCam (Chemistry and Camera) is an active remote sensing package mounted on the mast of the Curiosity rover designed for rapid geochemical "
            "screening of targets without needing to position the robotic arm:\n\n"
            "1. **LIBS Physical Principles**: ChemCam uses a Q-switched Nd:KGW solid-state laser emitting pulses at **1067 nm** with pulse energy >30 mJ and "
            "pulse duration of ~5 nanoseconds. The laser beam is focused through a 110 mm Schmidt-Cassegrain telescope onto rock or soil surfaces at standoff "
            "distances of **1.5 to 7.0 meters**:\n"
            "   - Each pulse delivers power densities exceeding 10 megawatts per square millimeter ($>10^7 \\text{ W/mm}^2$), vaporizing sub-milligram amounts "
            "of target material and generating an expanding, luminous optical plasma breakdown spark.\n"
            "   - As the ionized plasma cools, excited atoms and ions de-excite, emitting photons at discrete, characteristic atomic emission wavelengths.\n\n"
            "2. **Spectrometer Subsystems**: Optical light from the plasma spark is collected by the telescope and directed via an optical fiber bundle "
            "down the mast to three spectrometers inside the rover body:\n"
            "   - **UV Spectrometer**: 240.1 to 342.2 nm (detects Fe, Mg, Ti, Cr, Ni, Al, Si).\n"
            "   - **VIS (Violet/Visible) Spectrometer**: 382.1 to 469.4 nm (detects Ca, Al, Fe, Ti, Sr, Ba).\n"
            "   - **VNIR (Near-Infrared) Spectrometer**: 474.0 to 853.2 nm (detects Na, K, O, H, Li, C, and emission continuum).\n"
            "By firing a train of ~30 to 50 laser pulses at a single spot (at 3 to 10 Hz), the initial pulses blast away superficial Martian dust, allowing "
            "subsequent pulses to measure the pristine, underlying rock composition.\n\n"
            "3. **Role of the Remote Micro-Imager (RMI)**: ChemCam incorporates the RMI, a high-resolution monochromatic camera sharing the same optical telescope. "
            "The RMI provides sub-millimeter contextual images of the laser impact pits (pit diameter ~0.3 to 0.5 mm at 3 meters), allowing scientists to tie "
            "exact elemental compositions to individual mineral grains, veins, and rock laminations."
        ),
        "ground_truth_facts": [
            "ChemCam", "LIBS (Laser-Induced Breakdown Spectroscopy)", "Nd:KGW laser", "1067 nm", "plasma spark",
            "atomic emission lines", "1.5 to 7.0 meters", "Remote Micro-Imager (RMI)", "three spectrometers",
            "UV, VIS, VNIR", "dust clearing pulses", "elemental composition (Si, Fe, Al, Mg, Ca, Na, K, H, O)"
        ],
        "telemetry_metrics": [
            "1067 nm", "1.5 to 7 meters", ">30 mJ", "5 nanoseconds", "240.1 to 853.2 nm", "30 to 50 pulses", "0.3 to 0.5 mm pit size"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, explain the plasma excitation mechanism, list the 3 spectrometer bands (UV, VIS, VNIR), "
            "the 1.5-7m standoff distance, the dust-clearing laser train, and RMI's context imaging role."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses LIBS with Raman spectroscopy or X-ray diffraction (CheMin), claims ChemCam requires contact with the rock, or omits RMI."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Perfect explanation of LIBS laser plasma, wavelength bands, 1.5-7m range, and RMI; 3: General laser spectroscopy explanation lacking specs; 1: Confuses with other instruments.",
            "completeness": "5: Details laser physics, 3 spectrometers, shot sequencing, and RMI imaging; 3: Misses spectrometers or RMI; 1: Minimal.",
            "groundedness": "5: Strictly faithful to ChemCam instrument technical report; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q09",
        "domain": "Mars 2020 (Perseverance)",
        "subdomain": "SHERLOC & WATSON Astrobiological Arm Instruments",
        "primary_source": "Mars_2020_SHERLOC_WATSON_Imaging.pdf",
        "supporting_sources": ["Mars_2020_Astrobiology_Perseverance_Samples.pdf"],
        "source_pages": "SHERLOC Instrument Architecture pp. 1-8; WATSON Optical Subsystem pp. 9-16",
        "question": "How do the SHERLOC deep-UV fluorescence and Raman spectrometer and the WATSON imaging sensor operate in tandem on Perseverance's robotic arm to detect organic compounds and potential biosignatures?",
        "ground_truth_answer": (
            "SHERLOC and WATSON are complementary optical instruments co-located on the 2-meter robotic arm turret of the Mars 2020 Perseverance rover, "
            "engineered for non-destructive spatial mapping of organic carbon and mineralogy at microscopic scales:\n\n"
            "1. **SHERLOC (Scanning Habitable Environments with Raman & Luminescence for Organics & Chemicals)**:\n"
            "   - **Deep-UV Laser Excitation**: Utilizes a miniature neon-copper (NeCu) pulsed hollow-cathode laser emitting at **248.6 nm** in the deep ultraviolet (DUV).\n"
            "   - **Dual Spectroscopic Detection**: Exciting samples in the deep-UV overcomes the fundamental limitation of visible Raman (where intense mineral "
            "fluorescence swamps weak Raman scattering):\n"
            "     * **Native Fluorescence**: Emitted at **270 to 360 nm**, detecting aromatic organic molecules (1-ring to 4-ring aromatic rings) with parts-per-billion sensitivity.\n"
            "     * **Resonance Raman Scattering**: Emitted at **800 to 4000 cm⁻¹** shift relative to the laser line, providing diagnostic vibrational "
            "fingerprints of key minerals (sulfates, carbonates, silicates) and aliphatic/aromatic organic functional groups.\n"
            "   - **Micro-Mapping**: A high-precision internal scanning mirror rasters the 100-μm laser beam across an 8x8 mm target area, creating correlated 2D geochemical maps.\n\n"
            "2. **WATSON (Wide Angle Topographic Sensor for Operations and e-Xploration)**:\n"
            "   - Built as a high-resolution color camera (a flight-spare heritage design based on Curiosity's MAHLI), WATSON provides micro-imaging down to "
            "**13 to 30 microns per pixel**.\n"
            "   - It features variable autofocus (operational from 18 mm to infinity) and white/UV LED illumination.\n\n"
            "3. **Tandem Co-Registration**: WATSON captures microscopic context images of abraded rock patches. SHERLOC's autofocus sensor co-aligns its laser spot "
            "directly onto WATSON's color images, allowing scientists to correlate organic detections directly with mineral grains, veins, and micro-fossils "
            "before deciding to drill a sample core."
        ),
        "ground_truth_facts": [
            "SHERLOC", "WATSON", "deep-UV laser", "248.6 nm", "NeCu laser", "native fluorescence", "resonance Raman",
            "aromatic compounds", "organic molecules", "MAHLI heritage", "robotic arm turret", "micro-mapping", "Jezero Crater"
        ],
        "telemetry_metrics": [
            "248.6 nm", "270 to 360 nm", "800 to 4000 cm^-1", "13 to 30 microns/pixel", "100 um spot size", "8x8 mm scan"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_2020_SHERLOC_WATSON_Imaging.pdf, explain the 248.6 nm deep-UV advantage in separating Raman from fluorescence, "
            "describe native fluorescence (270-360 nm) and Raman shift (800-4000 cm⁻¹), and explain WATSON's co-registered microscopic imaging."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses SHERLOC with APXS or ChemCam, invents a destructive drill-and-bake mechanism (confusing it with SAM/MOMA), or omits WATSON's role."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Perfect laser wavelength (248.6 nm), Raman/fluorescence bands, and WATSON specs; 3: Mentions Raman/fluorescence but misses DUV physics or WATSON; 1: Completely incorrect.",
            "completeness": "5: Covers both instruments, physical working mechanisms, and co-registration; 3: Covers only one instrument; 1: Inadequate.",
            "groundedness": "5: Strictly aligned with NASA Mars 2020 instrument documentation; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q10",
        "domain": "Mars 2020 (Perseverance)",
        "subdomain": "Rock Coring, Sample Hermetic Sealing & Sample Return Depot",
        "primary_source": "Mars_2020_Astrobiology_Perseverance_Samples.pdf",
        "supporting_sources": ["Mars_2020_SHERLOC_WATSON_Imaging.pdf"],
        "source_pages": "Sample Acquisition Architecture pp. 1-10",
        "question": "What mechanisms and protocols does the Mars 2020 Perseverance rover use to drill, hermetically seal, and cache rock core samples in Jezero Crater for future Earth retrieval?",
        "ground_truth_answer": (
            "Perseverance carries the most sophisticated robotic sample collection system ever flown into space, designed to gather pristine rock and regolith cores "
            "to be returned to Earth by the joint NASA-ESA Mars Sample Return (MSR) campaign:\n\n"
            "1. **Rotary-Percussive Coring Drill**: Mounted on the 45-kg turret at the end of the robotic arm, the coring drill utilizes hollow cylindrical drill bits "
            "pre-loaded with ultra-clean sample tubes. The drill exerts up to 40 kg of force and strikes at up to 3,000 impacts per minute while rotating, "
            "extracting solid rock cores approximately **13 mm (0.5 inches) in diameter** and **55 to 76 mm (2.2 to 3.0 inches) in length** directly into the internal tube.\n\n"
            "2. **Adaptive Caching Assembly (ACA)**: Inside the front belly of the rover sits a secondary robotic mechanism—the 0.5-meter Sample Handling Arm (SHA). "
            "The coring tube is transferred from the external turret into the belly, where automated inspection cameras assess sample volume, measure core length, "
            "and take high-resolution multi-angle photographs.\n\n"
            "3. **Hermetic Metal-to-Metal Seal**: Once verified, the tube is moved to a sealing station where an automated ram drives a titanium-sleeved plug into "
            "the tube opening under immense mechanical force, creating an ultra-tight, hermetic, knife-edge metal-to-metal seal to retain volatile compounds "
            "and prevent organic contamination for decades.\n\n"
            "4. **Caching Architecture & Three Forks Depot**: Perseverance carries **43 sample tubes** (including 5 'witness tubes' containing pre-conditioned filters "
            "to capture spacecraft outgassing and background contamination). In late 2022 / early 2023, Perseverance established the world's first extraterrestrial "
            "sample depot at **Three Forks** in Jezero Crater, safely depositing **10 duplicate sample tubes** onto the surface as a backup cache, while retaining "
            "the primary set inside the rover body for direct delivery to the MSR Sample Retrieval Lander."
        ),
        "ground_truth_facts": [
            "rotary-percussive drill", "titanium sample tubes", "Adaptive Caching Assembly (ACA)", "Sample Handling Arm (SHA)",
            "hermetic metal-to-metal seal", "knife-edge seal", "witness tubes", "Three Forks depot", "Mars Sample Return (MSR)",
            "Jezero Crater", "deltaic fan sediments"
        ],
        "telemetry_metrics": [
            "13 mm diameter", "55 to 76 mm length", "43 sample tubes", "5 witness tubes", "10 tubes at Three Forks", "MSR delivery"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_2020_Astrobiology_Perseverance_Samples.pdf, describe the rotary-percussive coring bit, the internal belly Sample Handling Arm, "
            "the hermetic metal-to-metal seal, the 43 total tubes (with 5 witness tubes), and the 10-tube backup cache at Three Forks."
        ),
        "expected_no_rag_failure_modes": (
            "States that Perseverance pulverizes rocks into powder like Curiosity (missing the intact solid core extraction), omits witness tubes, "
            "or hallucinates that samples are already on Earth."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Accurate dimensions (13x60mm), metal-to-metal seal, 43 tubes, witness tubes, and Three Forks depot; 3: Mentions drilling and sealing without specs; 1: Confuses with rover internal wet-chemistry.",
            "completeness": "5: Covers drilling, internal handling, hermetic sealing, witness controls, and caching depot; 3: Omits depot or witness tubes; 1: Incomplete.",
            "groundedness": "5: Fully verified against NASA Mars 2020 sample documentation; 1: Extrapolated."
        }
    },
    {
        "id": "NASA_Q11",
        "domain": "Mars Rotorcraft (Ingenuity)",
        "subdomain": "Rotorcraft Aerodynamics in Thin Atmosphere",
        "primary_source": "Mars_Rotorcraft_Study_Ingenuity.pdf",
        "supporting_sources": ["Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf"],
        "source_pages": "Martian Atmospheric Flight pp. 1-15; Aerodynamic Rotor Design pp. 16-35",
        "question": "How does the Ingenuity Mars Helicopter generate sufficient lift to fly in the thin Martian atmosphere, and what are its physical dimensions, rotor configuration, and rotor speed?",
        "ground_truth_answer": (
            "The Ingenuity Mars Helicopter achieved humanity's first powered, controlled aerodynamic flight on another planet by solving the extreme "
            "aerodynamic challenge of the Martian atmosphere:\n\n"
            "1. **Atmospheric Environment**: Mars has an atmospheric surface density of only **0.015 to 0.020 kg/m³**, which is **less than 1% (<0.8%) of Earth's "
            "sea-level air density** (equivalent to an altitude of ~100,000 feet / 30 km on Earth). While Martian gravity is only ~38% of Earth's (0.38g), "
            "generating aerodynamic lift requires aggressive rotor sizing and blade design operating in an ultra-low chord Reynolds number ($Re \\approx 10,000$ "
            "to $30,000$) combined with high compressibility (transonic tip Mach numbers).\n\n"
            "2. **Rotor Configuration & Geometry**:\n"
            "   - **Coaxial Counter-Rotating Configuration**: Ingenuity uses two counter-rotating two-bladed rotors stacked vertically on a coaxial mast, "
            "eliminating the need for a tail rotor (which saves critical weight and avoids tail gear transmission losses).\n"
            "   - **Rotor Diameter**: **1.21 meters (4.0 feet)** across tip-to-tip, with an overall vehicle height of 0.49 meters.\n"
            "   - **Blade Structure**: The four blades are custom-machined from ultra-stiff carbon-fiber-reinforced polymer composite with a syntactic foam core, "
            "engineered with high chord width and custom non-cambered/cambered low-Re airfoil profiles to delay boundary layer stall.\n\n"
            "3. **Rotor Speed & Power Metrics**:\n"
            "   - **Operating RPM**: Blades spin at nominal speeds of **2,400 to 2,700 RPM** (and up to **2,800 to 2,900 RPM** during seasonal Martian summer "
            "when rising temperatures cause atmospheric density to drop even further).\n"
            "   - **Tip Speed**: Blade tips move at approximately **Mach 0.70 to 0.75** (given the cold Martian speed of sound of ~240 m/s).\n"
            "   - **Vehicle Mass & Power**: Total mass is merely **1.8 kg (4.0 lbs)**. It is powered by six Sony lithium-ion cells delivering ~350 to 500 Watts "
            "of peak flight power, recharged by a mast-mounted solar panel."
        ),
        "ground_truth_facts": [
            "thin Martian atmosphere", "<1% Earth density", "low Reynolds number", "coaxial counter-rotating",
            "carbon-fiber composite", "1.21-meter rotor diameter", "2400 to 2700 RPM", "2800 RPM summer high-speed",
            "1.8 kg mass", "Mach 0.7 tip speed", "tail rotor elimination", "solar panel Li-ion"
        ],
        "telemetry_metrics": [
            "0.015-0.020 kg/m3", "1.21 m", "2,400 to 2,700 RPM", "up to 2,900 RPM", "1.8 kg", "Mach 0.75", "0.49 m height", "350-500 W"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_Rotorcraft_Study_Ingenuity.pdf, explain the thin atmosphere density (<1% Earth), coaxial counter-rotating dual rotors, "
            "exact rotor diameter (1.2m), RPM ranges (2400-2700 nominal, up to 2900 RPM summer), and total mass (1.8 kg)."
        ),
        "expected_no_rag_failure_modes": (
            "Quotes Earth helicopter RPM (~400-500 RPM, which would immediately crash on Mars), claims it has a tail rotor, or gives wildly incorrect mass figures."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Exactly captures 1.8 kg mass, 1.21 m diameter, coaxial counter-rotating blades, and 2400-2900 RPM; 3: Missing RPM or diameter; 1: Earth-like parameters.",
            "completeness": "5: Explains aerodynamics, physical dimensions, rotor geometry, RPM, and power; 3: High-level summary; 1: Inadequate.",
            "groundedness": "5: Strictly verified against NASA rotorcraft studies; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q12",
        "domain": "Mars Rotorcraft (Mars Science Helicopter)",
        "subdomain": "Rotor Blade Structural Dynamics & Composite Fatigue Analysis",
        "primary_source": "Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf",
        "supporting_sources": ["Mars_Rotorcraft_Study_Ingenuity.pdf"],
        "source_pages": "Structural Modeling pp. 1-14; Aeroelastic Flap-Lag Dynamics pp. 15-28",
        "question": "What are the key structural, aeroelastic, and modal considerations identified in the 2026 NASA structural analysis of next-generation Mars Science Helicopter (MSH) rotor blades compared to Ingenuity?",
        "ground_truth_answer": (
            "Following the extraordinary 72-flight campaign of Ingenuity (which ended in January 2024 when a blade tip struck the terrain), NASA Ames, JPL, "
            "and Langley conducted comprehensive structural, aeroelastic, and modal evaluations in 2026 to design blades for the next-generation **Mars Science "
            "Helicopter (MSH)**:\n\n"
            "1. **Scale and Science Payload Transition**: While Ingenuity was a 1.8-kg technology demonstrator carrying zero dedicated science payloads, "
            "MSH is designed as a larger 6-rotor hexacopter (or advanced multi-rotor) with vehicle mass of **20 to 30 kg**, capable of transporting **2 to 5 kg "
            "of scientific instruments** (spectral imagers, magnetometers, samplers) over distances of several kilometers per sortie.\n\n"
            "2. **Aeroelastic Flap-Lag Dynamics & Mach Regimes**: Because MSH rotor diameters expand to **~1.25 to 1.8 meters per rotor**, blade tip speeds "
            "operate continuously at high subsonic Mach numbers (**Mach 0.65 to 0.78**). At low Martian ambient pressures (~600 Pa), the lack of aerodynamic "
            "damping causes intense aeroelastic coupling between blade out-of-plane flapping, in-plane lead-lag motion, and torsional twisting.\n\n"
            "3. **Composite Laminate Tailoring & Stress Concentrations**: The 2026 analysis modeled carbon-fiber-reinforced polymer (CFRP) composite plies "
            "(high-modulus carbon/epoxy layups). It identified critical interlaminar shear stresses and stress concentrations at the blade root retention clevis "
            "and transitions between the structural spar and aerodynamic skin. NASA optimized ply drop-offs and fiber orientations ([0/±45/90] balanced symmetric "
            "layups) to shift fundamental flap and torsion modal frequencies away from the integer harmonics of the rotor rotational frequency ($1/rev, 2/rev, 3/rev$), "
            "preventing destructive ground resonance and aeroelastic flutter.\n\n"
            "4. **Fatigue Endurance & Dust Erosion**: Long-duration mission survivability (>100 flights) requires fatigue design limits below the composite micro-cracking "
            "threshold under cyclic aerodynamic loading. Furthermore, high-velocity blade-tip impacts with abrasive Martian airborne dust require leading-edge "
            "abrasion protection caps (nickel or titanium leading-edge erosion sheaths) to prevent delamination of the carbon plies."
        ),
        "ground_truth_facts": [
            "Mars Science Helicopter (MSH)", "hexacopter / multi-rotor", "2 to 5 kg science payload",
            "aeroelastic flapping and lead-lag", "Mach 0.65 to 0.78 tip speed", "aerodynamic damping deficiency",
            "CFRP composite laminates", "modal frequency placement", "flutter avoidance", "dust erosion protection",
            "Ingenuity lessons learned"
        ],
        "telemetry_metrics": [
            "20 to 30 kg vehicle mass", "2 to 5 kg payload", "1.25 to 1.8 m rotor diameter", "Mach 0.65-0.78", "low damping (600 Pa)"
        ],
        "expected_rag_behavior": (
            "Must cite Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, distinguish MSH (20-30 kg, 2-5 kg science payload) from Ingenuity (1.8 kg), "
            "explain aeroelastic flap-lag coupling due to low Martian aerodynamic damping, composite laminate stress concentrations, and leading-edge dust erosion."
        ),
        "expected_no_rag_failure_modes": (
            "Unaware of the 2026 MSH study, repeats Ingenuity's baseline specs, or invents standard metal helicopter designs with traditional Earth mechanical hinges."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Accurately articulates MSH multi-rotor configuration, 2-5kg payload, aeroelastic flap-lag physics, and composite analysis; 3: Mentions bigger helicopter without structural/modal details; 1: Inaccurate.",
            "completeness": "5: Thoroughly addresses aeroelasticity, modal frequencies, composite layup, and erosion; 3: Partial coverage; 1: Superficial.",
            "groundedness": "5: Directly reflects 2026 NASA technical paper; 1: Extrapolated."
        }
    },
    {
        "id": "NASA_Q13",
        "domain": "Artemis Program (SLS / Orion)",
        "subdomain": "Space Launch System Core Stage Propulsion Architecture",
        "primary_source": "Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf",
        "supporting_sources": ["Artemis_I_Flight_Results_and_Path_Forward.pdf"],
        "source_pages": "Core Stage Propulsion pp. 1-18; RS-25 Engine Configuration pp. 22-40",
        "question": "What propulsion architecture powers the Space Launch System (SLS) Core Stage, what are the propellants and cryogenic temperatures, and how do the RS-25 engines and Solid Rocket Boosters combine at liftoff?",
        "ground_truth_answer": (
            "The NASA Space Launch System (SLS) Core Stage—the structural and propulsive backbone of the Artemis lunar exploration vehicle—measures "
            "**212 feet (64.6 meters) in height** and **27.6 feet (8.4 meters) in diameter**:\n\n"
            "1. **Propellant Volumes & Cryogenics**: The Core Stage contains two colossal insulated aluminum-lithium tanks holding a combined total of "
            "**733,000 gallons (2.77 million liters / ~2.3 million pounds)** of cryogenic propellants:\n"
            "   - **Liquid Hydrogen (LH₂)**: 537,000 gallons stored in the forward tank at an ultra-deep cryogenic temperature of **-423°F (20.3 Kelvin)**.\n"
            "   - **Liquid Oxygen (LOX)**: 196,000 gallons stored in the aft tank at **-297°F (90.2 Kelvin)**.\n\n"
            "2. **RS-25 Engine Configuration**: The Core Stage is powered by **four Aerojet Rocketdyne RS-25D/E engines** arranged in a square cross-pattern "
            "in the engine section. The RS-25 operates on a staged-combustion cycle with high chamber pressures (~3,000 psia):\n"
            "   - For SLS Block 1 (Artemis I and II), the engines operate at **109% of their original Space Shuttle Rated Power Level (RPL)**, producing "
            "approximately **512,000 pounds-force (2.28 MN) of vacuum thrust each**, yielding a combined Core Stage vacuum thrust of over **2.0 million lbf (9.1 MN)**.\n"
            "   - The four engines burn continuously for approximately **8 minutes and 20 seconds (500 seconds)** during ascent.\n\n"
            "3. **Combined Liftoff Thrust with Twin Solid Rocket Boosters (SRBs)**:\n"
            "   - Mounted on either side of the Core Stage are **two five-segment Solid Rocket Boosters (SRBs)**—the largest solid-propellant motors ever flown, "
            "burning Polybutadiene Acrylonitrile (PBAN) ammonium perchlorate composite propellant.\n"
            "   - Each SRB delivers **3.6 million lbf (16.0 MN)** of maximum thrust at liftoff.\n"
            "   - At liftoff, the four RS-25 engines (~1.6 million lbf sea-level thrust) and the twin SRBs (7.2 million lbf) ignite simultaneously to generate a "
            "staggering **8.8 million pounds-force (39.1 MN) of total liftoff thrust**—15% more thrust than the Apollo Saturn V."
        ),
        "ground_truth_facts": [
            "SLS Core Stage", "four RS-25 engines", "liquid hydrogen (LH2)", "liquid oxygen (LOX)", "twin five-segment SRBs",
            "733,000 gallons", "109% Rated Power Level (RPL)", "8.8 million lbf liftoff thrust", "staged combustion cycle",
            "212 feet height", "aluminum-lithium tanks"
        ],
        "telemetry_metrics": [
            "733,000 gallons", "-423 F (20 K)", "-297 F (90 K)", "4x RS-25", "109% RPL", "2.0 million lbf Core Stage",
            "3.6 million lbf per SRB", "8.8 million lbf total liftoff thrust", "500 seconds burn"
        ],
        "expected_rag_behavior": (
            "Must cite Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf, detail the 4 RS-25 engines, cryogenic LH2/LOX temperatures (-423°F / -297°F), "
            "the 733,000 gallons volume, 109% RPL throttle, and combine the twin 5-segment SRBs to yield 8.8 million lbf liftoff thrust."
        ),
        "expected_no_rag_failure_modes": (
            "States that SLS uses 3 engines (confusing with Shuttle), confuses propellants with RP-1/kerosene, or hallucinates thrust numbers below Saturn V."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Flawless figures (4 RS-25s, 109%, 733k gal, -423°F/-297°F, twin SRBs, 8.8M lbf); 3: General description with minor numerical errors; 1: Inaccurate engines or fuels.",
            "completeness": "5: Thoroughly addresses propellant chemistry, cryogenic temps, engine specs, and booster summation; 3: Leaves out boosters or temps; 1: Brief.",
            "groundedness": "5: Exactly matches NASA SLS technical papers; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q14",
        "domain": "Artemis Program (SLS / Orion)",
        "subdomain": "Artemis I Flight Telemetry & Translunar Injection Validation",
        "primary_source": "Artemis_I_Flight_Results_and_Path_Forward.pdf",
        "supporting_sources": ["Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf"],
        "source_pages": "Artemis I Telemetry Results pp. 1-15; Trajectory & Reentry pp. 20-35",
        "question": "What were the key flight performance metrics, translunar injection parameters, and reentry results recorded during the uncrewed Artemis I test flight of SLS and Orion?",
        "ground_truth_answer": (
            "Launched on **November 16, 2022, at 1:47 a.m. EST**, the uncrewed Artemis I mission executed a flawless 25.5-day flight demonstrating the end-to-end "
            "integration of the SLS rocket, Orion spacecraft, and Exploration Ground Systems:\n\n"
            "1. **Core Stage & ICPS Insertion Performance**:\n"
            "   - The SLS Core Stage burned for 500 seconds, inserting the Interim Cryogenic Propulsion Stage (ICPS) and Orion into an initial 972x16 nautical mile "
            "insertion orbit within **0.1% of target trajectory velocity**.\n"
            "   - After an initial perigee raise maneuver, the ICPS (powered by a single Aerojet Rocketdyne RL10B-2 engine burning LH₂/LOX) executed the critical "
            "**Translunar Injection (TLI) burn** lasting approximately **18 minutes**. The burn added **~2,800 m/s (~9,200 ft/s / 6,260 mph)** of velocity, "
            "placing Orion onto a precision lunar transfer trajectory with a targeting error of **less than 0.05%**.\n\n"
            "2. **Distant Retrograde Orbit (DRO) Telemetry**:\n"
            "   - Orion entered a high-altitude Distant Retrograde Orbit around the Moon, using gravity-assist burns (Outbound Powered Flyby within 81 miles of the lunar surface).\n"
            "   - On November 28, 2022, Orion reached its maximum distance from Earth at **268,563 miles (432,210 km)**—breaking the record set by Apollo 13 "
            "for the farthest distance traveled by any human-rated spacecraft from Earth.\n\n"
            "3. **Skip Reentry & Heat Shield Performance**:\n"
            "   - Returning directly from lunar distance, Orion demonstrated a historic **skip-entry technique**, dipping into the upper atmosphere, skipping back up "
            "to bleed off energy and precisely control touchdown location, before performing final descent.\n"
            "   - **Reentry Velocity**: **39,400 km/h (24,500 mph / ~11 km/s / Mach 32)**.\n"
            "   - **Ablative Thermal Protection**: The 5.0-meter Avcoat ablative heat shield endured temperatures of **nearly 5,000°F (~2,760°C)**. Post-flight "
            "inspection revealed unexpected liberation (spalling/char loss) of small Avcoat material fragments, prompting extensive root-cause investigation "
            "prior to the crewed Artemis II flight.\n"
            "   - Orion splashed down safely in the Pacific Ocean off Baja California on **December 11, 2022, after traveling 1.4 million miles**."
        ),
        "ground_truth_facts": [
            "November 16, 2022", "December 11, 2022", "25.5-day flight", "Interim Cryogenic Propulsion Stage (ICPS)",
            "RL10B-2 engine", "Translunar Injection (TLI)", "Distant Retrograde Orbit (DRO)", "268,563 miles record distance",
            "skip-entry maneuver", "Mach 32 / 24,500 mph", "Avcoat heat shield char loss", "Pacific Ocean splashdown"
        ],
        "telemetry_metrics": [
            "25.5 days", "2,800 m/s TLI delta-v", "268,563 miles", "24,500 mph (Mach 32)", "5,000 F (2,760 C)", "0.05% trajectory accuracy"
        ],
        "expected_rag_behavior": (
            "Must cite Artemis_I_Flight_Results_and_Path_Forward.pdf, include mission dates (Nov 16 - Dec 11, 2022), ICPS TLI burn delta-v (~2,800 m/s), "
            "Orion max distance (268,563 miles), skip-entry aerodynamics, Mach 32 reentry, and Avcoat heat shield phenomena."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses Artemis I with Artemis II (claiming astronauts were aboard), hallucinates standard low-Earth-orbit reentry speed (Mach 25 instead of Mach 32), "
            "or misses the Avcoat investigation finding."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Exact mission dates, TLI telemetry, DRO record distance (268,563 mi), and skip-entry Avcoat details; 3: Omits TLI delta-v or Avcoat findings; 1: Significant errors.",
            "completeness": "5: Thoroughly addresses launch insertion, TLI, DRO trajectory, and reentry; 3: Focuses only on launch; 1: Inadequate.",
            "groundedness": "5: Verifiable against NASA flight results report; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q15",
        "domain": "Artemis Program (Lunar Science)",
        "subdomain": "Lunar South Pole Strategy & Permanently Shadowed Regions",
        "primary_source": "Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf",
        "supporting_sources": ["Artemis_Human_Landing_System_HLS_Update_2025.pdf"],
        "source_pages": "Science Objectives pp. 1-24; South Pole Geological Environments pp. 45-72",
        "question": "What are the primary scientific exploration objectives and target geological environments defined in NASA's Integrated Lunar Science Strategy for Artemis surface missions at the Lunar South Pole?",
        "ground_truth_answer": (
            "NASA's Integrated Lunar Science Strategy shifts lunar exploration from the equatorial basaltic plains explored during Apollo to the rugged, "
            "ancient terrains of the **Lunar South Pole** (centered around craters such as Shackleton, Haworth, Shoemaker, and Faustini inside the ancient "
            "South Pole-Aitken Basin):\n\n"
            "1. **Permanently Shadowed Regions (PSRs) & Cryogenic Cold Traps**:\n"
            "   - Because the Moon has an axial tilt of only **1.54°**, the rim of deep impact craters casts permanent shadows where sunlight has not shone "
            "for over two billion years.\n"
            "   - **Thermal Telemetry**: Temperatures inside PSRs plunge passively to **25 to 40 Kelvin (-415°F to -388°F)**—substantially colder than the surface "
            "of Pluto. These extreme cryogenic conditions create stable 'cold traps' that preserve water ice ($H_2O$), hydroxyls, carbon monoxide ($CO$), methane "
            "($CH_4$), ammonia ($NH_3$), and other volatile species delivered by cometary and asteroidal impacts over solar system history.\n\n"
            "2. **Primary Science Objectives**:\n"
            "   - **Planetary Volatile Chronology**: Drill, excavate, and cryogenically return core samples of PSR regolith to establish the provenance, isotopic "
            "ratios (D/H ratios), and historical delivery mechanisms of water and organics to the Earth-Moon system.\n"
            "   - **In-Situ Resource Utilization (ISRU) Ground-Truthing**: Quantify the depth, lateral distribution, physical state (granular ice crystals vs. "
            "cemented regolith ice permafrost), and concentration (estimated 5 to 10+ weight percent) of water ice to support future rocket propellant production "
            "($LOX/LH_2$).\n"
            "   - **Ancient Crustal Geochemistry & Impact History**: Sample impact melt sheets from the **South Pole-Aitken (SPA) Basin**—the oldest and deepest "
            "confirmed impact structure on the Moon (over 2,500 km across)—to probe deep lunar mantle material and calibrate the impact chronology of the inner solar system.\n\n"
            "3. **Surface Deployments & Quotas**: Artemis astronauts will deploy long-lived autonomous geophysical stations (seismometers, heat-flow probes, retroreflectors) "
            "and utilize specialized cryogenic sealed sample containers to transport volatile-bearing cores back to Earth at sub-100 K temperatures."
        ),
        "ground_truth_facts": [
            "Lunar South Pole", "Permanently Shadowed Regions (PSRs)", "cold traps", "25 to 40 Kelvin",
            "water ice and volatiles", "South Pole-Aitken (SPA) basin", "In-Situ Resource Utilization (ISRU)",
            "axial tilt 1.54 degrees", "cryogenic sample return", "Shackleton crater"
        ],
        "telemetry_metrics": [
            "25 to 40 K (-415 F)", "1.54 deg axial tilt", "5 to 10 wt% water ice", "2,500 km SPA basin", ">2 billion years"
        ],
        "expected_rag_behavior": (
            "Must cite Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, emphasize the 1.54° axial tilt creating PSRs, cite extreme 25-40 K temps, "
            "list volatiles ($H_2O, CO, CH_4, NH_3$), explain the South Pole-Aitken basin context, and explain cryogenic sample return."
        ),
        "expected_no_rag_failure_modes": (
            "Generalizes lunar science as just looking for rocks, confuses South Pole with Apollo landing sites, or fails to mention cryogenic temperatures."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Accurately explains PSR mechanics, 25-40K temps, volatile chemistry, SPA basin, and ISRU; 3: Mentions ice at poles but lacks physics or temps; 1: Inaccurate.",
            "completeness": "5: Thoroughly addresses PSR physics, scientific goals, and geological targets; 3: Covers only water ice without SPA basin; 1: Inadequate.",
            "groundedness": "5: Directly reflects NASA's strategic science plan; 1: Speculative."
        }
    },
    {
        "id": "NASA_Q16",
        "domain": "Artemis Program (Human Landing System)",
        "subdomain": "HLS Multi-Lander Architectures & In-Space Propellant Transfer",
        "primary_source": "Artemis_Human_Landing_System_HLS_Update_2025.pdf",
        "supporting_sources": ["Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf"],
        "source_pages": "HLS Architecture Updates pp. 1-22; Cryogenic Propellant Management pp. 30-52",
        "question": "What are the architectural differences, cryogenic propellant requirements, and operational concepts between SpaceX Starship HLS and Blue Origin Blue Moon for Artemis crewed lunar landings?",
        "ground_truth_answer": (
            "Under NASA's NextSTEP Appendix H and Sustaining Lunar Development (Option A/B and SLD) contracts, NASA selected two commercial providers to develop "
            "independent, dissimilar Human Landing Systems (HLS) for Artemis surface missions:\n\n"
            "1. **SpaceX Starship HLS (Artemis III & IV)**:\n"
            "   - **Vehicle Architecture**: A massive 50-meter-tall, 9-meter-diameter stainless-steel single-stage lunar lander derived from the Starship upper stage, "
            "featuring an expansive crew cabin, forward RCS thruster ring, high-mounted landing thrusters (to avoid blowing high-velocity regolith dust and digging craters), "
            "and an elevator mechanism to lower astronauts 30+ meters to the lunar surface.\n"
            "   - **Propellant System**: Powered by Raptor 3 engines burning cryogenic **liquid methane ($CH_4$) and liquid oxygen ($LOX$)**.\n"
            "   - **Operational Concept & In-Space Refueling**: Requires an unprecedented in-space cryogenic propellant transfer campaign: a Starship Propellant Depot "
            "is launched to Low Earth Orbit (LEO), followed by multiple Starship tanker flights (estimated 10 to 15+ flights) that transfer cryogenic $CH_4$ and $LOX$ "
            "into the depot. The Starship HLS launches empty, refuels in LEO, and burns directly for Near-Rectilinear Halo Orbit (NRHO) around the Moon to dock with Orion.\n\n"
            "2. **Blue Origin Blue Moon National Team (Artemis V+)**:\n"
            "   - **Vehicle Architecture**: Developed under the Sustaining Lunar Development (SLD) contract by Blue Origin with Lockheed Martin, Draper, Boeing, "
            "Astrobotic, and Honeybee Robotics. A 16-meter tall vehicle tailored specifically to fit within a standard 7-meter payload fairing of the New Glenn rocket.\n"
            "   - **Propellant System**: Uses BE-7 deep-throttling engines burning high-efficiency **liquid hydrogen ($LH_2$) and liquid oxygen ($LOX$)**.\n"
            "   - **Operational Concept & Cryogenic Storage**: Operates with a dedicated Cislunar Transporter. Storing $LH_2$ at -423°F over multi-week lunar missions "
            "requires active 20 Kelvin cryocoolers, zero-boil-off sunshields, and in-space transfer of cryogenic hydrogen in cislunar space.\n\n"
            "3. **Operational Mission Profile**: In both architectures, the 4-person astronaut crew launches from Earth atop the SLS rocket inside Orion. "
            "Orion flies to NRHO and docks with the pre-staged HLS lander. Two astronauts transfer to HLS for a 6.5-day to 30-day surface stay conducting EVAs, "
            "then launch back from the Moon to redock with Orion for the return to Earth."
        ),
        "ground_truth_facts": [
            "Human Landing System (HLS)", "SpaceX Starship HLS", "Blue Origin Blue Moon", "liquid methane (CH4) and LOX",
            "liquid hydrogen (LH2) and LOX", "in-space cryogenic propellant transfer", "LEO depot tanker flights",
            "Near-Rectilinear Halo Orbit (NRHO)", "elevator mechanism", "zero-boil-off cryocoolers", "Artemis III, IV, V"
        ],
        "telemetry_metrics": [
            "50 m height / 9 m diameter", "10-15+ tanker flights", "20 K LH2 storage", "6.5 to 30 days surface stay", "NRHO rendezvous"
        ],
        "expected_rag_behavior": (
            "Must cite Artemis_Human_Landing_System_HLS_Update_2025.pdf, contrast Starship (methane/LOX, massive size, elevator, LEO depot refilling) "
            "with Blue Moon (hydrogen/LOX, BE-7, cislunar transporter, 20 K zero-boil-off storage), and detail NRHO docking with Orion."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses HLS with the Apollo Lunar Module (claiming single-launch expendable lander), fails to mention in-space propellant refilling, "
            "or assumes SLS launches the lander directly."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Clear distinctions on propellants (methane vs. hydrogen), refilling concepts, and vehicle layouts; 3: Confuses fuels or misses refilling details; 1: Completely incorrect.",
            "completeness": "5: Thoroughly covers SpaceX and Blue Origin architectures, propellants, and mission profiles; 3: Only discusses SpaceX; 1: Superficial.",
            "groundedness": "5: Exactly matches NASA HLS technical briefings; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q17",
        "domain": "Flagship Space Telescopes (Hubble)",
        "subdomain": "Servicing Mission 3A Avionics & Gyroscope Emergency Overhaul",
        "primary_source": "Hubble_Space_Telescope_Servicing_Mission.pdf",
        "supporting_sources": ["JWST_Mission_Overview_and_Status.pdf"],
        "source_pages": "Servicing Mission 3A Overview pp. 1-15",
        "question": "Why was Hubble Servicing Mission 3A (SM3A) launched ahead of schedule, and what specific avionics, gyroscope, and guidance upgrades were installed during STS-103?",
        "ground_truth_answer": (
            "NASA launched Hubble Servicing Mission 3A (STS-103) aboard Space Shuttle Discovery in **December 1999** as an emergency contingency mission:\n\n"
            "1. **Pre-Mission Crisis (Gyroscope Failures)**:\n"
            "   - Hubble requires at least three operating rate-sensing gyroscopes to perform precision pointing and astronomical science observations.\n"
            "   - Throughout 1999, gyroscopes began failing sequentially. When the fourth of its six gyroscopes failed on **November 13, 1999**, Hubble could no longer "
            "maintain science pointing and automatically entered a protective 'zero-gyro safe mode' (pointing its solar panels at the Sun and shutting down all science).\n"
            "   - Rather than waiting for the originally planned full Servicing Mission 3 in late 2000, NASA split the mission into SM3A and SM3B, rushing SM3A into orbit in December 1999.\n\n"
            "2. **Critical Hardware Replacements & Upgrades**:\n"
            "   - **Rate Sensor Units (RSUs)**: Astronauts replaced all three RSUs (each housing two rate-sensing gyroscopes), restoring Hubble to a complete complement "
            "of **six brand-new gyroscopes** with improved gas-bearing fluid and electrical leads.\n"
            "   - **Main Computer Upgrade (DF-224 to Intel 80486)**: The original, obsolete DF-224 flight computer (which had only 48,000 24-bit words of memory "
            "and a clock speed of 1.25 MHz) was replaced by an **Intel 80486 25-MHz 32-bit radiation-hardened processor**. This upgrade increased Hubble's computational "
            "processing speed by **20 times (2,000%)** and expanded its flight software memory by **6 times**, enabling autonomous flight software routines and "
            "drastically reducing ground commanding overhead.\n"
            "   - **Solid State Recorder (SSR)**: Replaced a failing 1970s-era reel-to-reel magnetic tape recorder with a 12.0-gigabit solid-state digital recorder, "
            "providing 10x greater data storage capacity, higher data transfer rates, and eliminating mechanical tape jam vulnerabilities.\n"
            "   - **Fine Guidance Sensor (FGS-1R)**: Astronauts replaced degraded Fine Guidance Sensor 1 with an upgraded, refurbished optical interferometer unit "
            "(FGS-1R) featuring an adjustable fold-flat mirror to overcome optical spherical aberration and provide astrometric positioning accuracy down to fractions of a milliarcsecond."
        ),
        "ground_truth_facts": [
            "Servicing Mission 3A (SM3A)", "STS-103 Discovery", "December 1999", "gyroscope failure", "zero-gyro safe mode",
            "Rate Sensor Units (RSUs)", "six new gyroscopes", "DF-224 computer replacement", "Intel 80486 25-MHz",
            "20x processing speed", "Solid State Recorder (SSR)", "Fine Guidance Sensor (FGS-1R)"
        ],
        "telemetry_metrics": [
            "4 of 6 gyros failed", "Nov 13 1999 shutdown", "6 new gyros in 3 RSUs", "Intel 486 25 MHz", "20x speed / 6x memory", "12 Gb SSR"
        ],
        "expected_rag_behavior": (
            "Must cite Hubble_Space_Telescope_Servicing_Mission.pdf, explain the emergency split of SM3 due to 4 gyros failing (putting HST in safe mode Nov 1999), "
            "detail the installation of 6 new gyros, the replacement of DF-224 with the Intel 80486 (20x faster, 6x memory), SSR, and FGS-1R."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses SM3A with SM1 (COSTAR mirror fix in 1993) or SM4 (last shuttle mission in 2009), or fails to name the 486 computer and gyroscope replacements."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Accurately explains 4-gyro failure, safe mode, 6 new gyros, Intel 486 (20x speed, 6x memory), SSR, and FGS-1R; 3: Mentions gyros but misses 486 computer; 1: Confuses with SM1 COSTAR.",
            "completeness": "5: Thoroughly addresses failure cause, mission timing, and all major avionics upgrades; 3: Mentions only one component; 1: Inadequate.",
            "groundedness": "5: Exactly matches NASA HST servicing technical documentation; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q18",
        "domain": "Historic Lunar Missions (Apollo 11)",
        "subdomain": "Saturn V (AS-506) Multi-Stage Propulsion & Ascent Telemetry",
        "primary_source": "Apollo_11_Technical_Information_Summary.pdf",
        "supporting_sources": ["Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf"],
        "source_pages": "Launch Vehicle Description pp. 1-28; Stage Propulsion pp. 35-60",
        "question": "What were the engine configurations, propellant combinations, thrust outputs, and burn durations of the three stages of the Saturn V launch vehicle (AS-506) that launched Apollo 11 to the Moon?",
        "ground_truth_answer": (
            "The Saturn V launch vehicle (designated **AS-506**) that propelled the Apollo 11 mission on July 16, 1969, stood **363 feet (110.6 meters) tall** "
            "and utilized a three-stage liquid propulsion architecture engineered by NASA Marshall Space Flight Center under Wernher von Braun:\n\n"
            "1. **Stage 1: S-IC (First Stage)**:\n"
            "   - **Engines**: Five Rocketdyne **F-1 engines** (one center fixed engine and four outer gimbaled engines for thrust vector control).\n"
            "   - **Propellants**: RP-1 high-grade kerosene (209,000 gallons) and Liquid Oxygen (LOX, 334,000 gallons).\n"
            "   - **Thrust**: Delivered approximately **7,500,000 pounds-force (33.3 MN)** of liftoff thrust (each F-1 producing 1.5 million lbf).\n"
            "   - **Burn Duration & Telemetry**: Burned for **168 seconds (2 minutes and 48 seconds)**, boosting the vehicle to an altitude of ~42 miles (67 km) "
            "and a velocity of ~6,100 mph (~2,720 m/s / Mach 8).\n\n"
            "2. **Stage 2: S-II (Second Stage)**:\n"
            "   - **Engines**: Five Rocketdyne **J-2 engines** arranged in a square pattern with one center engine.\n"
            "   - **Propellants**: Cryogenic Liquid Hydrogen ($LH_2$, 260,000 gallons) and Liquid Oxygen (LOX, 83,000 gallons).\n"
            "   - **Thrust**: Delivered **1,150,000 pounds-force (5.1 MN)** of vacuum thrust (each J-2 producing ~230,000 lbf).\n"
            "   - **Burn Duration & Telemetry**: Burned for approximately **390 seconds (6.5 minutes)**, accelerating the stack to ~115 miles (185 km) altitude "
            "and a near-orbital velocity of ~15,400 mph (~6,880 m/s).\n\n"
            "3. **Stage 3: S-IVB (Third Stage)**:\n"
            "   - **Engines**: A single restartable Rocketdyne **J-2 engine**.\n"
            "   - **Propellants**: Cryogenic Liquid Hydrogen ($LH_2$) and Liquid Oxygen (LOX).\n"
            "   - **Thrust**: Produced **230,000 pounds-force (1.02 MN)** of vacuum thrust.\n"
            "   - **Two-Burn Mission Profile**:\n"
            "     * **First Burn**: Lasted **156 seconds (2.6 minutes)** to insert Apollo 11 and the S-IVB into a circular Earth parking orbit at ~118 miles altitude (17,400 mph).\n"
            "     * **Second Burn (TLI)**: After orbital checkout, the J-2 reignited for **347 seconds (5.8 minutes)** to execute the Translunar Injection (TLI), "
            "accelerating the spacecraft to **24,500 mph (10.9 km/s / ~36,000 ft/s)** onto its lunar transfer trajectory."
        ),
        "ground_truth_facts": [
            "Saturn V AS-506", "S-IC Stage", "S-II Stage", "S-IVB Stage", "Rocketdyne F-1", "Rocketdyne J-2",
            "RP-1 and LOX", "liquid hydrogen (LH2) and LOX", "7.5 million lbf thrust", "1.15 million lbf thrust",
            "230,000 lbf thrust", "Translunar Injection (TLI)", "Earth parking orbit"
        ],
        "telemetry_metrics": [
            "363 feet tall", "7,500,000 lbf (S-IC)", "1,150,000 lbf (S-II)", "230,000 lbf (S-IVB)", "168 sec burn", "390 sec burn", "156s + 347s TLI", "24,500 mph"
        ],
        "expected_rag_behavior": (
            "Must cite Apollo_11_Technical_Information_Summary.pdf, specify the 3 distinct stages (S-IC, S-II, S-IVB), their engines (5x F-1, 5x J-2, 1x J-2), "
            "propellants (RP-1/LOX for stage 1, LH2/LOX for stages 2 and 3), exact thrust figures (7.5M lbf, 1.15M lbf, 230k lbf), and S-IVB's two burns."
        ),
        "expected_no_rag_failure_modes": (
            "Confuses engines (claiming F-1 on all stages), forgets that S-IVB is restartable for TLI, or confuses Saturn V propellant with solid boosters."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Flawless engines (5x F-1, 5x J-2, 1x J-2), propellants, thrusts (7.5M, 1.15M, 230k lbf), and burn durations; 3: Minor confusion in burn times or engine counts; 1: Inaccurate.",
            "completeness": "5: Covers all 3 stages, fuels, thrust values, and S-IVB TLI burn profile; 3: Leaves out stage 3 details; 1: Minimal.",
            "groundedness": "5: Matches official NASA Apollo 11 technical summary; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q19",
        "domain": "Cross-Mission Planetary Systems Engineering",
        "subdomain": "Apollo Lunar Module vs. MSL Sky Crane Deceleration Mechanics",
        "primary_source": "Apollo_11_Technical_Information_Summary.pdf",
        "supporting_sources": ["Mars_Curiosity_MSL_EDL_Assessment.pdf"],
        "source_pages": "Apollo LM Propulsion pp. 75-102; MSL Sky Crane Assessment pp. 50-75",
        "question": "How do the descent propulsion system, guidance control, and terminal touchdown mechanics of the Apollo 11 Lunar Module (Eagle) compare to the Entry, Descent, and Landing (EDL) Sky Crane of Curiosity on Mars?",
        "ground_truth_answer": (
            "The Apollo 11 Lunar Module (LM) *Eagle* and the Mars Science Laboratory (MSL) *Curiosity* represent two divergent masterpieces of planetary "
            "touchdown engineering, shaped fundamentally by atmospheric environment, gravity, and human vs. robotic autonomy:\n\n"
            "1. **Atmospheric Environment & Deceleration Pipeline**:\n"
            "   - **Apollo LM (Moon)**: Because the Moon has a near-perfect vacuum, aerodynamic drag and parachutes are impossible. 100% of the kinetic energy "
            "and orbital velocity (~1.6 km/s) had to be dissipated purely through propulsive rocket deceleration.\n"
            "   - **Curiosity (Mars)**: Mars has a thin CO₂ atmosphere (~1% Earth density). MSL exploited this by dissipating >99% of its kinetic entry energy "
            "(~5.9 km/s down to 80 m/s) passively via a hypersonic ablative heat shield and a 21.5-meter supersonic parachute, requiring rocket propulsion "
            "for only the final 1.8 km of descent.\n\n"
            "2. **Propulsion Architecture & Propellants**:\n"
            "   - **Apollo LM Descent Propulsion System (DPS)**: A single TRW throttlable rocket engine burning storable hypergolic bipropellants (Aerozine-50 "
            "and Nitrogen Tetroxide, $N_2O_4$). It was the first human-rated throttleable rocket (throttling between 10% and 60% and at 100%, producing "
            "1,050 to 9,870 lbf thrust).\n"
            "   - **MSL Descent Stage**: Powered by eight fixed-geometry Mars Landing Engines (MLE) running on monopropellant hydrazine ($N_2H_4$) over catalyst beds. "
            "They throttled via high-frequency pulse modulation between 400 and 3,100 N each to stabilize the descent platform.\n\n"
            "3. **Guidance, Navigation, and Pilot Control**:\n"
            "   - **Apollo LM**: Driven by the Apollo Guidance Computer (AGC) running fixed guidance phases (P63 Braking, P64 Pitchover/Approach). Crucially, "
            "at ~500 feet altitude, Neil Armstrong switched the computer to Semi-Automatic/Manual Mode (P66), visually identifying boulders in the landing ellipse "
            "and hand-flying the lander past West Crater to touchdown with only ~25 seconds of propellant remaining.\n"
            "   - **Curiosity**: Entirely autonomous due to the 14-minute one-way light-time communication latency to Mars. Onboard flight software and the Terminal "
            "Descent Sensor (radar) made all split-second guidance decisions with zero human intervention.\n\n"
            "4. **Touchdown Mechanics & Plume Interaction**:\n"
            "   - **Apollo LM**: Four landing gear legs with crushable honeycomb aluminum shock absorbers. Touchdown was triggered by 5.6-foot lunar surface contact "
            "probes hanging from the footpads; contact lit a blue 'LUNAR CONTACT' indicator, commanding Armstrong to press the engine stop button.\n"
            "   - **Curiosity Sky Crane**: Directly landing a 900-kg rover with belly thrusters would blast deep trenches and coat delicate optics in abrasive soil. "
            "The Sky Crane solved this by hovering 20 meters overhead, lowering the rover on a 7.5-meter bridle cable, deploying the rover wheels to absorb landing shock, "
            "severing the tether with pyrotechnic guillotines upon weight-off-wheels, and flying the descent stage away to crash."
        ),
        "ground_truth_facts": [
            "Apollo Lunar Module (Eagle)", "Curiosity MSL Sky Crane", "vacuum vs. thin atmosphere", "aerodynamic braking vs. 100% propulsive",
            "Descent Propulsion System (DPS)", "throttleable hypergolic bipropellant", "Aerozine-50 and N2O4",
            "Mars Landing Engines (MLE)", "monopropellant hydrazine", "Apollo Guidance Computer (P66 manual control)",
            "autonomous radar guidance", "lunar contact probes", "7.5-meter bridle cables", "plume impingement avoidance"
        ],
        "telemetry_metrics": [
            "1/6g Moon vs. 3/8g Mars", "1,050 to 9,870 lbf DPS thrust", "8x MLE thrusters", "7.5 m bridle", "5.6 ft contact probes", "14-min light delay"
        ],
        "expected_rag_behavior": (
            "Must synthesize Apollo_11_Technical_Information_Summary.pdf and Mars_Curiosity_MSL_EDL_Assessment.pdf, highlighting the physics of vacuum "
            "propulsion vs. atmospheric aerodynamic drag, comparing the throttleable DPS bipropellant engine with MSL's 8 monopropellant MLEs, and explaining "
            "human-in-the-loop manual landing (P66) vs. Sky Crane autonomous tether descent to prevent rocket plume surface scouring."
        ),
        "expected_no_rag_failure_modes": (
            "Overlooks plume scouring as the primary reason for the Sky Crane, claims Apollo used parachutes, or assumes Curiosity was manually piloted."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Superb technical cross-comparison covering thermodynamics, propellants, control loops, and touchdown physics; 3: Compares vehicles broadly without propulsion/control specifics; 1: Fundamentally flawed.",
            "completeness": "5: Thoroughly addresses atmosphere, engines, guidance/human control, and landing gear/Sky Crane mechanics; 3: Omits guidance or plume interaction; 1: Superficial.",
            "groundedness": "5: Deeply grounded in both NASA technical engineering reports; 1: Fabricated."
        }
    },
    {
        "id": "NASA_Q20",
        "domain": "Planetary Defense & Orbital Mechanics",
        "subdomain": "Kinetic Impactor vs. Slow-Push Deflection Physics",
        "primary_source": "DART_Planetary_Defense_Technical_Report.pdf",
        "supporting_sources": ["DART_Kinetic_Impactor_Deflection_Results.pdf"],
        "source_pages": "Deflection Physics pp. 5-25; Planetary Defense Comparisons pp. 110-130",
        "question": "Based on the technical results of the DART mission, what is the mathematical physics of momentum transfer in kinetic impact deflection, and how does kinetic impact compare in effectiveness, warning time, and operational risk to slow-push methods like gravity tractors?",
        "ground_truth_answer": (
            "The DART mission provided empirical validation of kinetic impact physics, allowing planetary defense engineers to mathematically model "
            "asteroid deflection and rigorously evaluate trade-offs against alternative slow-push concepts:\n\n"
            "1. **Mathematical Physics of Kinetic Impact Deflection**:\n"
            "   - The instantaneous velocity change $\\Delta \\mathbf{v}_{ast}$ imparted to an asteroid of mass $M_{ast}$ by a kinetic impactor of mass $m_{sc}$ "
            "striking at relative velocity $\\mathbf{v}_{rel}$ is governed by the momentum conservation equation:\n"
            "$$\\Delta \\mathbf{v}_{ast} = \\beta \\left( \\frac{m_{sc}}{M_{ast}} \\right) \\mathbf{v}_{rel}$$\n"
            "where $\\beta$ is the momentum enhancement factor from crater ejecta recoil.\n"
            "   - For DART on Dimorphos: $m_{sc} \\approx 580 \\text{ kg}$, $\\mathbf{v}_{rel} \\approx 6.14 \\text{ km/s}$, $M_{ast} \\approx 4.3 \\times 10^9 \\text{ kg}$, "
            "and $\\beta \\approx 3.6$. This produced an instantaneous velocity change of $\\Delta v \\approx 2.7 \\text{ mm/s}$ (or $\\sim 2.7 \\times 10^{-3} \\text{ m/s}$).\n"
            "   - While 2.7 mm/s appears tiny, when projected along an asteroid's heliocentric orbital path over an operational warning time of 10 years "
            "($\\Delta t = 3.15 \\times 10^8 \\text{ s}$), the cumulative orbital position displacement $\\Delta x$ is:\n"
            "$$\\Delta x \\approx 3 \\cdot \\Delta v \\cdot \\Delta t \\approx 3 \\cdot (0.0027) \\cdot (3.15 \\times 10^8) \\approx 2.55 \\times 10^6 \\text{ m} \\approx 2,550 \\text{ km}$$\n"
            "which shifts the asteroid's intersection point by thousands of kilometers, easily transforming a direct Earth collision into a safe miss.\n\n"
            "2. **Comparison with Slow-Push Techniques (Gravity Tractor)**:\n"
            "   - **Gravity Tractor Mechanism**: A massive spacecraft hovers near an asteroid without docking, using mutual gravitational attraction ($F_g = G \\frac{m_{sc} M_{ast}}{r^2}$) "
            "and low-thrust ion engines canted outward to slowly tow the asteroid over years.\n"
            "   - **Warning Time Requirements**:\n"
            "     * **Kinetic Impactor**: High effectiveness for short-to-medium warning times (**5 to 20 years**). Delivers an instantaneous, single-impulse velocity change.\n"
            "     * **Gravity Tractor**: Requires extremely long warning times (**20 to 50+ years**) because gravitational force is minuscule, producing tiny accelerations "
            "($\\Delta v \\sim 10^{-5} \\text{ m/s per year}$). However, it provides exquisite trajectory trim control with zero risk of fragmentation.\n"
            "   - **Operational Risks & Rubble-Pile Asteroids**:\n"
            "     * Kinetic impact carries the risk of asteroid disruption or fragmentation if the impact energy exceeds the specific catastrophic disruption energy ($Q^*_D$). "
            "DART proved that for a 160-meter rubble-pile asteroid, a 6.1 km/s impact deflected Dimorphos without catastrophically blowing it apart, while ejecta recoil "
            "multiplied deflection efficiency by a factor of 3.6."
        ),
        "ground_truth_facts": [
            "kinetic impact physics", "momentum equation: Delta v = beta * (m / M) * v", "momentum enhancement factor beta",
            "Dimorphos mass ~4.3e9 kg", "instantaneous velocity change ~2.7 mm/s", "cumulative displacement over warning time",
            "gravity tractor", "ion propulsion", "warning time: 5-20 years vs. 20-50+ years", "catastrophic disruption risk (Q*D)",
            "rubble-pile asteroid cohesion"
        ],
        "telemetry_metrics": [
            "Delta v ~ 2.7 mm/s", "beta ~ 3.6", "m = 580 kg", "v = 6.14 km/s", "M ~ 4.3e9 kg", "5 to 20 years warning time", "thousands of km displacement"
        ],
        "expected_rag_behavior": (
            "Must cite DART_Planetary_Defense_Technical_Report.pdf, formulate the momentum equation including beta, calculate how small mm/s velocity changes "
            "compound into thousands of kilometers over multi-year orbital baselines, compare warning time needs with gravity tractors (5-20 yrs vs 20-50+ yrs), "
            "and discuss fragmentation risks."
        ),
        "expected_no_rag_failure_modes": (
            "Fails to state the momentum formula, claims kinetic impact stops an asteroid dead in its tracks (physically impossible), or fails to explain "
            "how a tiny millimeter-per-second velocity change prevents an Earth impact."
        ),
        "annotation_rubric": {
            "factual_accuracy": "5: Clear equations, exact numbers (2.7 mm/s, beta 3.6), orbital mechanics compounding, and gravity tractor comparison; 3: Explains concept without math or timelines; 1: Inaccurate.",
            "completeness": "5: Covers mathematical physics, numerical example, warning times, and risk trade-offs; 3: Misses gravity tractor or math; 1: Superficial.",
            "groundedness": "5: Strictly reflects NASA planetary defense report; 1: Speculative."
        }
    }
]


def create_json_dataset(target_path: Path):
    """Outputs the complete ground truth dataset to JSON."""
    payload = {
        "title": "NASA Space Missions 20-Question Ground Truth Dataset for RAG Evaluation",
        "course": "Natural Language Interaction (ILN) 2026/2027",
        "institution": "Universidade de Coimbra (DEI-FCTUC)",
        "authors": ["Mohammed Abdelqader", "Michael O'Shea"],
        "corpus": "17 NASA Technical Reports (1,600 chunks indexed in ChromaDB `nasa_missions`)",
        "total_questions": len(DATASET_QUESTIONS),
        "questions": DATASET_QUESTIONS
    }
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)
    print(f"[OK] Generated: {target_path} ({target_path.stat().st_size:,} bytes)")


def create_annotation_markdown(target_path: Path):
    """Outputs the human annotation guide in Markdown."""
    lines = []
    lines.append("# NASA Space Missions: 20-Question Annotation & Ground Truth Evaluation Guide\n")
    lines.append("**Course:** Natural Language Interaction (ILN) 2026/2027  ")
    lines.append("**Institution:** Universidade de Coimbra — Departamento de Engenharia Informática (DEI-FCTUC)  ")
    lines.append("**Authors:** Mohammed Abdelqader & Michael O'Shea  ")
    lines.append("**Knowledge Source:** 17 NASA Technical Reports (`data/nasa_docs/`, 1,600 Chunks in ChromaDB `nasa_missions`)  ")
    lines.append("**Theoretical Course Source:** `E:\\Coimbra University 2025-2027\\Second Year\\First Semester\\Natural Language Interaction\\Theoretical`  \n")
    lines.append("---\n")
    lines.append("## 1. Annotation Protocol & Scoring Criteria\n")
    lines.append("This document provides the authoritative ground truth for evaluating and annotating candidate responses from **With-RAG** and **Without-RAG** systems.\n")
    lines.append("### Likert Scoring Dimensions (1 to 5):\n")
    lines.append("| Score | Factual Accuracy | Completeness | Groundedness / Attribution |")
    lines.append("|:---:|:---|:---|:---|")
    lines.append("| **5** | 100% accurate; exact physics, telemetry numbers, dates, and vehicle names. | Thoroughly addresses every sub-clause and technical requirement. | Fully grounded in the text; exact inline citations `[Document.pdf, Page X]`. |")
    lines.append("| **4** | Accurate with minor rounding or trivial secondary detail omitted. | Covers all primary points with minor secondary gaps. | Well-grounded with valid citations; minor phrasing ambiguity. |")
    lines.append("| **3** | Conceptually correct but missing exact metrics or parameters. | Addresses roughly half of the required technical criteria. | General claims supported, but includes ungrounded generic filler. |")
    lines.append("| **2** | Notable factual errors, wrong parameters, or incorrect physics. | Misses key mechanisms or misidentifies subsystems. | Obvious hallucinations; cites wrong documents or nonexistent pages. |")
    lines.append("| **1** | Grossly inaccurate or irrelevant. | Completely fails to address question requirements. | Pure fabrication or blank output. |")
    lines.append("\n---\n")
    lines.append("## 2. Table of 20 Ground Truth Questions\n")
    lines.append("| ID | Mission Domain | Subdomain | Primary Document |")
    lines.append("|:---:|:---|:---|:---|")
    for q in DATASET_QUESTIONS:
        lines.append(f"| **{q['id']}** | {q['domain']} | {q['subdomain']} | `{q['primary_source']}` |")
    lines.append("\n---\n")
    lines.append("## 3. Question-by-Question Ground Truth & Annotation Sheets\n")

    for idx, q in enumerate(DATASET_QUESTIONS, start=1):
        lines.append(f"### Question {idx:02d}: {q['id']} — {q['domain']}\n")
        lines.append(f"**Subdomain:** {q['subdomain']}  ")
        lines.append(f"**Primary Source Document:** `{q['primary_source']}` ({q['source_pages']})  ")
        if q.get("supporting_sources"):
            lines.append(f"**Supporting Documents:** {', '.join(f'`{s}`' for s in q['supporting_sources'])}  ")
        lines.append("")
        lines.append(f"> **Technical Question:**  \n> *\"{q['question']}\"*\n")
        lines.append("#### Authoritative Ground Truth Answer\n")
        lines.append(q["ground_truth_answer"] + "\n")
        lines.append("#### Evaluation Targets & Telemetry Metrics\n")
        lines.append(f"- **Mandatory Key Facts (`ground_truth_facts`):**  \n  `{', '.join(q['ground_truth_facts'])}`\n")
        lines.append(f"- **Quantitative Telemetry Targets (`telemetry_metrics`):**  \n  `{', '.join(q['telemetry_metrics'])}`\n")
        lines.append("#### Behavioral Comparison Guide (With-RAG vs. Without-RAG)\n")
        lines.append(f"- **Expected With-RAG Output:** {q['expected_rag_behavior']}\n")
        lines.append(f"- **Expected Without-RAG Failure Modes:** {q['expected_no_rag_failure_modes']}\n")
        lines.append("#### Annotation Scorecard (Human Evaluator):\n")
        rub = q["annotation_rubric"]
        lines.append(f"- [ ] **Factual Accuracy (1-5):** _____ / 5  *(Guideline: {rub['factual_accuracy']})*")
        lines.append(f"- [ ] **Completeness (1-5):** _____ / 5  *(Guideline: {rub['completeness']})*")
        lines.append(f"- [ ] **Groundedness & Citations (1-5):** _____ / 5  *(Guideline: {rub['groundedness']})*")
        lines.append("- **Notes / Annotator Comments:** _____________________________________________________\n")
        lines.append("---\n")

    with open(target_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Generated: {target_path} ({target_path.stat().st_size:,} bytes)")


def main():
    json_path = BASE_DIR / "nasa_eval_dataset.json"
    md_path = BASE_DIR / "nasa_annotation_guide.md"
    create_json_dataset(json_path)
    create_annotation_markdown(md_path)


if __name__ == "__main__":
    main()
