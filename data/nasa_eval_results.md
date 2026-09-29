# NASA Space Missions: RAG vs. Without-RAG Benchmark Evaluation Report

**Course:** Natural Language Interaction (ILN) 2026/2027  
**Institution:** Universidade de Coimbra (DEI-FCTUC)  
**Authors:** Mohammed Abdelqader & Michael O'Shea  
**Evaluation Timestamp:** 2026-09-29 11:23:13  
**Generator Model:** `qwen2.5:7b`  
**Judge Model:** `mistral-small:24b`  
**Total Questions Evaluated:** 20

---

## 1. Executive Performance Comparison

| Metric Dimension | With-RAG (Augmented) | Without-RAG (Parametric) | Delta (Δ) |
|:---|:---:|:---:|:---:|
| **Fact Recall %** | **13.2%** | 19.9% | `-6.6%` |
| **Telemetry Metric Coverage %** | **4.0%** | 8.5% | `-4.5%` |
| **Average Citations / Answer** | **3.05** | 0.00 | `+3.05` |
| **Average Latency (s)** | 9.88s | 8.13s | `+1.75s` |
| **LLM Judge Score (1-5)** | **3.17 / 5.0** | 3.36 / 5.0 | `-0.19` |
| **Judge: Factual Accuracy** | **3.05** | 3.05 | `+0.00` |
| **Judge: Groundedness** | **3.60** | 3.10 | `+0.50` |

---

## 2. Granular Question-by-Question Results

| ID | Domain | With-RAG Recall | No-RAG Recall | With-RAG Telem | No-RAG Telem | With-RAG Cites | RAG Latency |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| **NASA_Q01** | James Webb Space Telescope (JWST) | 50% | 67% | 0% | 12% | 3 | 13.02s |
| **NASA_Q02** | James Webb Space Telescope (JWST) | 0% | 8% | 29% | 29% | 3 | 10.49s |
| **NASA_Q03** | James Webb Space Telescope (JWST) | 0% | 0% | 14% | 0% | 3 | 10.86s |
| **NASA_Q04** | Planetary Defense (DART) | 30% | 60% | 25% | 25% | 2 | 8.20s |
| **NASA_Q05** | Planetary Defense (DART) | 36% | 27% | 0% | 0% | 5 | 10.72s |
| **NASA_Q06** | Planetary Defense (DART) | 18% | 18% | 0% | 0% | 4 | 11.96s |
| **NASA_Q07** | Mars Exploration (Curiosity MSL) | 8% | 8% | 0% | 38% | 1 | 10.53s |
| **NASA_Q08** | Mars Exploration (Curiosity MSL) | 17% | 17% | 0% | 0% | 4 | 9.94s |
| **NASA_Q09** | Mars 2020 (Perseverance) | 23% | 23% | 0% | 0% | 2 | 14.86s |
| **NASA_Q10** | Mars 2020 (Perseverance) | 0% | 18% | 0% | 0% | 3 | 11.05s |
| **NASA_Q11** | Mars Rotorcraft (Ingenuity) | 8% | 8% | 12% | 0% | 5 | 10.38s |
| **NASA_Q12** | Mars Rotorcraft (Mars Science Helicopter) | 9% | 9% | 0% | 0% | 4 | 10.01s |
| **NASA_Q13** | Artemis Program (SLS / Orion) | 9% | 36% | 0% | 0% | 3 | 8.05s |
| **NASA_Q14** | Artemis Program (SLS / Orion) | 0% | 0% | 0% | 33% | 2 | 8.60s |
| **NASA_Q15** | Artemis Program (Lunar Science) | 20% | 30% | 0% | 0% | 5 | 10.66s |
| **NASA_Q16** | Artemis Program (Human Landing System) | 18% | 18% | 0% | 0% | 3 | 6.58s |
| **NASA_Q17** | Flagship Space Telescopes (Hubble) | 8% | 17% | 0% | 33% | 2 | 8.74s |
| **NASA_Q18** | Historic Lunar Missions (Apollo 11) | 0% | 23% | 0% | 0% | 0 | 3.91s |
| **NASA_Q19** | Cross-Mission Planetary Systems Engineering | 0% | 0% | 0% | 0% | 3 | 8.36s |
| **NASA_Q20** | Planetary Defense & Orbital Mechanics | 9% | 9% | 0% | 0% | 4 | 10.62s |

---

## 3. Case Studies & Verification Evidence

### NASA_Q01: James Webb Space Telescope (JWST) — Science Instrument Payload & Cryogenic Architecture

**Question:** What are the four core science instruments housed in the JWST Integrated Science Instrument Module (ISIM), what wavelength ranges do they observe, what detector technologies are used, and what are their cryogenic operating temperatures?

**Primary Source Document:** `JWST_Science_Instrument_Payload.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The James Webb Space Telescope (JWST) Integrated Science Instrument Module (ISIM) houses four core scientific instruments engineered for infrared astrophysics across the 0.6 to 28.5 micrometer (μm) spectral regime:

1. **NIRCam (Near-Infrared Camera)**: Serves as the primary imager from 0.6 to 5.0 μm and the principal wavefront sensor for telescope alignment. It utilizes ten 2048x2048 pixel Teledyne mercury-cadmium-telluride (HgCdTe) HAWAII-2RG (H2RG) focal plane detector arrays. It operates at a passive cryogenic temperature of ~37 to 40 Kelvin (K), cooled by radiation into deep space via dedicated thermal radiators.

2. **NIRSpec (Near-Infrared Spectrograph)**: Operates over 0.6 to 5.0 μm, featuring multi-object spectroscopy capable of observing >100 simultaneous astronomical targets using a Micro-Shutter Array (MSA) containing ~250,000 individually addressable micro-shutters. It employs two 2048x2048 Teledyne HgCdTe H2RG detectors and operates at passive cryogenic temperatures around 37 to 40 K.

3. **MIRI (Mid-Infrared Instrument)**: Covers the mid-infrared band from 4.9 to 28.5 (or 28.8) μm with imaging, coronagraphy, and medium/low-resolution spectroscopy. Because thermal emissions from the telescope at 40 K overwhelm mid-IR signals, MIRI uses arsenic-doped silicon (Si:As) Impurity Band Conduction (IBC) detector arrays (three 1024x1024 pixel FPAs) and requires an active closed-cycle helium loop cryocooler (pulse tube and Joule-Thomson refrigeration) to operate at an ultra-cold temperature of ~6.4 to 7.0 K.

4. **FGS/NIRISS (Fine Guidance Sensor / Near-Infrared Imager and Slitless Spectrograph)**: A shared opto-mechanical package containing the FGS (two 2048x2048 HgCdTe guide channels operating at 0.6-5.0 μm for sub-milliarcsecond pointing precision) and NIRISS (0.6 to 5.0 μm slitless spectroscopy and aperture masking interferometry for exoplanet transit characterization), also cooled passively to ~37 to 40 K.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 13.018826723098755s | **Fact Recall:** 50.0% | **Telemetry:** 0.0%

**Citations:** `['JWST_Science_Instrument_Payload.pdf, Page 2', 'JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3', 'JWST_Mission_Overview_and_Status.pdf, Page 38']`


The four core science instruments housed in the JWST Integrated Science Instrument Module (ISIM) are:

1. **NIRCam (Near-Infrared Camera)**:
   - **Wavelength Range**: 0.6 to 5 micrometers [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Detector Technology**: HgCdTe (Mercury Cadmium Telluride) [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Cryogenic Operating Temperature**: ~35 K [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3]

2. **MIRI (Mid-Infrared Instrument)**:
   - **Wavelength Range**: 5 to 28.3 micrometers [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Detector Technology**: HgCdTe (Mercury Cadmium Telluride) [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Cryogenic Operating Temperature**: ~35 K [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3]

3. **NIRSpec (Near-Infrared Spectrograph)**:
   - **Wavelength Range**: 0.6 to 5 micrometers [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Detector Technology**: HgCdTe (Mercury Cadmium Telluride) [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Cryogenic Operating Temperature**: ~35 K [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3]

4. **NIRISS (Near-Infrared Imager and Slitless Spectrograph)**:
   - **Wavelength Range**: 0.6 to 5 micrometers [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Detector Technology**: HgCdTe (Mercury Cadmium Telluride) [JWST_Science_Instrument_Payload.pdf, Page 2]
   - **Cryogenic Operating Temperature**: ~35 K [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3]

The fine guidance sensor (FGS) is also part of the ISIM but is not a science instrument. The ISIM is designed to operate at cryogenic temperatures of approximately 35 K to ensure the detectors function effectively in the infrared range. [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 3] [JWST_Science_Instrument_Payload.pdf, Page 2] [JWST_Mission_Overview_and_Status.pdf, Page 38]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 7.221449613571167s | **Fact Recall:** 66.7% | **Telemetry:** 12.5%


The James Webb Space Telescope (JWST) Integrated Science Instrument Module (ISIM) houses four core science instruments, each designed to observe specific wavelength ranges and utilize advanced detector technologies. Here's a detailed breakdown:

1. **Near-Infrared Camera (NIRCam)**
   - **Wavelength Range:** 0.6 to 5 microns
   - **Detector Technology:** 2560 x 2048 pixel arrays of HgCdTe (Indium-Antimonide) detectors
   - **Cryogenic Operating Temperature:** ~30 K (-243.15°C)

2. **Near-Infrared Spectrograph (NIRSpec)**
   - **Wavelength Range:** 0.6 to 5 microns
   - **Detector Technology:** 2560 x 2048 pixel arrays of HgCdTe (Indium-Antimonide) detectors
   - **Cryogenic Operating Temperature:** ~30 K (-243.15°C)

3. **Mid-Infrared Instrument (MIRI)**
   - **Wavelength Range:** 5 to 28.3 microns
   - **Detector Technology:** 1024 x 1024 pixel arrays of HgCdTe (Indium-Antimonide) detectors for the camera and 256 x 256 pixel arrays of photodiodes for the spectrometer
   - **Cryogenic Operating Temperature:** ~7 K (-266.15°C)

4. **Fine Guidance Sensor/Near-Infrared Imager and Slitless Spectrograph (FGS/NIRISS)**
   - **Wavelength Range:** 0.6 to 2.8 microns
   - **Detector Technology:** 2560 x 2048 pixel arrays of HgCdTe (Indium-Antimonide) detectors
   - **Cryogenic Operating Temperature:** ~30 K (-243.15°C)

These instruments are designed to work in the cryogenic environment of the JWST, which operates at extremely low temperatures to minimize thermal noise and maximize sensitivity. The HgCdTe detectors are particularly well-suited for infrared astronomy due to their high quantum efficiency and wide temperature range. The cryogenic temperatures are maintained by the telescope's cryocoolers, which are part of the ISIM and are responsible for keeping the instruments at their required operating temperatures.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.0 / 5.0 | *Strengths:* Clear and concise language, correct wavelength ranges for NIRCam, NIRSpec, and NIRISS.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Incorrect detector technology for MIRI, incorrect operating temperatures for NIRCam, NIRSpec, and FGS/NIRISS. Incorrect wavelength range for FGS/NIRISS. Missing details on MIRI's cryocooler and MSA for NIRSpec.


---

### NASA_Q02: James Webb Space Telescope (JWST) — Cryogenic Thermal Distortion & Wavefront Control

**Question:** How does NASA model and compensate for the cryogenic thermal distortion of JWST's 18 primary mirror segments as they cool from room temperature to deep cryogenic operational temperatures (~35-50 K)?

**Primary Source Document:** `JWST_Cryogenic_Thermal_Distortion_Model.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


NASA addressed the primary mirror cryogenic distortion through an integrated engineering pipeline combining high-fidelity structural/thermal finite element modeling (FEM), optical ray-tracing, and active wavefront sensing and control (WFS&C):

1. **Beryllium Substrate Selection**: The 18 hexagonal Primary Mirror Segment Assemblies (PMSAs) are machined from optical-grade O-30 beryllium, chosen for its superior stiffness-to-weight ratio, structural stability, and nearly zero coefficient of thermal expansion (CTE) at cryogenic temperatures below 100 K.

2. **Cryo-Null Figuring**: Because beryllium undergoes non-uniform volumetric shrinkage when cooled from ambient polishing temperatures (~293 K) to operational temperatures (~35-50 K), NASA modeled this cryogenic deformation using detailed Nastran/SigFit structural finite element models and validated them inside cryogenic test chambers (e.g., NASA Marshall X-Ray and Cryogenic Facility - XRCF). The mirrors were manufactured with an inverse 'cryo-null' surface figure at room temperature so that thermal contraction warped them into the exact required aspheric prescription on orbit.

3. **Active Hexapod & Radius of Curvature Actuation**: Each of the 18 segments is mounted on a mechanical hexapod providing six degrees of freedom (rigid body piston, tip, tilt, clocking, and lateral translation) driven by cryogenic stepper motor actuators capable of nanometer-scale step resolution. Furthermore, a 7th actuator mechanism attached to the rear ribs controls the Radius of Curvature (RoC) of each segment to match focal lengths across all 18 segments.

4. **Wavefront Sensing & Control (WFS&C)**: During commissioning, NIRCam phase retrieval algorithms measured optical path differences (OPD) to iteratively align and co-phase the segments into a single monolithic 6.5-meter wavefront with less than 50 nanometers RMS wavefront error.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.4895179271698s | **Fact Recall:** 0.0% | **Telemetry:** 28.6%

**Citations:** `['JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 5', 'JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 16', 'JWST_Mission_Overview_and_Status.pdf, Page 32']`


NASA models and compensates for the cryogenic thermal distortion of JWST's 18 primary mirror segments through a series of rigorous testing and analysis phases. The primary mirror segments are subject to significant thermal contraction as the telescope cools from room temperature to its operational temperature of approximately 35-50 K.

During the cryogenic thermal testing, the hardware under test is thermal cycled between ambient and cryogenic temperatures, with metrology performed via photogrammetry at both warm and cold states. This process validates the thermal distortion models [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 5].

The Cryoset and Cryoproof tests were conducted to validate the thermal distortion model at the JWST level. These tests involved the combined ISIM and OTE (optical telescope element) system to characterize optical and thermal performance [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 16].

The testing and model validation were successfully completed in 2010, with detailed comparisons made between test measurements and analytical predictions from nominal and stochastic analyses for the cooldown performance of the protoflight ISIM structure and critical MGSE (Mirror Support Equipment) [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 16].

These tests and models are crucial for ensuring the optical performance of the primary mirror segments during the mission. The space simulation chamber at MSFC, capable of testing the primary mirror segments at 50 K, plays a significant role in this process [JWST_Mission_Overview_and_Status.pdf, Page 32].

In summary, the cryogenic thermal distortion of JWST's primary mirror segments is managed through comprehensive testing and modeling, ensuring that the telescope can maintain its optical performance at operational temperatures. [JWST_Cryogenic_Thermal_Distortion_Model.pdf, Page 16]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 10.091726064682007s | **Fact Recall:** 8.3% | **Telemetry:** 28.6%


NASA's James Webb Space Telescope (JWST) employs sophisticated thermal modeling and compensation techniques to address the cryogenic thermal distortion of its 18 primary mirror segments as they cool from room temperature to operational temperatures of about 35-50 Kelvin. Here's a detailed technical explanation:

1. **Thermal Modeling:**
   - **Finite Element Analysis (FEA):** NASA uses advanced FEA software to model the thermal behavior of the mirror segments and their support structures. This involves creating detailed 3D models of the mirror substrates, backplanes, and support structures.
   - **Thermal Conductivity and Expansion:** The models account for the thermal conductivity and expansion coefficients of the materials used, such as beryllium for the mirror substrates and carbon composite for the backplanes.
   - **Heat Transfer Analysis:** The models simulate heat transfer through conduction, convection, and radiation, considering the effects of the cryogenic environment and the thermal control blankets.

2. **Mirror Segment Design:**
   - **Active Cooling:** Each primary mirror segment is actively cooled by a small cryocooler, which helps maintain a uniform temperature across the segment. This active cooling is crucial for minimizing thermal distortion.
   - **Shape Memory Alloys (SMAs):** The backplane of each mirror segment is made from SMAs, which can change shape in response to temperature changes. This allows for precise control of the mirror's shape and alignment.
   - **Hexagonal Shape:** The hexagonal shape of the mirror segments is chosen to optimize the distribution of thermal loads and minimize distortion.

3. **Compensation Mechanisms:**
   - **Actuators and Fine Guidance Sensors:** JWST has 48 actuators, 24 on each side of the primary mirror, that can adjust the position of the mirror segments. These actuators are controlled by the Fine Guidance Sensor (FGS) and the Near-Infrared Camera (NIRCam) to maintain the mirror's shape and alignment.
   - **Mirror Segment Alignment:** The actuators can adjust the mirror segments to compensate for any thermal distortion. The alignment is maintained within a few microns, ensuring that the mirror's optical performance remains high even as the temperature changes.
   - **Mirror Segment Stiffness:** The stiffness of the mirror segments is carefully designed to minimize thermal distortion. The segments are made from beryllium, which has a low coefficient of thermal expansion.

4. **In-Space Calibration:**
   - **On-Orbit Testing:** After deployment, JWST undergoes extensive on-orbit testing to verify the mirror's performance and make any necessary adjustments. The Fine Guidance Sensor and the Near-Infrared Camera are used to monitor the mirror's alignment and make fine adjustments as needed.
   - **Thermal Cycle Testing:** The telescope undergoes thermal cycle testing to ensure that it can handle the temperature changes and maintain its optical performance.

5. **Operational Considerations:**
   - **Thermal Control System:** The JWST's thermal control system is designed to maintain a stable temperature environment for the mirrors. This includes the use of thermal control blankets and the active cooling of the mirror segments.
   - **Operational Temperature Range:** The operational temperature range of 35-50 Kelvin is carefully chosen to balance the need for low temperature and the practical limitations of the materials and systems used.

By combining advanced thermal modeling, precise mirror segment design, and sophisticated compensation mechanisms, NASA ensures that the JWST's primary mirror can maintain its optical performance even as it cools to cryogenic temperatures.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 2.75 / 5.0 | *Strengths:* Mentions key testing phases and the importance of cryogenic thermal testing.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Incorrect details on cryo-null figuring, incorrect materials for backplane, incorrect number of actuators, missing details on cryogenic testing and validation, incorrect operational temperature range.


---

### NASA_Q03: James Webb Space Telescope (JWST) — Sunshield Thermal Isolation Architecture

**Question:** What is the mechanical design, material composition, and thermal gradient performance of JWST's five-layer deployable sunshield?

**Primary Source Document:** `JWST_Mission_Overview_and_Status.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


JWST's five-layer sunshield is a passive thermal isolation system measuring approximately 21.2 meters by 14.2 meters (~69.5 ft by 46.5 ft, comparable to the footprint of a regulation tennis court), engineered to protect the observatory from solar, terrestrial, and lunar infrared radiation:

1. **Layer Composition & Coatings**: All five membranes are fabricated from lightweight Kapton E polyimide film. Layer 1 (sun-facing) is 0.05 mm (50 μm / 2 mil) thick, while Layers 2 through 5 are 0.025 mm (25 μm / 1 mil) thick to minimize launch mass. Layer 1 is coated on the sun-facing surface with a 100 nm vapor-deposited aluminum layer topped by a 50 nm silicon-doped coating for high solar reflectivity, low solar absorptance, and electrical conductivity to mitigate electrostatic discharge. All subsequent layers and the back of Layer 1 are vapor-deposited aluminum (100 nm).

2. **V-Groove Geometric Thermal Isolation**: The five layers are arranged in a flared, kite-shaped geometry separated by varying vacuum gaps forming V-grooves that taper outward. Heat radiated from Layer 1 into Layer 2 is primarily reflected and channeled out into the vacuum of deep space through the open perimeter gaps between layers, rather than conducting to Layer 3, 4, or 5.

3. **Thermal Telemetry & Gradient**: The sunshield achieves an effective Sun Protection Factor (SPF) of >1,000,000, dropping incoming solar power from approximately 200–300 kilowatts down to a fraction of a milliwatt on the telescope side. Telemetry records:
   - **Sun-Facing Side (Layer 1)**: Reaches peak temperatures of +85°C to +109°C (~358 K to 382 K).
   - **Cold Side (Telescope / Layer 5)**: Drops passively to approximately -233°C to -238°C (~35 K to 40 K), creating an extreme thermal gradient of roughly 320 to 340 Kelvin across a distance of only a few feet.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.855962038040161s | **Fact Recall:** 0.0% | **Telemetry:** 14.3%

**Citations:** `['JWST_Mission_Overview_and_Status.pdf, Page 2', 'JWST_Mission_Overview_and_Status.pdf, Page 35', 'JWST_Mission_Overview_and_Status.pdf, Page 52']`


The mechanical design, material composition, and thermal gradient performance of the James Webb Space Telescope's (JWST) five-layer deployable sunshield are as follows:

1. **Mechanical Design and Deployment**:
   - The sunshield is designed to be stowed within the Ariane 5 m diameter fairing and will deploy into its operational configuration after launch [JWST_Mission_Overview_and_Status.pdf, Page 2].

2. **Material Composition**:
   - The sunshield consists of five layers, with each layer made of different materials:
     - **Layer 1**: Made of heat-resistant Kapton, coated with silicon on the sun side [JWST_Mission_Overview_and_Status.pdf, Page 35].
     - **Layers 2-5**: Composed of a combination of materials including:
       - **Baffles**: E765 1 k FW Carbon Rber, E765 120 Fiber Glass, and Vapor Depooit Gold [JWST_Mission_Overview_and_Status.pdf, Page 52].
       - **Core Material**: NomexCore and Rohacell [JWST_Mission_Overview_and_Status.pdf, Page 52].
       - **Inserts**: Titanium [JWST_Mission_Overview_and_Status.pdf, Page 52].

3. **Thermal Gradient Performance**:
   - The sunshield has a significant thermal gradient between its sun-facing and dark sides:
     - **Sun Side**: Reaches 358 K (850°C) [JWST_Mission_Overview_and_Status.pdf, Page 35].
     - **Dark Side**: Stays at 40 K (-233°C) [JWST_Mission_Overview_and_Status.pdf, Page 35].
   - The sunshield measures 73 x 40 feet [JWST_Mission_Overview_and_Status.pdf, Page 35].

4. **Thermal Management**:
   - The sunshield is designed to reject -220 W of power to space in a controlled beam pattern to achieve the required observatory thermal balance and avoid thermal stray light [JWST_Mission_Overview_and_Status.pdf, Page 52].
   - The thermal balance is verified through prototype tests [JWST_Mission_Overview_and_Status.pdf, Page 52].

The provided NASA documentation does not contain sufficient data to address the specific details of the thermal distortion model validation or the exact thermal gradient performance during the deployment phase. However, the thermal gradient performance during the operational phase is well-documented [JWST_Mission_Overview_and_Status.pdf, Page 35].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 9.15883493423462s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%


The James Webb Space Telescope (JWST) features a deployable five-layer sunshield designed to protect the telescope's optics and instruments from the heat of the Sun. Here's a detailed technical overview of its mechanical design, material composition, and thermal gradient performance:

Mechanical Design:
The sunshield is a deployable structure that consists of five layers of a composite material called Kapton E. Each layer is coated with a reflective material, typically aluminum. The layers are arranged in a specific sequence to maximize their effectiveness in reflecting sunlight. The sunshield is deployed after launch when the telescope is in space, and it is designed to withstand the harsh environment of space for the duration of the mission.

The sunshield is composed of a central truss structure that supports the five layers. This truss structure is made of lightweight, yet strong materials such as aluminum and titanium. The truss is designed to be rigid enough to maintain the proper shape of the sunshield while being flexible enough to allow for deployment. The truss structure is also designed to minimize the amount of heat it absorbs, which could otherwise interfere with the sunshield's performance.

Material Composition:
The primary material used in the sunshield is a composite called Kapton E. Each layer of the sunshield is made of two layers of Kapton E, with a reflective coating applied to the outer layer. Kapton E is a polyimide film that is known for its excellent thermal stability, chemical resistance, and flexibility. The reflective coating is typically aluminum, which is applied using a vacuum deposition process to ensure a uniform and high-quality finish.

The layers are arranged in a specific sequence to maximize their effectiveness in reflecting sunlight. The first layer is the thickest and has the highest reflectivity, while the subsequent layers are progressively thinner and have slightly lower reflectivity. This arrangement helps to ensure that the sunshield can effectively block the majority of the Sun's radiation while still allowing some heat to escape from the telescope.

Thermal Gradient Performance:
The sunshield is designed to maintain a significant temperature difference between the sun-facing side and the side facing the telescope. This temperature difference is crucial for maintaining the telescope's operational temperature range, which is critical for the performance of its sensitive instruments.

The sunshield's thermal performance is optimized through the use of its multi-layer design. Each layer reflects a portion of the incoming sunlight, and the combination of these reflections helps to create a significant temperature gradient between the sun-facing side and the side facing the telescope. The temperature on the sun-facing side can reach up to 230°C (446°F), while the temperature on the side facing the telescope is kept at around -223°C (-369°F).

The sunshield's performance is further enhanced by its deployment after launch, which allows it to be folded for launch and then deployed in space. This deployment process helps to ensure that the sunshield is in the correct position and orientation to maximize its effectiveness.

In summary, the JWST's five-layer deployable sunshield is a complex and sophisticated system designed to protect the telescope's optics and instruments from the Sun's heat. Its mechanical design, material composition, and thermal gradient performance are all carefully engineered to ensure that the telescope can operate effectively in the harsh environment of space.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 2.5 / 5.0 | *Strengths:* Provides some correct details on deployment and thermal gradient.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Incorrect layer thicknesses and coating details. Incorrect temperature values for both hot and cold sides. Misses specific geometric design details and thermal isolation mechanisms. Incorrect material composition of the truss structure.


---

### NASA_Q04: Planetary Defense (DART) — Kinetic Impactor Performance & Orbital Period Change

**Question:** On what date and target did the Double Asteroid Redirection Test (DART) execute its kinetic impact, what was the pre-impact vs. post-impact orbital period of Dimorphos, and how did the measured change compare to NASA's minimum mission success criterion?

**Primary Source Document:** `DART_Planetary_Defense_Technical_Report.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


NASA's Double Asteroid Redirection Test (DART)—humanity's first planetary defense technology demonstration—targeted the near-Earth binary asteroid system (65803) Didymos:

1. **Impact Execution & Target**: On **September 26, 2022, at 23:14 UTC**, the DART spacecraft (approximate impact mass ~570-580 kg) intentionally impacted **Dimorphos**, the smaller 160-meter secondary moonlet orbiting the 780-meter primary asteroid Didymos, at a relative closing velocity of approximately **6.14 km/s** (~13,700 mph / 22,100 km/h).

2. **Orbital Period Change**: Prior to the kinetic impact, Dimorphos orbited Didymos with an established mutual orbital period of **11 hours, 55 minutes, and 17 seconds (11.921 hours / ~715.3 minutes)**. Following the impact, extensive worldwide optical lightcurve observations and planetary radar measurements (Goldstone and Green Bank) confirmed the new orbital period was shortened to **11 hours, 22 minutes, and 37 seconds (~11.372 hours)**, representing a net orbital period reduction of **32.6 minutes (± 1.9 minutes)**, or approximately **33 minutes**.

3. **Comparison with Mission Success Criterion**: NASA's pre-mission Level 1 Requirement defined the minimum success criterion as causing a change in the orbital period of at least **73 seconds (1 minute and 13 seconds)**. The actual measured reduction of ~32 to 33 minutes exceeded the minimum threshold by a factor of more than **25 times (over 2,500%)**, demonstrating the immense efficiency of kinetic impact deflection.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 8.20206332206726s | **Fact Recall:** 30.0% | **Telemetry:** 25.0%

**Citations:** `['DART_Planetary_Defense_Technical_Report.pdf, Page 24', 'DART_Planetary_Defense_Technical_Report.pdf, Page 7']`


The Double Asteroid Redirection Test (DART) executed its kinetic impact on 26 September 2022 on the asteroid Dimorphos [DART_Planetary_Defense_Technical_Report.pdf, Page 24].

Pre-impact, Dimorphos had an orbital period of 11 hours and 55 minutes. Post-impact, the orbital period was shortened to 11 hours and 23 minutes [DART_Planetary_Defense_Technical_Report.pdf, Page 7].

The measured change in the orbital period was a reduction of approximately 32 ± 2 minutes [DART_Planetary_Defense_Technical_Report.pdf, Page 7]. According to NASA's minimum mission success criterion, the mission was considered successful if the orbital period change was at least 73 minutes [DART_Planetary_Defense_Technical_Report.pdf, Page 7]. The measured change of 32 minutes significantly exceeded the minimum success criterion, indicating a successful mission.

The momentum transfer enhancement parameter, β, was reported to be 3.6, further confirming the mission's success [DART_Planetary_Defense_Technical_Report.pdf, Page 7]. This value indicates that the impactor's momentum was effectively transferred to Dimorphos, altering its orbit as predicted [DART_Planetary_Defense_Technical_Report.pdf, Page 7].

[Note: The exact minimum mission success criterion value of 73 minutes was not directly cited in the provided excerpts, but it is a well-known fact from the DART mission documentation and is commonly referenced in mission reports and summaries.]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 3.76814341545105s | **Fact Recall:** 60.0% | **Telemetry:** 25.0%


The Double Asteroid Redirection Test (DART) executed its kinetic impact on September 26, 2022, at 07:14 UTC. The target of the mission was the smaller of the Didymos binary asteroid system, Dimorphos. Prior to the impact, Dimorphos had an orbital period of approximately 11 hours and 55 minutes around its larger partner, Didymos A.

After the impact, the orbital period of Dimorphos was reduced to approximately 11 hours and 23 minutes. This change in the orbital period of Dimorphos was a direct result of the kinetic impactor's collision with the asteroid, which imparted a small but measurable change to Dimorphos's orbit.

The measured change in the orbital period of Dimorphos was 32 minutes, which is significantly more than the mission's minimum success criterion of a 73-second change. This substantial increase in the orbital period change indicates that DART successfully demonstrated the kinetic impactor technique as a potential method for planetary defense against potentially hazardous asteroids.

The mission's success in achieving a much larger than expected change in Dimorphos's orbit validated the effectiveness of the DART spacecraft and its impactor, providing valuable data for future asteroid deflection missions.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 4.0 / 5.0 | *Strengths:* Accurate date, target, and orbital period changes. Correctly identifies mission success.

- **Without-RAG Overall Score:** 4.0 / 5.0 | *Weaknesses:* Incorrect UTC time for impact. Slightly inaccurate post-impact orbital period. Does not mention the impact mass, relative velocity, or the specific measurement techniques used for the orbital period.


---

### NASA_Q05: Planetary Defense (DART) — Momentum Enhancement Factor (Beta) & Ejecta Dynamics

**Question:** How is the momentum enhancement factor (beta, beta) defined and calculated for the DART impact on Dimorphos, and what physical role did cratering ejecta recoil play in the deflection?

**Primary Source Document:** `DART_Planetary_Defense_Technical_Report.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The momentum enhancement factor, denoted by the Greek letter beta (β), quantifies the efficiency of momentum transfer in a hypervelocity kinetic impact:

1. **Mathematical Formulation**: When an impactor of mass $m$ strikes an asteroid of mass $M$ at velocity $\mathbf{v}_{imp}$, the total momentum imparted to the asteroid $\Delta \mathbf{P}$ consists of the direct momentum of the spacecraft plus the additional reaction force imparted by material ejected backwards into space:
$$\Delta \mathbf{P} = m \mathbf{v}_{imp} + \mathbf{p}_{ejecta} = \beta m \mathbf{v}_{imp}$$
Thus, $\beta$ is defined as:
$$\beta = \frac{\Delta P}{m v_{imp}} = 1 + \frac{p_{ejecta}}{m v_{imp}}$$
   - If $\beta = 1$: The impact is completely inelastic with zero ejecta recoil (pure momentum capture).
   - If $\beta > 1$: High-speed ejecta particles escaping opposite the impact direction act like a rocket thruster, boosting the deflection momentum.

2. **Physical Role of Ejecta Recoil**: High-speed imagery from DART's DRACO camera, LICIACube, and the Hubble/Webb space telescopes revealed that the hypervelocity impact at 6.14 km/s blasted thousands of metric tons of shattered rocky debris and dust away from Dimorphos at speeds exceeding the asteroid's escape velocity (~9 cm/s). This fast-moving ejecta plume created an immense backward thrust (recoil impulse) that pushed Dimorphos significantly harder than the direct kinetic blow of the spacecraft alone.

3. **Measured β Value**: Based on Dimorphos mass estimates derived from Didymos binary dynamics, NASA calculated that **$\beta$ ranged between approximately 2.2 and 4.9** (nominal consensus $\beta \approx 3.6$ assuming bulk density ~2,400 kg/m³). This proves that ejecta recoil contributed more than double to triple the deflection momentum imparted by the spacecraft body itself, demonstrating that rubble-pile asteroids are exceptionally receptive to kinetic deflection.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.716052055358887s | **Fact Recall:** 36.4% | **Telemetry:** 0.0%

**Citations:** `['DART_Planetary_Defense_Technical_Report.pdf, Page 9', 'DART_Planetary_Defense_Technical_Report.pdf, Page 10', 'DART_Planetary_Defense_Technical_Report.pdf, Page 52', 'DART_Kinetic_Impactor_Deflection_Results.pdf, Page 2', 'DART_Planetary_Defense_Technical_Report.pdf, Page 45']`


The momentum enhancement factor, denoted as β, quantifies how the ejecta produced during a deflection attempt contributes to the momentum imparted to the target. In a perfectly inelastic collision, with zero ejecta momentum, β = 1 by definition [DART_Planetary_Defense_Technical_Report.pdf, Page 9].

For the DART impact on Dimorphos, the DART project will use the velocity change imparted to the target to obtain a measure of the momentum transfer enhancement parameter, β, using the best available estimate of the mass of Didymos B. The required value of 7.3 seconds was derived from ensuring the post-impact orbital period was determined with an accuracy of at least 10%, even if only the minimum 73-second period change resulted from DART’s impact [DART_Planetary_Defense_Technical_Report.pdf, Page 9].

Impact simulations conducted in preparation for DART’s kinetic impact test indicated that there could be considerable enhancement to the momentum transferred to Dimorphos because of the ejecta produced, depending on the material strength, impact conditions, and other properties of Dimorphos and DART’s impact [DART_Planetary_Defense_Technical_Report.pdf, Page 10].

Cratering ejecta recoil played a significant role in the deflection. The DART mission's kinetic impact on Dimorphos generated ejecta plumes, which were characterized using various observational techniques. For instance, the VLT/MUSE characterization of Dimorphos ejecta from the DART impact provided insights into the ejecta plume evolution and its implications for Dimorphos [DART_Planetary_Defense_Technical_Report.pdf, Page 52]. Additionally, the DART impact ejecta plume evolution was studied in detail, showing that a particular direction-specific β will be directly determined by the DART results, and that a related direction-specific β is a figure of merit for a kinetic impact mission [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 2].

The characterization of the ejecta from the NASA/DART impact on Dimorphos, including observations and Monte Carlo models, further refined our understanding of the ejecta's role in the momentum transfer [DART_Planetary_Defense_Technical_Report.pdf, Page 45]. The results from these studies will help refine knowledge of the physical properties of asteroidal materials and predictive power of impact simulations, providing valuable information for future planetary defense missions [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 2].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 8.672434329986572s | **Fact Recall:** 27.3% | **Telemetry:** 0.0%


The momentum enhancement factor (β) is a crucial concept in understanding the effectiveness of the DART mission in deflecting the asteroid Dimorphos. This factor is defined as the ratio of the momentum delivered to the asteroid to the momentum of the impactor spacecraft before impact. For the DART mission, the β factor is particularly important as it helps quantify the change in Dimorphos' orbit around its primary body, the asteroid Didymos.

### Definition and Calculation of β

The momentum enhancement factor (β) is calculated using the following formula:

\[ \beta = \frac{m_{\text{imp}} v_{\text{imp}}}{m_{\text{target}} v_{\text{target}}} \]

Where:
- \( m_{\text{imp}} \) is the mass of the impactor (DART spacecraft).
- \( v_{\text{imp}} \) is the velocity of the impactor just before impact.
- \( m_{\text{target}} \) is the mass of the asteroid (Dimorphos).
- \( v_{\text{target}} \) is the velocity of the asteroid relative to the impactor.

For the DART mission, the β factor was designed to be around 0.1, meaning that the momentum delivered to Dimorphos would be 10% of the momentum of the DART spacecraft. This was chosen to ensure a significant but manageable change in Dimorphos' orbit.

### Role of Cratering Ejecta Recoil

Cratering ejecta recoil played a significant role in the deflection mechanism of the DART mission. When the DART spacecraft impacted Dimorphos, it created a crater and ejected a substantial amount of material from the asteroid's surface. This ejected material, due to the high velocity of the impact, imparted a significant amount of momentum back onto the asteroid.

The physical role of this ejecta recoil can be understood through the conservation of momentum. The momentum of the ejecta, which is moving away from the asteroid at high speeds, must be balanced by an equal and opposite momentum change in the asteroid itself. This momentum transfer effectively increases the overall momentum delivered to Dimorphos, enhancing the deflection effect.

### Quantitative Impact

The ejecta recoil contributed to the overall momentum transfer by providing additional momentum to the asteroid. While the primary momentum transfer is due to the direct impact of the DART spacecraft, the ejecta can significantly increase the total momentum delivered, especially if the impact is oblique or if the ejecta is ejected at a high velocity.

### Conclusion

In summary, the momentum enhancement factor (β) for the DART mission was carefully calculated to ensure a significant but controlled deflection of Dimorphos. The cratering ejecta recoil played a crucial role in enhancing the overall momentum transfer, contributing to the observed change in Dimorphos' orbit around Didymos. This mechanism demonstrated the effectiveness of kinetic impactor technology in asteroid deflection, paving the way for future planetary defense strategies.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.75 / 5.0 | *Strengths:* Provides accurate definition of β, mentions key observational techniques, and references authoritative documents.

- **Without-RAG Overall Score:** 2.5 / 5.0 | *Weaknesses:* Incorrect formula for β, incorrect β value, and lack of specific details on ejecta velocity and mass estimates.


---

### NASA_Q06: Planetary Defense (DART) — Autonomous Guidance & Optical Targeting (SMART Nav / DRACO)

**Question:** How did the Small-body Maneuvering Autonomous Real-Time Navigation (SMART Nav) system and the DRACO optical imaging camera guide DART to target Dimorphos during the final hours before impact?

**Primary Source Document:** `DART_Planetary_Defense_Technical_Report.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Because DART was approximately 11 million kilometers from Earth at impact, round-trip radio signal latency was approximately **38 to 40 seconds** (~19 seconds one-way). Ground controllers could not pilot the spacecraft in real-time. Instead, NASA employed an autonomous terminal navigation suite:

1. **DRACO Imaging Sensor**: The Didymos Reconnaissance and Asteroid Camera for Optical navigation (DRACO) was a high-resolution Ritchey-Chrétien telescopic imager (20.8 cm aperture, f/12.6) with a 2048x2048 CMOS detector. It captured visible-light streaming frames of the Didymos system at up to 1 Hz during the terminal approach, providing optical data down to millimeters per pixel just seconds before impact.

2. **SMART Nav Software Pipeline**: Developed by Johns Hopkins Applied Physics Laboratory (JPL/APL), SMART Nav ran directly on the spacecraft's radiation-hardened flight computer:
   - **Detection & Centroiding (T-4 hours to T-1 hour)**: At 4 hours out, Didymos and Dimorphos appeared as a single unresolved sub-pixel point of light. SMART Nav performed scene segmentation, background suppression, and center-of-light tracking.
   - **Target Discrimination (T-1 hour / ~60-90 minutes)**: At approximately 65 minutes before impact, Dimorphos resolved into a distinct point separated from Didymos by ~4 pixels. SMART Nav autonomously recognized Dimorphos based on orbital ephemeris models, rejected the much brighter Didymos parent asteroid, and shifted its guidance solution entirely to Dimorphos.
   - **Terminal Precision Maneuvers (T-50 minutes to impact)**: SMART Nav fed line-of-sight pointing errors directly into the guidance, navigation, and control (GNC) thruster manager, firing 12 hydrazine reaction control system (RCS) thrusters in closed-loop pulses to steer the spacecraft to impact within 17 meters of Dimorphos's center-of-figure.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 11.958693504333496s | **Fact Recall:** 18.2% | **Telemetry:** 0.0%

**Citations:** `['DART_Planetary_Defense_Technical_Report.pdf, Page 17', 'DART_Kinetic_Impactor_Deflection_Results.pdf, Page 3', 'DART_Planetary_Defense_Technical_Report.pdf, Page 24', 'DART_Planetary_Defense_Technical_Report.pdf, Page 7']`


The Small-body Maneuvering Autonomous Real-Time Navigation (SMART Nav) system and the DRACO optical imaging camera guided DART to target Dimorphos during the final hours before impact through a series of steps and processes. 

First, SMART Nav was responsible for asteroid acquisition and tracking throughout the terminal phase, autonomously guiding DART onto an impact trajectory with Dimorphos B. This was necessary due to the high closing velocity of 6 km/s, which required an onboard, autonomous approach to ensure the mission's Level 1 impact requirement could not be met with ground-based commanding. [DART_Planetary_Defense_Technical_Report.pdf, Page 17]

DRACO, the Didymos Reconnaissance & Asteroid Camera for OpNav, acquired images for the autonomous navigation system and for the Investigation Team’s analysis. During the terminal approach phase, DRACO acquired and returned images at a rate of approximately one per second, with the highest-resolution images required to have a pixel scale of 50 cm/pixel or finer, to be achieved roughly 16 seconds prior to DART’s impact. [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 3]

Optical navigation was heavily used during the final month to ensure the spacecraft was positioned to impact Dimorphos and to inform the associated trajectory correction maneuvers (TCMs). At 4 hours and 5 minutes before impact, SMART Nav took control of the spacecraft navigation. The SMART Nav system obtained its final stable track for Dimorphos 68 minutes before impact and began maneuvering toward Dimorphos 50 minutes before impact. [DART_Planetary_Defense_Technical_Report.pdf, Page 24]

On the day of impact, 26 September 2022, the spacecraft’s autonomous systems successfully detected and locked on to Dimorphos, impacting its surface within 2 meters of the center of the illuminated figure. No human intervention was required for a successful impact, demonstrating that humanity possesses the technology to perform a kinetic impact. [DART_Planetary_Defense_Technical_Report.pdf, Page 7]

The SMART Nav system, a collection of algorithms, firmware, and software, was developed as part of an Independent Research and Development effort in collaboration with APL’s Air and Missile Defense Sector. The system was designed to address the challenges of providing the navigation accuracy needed to ensure impact with the Didymos secondary, including the need to distinguish the shadowed side of the asteroid from the background and the transition from tracking the primary asteroid to tracking the secondary. [DART_Planetary_Defense_Technical_Report.pdf, Page 17]

The SMART Nav system and DRACO camera worked together to ensure DART’s successful impact on Dimorphos, highlighting the importance of autonomous navigation and real-time imaging in planetary defense missions. [DART_Planetary_Defense_Technical_Report.pdf, Page 24]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 11.029502391815186s | **Fact Recall:** 18.2% | **Telemetry:** 0.0%


The Small-body Maneuvering Autonomous Real-Time Navigation (SMART Nav) system and the DRACO optical imaging camera played crucial roles in guiding the Double Asteroid Redirection Test (DART) spacecraft to its target, the asteroid Dimorphos, during the final hours before impact. Here's a detailed technical explanation of their functions and how they worked together:

1. SMART Nav System:
   - SMART Nav is an autonomous navigation system designed to guide DART to Dimorphos without relying on ground-based commands.
   - It uses a series of star trackers and a visible-light camera to determine the spacecraft's position relative to Dimorphos.
   - The system calculates the necessary course corrections in real-time, adjusting DART's trajectory as needed.
   - SMART Nav continuously measures the spacecraft's velocity and position, comparing them to pre-programmed navigation data.
   - If the spacecraft deviates from its planned path, SMART Nav automatically calculates and implements small thruster firings to correct the trajectory.
   - The system operates in real-time, providing continuous guidance during the final hours of the mission.

2. DRACO Optical Imaging Camera:
   - DRACO (Descent, Relative, and Approach Camera) is a high-resolution camera that captures images of Dimorphos and the DART spacecraft.
   - It provides visual data to SMART Nav, allowing the system to refine the spacecraft's trajectory based on real-time observations.
   - DRACO captures images of Dimorphos at various distances, enabling SMART Nav to determine the asteroid's size, shape, and relative position.
   - The camera's high-resolution images help SMART Nav identify any unexpected features or changes in Dimorphos' appearance that could affect the spacecraft's trajectory.
   - DRACO also captures images of the DART spacecraft, allowing SMART Nav to monitor the spacecraft's orientation and position relative to Dimorphos.

3. Integration and Functionality:
   - SMART Nav and DRACO work in tandem to guide DART to Dimorphos. DRACO provides visual data, while SMART Nav processes this information and calculates course corrections.
   - The system uses a combination of star tracker data and DRACO images to create a real-time model of the spacecraft's position and trajectory.
   - SMART Nav continuously compares the model to pre-programmed navigation data, making real-time adjustments as needed.
   - The system is designed to handle unexpected situations, such as changes in Dimorphos' appearance or unexpected debris in the vicinity.
   - SMART Nav and DRACO work together to ensure that DART is on course for a successful impact with Dimorphos, even in the final hours before the event.

4. Final Hours:
   - In the final hours before impact, SMART Nav and DRACO work together to guide DART to Dimorphos with increasing precision.
   - The system uses the high-resolution images from DRACO to identify Dimorphos and track its position.
   - SMART Nav calculates the necessary course corrections based on the real-time data from DRACO and implements them using DART's thrusters.
   - The system continues to monitor the spacecraft's trajectory and make adjustments as needed, ensuring that DART is on course for a successful impact with Dimorphos.
   - SMART Nav and DRACO work together to provide real-time guidance, allowing DART to make the necessary adjustments to its trajectory in the final moments before impact.

In summary, the SMART Nav system and DRACO optical imaging camera worked together to guide DART to Dimorphos during the final hours before impact. SMART Nav used real-time data from DRACO to calculate course corrections, while DRACO provided high-resolution images of Dimorphos and the DART spacecraft. This combination of real-time navigation and high-resolution imaging allowed SMART Nav to guide DART to its target with increasing precision in the final moments before the historic impact.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 4.25 / 5.0 | *Strengths:* Accurate details on DRACO specifications, SMART Nav's autonomous functions, and the overall process of guiding DART to Dimorphos.

- **Without-RAG Overall Score:** 3.5 / 5.0 | *Weaknesses:* Contains inaccuracies in technical details (e.g., star trackers not mentioned in ground truth, incorrect camera name, missing specific technical details about DRACO and SMART Nav operations)


---

### NASA_Q07: Mars Exploration (Curiosity MSL) — Entry, Descent, and Landing (EDL) Architecture

**Question:** What were the sequential phases of the Mars Science Laboratory (Curiosity) Entry, Descent, and Landing (EDL) architecture, and how did the Sky Crane maneuver execute the rover's surface touchdown?

**Primary Source Document:** `Mars_Curiosity_MSL_EDL_Assessment.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Because the Mars Science Laboratory (Curiosity) weighed nearly 900 kg—far too massive for previous airbag landing systems—NASA engineered the groundbreaking 'Seven Minutes of Terror' Entry, Descent, and Landing (EDL) sequence consisting of four synchronized phases:

1. **Guided Hypersonic Entry**: Entering the Martian atmosphere at ~5,900 m/s (~13,200 mph) at an altitude of ~125 km inside a 4.5-meter aeroshell, the craft ejected two 75-kg tungsten balance masses to offset its center of mass, generating an aerodynamic lift-to-drag ratio ($L/D \approx 0.24$). Active RCS hydrazine thrusters performed bank-angle reversals to steer through Martian atmospheric density variations, reducing landing error from hundreds of kilometers to a 20x7 km landing ellipse.

2. **Supersonic Parachute Deceleration**: At Mach ~2.05 (~405 m/s) and ~10 km altitude, the world's largest supersonic Disk-Gap-Band (DGB) parachute (21.5 meters diameter) deployed via mortar. Twenty seconds later, the ablative heat shield was pyrotechnically jettisoned, exposing the rover, its downward-looking cameras (MARDI), and the Terminal Descent Sensor (TDS) pulse-Doppler landing radar.

3. **Powered Descent & Divert**: At ~1.8 km altitude and ~80 m/s, the rover and descent stage separated from the backshell and parachute. Eight throttleable Mars Landing Engines (MLE) running on hydrazine fired to execute an autonomous divert maneuver, flying hundreds of meters horizontally away from the falling backshell, then establishing a steady vertical descent rate of ~0.75 m/s (1.7 mph).

4. **The Sky Crane Maneuver**: At an altitude of ~20 meters above the floor of Gale Crater, the descent stage engaged the Sky Crane:
   - Three nylon-bridle cords and an electrical umbilical line unwound from a central spool, lowering the 899-kg rover 7.5 meters below the descent stage.
   - Curiosity deployed its mobility system (six-wheel rocker-bogie chassis and wheels) in mid-air to act as landing gear.
   - Upon ground touchdown, load sensors in the bridle slackened, triggering pyrotechnic guillotine cutters to sever all bridle cables in <0.5 seconds.
   - The descent stage throttled up its MLE thrusters to 100%, executing a pitched flyaway climb to crash-land at a safe distance (>650 meters away).

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.527392148971558s | **Fact Recall:** 7.7% | **Telemetry:** 0.0%

**Citations:** `['Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2']`


The Mars Science Laboratory (MSL) Curiosity rover's Entry, Descent, and Landing (EDL) architecture consisted of six sequential phases, as detailed in [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]:

1. **Exo-atmospheric Flight**: This phase occurred before the rover entered the Martian atmosphere. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

2. **Guided Entry**: During this phase, the spacecraft was guided through the Martian atmosphere using thrusters to control its trajectory. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

3. **Parachute Descent**: The largest supersonic parachute ever flown at Mars deployed to slow the descent. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

4. **Powered Descent**: After the parachute deployment, the rover used its descent stage with retro-rockets to further slow its descent. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

5. **Sky Crane**: This was a novel landing system where the rover was lowered to the surface by a hovering descent stage. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

6. **Flyaway**: This phase involved the separation of the descent stage from the rover after touchdown, allowing the descent stage to fly away to a safe distance. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

The Sky Crane maneuver executed the rover's surface touchdown as follows:

- After the powered descent phase, the rover was detached from the descent stage and lowered to the surface by a series of cables. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]
- The rover touched down on the surface while the descent stage remained hovering above it, providing additional stability and control. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]
- Once the rover was safely on the surface, the descent stage separated and flew away to a safe distance, ensuring the rover was not in danger from any potential hazards from the descent stage. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2]

These phases and maneuvers were critical for the successful landing of the Curiosity rover on Mars, as detailed in [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 2].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 10.561903715133667s | **Fact Recall:** 7.7% | **Telemetry:** 37.5%


The Mars Science Laboratory (MSL) Entry, Descent, and Landing (EDL) architecture for the Curiosity rover involved a series of carefully orchestrated phases to safely deliver the rover to the Martian surface. Here is a detailed breakdown of the sequential phases and the Sky Crane maneuver:

1. **Entry Phase:**
   - **Atmospheric Entry:** The MSL spacecraft, containing the Curiosity rover, entered the Martian atmosphere at approximately 5,800 meters per second (13,000 mph) and 125 kilometers (78 miles) above the surface. The heat shield, measuring 4.8 meters (16 feet) in diameter, protected the rover from the intense heat generated by atmospheric friction.
   - **Parachute Deployment:** At an altitude of about 12 kilometers (7.5 miles) and a speed of 1,000 meters per second (2,200 mph), the supersonic parachute deployed. This parachute was the largest ever used on a planetary entry, measuring 15 meters (49 feet) in diameter.

2. **Descent Phase:**
   - **Backshell Separation:** After the parachute had slowed the descent to about 425 meters per second (950 mph), the backshell separated from the parachute and the rover. The backshell, along with the parachute, continued to descend to the surface.
   - **Sky Crane Maneuver:** The descent stage, which included the rover and the Sky Crane system, separated from the backshell. The descent stage had its own rocket engines to control its descent. The Sky Crane maneuver involved several critical steps:
     - **Rocket Engine Cutoff (RECO):** At an altitude of about 1.2 kilometers (0.75 miles) and a speed of 160 meters per second (360 mph), the rocket engines reduced thrust to allow the rover to descend to the surface.
     - **Sky Crane Maneuver:** The descent stage, now equipped with a bridle system, lowered the rover to the surface using a tether. The Sky Crane maneuver involved a complex series of actions to ensure the rover touched down safely:
       - The rover was lowered on three nylon tethers, each 21.5 meters (70.5 feet) long.
       - The descent stage hovered about 4 meters (13 feet) above the surface.
       - The rover's wheels were deployed and the bridle system was released.
       - The descent stage then moved away from the rover, using its rear thrusters, to a safe distance.

3. **Landing Phase:**
   - **Surface Touchdown:** The rover touched down on the surface of Mars, with its wheels in contact, at approximately 1:32 AM UTC on August 6, 2012 (10:32 PM PDT on August 5, 2012). The landing site was named Gale Crater.
   - **Confirmation of Landing:** After a brief period to ensure the rover was stable and safe, the rover sent a signal to the Mars Reconnaissance Orbiter (MRO), which then relayed the signal to Earth. Confirmation of the landing was received by mission control at the Jet Propulsion Laboratory (JPL) about 14 minutes after the landing.

The Sky Crane maneuver was a critical and innovative part of the EDL process, allowing for a soft landing and ensuring the rover was placed in a stable position on the Martian surface. This approach was necessary due to the size and weight of the Curiosity rover, which required a more complex landing system compared to previous Mars missions.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.0 / 5.0 | *Strengths:* Clear and concise description of the EDL phases and Sky Crane maneuver.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Errors in speeds, altitudes, parachute size, and other technical details; omits key aspects like RCS thrusters and TDS radar.


---

### NASA_Q08: Mars Exploration (Curiosity MSL) — ChemCam Remote Geochemical Sensing & LIBS Spectroscopy

**Question:** How does the ChemCam Laser-Induced Breakdown Spectroscopy (LIBS) instrument on Curiosity determine rock and soil elemental composition from standoff distances, and what complementary role does the Remote Micro-Imager (RMI) play?

**Primary Source Document:** `Mars_Curiosity_ChemCam_LIBS_Instrument.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


ChemCam (Chemistry and Camera) is an active remote sensing package mounted on the mast of the Curiosity rover designed for rapid geochemical screening of targets without needing to position the robotic arm:

1. **LIBS Physical Principles**: ChemCam uses a Q-switched Nd:KGW solid-state laser emitting pulses at **1067 nm** with pulse energy >30 mJ and pulse duration of ~5 nanoseconds. The laser beam is focused through a 110 mm Schmidt-Cassegrain telescope onto rock or soil surfaces at standoff distances of **1.5 to 7.0 meters**:
   - Each pulse delivers power densities exceeding 10 megawatts per square millimeter ($>10^7 \text{ W/mm}^2$), vaporizing sub-milligram amounts of target material and generating an expanding, luminous optical plasma breakdown spark.
   - As the ionized plasma cools, excited atoms and ions de-excite, emitting photons at discrete, characteristic atomic emission wavelengths.

2. **Spectrometer Subsystems**: Optical light from the plasma spark is collected by the telescope and directed via an optical fiber bundle down the mast to three spectrometers inside the rover body:
   - **UV Spectrometer**: 240.1 to 342.2 nm (detects Fe, Mg, Ti, Cr, Ni, Al, Si).
   - **VIS (Violet/Visible) Spectrometer**: 382.1 to 469.4 nm (detects Ca, Al, Fe, Ti, Sr, Ba).
   - **VNIR (Near-Infrared) Spectrometer**: 474.0 to 853.2 nm (detects Na, K, O, H, Li, C, and emission continuum).
By firing a train of ~30 to 50 laser pulses at a single spot (at 3 to 10 Hz), the initial pulses blast away superficial Martian dust, allowing subsequent pulses to measure the pristine, underlying rock composition.

3. **Role of the Remote Micro-Imager (RMI)**: ChemCam incorporates the RMI, a high-resolution monochromatic camera sharing the same optical telescope. The RMI provides sub-millimeter contextual images of the laser impact pits (pit diameter ~0.3 to 0.5 mm at 3 meters), allowing scientists to tie exact elemental compositions to individual mineral grains, veins, and rock laminations.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 9.93791937828064s | **Fact Recall:** 16.7% | **Telemetry:** 0.0%

**Citations:** `['Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 1', 'Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 18', 'Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 47', 'Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 24']`


The ChemCam Laser-Induced Breakdown Spectroscopy (LIBS) instrument on the Curiosity rover determines rock and soil elemental composition from standoff distances through a process that involves laser-induced breakdown of the sample material. The laser beam from the instrument is focused on the target, creating a plasma that emits light at specific wavelengths corresponding to the elements present in the sample. This light is then collected by a telescope and analyzed using a spectrometer to determine the elemental composition [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 1].

The Remote Micro-Imager (RMI) plays a complementary role by providing high-resolution images of the target area. These images are crucial for selecting appropriate targets for LIBS analysis and for context, ensuring that the laser is accurately aimed at the desired location [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 1].

For instance, ChemCam can operate in two modes: active and passive. In the active mode, the LIBS laser is used to create a plasma, and the RMI captures images of the target area before and after the laser pulse to ensure that the correct area is being analyzed. In the passive mode, the RMI captures images of the target area, and the LIBS instrument analyzes the target based on the RMI images [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 18].

Regarding the protection of the baseline raster from dust, the instrument discards the first 5 laser shots to avoid contamination from dust. These early shots are known to show evidence of dust, and they also help in blowing away surface dust from around the LIBS pits. After these initial shots, the data from the subsequent shots are considered reliable, as there is no evidence of residual dust on calibration targets or most rocks [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 47].

The ChemCam LIBS instrument has also provided evidence of the ubiquity of water in the soils of Gale crater, Mars, through the detection of hydrogen in the LIBS spectra [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 24]. This detection is significant for understanding the history of water on Mars and its potential role in creating a habitable environment [Mars_Curiosity_ChemCam_LIBS_Instrument.pdf, Page 24].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 8.367330551147461s | **Fact Recall:** 16.7% | **Telemetry:** 0.0%


The ChemCam instrument on the Curiosity rover uses Laser-Induced Breakdown Spectroscopy (LIBS) to determine the elemental composition of rocks and soils from a standoff distance. Here's a detailed explanation of how it works and the role of the Remote Micro-Imager (RMI):

1. **Laser-Induced Breakdown Spectroscopy (LIBS) Process:**
   - **Laser Firing:** The ChemCam instrument fires a high-energy laser pulse (about 10 ns duration) at the target surface. The laser energy is typically around 30-40 mJ, depending on the target type.
   - **Plasma Generation:** The intense laser pulse generates a small plasma (a hot, ionized gas) in the target material. This plasma emits light across a wide range of wavelengths.
   - **Spectral Analysis:** The emitted light is collected by a telescope and directed to a spectrometer. The spectrometer disperses the light into its component wavelengths, creating a spectrum.
   - **Elemental Identification:** The spectrum is analyzed to identify the elements present in the target. Each element emits light at specific wavelengths, which correspond to its atomic structure. By comparing the observed spectrum to known emission spectra, the instrument can determine the elemental composition of the target.

2. **Standoff Distance Capability:**
   - The laser can operate effectively from a standoff distance of up to 7 meters. This allows the rover to analyze targets without having to approach them closely, which is beneficial for safety and to avoid contamination.
   - The laser and telescope are mounted on a mast above the rover, providing a clear line of sight to the target.

3. **Remote Micro-Imager (RMI) Role:**
   - **Target Identification:** The RMI provides high-resolution images of the target area. These images help the scientists to select specific targets for analysis and to confirm that the laser has hit the intended spot.
   - **Context Information:** The RMI images provide context about the rock or soil structure, helping to understand the target's geological context and potential for interesting compositions.
   - **Post-Analysis Verification:** After LIBS analysis, the RMI can be used to take additional images to verify the results and gather more detailed information about the target area.

4. **Data Integration:**
   - The data from the LIBS and RMI are often integrated to provide a comprehensive understanding of the target. The RMI images can help in identifying the best targets for analysis, while the LIBS data provides the elemental composition information.
   - This combination allows for a more thorough scientific investigation of the Martian surface, enhancing the rover's ability to study the planet's geology and potential habitability.

In summary, the ChemCam LIBS instrument on Curiosity provides a powerful tool for remote elemental analysis, while the RMI offers essential context and verification, working together to enhance the rover's scientific capabilities.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.75 / 5.0 | *Strengths:* Accurately describes the basic principles of LIBS and the role of RMI. Mentions key operational details and scientific findings.

- **Without-RAG Overall Score:** 4.0 / 5.0 | *Weaknesses:* Lacks specific details on laser wavelength, power density, and spectrometer ranges; omits mention of dust removal by initial pulses.


---

### NASA_Q09: Mars 2020 (Perseverance) — SHERLOC & WATSON Astrobiological Arm Instruments

**Question:** How do the SHERLOC deep-UV fluorescence and Raman spectrometer and the WATSON imaging sensor operate in tandem on Perseverance's robotic arm to detect organic compounds and potential biosignatures?

**Primary Source Document:** `Mars_2020_SHERLOC_WATSON_Imaging.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


SHERLOC and WATSON are complementary optical instruments co-located on the 2-meter robotic arm turret of the Mars 2020 Perseverance rover, engineered for non-destructive spatial mapping of organic carbon and mineralogy at microscopic scales:

1. **SHERLOC (Scanning Habitable Environments with Raman & Luminescence for Organics & Chemicals)**:
   - **Deep-UV Laser Excitation**: Utilizes a miniature neon-copper (NeCu) pulsed hollow-cathode laser emitting at **248.6 nm** in the deep ultraviolet (DUV).
   - **Dual Spectroscopic Detection**: Exciting samples in the deep-UV overcomes the fundamental limitation of visible Raman (where intense mineral fluorescence swamps weak Raman scattering):
     * **Native Fluorescence**: Emitted at **270 to 360 nm**, detecting aromatic organic molecules (1-ring to 4-ring aromatic rings) with parts-per-billion sensitivity.
     * **Resonance Raman Scattering**: Emitted at **800 to 4000 cm⁻¹** shift relative to the laser line, providing diagnostic vibrational fingerprints of key minerals (sulfates, carbonates, silicates) and aliphatic/aromatic organic functional groups.
   - **Micro-Mapping**: A high-precision internal scanning mirror rasters the 100-μm laser beam across an 8x8 mm target area, creating correlated 2D geochemical maps.

2. **WATSON (Wide Angle Topographic Sensor for Operations and e-Xploration)**:
   - Built as a high-resolution color camera (a flight-spare heritage design based on Curiosity's MAHLI), WATSON provides micro-imaging down to **13 to 30 microns per pixel**.
   - It features variable autofocus (operational from 18 mm to infinity) and white/UV LED illumination.

3. **Tandem Co-Registration**: WATSON captures microscopic context images of abraded rock patches. SHERLOC's autofocus sensor co-aligns its laser spot directly onto WATSON's color images, allowing scientists to correlate organic detections directly with mineral grains, veins, and micro-fossils before deciding to drill a sample core.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 14.863715410232544s | **Fact Recall:** 23.1% | **Telemetry:** 0.0%

**Citations:** `['Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1', 'Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2']`


The SHERLOC deep-UV fluorescence and Raman spectrometer and the WATSON imaging sensor operate in tandem to detect organic compounds and potential biosignatures on the Martian surface through a coordinated approach. SHERLOC, which includes a deep-UV laser and a spectrometer, is designed to identify and analyze organic compounds and minerals by exciting them with UV light and measuring the emitted fluorescence and Raman scattered light [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1]. WATSON, a color imaging sensor, provides the necessary context and localization for SHERLOC observations [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1].

Specifically, WATSON serves several roles in this process. First, it provides color context imaging of SHERLOC and Planetary Instrument for X-Ray Lithochemistry (PIXL) analysis locations, placing the spatial distribution of organics and mineralogy detected by SHERLOC and the elemental maps generated by PIXL within the context of rock texture and structure [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1]. Second, WATSON acquires stand-alone observations of rock structures and textures from the outcrop to the grain scale, which can be crucial for understanding the geological context of the samples [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1]. Third, WATSON images rover components and other instruments to monitor their health and condition, ensuring that the instruments are functioning correctly and can be used for further analysis [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1].

When SHERLOC identifies a target of interest, WATSON can be used to capture a suite of nested images of the target, covering a range of fields of view and resolutions to fully interrogate the target. For example, WATSON can acquire a context image (~105 µm/pixel, ~17x13 cm FOV) from 27 cm working distance to support localization of the abraded patch relative to pre-abrasion imaging, and a moderate resolution image from 10 cm (~43 µm/pixel, ~7x5 cm FOV) to capture the 4.5 cm diameter abraded patch in a single image [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2]. Additionally, SHERLOC ACI will image the interior of the abraded patch at ~10.1 µm/pixel resolution before and after SHERLOC spectroscopy measurements, providing detailed structural and textural information that can be correlated with the surface characteristics observed by WATSON [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2].

Furthermore, WATSON can also be used to image the interior of the borehole left behind after sample extraction, documenting the structure and texture within the drilled target, and permitting correlation of identifying characteristics on the acquired sample surface with the borehole interior [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2]. This imaging capability is particularly important for borehole imaging, as it allows for a comprehensive understanding of the sample's context and potential biosignatures.

In summary, WATSON and SHERLOC work together to provide a comprehensive analysis of the Martian surface, combining the high-resolution imaging capabilities of WATSON with the chemical analysis capabilities of SHERLOC to detect organic compounds and potential biosignatures [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1]. [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 1] [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 9.387950897216797s | **Fact Recall:** 23.1% | **Telemetry:** 0.0%


The SHERLOC (Scanning Habitable Environments with Raman & Luminescence for Organics and Chemicals) and WATSON (Wide Angle Topographic Sensor for Operations and Relative Navigation) instruments on the Perseverance rover work in tandem to detect organic compounds and potential biosignatures on Mars. Here's a detailed technical explanation of their operation:

1. **SHERLOC Instrument Operation:**
   - **UV Light Emission:** SHERLOC uses a laser that emits deep-UV light (253.7 nm) to illuminate the Martian surface. This specific wavelength is chosen because it is effective at exciting certain organic compounds and minerals.
   - **Fluorescence Detection:** The laser's UV light causes any organic molecules or minerals present to fluoresce, emitting light at a longer wavelength. SHERLOC's camera captures this fluorescence, which can indicate the presence of organic compounds.
   - **Raman Spectroscopy:** In addition to fluorescence, SHERLOC also performs Raman spectroscopy. When the UV light interacts with molecules, it causes a small shift in the energy of the emitted light, known as the Raman shift. This shift provides information about the molecular structure of the compounds.
   - **Data Analysis:** The fluorescence and Raman spectra are analyzed to identify specific organic compounds or mineralogical features that could be indicative of past life or organic processes.

2. **WATSON Instrument Operation:**
   - **Imaging Capabilities:** WATSON is a high-resolution camera that provides wide-angle, high-resolution imaging of the Martian surface. It can capture detailed images of the terrain, including the areas where SHERLOC is analyzing samples.
   - **Contextual Information:** WATSON provides the necessary context for SHERLOC's findings. It can capture images of the same area before and after SHERLOC's analysis, helping to determine the spatial distribution and extent of any organic compounds or biosignatures.
   - **Navigation and Guidance:** WATSON's primary function is to assist in the rover's navigation and relative navigation. However, it also serves as a valuable tool for scientific analysis by providing detailed images that can be correlated with SHERLOC's data.

3. **Tandem Operation:**
   - **Sample Selection:** The Perseverance rover's robotic arm can position SHERLOC over a target area. WATSON can capture images of the area before SHERLOC's analysis to provide context.
   - **Analysis and Correlation:** After SHERLOC has performed its analysis, WATSON can capture additional images to document the results. This allows scientists to correlate the fluorescence and Raman spectra with the visible characteristics of the surface.
   - **Data Integration:** The data from SHERLOC and WATSON are integrated to provide a comprehensive understanding of the organic compounds and potential biosignatures in the Martian regolith. This integration helps in validating the findings and providing a more complete picture of the Martian environment.

In summary, SHERLOC and WATSON work together by using SHERLOC's deep-UV fluorescence and Raman spectroscopy to detect organic compounds and WATSON's imaging to provide context and additional data for analysis. This combination allows for a more robust and accurate assessment of the Martian surface for signs of past life or organic processes.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 4.25 / 5.0 | *Strengths:* Detailed description of SHERLOC and WATSON functionalities, accurate technical details, and clear explanation of their tandem operation.

- **Without-RAG Overall Score:** 3.5 / 5.0 | *Weaknesses:* Incorrect laser wavelength for SHERLOC (253.7 nm instead of 248.6 nm), incorrect WATSON acronym, and lack of specific technical details on Raman shift range and fluorescence detection range.


---

### NASA_Q10: Mars 2020 (Perseverance) — Rock Coring, Sample Hermetic Sealing & Sample Return Depot

**Question:** What mechanisms and protocols does the Mars 2020 Perseverance rover use to drill, hermetically seal, and cache rock core samples in Jezero Crater for future Earth retrieval?

**Primary Source Document:** `Mars_2020_Astrobiology_Perseverance_Samples.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Perseverance carries the most sophisticated robotic sample collection system ever flown into space, designed to gather pristine rock and regolith cores to be returned to Earth by the joint NASA-ESA Mars Sample Return (MSR) campaign:

1. **Rotary-Percussive Coring Drill**: Mounted on the 45-kg turret at the end of the robotic arm, the coring drill utilizes hollow cylindrical drill bits pre-loaded with ultra-clean sample tubes. The drill exerts up to 40 kg of force and strikes at up to 3,000 impacts per minute while rotating, extracting solid rock cores approximately **13 mm (0.5 inches) in diameter** and **55 to 76 mm (2.2 to 3.0 inches) in length** directly into the internal tube.

2. **Adaptive Caching Assembly (ACA)**: Inside the front belly of the rover sits a secondary robotic mechanism—the 0.5-meter Sample Handling Arm (SHA). The coring tube is transferred from the external turret into the belly, where automated inspection cameras assess sample volume, measure core length, and take high-resolution multi-angle photographs.

3. **Hermetic Metal-to-Metal Seal**: Once verified, the tube is moved to a sealing station where an automated ram drives a titanium-sleeved plug into the tube opening under immense mechanical force, creating an ultra-tight, hermetic, knife-edge metal-to-metal seal to retain volatile compounds and prevent organic contamination for decades.

4. **Caching Architecture & Three Forks Depot**: Perseverance carries **43 sample tubes** (including 5 'witness tubes' containing pre-conditioned filters to capture spacecraft outgassing and background contamination). In late 2022 / early 2023, Perseverance established the world's first extraterrestrial sample depot at **Three Forks** in Jezero Crater, safely depositing **10 duplicate sample tubes** onto the surface as a backup cache, while retaining the primary set inside the rover body for direct delivery to the MSR Sample Retrieval Lander.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 11.053369045257568s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%

**Citations:** `['Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8', 'Mars_2020_Astrobiology_Perseverance_Samples.pdf, Page 1', 'Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2']`


The Mars 2020 Perseverance rover uses a percussive drill, designed by Honeybee Robotics, to collect rock core samples from a wide variety of rock types [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8]. This drill is mounted on the robotic arm of the rover and is capable of changing bits for different collection methods [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8].

After collecting the sample, the drill stores the sample in a hermetically sealed container for future analysis [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8]. The collected rock cores are pencil-sized and oriented in the absolute Martian geographic coordinates [Mars_2020_Astrobiology_Perseverance_Samples.pdf, Page 1].

The rover's Sampling and Caching Subsystem is responsible for caching the samples. The collected samples are cached in the rover's Sample Cache, which is designed to store the rock cores for eventual return to Earth [Mars_2020_Astrobiology_Perseverance_Samples.pdf, Page 1]. The cache containers are sealed to protect the samples from contamination and to preserve their integrity for future analysis [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8].

For context and localization of the samples, the WATSON imager provides imaging of the interior of the abraded patch at ~10.1 µm/pixel resolution before and after SHERLOC spectroscopy measurements [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2]. This imaging capability allows for the documentation of the structure and texture within the drilled target and the correlation of identifying characteristics on the acquired sample surface with the borehole interior [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2].

The CacheCam, part of the Sampling and Caching Subsystem, provides limited imaging of the acquired sample at one end of the sample [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2]. However, WATSON imaging can observe the interior of the borehole left behind after sample extraction, providing more comprehensive documentation of the sample's structure and texture [Mars_2020_SHERLOC_WATSON_Imaging.pdf, Page 2].

The provided NASA documentation does not contain sufficient data to address the specific mechanisms and protocols for hermetically sealing the samples before caching. However, it is implied that the samples are stored in sealed containers to protect them from contamination and preserve their integrity for future analysis [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 8].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 10.009639263153076s | **Fact Recall:** 18.2% | **Telemetry:** 0.0%


The Mars 2020 Perseverance rover employs a sophisticated suite of mechanisms and protocols to drill, hermetically seal, and cache rock core samples in Jezero Crater for potential future retrieval to Earth. Here's a detailed breakdown of the process:

1. **Drilling Mechanism:**
   - The rover uses a rotary-percussive drill, which is mounted on the end of the robotic arm. This drill can operate in two modes: percussive and rotary. The percussive mode uses a hammering action to break through hard rock, while the rotary mode uses a rotating action to grind through softer materials.
   - The drill bit is capable of penetrating up to 4.5 inches (11.4 cm) into the rock. It can collect samples ranging from 0.8 to 2.0 inches (2 to 5 cm) in length.

2. **Sample Collection:**
   - Once the drill has collected a sample, it is transferred to a coring tube within the drill. The coring tube is designed to maintain a clean, uncontaminated sample environment.
   - The sample is then pushed into a sample tube, which is part of the Sample Caching System (SCS).

3. **Sample Tube Mechanism:**
   - The SCS includes a set of sample tubes, each with a unique ID tag. These tubes are stored in a dedicated cache on the rover.
   - The sample tube is sealed using a hermetically sealed cap, which is designed to prevent contamination and maintain the integrity of the sample.

4. **Sealing and Caching:**
   - The sample tube is sealed using a hermetically sealed cap, which is designed to prevent contamination and maintain the integrity of the sample. The cap is secured using a titanium screw and a Teflon washer.
   - The sample tube is then stored in a dedicated cache on the rover. Each cache location is carefully chosen to ensure the best possible preservation of the sample.

5. **Sample Caching System (SCS):**
   - The SCS is a complex system that includes the drill, sample tubes, and caching mechanism. It is designed to work in conjunction with the Sample Analysis at Mars (SAM) and Planetary Instrument for X-ray Lithochemistry (PIXL) instruments.
   - The SCS is capable of collecting and caching up to 38 sample tubes, providing a diverse set of samples from different locations and depths within Jezero Crater.

6. **Sample Retrieval Protocol:**
   - For future retrieval, the samples would need to be collected by a future mission. The Perseverance rover is equipped with a Sample Tube Handling System (STHS) that can manipulate the sample tubes and prepare them for retrieval.
   - The STHS can place the sample tubes into a specially designed container, which would be returned to Earth by a future mission. This container would be designed to protect the samples during the journey back to Earth and to facilitate their analysis upon arrival.

7. **Sample Analysis:**
   - While the samples are cached on the rover, they can also be analyzed by the onboard instruments, such as SAM and PIXL. These instruments can provide valuable scientific data about the samples' composition and history, even before they are returned to Earth.

This comprehensive system ensures that the samples collected by the Perseverance rover are well-protected and ready for potential future analysis on Earth, providing a valuable resource for understanding the geology and potential habitability of Mars.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 2.75 / 5.0 | *Strengths:* Mentions key components like the percussive drill and hermetic sealing, and references to relevant documentation.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Contains several factual inaccuracies, such as incorrect drill penetration depth, sample length, and number of sample tubes. Includes unverified assumptions about the sealing mechanism and sample retrieval protocol.


---

### NASA_Q11: Mars Rotorcraft (Ingenuity) — Rotorcraft Aerodynamics in Thin Atmosphere

**Question:** How does the Ingenuity Mars Helicopter generate sufficient lift to fly in the thin Martian atmosphere, and what are its physical dimensions, rotor configuration, and rotor speed?

**Primary Source Document:** `Mars_Rotorcraft_Study_Ingenuity.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The Ingenuity Mars Helicopter achieved humanity's first powered, controlled aerodynamic flight on another planet by solving the extreme aerodynamic challenge of the Martian atmosphere:

1. **Atmospheric Environment**: Mars has an atmospheric surface density of only **0.015 to 0.020 kg/m³**, which is **less than 1% (<0.8%) of Earth's sea-level air density** (equivalent to an altitude of ~100,000 feet / 30 km on Earth). While Martian gravity is only ~38% of Earth's (0.38g), generating aerodynamic lift requires aggressive rotor sizing and blade design operating in an ultra-low chord Reynolds number ($Re \approx 10,000$ to $30,000$) combined with high compressibility (transonic tip Mach numbers).

2. **Rotor Configuration & Geometry**:
   - **Coaxial Counter-Rotating Configuration**: Ingenuity uses two counter-rotating two-bladed rotors stacked vertically on a coaxial mast, eliminating the need for a tail rotor (which saves critical weight and avoids tail gear transmission losses).
   - **Rotor Diameter**: **1.21 meters (4.0 feet)** across tip-to-tip, with an overall vehicle height of 0.49 meters.
   - **Blade Structure**: The four blades are custom-machined from ultra-stiff carbon-fiber-reinforced polymer composite with a syntactic foam core, engineered with high chord width and custom non-cambered/cambered low-Re airfoil profiles to delay boundary layer stall.

3. **Rotor Speed & Power Metrics**:
   - **Operating RPM**: Blades spin at nominal speeds of **2,400 to 2,700 RPM** (and up to **2,800 to 2,900 RPM** during seasonal Martian summer when rising temperatures cause atmospheric density to drop even further).
   - **Tip Speed**: Blade tips move at approximately **Mach 0.70 to 0.75** (given the cold Martian speed of sound of ~240 m/s).
   - **Vehicle Mass & Power**: Total mass is merely **1.8 kg (4.0 lbs)**. It is powered by six Sony lithium-ion cells delivering ~350 to 500 Watts of peak flight power, recharged by a mast-mounted solar panel.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.382853746414185s | **Fact Recall:** 8.3% | **Telemetry:** 12.5%

**Citations:** `['Mars_Rotorcraft_Study_Ingenuity.pdf, Page 7', 'Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 1', 'Mars_Rotorcraft_Study_Ingenuity.pdf, Page 3', 'Mars_Rotorcraft_Study_Ingenuity.pdf, Page 4', 'Mars_Rotorcraft_Study_Ingenuity.pdf, Page 1']`


The Ingenuity Mars Helicopter generates sufficient lift to fly in the thin Martian atmosphere by operating at much higher speeds and with larger surface areas for its rotor blades compared to Earth-based helicopters. The Martian atmosphere has a pressure averaging 6.36 millibars, which is 0.6% the pressure of Earth's atmosphere, and an average air density of 0.02 kg/m³, just 1.6% of Earth's 1.225 kg/m³ [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 7].

Ingenuity has a total mass of 1.8 kg and operates with a flight speed of ~10 m/s, with original flight specifications of about 90 seconds over a range of 180 meters [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 1]. The helicopter has two rotors on each of its four arms, with one optimized for hover and one for cruise [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 3].

The rotor speed also has an upper bound due to rotor tip speed constraints, but the exact rotor speed is not explicitly stated in the provided excerpts. However, the Ingenuity's rotor blades are designed to operate at much higher speeds than they would on Earth for the same mission, to compensate for the thin air and low density [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 7].

The physical dimensions of Ingenuity are not explicitly detailed in the provided excerpts, but it is noted that the Mars Science Helicopter concept vehicles, including a small advanced coaxial design, have the same rotor size as Ingenuity [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 4]. The Ingenuity is part of the Mars 2020 mission as a technology demonstrator for extraterrestrial flight [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 1].

For more detailed specifications and rotor performance, one would need to refer to the specific technical reports and studies cited, such as the rotor performance studies [16, 17, 18] and rotor blade aerodynamic optimization for advanced Martian rotorcraft [19, 20, 21] [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 1].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 6.766801357269287s | **Fact Recall:** 8.3% | **Telemetry:** 0.0%


The Ingenuity Mars Helicopter, developed by NASA's Jet Propulsion Laboratory, is designed to operate in the thin Martian atmosphere, which has about 1% of Earth's atmospheric density. To generate sufficient lift, the helicopter employs several innovative design features:

1. Rotor Configuration and Dimensions:
   - Rotor Diameter: 4 feet 9 inches (1.4 meters)
   - Rotor Spin Rate: 2,400 RPM (revolutions per minute)
   - Blade Tip Speed: 29 meters per second (about 65 mph or 105 km/h)
   - Rotor Material: The rotors are made of carbon fiber composites, which are lightweight yet strong enough to withstand the stresses of operation in the thin Martian atmosphere.

2. Lift Generation:
   - The high rotor spin rate and large diameter allow the helicopter to generate enough lift to overcome its weight in the thin Martian air. At 1.6 times the density of Earth's atmosphere at the surface, the air is still much thinner than Earth's, requiring a higher spin rate to achieve the necessary lift.
   - The rotors are designed to create a significant amount of lift at the lower atmospheric density, using a combination of blade design and aerodynamic principles.

3. Power and Control:
   - The helicopter is powered by a solar panel that charges a lithium-ion battery, allowing it to operate during the day and at night.
   - Ingenuity uses a complex system of sensors, including accelerometers, gyroscopes, and a camera, to maintain stability and control during flight.
   - The helicopter's flight control system is designed to handle the unique challenges of operating in the Martian atmosphere, including dust storms and temperature fluctuations.

4. Flight Performance:
   - Ingenuity is capable of performing short flights of up to 90 seconds, covering distances of up to 164 feet (50 meters) in a single flight.
   - The helicopter can hover, move forward, backward, and side-to-side, and perform a controlled descent to land safely.

In summary, the Ingenuity Mars Helicopter generates sufficient lift through its large rotor diameter and high spin rate, allowing it to operate in the thin Martian atmosphere. Its physical dimensions and rotor configuration are optimized for this unique environment, enabling it to perform short flights and gather valuable data about the potential for future aerial exploration on Mars.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.0 / 5.0 | *Strengths:* Provides some accurate details on atmospheric conditions and rotor design principles.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Incorrect rotor diameter, incorrect atmospheric density comparison, incorrect blade tip speed, and incorrect rotor configuration. Misses details on rotor geometry, blade structure, and specific power metrics.


---

### NASA_Q12: Mars Rotorcraft (Mars Science Helicopter) — Rotor Blade Structural Dynamics & Composite Fatigue Analysis

**Question:** What are the key structural, aeroelastic, and modal considerations identified in the 2026 NASA structural analysis of next-generation Mars Science Helicopter (MSH) rotor blades compared to Ingenuity?

**Primary Source Document:** `Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Following the extraordinary 72-flight campaign of Ingenuity (which ended in January 2024 when a blade tip struck the terrain), NASA Ames, JPL, and Langley conducted comprehensive structural, aeroelastic, and modal evaluations in 2026 to design blades for the next-generation **Mars Science Helicopter (MSH)**:

1. **Scale and Science Payload Transition**: While Ingenuity was a 1.8-kg technology demonstrator carrying zero dedicated science payloads, MSH is designed as a larger 6-rotor hexacopter (or advanced multi-rotor) with vehicle mass of **20 to 30 kg**, capable of transporting **2 to 5 kg of scientific instruments** (spectral imagers, magnetometers, samplers) over distances of several kilometers per sortie.

2. **Aeroelastic Flap-Lag Dynamics & Mach Regimes**: Because MSH rotor diameters expand to **~1.25 to 1.8 meters per rotor**, blade tip speeds operate continuously at high subsonic Mach numbers (**Mach 0.65 to 0.78**). At low Martian ambient pressures (~600 Pa), the lack of aerodynamic damping causes intense aeroelastic coupling between blade out-of-plane flapping, in-plane lead-lag motion, and torsional twisting.

3. **Composite Laminate Tailoring & Stress Concentrations**: The 2026 analysis modeled carbon-fiber-reinforced polymer (CFRP) composite plies (high-modulus carbon/epoxy layups). It identified critical interlaminar shear stresses and stress concentrations at the blade root retention clevis and transitions between the structural spar and aerodynamic skin. NASA optimized ply drop-offs and fiber orientations ([0/±45/90] balanced symmetric layups) to shift fundamental flap and torsion modal frequencies away from the integer harmonics of the rotor rotational frequency ($1/rev, 2/rev, 3/rev$), preventing destructive ground resonance and aeroelastic flutter.

4. **Fatigue Endurance & Dust Erosion**: Long-duration mission survivability (>100 flights) requires fatigue design limits below the composite micro-cracking threshold under cyclic aerodynamic loading. Furthermore, high-velocity blade-tip impacts with abrasive Martian airborne dust require leading-edge abrasion protection caps (nickel or titanium leading-edge erosion sheaths) to prevent delamination of the carbon plies.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.008925676345825s | **Fact Recall:** 9.1% | **Telemetry:** 0.0%

**Citations:** `['Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 2', 'Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 7', 'Mars_Rotorcraft_Study_Ingenuity.pdf, Page 4', 'Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 1']`


The key structural, aeroelastic, and modal considerations identified in the 2026 NASA structural analysis of next-generation Mars Science Helicopter (MSH) rotor blades compared to Ingenuity are as follows:

1. **Structural Analysis**:
   - The MSH concept was a hexacopter designed to carry dedicated payload for independent science investigations on Mars, unlike Ingenuity which had a coaxial rotor configuration [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 2].
   - Structural analyses were performed on the MSH’s load-bearing components, including the rotor arms and frame/fuselage, to ensure airworthiness standards for flight in the Martian atmosphere [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 2].

2. **Aeroelastic Considerations**:
   - Blade flexibility may yield elastic deformation that may negatively influence aerodynamic performance, especially for thin blades designed for the Martian atmosphere [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 7].
   - The structural design and weight optimization of the blades are critical to maintain structural integrity while ensuring optimal aerodynamic performance [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 7].

3. **Modal Considerations**:
   - The MSH was a proposed vehicle concept that would perform science investigations independently of a land-based vehicle, indicating the need for robust modal analysis to ensure stability and control during flight [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 2].
   - The performance results from the study indicate that optimized rotor design enables a substantial increase in science payload capability, hover time, and range compared to the first-generation Ingenuity design [Mars_Rotorcraft_Study_Ingenuity.pdf, Page 4].

These considerations highlight the need for advanced structural and aerodynamic design to support the operational requirements of next-generation Mars rotorcraft. The MSH concept aims to bridge the gap between spacecraft and aircraft best practices to ensure the feasibility and viability of successful mission performance [Mars_Science_Helicopter_Blade_Structural_Analysis_2026.pdf, Page 1].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 7.5552754402160645s | **Fact Recall:** 9.1% | **Telemetry:** 0.0%


Based on my general knowledge, the 2026 NASA structural analysis of the next-generation Mars Science Helicopter (MSH) rotor blades would likely consider several key factors compared to the Ingenuity helicopter. While I don't have access to the specific 2026 analysis, I can provide a technical overview of the considerations that would be relevant:

1. Structural Integrity:
   - Material selection: The MSH may use advanced composite materials for improved strength-to-weight ratio and durability in the Martian environment.
   - Blade design: Optimized airfoil shapes and cross-sections for better lift and reduced drag.
   - Joint and hinge design: More robust mechanisms to handle increased payload and higher operational temperatures.

2. Aeroelasticity:
   - Blade flexibility: Analysis of blade deflection and twist under various operating conditions.
   - Flutter characteristics: Ensuring the helicopter can operate safely at higher speeds and altitudes.
   - Vibration modes: Identifying and mitigating potential resonance frequencies that could cause structural failure.

3. Modal Analysis:
   - Natural frequencies: Determining the helicopter's natural modes of vibration to avoid resonance with operational loads.
   - Mode shapes: Visualizing how the structure deforms during different modes of vibration.
   - Dynamic response: Evaluating how the helicopter responds to external disturbances like wind gusts.

4. Environmental Considerations:
   - Martian atmospheric conditions: Accounting for the thin, cold Martian atmosphere with lower air density and higher dust content.
   - Dust accumulation: Designing for reduced impact of dust on aerodynamic performance and structural integrity.
   - Temperature variations: Ensuring materials and components can withstand extreme temperature swings.

5. Performance Enhancements:
   - Increased lift: Optimizing blade design for higher lift-to-drag ratios.
   - Extended range: Improving endurance and range through more efficient blade design.
   - Payload capacity: Allowing for larger payloads or additional scientific instruments.

6. Safety and Reliability:
   - Redundancy: Implementing backup systems for critical components.
   - Fault tolerance: Designing systems to continue operation in the event of partial failure.
   - Reducing risk: Minimizing the likelihood of catastrophic failure through rigorous testing and design validation.

7. Integration with Mars 2026 Mission:
   - Compatibility with mission requirements: Ensuring the helicopter can operate within the constraints of the overall mission.
   - Interoperability: Designing the helicopter to work seamlessly with other Mars 2026 mission assets.

These considerations would be part of a comprehensive structural analysis to ensure the next-generation Mars Science Helicopter can perform its mission objectives more effectively than Ingenuity while operating in the challenging Martian environment.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.0 / 5.0 | *Strengths:* Mentions key differences in design and some structural considerations.

- **Without-RAG Overall Score:** 2.75 / 5.0 | *Weaknesses:* Lacks specific details and numbers from the 2026 analysis, includes unverified assumptions and omissions (e.g., no mention of MSH's 6-rotor hexacopter design, specific Mach regimes, or composite laminate tailoring details).


---

### NASA_Q13: Artemis Program (SLS / Orion) — Space Launch System Core Stage Propulsion Architecture

**Question:** What propulsion architecture powers the Space Launch System (SLS) Core Stage, what are the propellants and cryogenic temperatures, and how do the RS-25 engines and Solid Rocket Boosters combine at liftoff?

**Primary Source Document:** `Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The NASA Space Launch System (SLS) Core Stage—the structural and propulsive backbone of the Artemis lunar exploration vehicle—measures **212 feet (64.6 meters) in height** and **27.6 feet (8.4 meters) in diameter**:

1. **Propellant Volumes & Cryogenics**: The Core Stage contains two colossal insulated aluminum-lithium tanks holding a combined total of **733,000 gallons (2.77 million liters / ~2.3 million pounds)** of cryogenic propellants:
   - **Liquid Hydrogen (LH₂)**: 537,000 gallons stored in the forward tank at an ultra-deep cryogenic temperature of **-423°F (20.3 Kelvin)**.
   - **Liquid Oxygen (LOX)**: 196,000 gallons stored in the aft tank at **-297°F (90.2 Kelvin)**.

2. **RS-25 Engine Configuration**: The Core Stage is powered by **four Aerojet Rocketdyne RS-25D/E engines** arranged in a square cross-pattern in the engine section. The RS-25 operates on a staged-combustion cycle with high chamber pressures (~3,000 psia):
   - For SLS Block 1 (Artemis I and II), the engines operate at **109% of their original Space Shuttle Rated Power Level (RPL)**, producing approximately **512,000 pounds-force (2.28 MN) of vacuum thrust each**, yielding a combined Core Stage vacuum thrust of over **2.0 million lbf (9.1 MN)**.
   - The four engines burn continuously for approximately **8 minutes and 20 seconds (500 seconds)** during ascent.

3. **Combined Liftoff Thrust with Twin Solid Rocket Boosters (SRBs)**:
   - Mounted on either side of the Core Stage are **two five-segment Solid Rocket Boosters (SRBs)**—the largest solid-propellant motors ever flown, burning Polybutadiene Acrylonitrile (PBAN) ammonium perchlorate composite propellant.
   - Each SRB delivers **3.6 million lbf (16.0 MN)** of maximum thrust at liftoff.
   - At liftoff, the four RS-25 engines (~1.6 million lbf sea-level thrust) and the twin SRBs (7.2 million lbf) ignite simultaneously to generate a staggering **8.8 million pounds-force (39.1 MN) of total liftoff thrust**—15% more thrust than the Apollo Saturn V.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 8.052592039108276s | **Fact Recall:** 9.1% | **Telemetry:** 0.0%

**Citations:** `['Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4', 'Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf, Page 8', 'Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 2']`


The Space Launch System (SLS) Core Stage is powered by four RS-25 liquid hydrogen/liquid oxygen (LH2/LOX) engines. The propellants used are liquid hydrogen for fuel and liquid oxygen for oxidizer. The RS-25 engines are capable of producing sea level thrust of 418,000 pounds (1,890 kN) and vacuum thrust of 512,000 pounds (2,300 kN) [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4].

At liftoff, the SLS Core Stage combines with two five-segment solid rocket boosters. The solid rocket boosters are powered by solid propellant, with each booster producing 3.6 million pounds (16,000 kN) of thrust, totaling 7.2 million pounds (32,000 kN) for both [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4].

The RS-25 engines and solid rocket boosters are integrated into the SLS configuration as follows: The RS-25 engines are located in the core stage, while the solid rocket boosters are attached to the core stage via the launch vehicle stage adapter (LVSA) [Artemis_SLS_Rocket_Artemis_II_Readiness_2026.pdf, Page 8]. The combined thrust at liftoff for the Block 1 configuration is 8.8 million pounds (39,100 kN) [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 2].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 7.310850143432617s | **Fact Recall:** 36.4% | **Telemetry:** 0.0%


The Space Launch System (SLS) Core Stage is powered by a combination of RS-25 engines and Solid Rocket Boosters (SRBs). Here's a detailed technical breakdown:

1. RS-25 Engines:
   - The SLS Core Stage uses four RS-25 engines, which are derived from the Space Shuttle Main Engines.
   - Each RS-25 engine produces approximately 512,000 pounds of thrust.
   - The engines are fueled by liquid hydrogen (LH2) and liquid oxygen (LOX).
   - Cryogenic temperatures for LH2 and LOX are -423°F (-253°C) and -297°F (-183°C), respectively.
   - The engines are arranged in a crossfire configuration, with two on each side of the stage.

2. Solid Rocket Boosters (SRBs):
   - The SLS Core Stage also uses two SRBs, which are located at the base of the stage.
   - Each SRB produces about 3.3 million pounds of thrust.
   - The SRBs are fueled by a mixture of aluminum and ammonium perchlorate, with a rubber binder.
   - The SRBs are ignited simultaneously with the RS-25 engines, providing an initial boost to the rocket.

3. Combining RS-25 Engines and SRBs at Liftoff:
   - At liftoff, the SRBs provide the initial thrust, which is crucial for overcoming gravity and reaching the speed needed to ignite the RS-25 engines.
   - The SRBs burn for about 2 minutes, after which they are jettisoned and fall into the ocean.
   - The RS-25 engines ignite shortly after SRB separation, providing continuous thrust throughout the first stage of the flight.
   - The combined thrust from the RS-25 engines and the SRBs is approximately 8.8 million pounds of thrust at liftoff.

4. Cryogenic Management:
   - The LH2 and LOX tanks in the Core Stage are pressurized and maintained at cryogenic temperatures to keep the propellants in a liquid state.
   - The tanks are insulated to minimize heat transfer and maintain the required temperatures.
   - The propellants are fed to the engines through a network of pipes and valves, which are designed to handle the extreme cold and pressure conditions.

This propulsion architecture provides the necessary thrust and performance for the SLS to achieve the required trajectories for its various missions, including crewed and uncrewed deep space exploration.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 4.25 / 5.0 | *Strengths:* Accurate thrust values, correct propellants, and proper integration of RS-25 engines and SRBs.

- **Without-RAG Overall Score:** 3.75 / 5.0 | *Weaknesses:* Incorrect SRB thrust value, incorrect propellant mixture for SRBs, and incorrect RS-25 engine arrangement.


---

### NASA_Q14: Artemis Program (SLS / Orion) — Artemis I Flight Telemetry & Translunar Injection Validation

**Question:** What were the key flight performance metrics, translunar injection parameters, and reentry results recorded during the uncrewed Artemis I test flight of SLS and Orion?

**Primary Source Document:** `Artemis_I_Flight_Results_and_Path_Forward.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Launched on **November 16, 2022, at 1:47 a.m. EST**, the uncrewed Artemis I mission executed a flawless 25.5-day flight demonstrating the end-to-end integration of the SLS rocket, Orion spacecraft, and Exploration Ground Systems:

1. **Core Stage & ICPS Insertion Performance**:
   - The SLS Core Stage burned for 500 seconds, inserting the Interim Cryogenic Propulsion Stage (ICPS) and Orion into an initial 972x16 nautical mile insertion orbit within **0.1% of target trajectory velocity**.
   - After an initial perigee raise maneuver, the ICPS (powered by a single Aerojet Rocketdyne RL10B-2 engine burning LH₂/LOX) executed the critical **Translunar Injection (TLI) burn** lasting approximately **18 minutes**. The burn added **~2,800 m/s (~9,200 ft/s / 6,260 mph)** of velocity, placing Orion onto a precision lunar transfer trajectory with a targeting error of **less than 0.05%**.

2. **Distant Retrograde Orbit (DRO) Telemetry**:
   - Orion entered a high-altitude Distant Retrograde Orbit around the Moon, using gravity-assist burns (Outbound Powered Flyby within 81 miles of the lunar surface).
   - On November 28, 2022, Orion reached its maximum distance from Earth at **268,563 miles (432,210 km)**—breaking the record set by Apollo 13 for the farthest distance traveled by any human-rated spacecraft from Earth.

3. **Skip Reentry & Heat Shield Performance**:
   - Returning directly from lunar distance, Orion demonstrated a historic **skip-entry technique**, dipping into the upper atmosphere, skipping back up to bleed off energy and precisely control touchdown location, before performing final descent.
   - **Reentry Velocity**: **39,400 km/h (24,500 mph / ~11 km/s / Mach 32)**.
   - **Ablative Thermal Protection**: The 5.0-meter Avcoat ablative heat shield endured temperatures of **nearly 5,000°F (~2,760°C)**. Post-flight inspection revealed unexpected liberation (spalling/char loss) of small Avcoat material fragments, prompting extensive root-cause investigation prior to the crewed Artemis II flight.
   - Orion splashed down safely in the Pacific Ocean off Baja California on **December 11, 2022, after traveling 1.4 million miles**.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 8.59658694267273s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%

**Citations:** `['Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4', 'Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 1']`


The key flight performance metrics, translunar injection parameters, and reentry results recorded during the uncrewed Artemis I test flight of SLS and Orion are as follows:

1. **Launch and Initial Orbit Insertion:**
   - The SLS core stage and boosters inserted the ICPS and Orion into an initial Earth orbit at a velocity of 25,579.86 ft./sec. (7,796.74 m/sec.), which was 6.58 ft./sec. (2.01 m/sec.) off nominal, a difference of 0.026%. [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4]

2. **Translunar Injection:**
   - The mission sent an uncrewed Orion spacecraft into a distant retrograde orbit about the Moon. [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 1]
   - The predicted orbital insertion parameters were 975 mi. (1,560 km) by 16 mi. (25.7 km), with actual parameters being 972.1 mi. (1,564 km) by 16 mi. (25.7 km), a difference of 0.30%. [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 4]

3. **Reentry:**
   - Orion splashed down approximately 80 miles off the coast of Baja, California, at the conclusion of the mission on December 11. [Artemis_I_Flight_Results_and_Path_Forward.pdf, Page 1]

The provided NASA documentation does not contain sufficient data to address this aspect: specific reentry performance metrics or detailed translunar injection parameters beyond the orbital insertion details.

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 7.779368877410889s | **Fact Recall:** 0.0% | **Telemetry:** 33.3%


During the uncrewed Artemis I test flight, the Space Launch System (SLS) and Orion spacecraft demonstrated several key flight performance metrics, translunar injection parameters, and reentry results. Here is a detailed technical summary based on my internal training:

Flight Performance Metrics:
1. Launch Performance: The SLS core stage successfully burned for 8.5 minutes, producing 2.0 million pounds of thrust. The four RS-25 engines operated nominally, achieving a total of 1.6 million pounds of thrust each.
2. Orion Performance: Orion's service module performed as expected, with the European Service Module's 8 engines firing multiple times to achieve the necessary trajectory. The service module's solar arrays deployed successfully, providing power to the spacecraft.
3. Trajectory Performance: Orion's trajectory was closely monitored and adjusted as needed, with the spacecraft successfully achieving the required trans-lunar injection (TLI) velocity of approximately 3.65 km/s (12,800 ft/s).

Translunar Injection Parameters:
1. Injection Burn: The service module's 8 engines fired for 6 minutes and 29 seconds, providing the necessary delta-v to achieve the TLI and send Orion on its trajectory to the Moon.
2. Injection Velocity: As mentioned, Orion achieved a velocity of about 3.65 km/s (12,800 ft/s) at the end of the TLI burn.
3. Injection Trajectory: Orion's trajectory was carefully calculated to ensure a safe and efficient journey to the Moon, with the spacecraft following a lunar flyby trajectory.

Reentry Results:
1. Entry Interface: Orion reentered Earth's atmosphere at approximately 24,200 mph (38,900 km/h) at an angle of 30 degrees.
2. Heat Shield Performance: The Avcoat heat shield on Orion's crew module performed as expected, with temperatures reaching over 5,000°F (2,760°C) during reentry.
3. Parachute Deployment: Orion's three main parachutes deployed successfully, slowing the spacecraft from 340 mph (547 km/h) to a safe splashdown speed of 20 mph (32 km/h).
4. Splashdown: Orion splashed down in the Pacific Ocean, approximately 270 miles (434 km) west of Baja California, as planned.

Overall, the Artemis I mission demonstrated the readiness of the SLS and Orion spacecraft for crewed missions to the Moon. The flight performance metrics, translunar injection parameters, and reentry results were all within acceptable ranges, with some minor deviations that were expected and managed effectively.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.75 / 5.0 | *Strengths:* Accurate details on initial orbit insertion velocity and minor discrepancies, well-grounded in provided documentation.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Incorrect launch date and time; incorrect core stage burn duration and thrust; incorrect TLI burn duration and velocity; incorrect reentry velocity and angle; incorrect splashdown location.


---

### NASA_Q15: Artemis Program (Lunar Science) — Lunar South Pole Strategy & Permanently Shadowed Regions

**Question:** What are the primary scientific exploration objectives and target geological environments defined in NASA's Integrated Lunar Science Strategy for Artemis surface missions at the Lunar South Pole?

**Primary Source Document:** `Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


NASA's Integrated Lunar Science Strategy shifts lunar exploration from the equatorial basaltic plains explored during Apollo to the rugged, ancient terrains of the **Lunar South Pole** (centered around craters such as Shackleton, Haworth, Shoemaker, and Faustini inside the ancient South Pole-Aitken Basin):

1. **Permanently Shadowed Regions (PSRs) & Cryogenic Cold Traps**:
   - Because the Moon has an axial tilt of only **1.54°**, the rim of deep impact craters casts permanent shadows where sunlight has not shone for over two billion years.
   - **Thermal Telemetry**: Temperatures inside PSRs plunge passively to **25 to 40 Kelvin (-415°F to -388°F)**—substantially colder than the surface of Pluto. These extreme cryogenic conditions create stable 'cold traps' that preserve water ice ($H_2O$), hydroxyls, carbon monoxide ($CO$), methane ($CH_4$), ammonia ($NH_3$), and other volatile species delivered by cometary and asteroidal impacts over solar system history.

2. **Primary Science Objectives**:
   - **Planetary Volatile Chronology**: Drill, excavate, and cryogenically return core samples of PSR regolith to establish the provenance, isotopic ratios (D/H ratios), and historical delivery mechanisms of water and organics to the Earth-Moon system.
   - **In-Situ Resource Utilization (ISRU) Ground-Truthing**: Quantify the depth, lateral distribution, physical state (granular ice crystals vs. cemented regolith ice permafrost), and concentration (estimated 5 to 10+ weight percent) of water ice to support future rocket propellant production ($LOX/LH_2$).
   - **Ancient Crustal Geochemistry & Impact History**: Sample impact melt sheets from the **South Pole-Aitken (SPA) Basin**—the oldest and deepest confirmed impact structure on the Moon (over 2,500 km across)—to probe deep lunar mantle material and calibrate the impact chronology of the inner solar system.

3. **Surface Deployments & Quotas**: Artemis astronauts will deploy long-lived autonomous geophysical stations (seismometers, heat-flow probes, retroreflectors) and utilize specialized cryogenic sealed sample containers to transport volatile-bearing cores back to Earth at sub-100 K temperatures.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.662416219711304s | **Fact Recall:** 20.0% | **Telemetry:** 0.0%

**Citations:** `['Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 27', 'Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 10', 'Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 33', 'Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 43', 'Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 53']`


The primary scientific exploration objectives and target geological environments defined in NASA's Integrated Lunar Science Strategy for Artemis surface missions at the Lunar South Pole are as follows:

1. **Primary Scientific Exploration Objectives:**
   - **Uncover the Record of Solar System Origin and Early History:** This objective is captured under LPS-1 [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 27].
   - **Advance Understanding of Geologic Processes Affecting Planetary Bodies:** This objective is captured under LPS-2 [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 27].

2. **Target Geological Environments:**
   - The Lunar South Pole is the initial exploration target, with the ultimate goal of global access [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 27].
   - Specific challenges include the South Pole-Aitken (SPA) Basin Sample Return, Lunar Geophysical Network, Cryogenic Volatile Sample Return, Lunar Chronology, Lunar Formation and Evolution, and Lunar Volatiles [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 10].

3. **Supporting Infrastructure:**
   - Geologic mapping is a critical component, with NASA working closely with the USGS to define a coordinated geologic mapping effort for the lunar south pole [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 33].

4. **Mission-Supporting Infrastructure:**
   - NASA is continuing to assemble an Artemis Science Team to identify and advocate for the highest-priority science questions for Artemis [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 43].

5. **Strategic Directions:**
   - The strategy includes developing a South Pole Aitken sample return and exploration science definition team to further flesh out science objectives and measurement requirements [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Page 53].

These objectives and environments are central to the Artemis Program's scientific goals and will guide the exploration and mission planning for the Lunar South Pole. [Artemis_Lunar_Science_Strategy_Implementation_Plan_2024.pdf, Pages 27, 10, 33, 43, 53]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 6.225183486938477s | **Fact Recall:** 30.0% | **Telemetry:** 0.0%


NASA's Integrated Lunar Science Strategy for Artemis surface missions at the Lunar South Pole focuses on several key scientific exploration objectives and target geological environments. These objectives are designed to support the overall Artemis program goals of lunar exploration and preparation for future missions to Mars.

Primary Scientific Exploration Objectives:
1. Investigate the lunar South Pole's unique geological and environmental characteristics, including permanently shadowed regions (PSRs) and areas with potential water ice deposits.
2. Characterize the lunar South Pole's regolith and surface materials to understand their composition and potential resources.
3. Study the South Pole's geological history, including the formation and evolution of the lunar crust in this region.
4. Assess the potential for lunar South Pole regions to support long-term human habitation and operations.
5. Conduct in-situ resource utilization (ISRU) experiments to demonstrate the extraction and use of lunar materials.

Target Geological Environments:
1. Permanently Shadowed Regions (PSRs): These areas are of particular interest due to their potential to harbor water ice deposits. The PSRs are located in deep craters near the lunar poles, where sunlight never reaches, and temperatures remain extremely cold.
2. High-Latitude Volcanic Terrains: These areas, including the South Pole-Aitken Basin, offer insights into the Moon's volcanic history and the distribution of lunar mare basalts.
3. South Pole-Aitken Basin: This is the largest known impact basin in the solar system, providing a unique opportunity to study the Moon's deep interior and the geological processes that have shaped its surface.
4. High-Reflection Areas: These regions, often associated with ice deposits, are of interest for their potential to support future human missions and scientific research.
5. Regolith and Surface Materials: The diverse regolith and surface materials in the lunar South Pole offer opportunities to study the Moon's geological history and the effects of space weathering.

The Artemis program aims to use these scientific objectives and target environments to advance our understanding of the Moon and prepare for future human missions to the lunar surface and beyond. The data collected from these missions will inform the development of technologies and strategies for sustainable lunar exploration and potential future Mars missions.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.0 / 5.0 | *Strengths:* Cites specific documents and pages, mentions key objectives and environments.

- **Without-RAG Overall Score:** 3.75 / 5.0 | *Weaknesses:* Lacks specific details on thermal telemetry, isotopic ratios, and cryogenic conditions; misses specific craters and exact temperatures; omits details on drilling, cryogenic return, and ISRU ground-truthing.


---

### NASA_Q16: Artemis Program (Human Landing System) — HLS Multi-Lander Architectures & In-Space Propellant Transfer

**Question:** What are the architectural differences, cryogenic propellant requirements, and operational concepts between SpaceX Starship HLS and Blue Origin Blue Moon for Artemis crewed lunar landings?

**Primary Source Document:** `Artemis_Human_Landing_System_HLS_Update_2025.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


Under NASA's NextSTEP Appendix H and Sustaining Lunar Development (Option A/B and SLD) contracts, NASA selected two commercial providers to develop independent, dissimilar Human Landing Systems (HLS) for Artemis surface missions:

1. **SpaceX Starship HLS (Artemis III & IV)**:
   - **Vehicle Architecture**: A massive 50-meter-tall, 9-meter-diameter stainless-steel single-stage lunar lander derived from the Starship upper stage, featuring an expansive crew cabin, forward RCS thruster ring, high-mounted landing thrusters (to avoid blowing high-velocity regolith dust and digging craters), and an elevator mechanism to lower astronauts 30+ meters to the lunar surface.
   - **Propellant System**: Powered by Raptor 3 engines burning cryogenic **liquid methane ($CH_4$) and liquid oxygen ($LOX$)**.
   - **Operational Concept & In-Space Refueling**: Requires an unprecedented in-space cryogenic propellant transfer campaign: a Starship Propellant Depot is launched to Low Earth Orbit (LEO), followed by multiple Starship tanker flights (estimated 10 to 15+ flights) that transfer cryogenic $CH_4$ and $LOX$ into the depot. The Starship HLS launches empty, refuels in LEO, and burns directly for Near-Rectilinear Halo Orbit (NRHO) around the Moon to dock with Orion.

2. **Blue Origin Blue Moon National Team (Artemis V+)**:
   - **Vehicle Architecture**: Developed under the Sustaining Lunar Development (SLD) contract by Blue Origin with Lockheed Martin, Draper, Boeing, Astrobotic, and Honeybee Robotics. A 16-meter tall vehicle tailored specifically to fit within a standard 7-meter payload fairing of the New Glenn rocket.
   - **Propellant System**: Uses BE-7 deep-throttling engines burning high-efficiency **liquid hydrogen ($LH_2$) and liquid oxygen ($LOX$)**.
   - **Operational Concept & Cryogenic Storage**: Operates with a dedicated Cislunar Transporter. Storing $LH_2$ at -423°F over multi-week lunar missions requires active 20 Kelvin cryocoolers, zero-boil-off sunshields, and in-space transfer of cryogenic hydrogen in cislunar space.

3. **Operational Mission Profile**: In both architectures, the 4-person astronaut crew launches from Earth atop the SLS rocket inside Orion. Orion flies to NRHO and docks with the pre-staged HLS lander. Two astronauts transfer to HLS for a 6.5-day to 30-day surface stay conducting EVAs, then launch back from the Moon to redock with Orion for the return to Earth.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 6.5843706130981445s | **Fact Recall:** 18.2% | **Telemetry:** 0.0%

**Citations:** `['Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 10', 'Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 4', 'Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 11']`


The provided NASA documentation does not contain sufficient data to address the architectural differences, cryogenic propellant requirements, and operational concepts between SpaceX Starship HLS and Blue Origin Blue Moon for Artemis crewed lunar landings. The excerpts primarily discuss the contracts, mission roles, and development progress of the landers but do not provide detailed technical specifications or operational concepts. 

For instance, [Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 10] mentions that Blue Origin is developing the Blue Moon MK2 lander for Artemis V, and [Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 4] states that SpaceX is contracted to provide the lunar landing for Artemis IV and V, but neither excerpt provides the specific details requested. 

[Artemis_Human_Landing_System_HLS_Update_2025.pdf, Page 11] notes that both SpaceX and Blue Origin have completed Certification Baseline Reviews for their cargo landers, but it does not specify the differences or requirements for crewed missions. 

Therefore, based on the provided excerpts, the necessary technical details to fully answer the query are not available.

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 5.869692087173462s | **Fact Recall:** 18.2% | **Telemetry:** 0.0%


Based on my general knowledge, here are the key architectural differences, cryogenic propellant requirements, and operational concepts between SpaceX Starship HLS and Blue Origin Blue Moon for potential Artemis crewed lunar landings:

Architectural Differences:
1. Starship is a fully reusable, two-stage-to-orbit vehicle designed for both crew and cargo. It stands 50 meters tall and has a diameter of 9 meters. Blue Moon is a lander designed to carry a crew of four and has a diameter of 8 meters.
2. Starship uses methane and liquid oxygen as propellants. Blue Moon uses a combination of liquid hydrogen and liquid oxygen.
3. Starship is designed for multiple flights and rapid turnaround. Blue Moon is intended to be a single-use lander.

Cryogenic Propellant Requirements:
1. Starship requires approximately 160,000 kg of methane and 240,000 kg of liquid oxygen for a trans-lunar injection (TLI) mission.
2. Blue Moon requires about 120,000 kg of liquid hydrogen and 240,000 kg of liquid oxygen for a TLI mission.

Operational Concepts:
1. Starship would be launched from Kennedy Space Center, Florida, and perform a direct ascent to the lunar surface. It would land in the South Pole-Aitken Basin or another designated area.
2. Blue Moon would be launched from Kennedy Space Center and would first dock with a lunar orbiting spacecraft. It would then perform a powered descent to the lunar surface and land in the polar regions.

Both vehicles are designed to support long-term lunar exploration and habitation. Starship is part of SpaceX's broader Mars colonization plans and could potentially be used for multiple Artemis missions. Blue Moon is specifically designed for the Artemis program and would be the first dedicated lunar lander since Apollo.

It's important to note that these details are based on publicly available information and may not reflect the most up-to-date or finalized designs. Both companies are continuously evolving their concepts and requirements.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 2.0 / 5.0 | *Strengths:* Clear and precise language, acknowledges lack of data in provided documentation.

- **Without-RAG Overall Score:** 3.25 / 5.0 | *Weaknesses:* Contains inaccuracies in vehicle dimensions, propellant requirements, and operational details; lacks specific mission profiles and in-space refueling concepts.


---

### NASA_Q17: Flagship Space Telescopes (Hubble) — Servicing Mission 3A Avionics & Gyroscope Emergency Overhaul

**Question:** Why was Hubble Servicing Mission 3A (SM3A) launched ahead of schedule, and what specific avionics, gyroscope, and guidance upgrades were installed during STS-103?

**Primary Source Document:** `Hubble_Space_Telescope_Servicing_Mission.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


NASA launched Hubble Servicing Mission 3A (STS-103) aboard Space Shuttle Discovery in **December 1999** as an emergency contingency mission:

1. **Pre-Mission Crisis (Gyroscope Failures)**:
   - Hubble requires at least three operating rate-sensing gyroscopes to perform precision pointing and astronomical science observations.
   - Throughout 1999, gyroscopes began failing sequentially. When the fourth of its six gyroscopes failed on **November 13, 1999**, Hubble could no longer maintain science pointing and automatically entered a protective 'zero-gyro safe mode' (pointing its solar panels at the Sun and shutting down all science).
   - Rather than waiting for the originally planned full Servicing Mission 3 in late 2000, NASA split the mission into SM3A and SM3B, rushing SM3A into orbit in December 1999.

2. **Critical Hardware Replacements & Upgrades**:
   - **Rate Sensor Units (RSUs)**: Astronauts replaced all three RSUs (each housing two rate-sensing gyroscopes), restoring Hubble to a complete complement of **six brand-new gyroscopes** with improved gas-bearing fluid and electrical leads.
   - **Main Computer Upgrade (DF-224 to Intel 80486)**: The original, obsolete DF-224 flight computer (which had only 48,000 24-bit words of memory and a clock speed of 1.25 MHz) was replaced by an **Intel 80486 25-MHz 32-bit radiation-hardened processor**. This upgrade increased Hubble's computational processing speed by **20 times (2,000%)** and expanded its flight software memory by **6 times**, enabling autonomous flight software routines and drastically reducing ground commanding overhead.
   - **Solid State Recorder (SSR)**: Replaced a failing 1970s-era reel-to-reel magnetic tape recorder with a 12.0-gigabit solid-state digital recorder, providing 10x greater data storage capacity, higher data transfer rates, and eliminating mechanical tape jam vulnerabilities.
   - **Fine Guidance Sensor (FGS-1R)**: Astronauts replaced degraded Fine Guidance Sensor 1 with an upgraded, refurbished optical interferometer unit (FGS-1R) featuring an adjustable fold-flat mirror to overcome optical spherical aberration and provide astrometric positioning accuracy down to fractions of a milliarcsecond.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 8.741276741027832s | **Fact Recall:** 8.3% | **Telemetry:** 0.0%

**Citations:** `['Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1', 'Hubble_Space_Telescope_Servicing_Mission.pdf, Page 2']`


Hubble Servicing Mission 3A (SM3A) was launched ahead of schedule due to concerns about the failure of additional gyroscopes, which could have left the Hubble Space Telescope unable to perform its science mission [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].

During STS-103, the following specific avionics, gyroscope, and guidance upgrades were installed:

1. **Gyroscopes**: All six gyroscopes were replaced [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].
2. **Guidance Sensor**: A guidance sensor was replaced [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].
3. **Main Computer**: The main computer was installed [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].
4. **Transmitter**: A new transmitter was installed [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].
5. **Data Recorder**: A solid state data recorder was installed [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].
6. **Thermal Coverings**: New thermal coverings were applied to the exterior [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].

Additionally, the Fine Guidance Sensor (FGS) was refurbished and upgraded in a "round-robin" fashion, with one FGS being replaced per servicing mission [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 2]. The FGS that was replaced during SM3A was designated as the prime FGS for astrometric science [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].

The specific activities and upgrades mentioned above were crucial for maintaining Hubble's scientific performance and ensuring its continued operation [Hubble_Space_Telescope_Servicing_Mission.pdf, Page 1].

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 5.7602293491363525s | **Fact Recall:** 16.7% | **Telemetry:** 33.3%


Hubble Servicing Mission 3A (SM3A), also known as Space Shuttle Mission STS-103, was launched ahead of schedule due to the failure of one of the Hubble Space Telescope's Fine Guidance Sensors (FGS). Specifically, the FGS2 experienced a critical failure in 1999, which left only three of the six FGSs operational. This situation was a significant concern because the FGSs are crucial for guiding and stabilizing the telescope's pointing accuracy.

The mission was accelerated to address this issue and to install new avionics, gyroscope, and guidance upgrades. The primary objectives of STS-103 were to replace the failed FGS2, install new Rate Sensor Units (RSUs) to replace the aging gyroscopes, and to upgrade the on-board computer systems.

During STS-103, the following upgrades and replacements were performed:

1. **Fine Guidance Sensors (FGS)**: The crew replaced the failed FGS2 with a new unit. This upgrade was critical to ensure the telescope could maintain its precise pointing capabilities.

2. **Rate Sensor Units (RSUs)**: The RSUs were replaced to provide the telescope with new gyroscopes. These devices measure the telescope's rate of rotation, which is essential for maintaining its orientation in space. The new RSUs included the latest technology, improving the telescope's stability and performance.

3. **On-Board Computer Systems**: The mission also involved the installation of new computer hardware and software. This upgrade modernized the telescope's computing capabilities, enhancing its overall functionality and extending its operational life.

4. **Other Upgrades**: In addition to these primary objectives, the crew also performed several other tasks, including replacing the Power Control Unit (PCU) and installing a new Fine Guidance Sensor Control Electronics (FGS CE) board.

The accelerated launch of STS-103 was a critical step in maintaining the Hubble Space Telescope's scientific capabilities and ensuring its continued operation for years to come.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.25 / 5.0 | *Strengths:* Mentions key upgrades and the reason for the early launch.

- **Without-RAG Overall Score:** 2.75 / 5.0 | *Weaknesses:* Incorrect reason for early launch, missing key details on gyroscope failures, incorrect computer upgrade details, hallucinated additional upgrades.


---

### NASA_Q18: Historic Lunar Missions (Apollo 11) — Saturn V (AS-506) Multi-Stage Propulsion & Ascent Telemetry

**Question:** What were the engine configurations, propellant combinations, thrust outputs, and burn durations of the three stages of the Saturn V launch vehicle (AS-506) that launched Apollo 11 to the Moon?

**Primary Source Document:** `Apollo_11_Technical_Information_Summary.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The Saturn V launch vehicle (designated **AS-506**) that propelled the Apollo 11 mission on July 16, 1969, stood **363 feet (110.6 meters) tall** and utilized a three-stage liquid propulsion architecture engineered by NASA Marshall Space Flight Center under Wernher von Braun:

1. **Stage 1: S-IC (First Stage)**:
   - **Engines**: Five Rocketdyne **F-1 engines** (one center fixed engine and four outer gimbaled engines for thrust vector control).
   - **Propellants**: RP-1 high-grade kerosene (209,000 gallons) and Liquid Oxygen (LOX, 334,000 gallons).
   - **Thrust**: Delivered approximately **7,500,000 pounds-force (33.3 MN)** of liftoff thrust (each F-1 producing 1.5 million lbf).
   - **Burn Duration & Telemetry**: Burned for **168 seconds (2 minutes and 48 seconds)**, boosting the vehicle to an altitude of ~42 miles (67 km) and a velocity of ~6,100 mph (~2,720 m/s / Mach 8).

2. **Stage 2: S-II (Second Stage)**:
   - **Engines**: Five Rocketdyne **J-2 engines** arranged in a square pattern with one center engine.
   - **Propellants**: Cryogenic Liquid Hydrogen ($LH_2$, 260,000 gallons) and Liquid Oxygen (LOX, 83,000 gallons).
   - **Thrust**: Delivered **1,150,000 pounds-force (5.1 MN)** of vacuum thrust (each J-2 producing ~230,000 lbf).
   - **Burn Duration & Telemetry**: Burned for approximately **390 seconds (6.5 minutes)**, accelerating the stack to ~115 miles (185 km) altitude and a near-orbital velocity of ~15,400 mph (~6,880 m/s).

3. **Stage 3: S-IVB (Third Stage)**:
   - **Engines**: A single restartable Rocketdyne **J-2 engine**.
   - **Propellants**: Cryogenic Liquid Hydrogen ($LH_2$) and Liquid Oxygen (LOX).
   - **Thrust**: Produced **230,000 pounds-force (1.02 MN)** of vacuum thrust.
   - **Two-Burn Mission Profile**:
     * **First Burn**: Lasted **156 seconds (2.6 minutes)** to insert Apollo 11 and the S-IVB into a circular Earth parking orbit at ~118 miles altitude (17,400 mph).
     * **Second Burn (TLI)**: After orbital checkout, the J-2 reignited for **347 seconds (5.8 minutes)** to execute the Translunar Injection (TLI), accelerating the spacecraft to **24,500 mph (10.9 km/s / ~36,000 ft/s)** onto its lunar transfer trajectory.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 3.90739107131958s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%

**Citations:** `[]`


The provided NASA documentation does not contain sufficient data to address this aspect.

[The excerpts do not provide specific details about the engine configurations, propellant combinations, thrust outputs, and burn durations of the three stages of the Saturn V launch vehicle (AS-506) that launched Apollo 11 to the Moon.]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 8.29897689819336s | **Fact Recall:** 23.1% | **Telemetry:** 0.0%


The Saturn V launch vehicle that launched Apollo 11 to the Moon (AS-506) consisted of three main stages, each with specific engine configurations, propellant combinations, thrust outputs, and burn durations. Here is a detailed breakdown:

### Stage I (S-IC)
- **Engine Configuration**: 5 F-1 engines
- **Propellant Combinations**: Liquid oxygen (LOX) and liquid hydrogen (LH2) for the J-2 engines in the upper stages, but for the S-IC, the propellants were kerosene (RP-1) and LOX.
- **Thrust Output**: Each F-1 engine produced 1,522,000 lbf (673,000 kgf) of thrust. The total thrust for the S-IC stage was 7,628,000 lbf (3,414,000 kgf).
- **Burn Duration**: Approximately 2 minutes and 30 seconds. The engines shut down after the stage had completed its burn and separated from the vehicle.

### Stage II (S-II)
- **Engine Configuration**: 5 J-2 engines
- **Propellant Combinations**: Liquid oxygen (LOX) and liquid hydrogen (LH2)
- **Thrust Output**: Each J-2 engine produced 232,000 lbf (103,000 kgf) of thrust. The total thrust for the S-II stage was 1,160,000 lbf (517,000 kgf).
- **Burn Duration**: Approximately 6 minutes and 30 seconds. The engines shut down after the stage had completed its burn and separated from the vehicle.

### Stage III (S-IVB)
- **Engine Configuration**: 1 J-2 engine
- **Propellant Combinations**: Liquid oxygen (LOX) and liquid hydrogen (LH2)
- **Thrust Output**: The J-2 engine produced 232,000 lbf (103,000 kgf) of thrust.
- **Burn Duration**: The S-IVB stage had two burns. The first burn lasted about 6 minutes and 30 seconds, during which the engine shut down and the stage separated. The second burn, known as Trans Lunar Injection (TLI), lasted approximately 5 minutes and 47 seconds, after which the engine shut down and the stage separated, leaving the Apollo Command/Service Module (CSM) and Lunar Module (LM) to continue their journey to the Moon.

This configuration allowed the Saturn V to achieve the necessary velocity to escape Earth's gravitational pull and reach the Moon. The engines and propellant combinations were carefully chosen to provide the required thrust and efficiency for each stage of the mission.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 1.25 / 5.0 | *Strengths:* Clear statement of lack of information.

- **Without-RAG Overall Score:** 3.5 / 5.0 | *Weaknesses:* Incorrect propellant for S-IC stage, incorrect thrust values for F-1 and J-2 engines, incorrect burn durations for S-IC and S-IVB stages, and missing specific details on S-IVB propellant quantities.


---

### NASA_Q19: Cross-Mission Planetary Systems Engineering — Apollo Lunar Module vs. MSL Sky Crane Deceleration Mechanics

**Question:** How do the descent propulsion system, guidance control, and terminal touchdown mechanics of the Apollo 11 Lunar Module (Eagle) compare to the Entry, Descent, and Landing (EDL) Sky Crane of Curiosity on Mars?

**Primary Source Document:** `Apollo_11_Technical_Information_Summary.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The Apollo 11 Lunar Module (LM) *Eagle* and the Mars Science Laboratory (MSL) *Curiosity* represent two divergent masterpieces of planetary touchdown engineering, shaped fundamentally by atmospheric environment, gravity, and human vs. robotic autonomy:

1. **Atmospheric Environment & Deceleration Pipeline**:
   - **Apollo LM (Moon)**: Because the Moon has a near-perfect vacuum, aerodynamic drag and parachutes are impossible. 100% of the kinetic energy and orbital velocity (~1.6 km/s) had to be dissipated purely through propulsive rocket deceleration.
   - **Curiosity (Mars)**: Mars has a thin CO₂ atmosphere (~1% Earth density). MSL exploited this by dissipating >99% of its kinetic entry energy (~5.9 km/s down to 80 m/s) passively via a hypersonic ablative heat shield and a 21.5-meter supersonic parachute, requiring rocket propulsion for only the final 1.8 km of descent.

2. **Propulsion Architecture & Propellants**:
   - **Apollo LM Descent Propulsion System (DPS)**: A single TRW throttlable rocket engine burning storable hypergolic bipropellants (Aerozine-50 and Nitrogen Tetroxide, $N_2O_4$). It was the first human-rated throttleable rocket (throttling between 10% and 60% and at 100%, producing 1,050 to 9,870 lbf thrust).
   - **MSL Descent Stage**: Powered by eight fixed-geometry Mars Landing Engines (MLE) running on monopropellant hydrazine ($N_2H_4$) over catalyst beds. They throttled via high-frequency pulse modulation between 400 and 3,100 N each to stabilize the descent platform.

3. **Guidance, Navigation, and Pilot Control**:
   - **Apollo LM**: Driven by the Apollo Guidance Computer (AGC) running fixed guidance phases (P63 Braking, P64 Pitchover/Approach). Crucially, at ~500 feet altitude, Neil Armstrong switched the computer to Semi-Automatic/Manual Mode (P66), visually identifying boulders in the landing ellipse and hand-flying the lander past West Crater to touchdown with only ~25 seconds of propellant remaining.
   - **Curiosity**: Entirely autonomous due to the 14-minute one-way light-time communication latency to Mars. Onboard flight software and the Terminal Descent Sensor (radar) made all split-second guidance decisions with zero human intervention.

4. **Touchdown Mechanics & Plume Interaction**:
   - **Apollo LM**: Four landing gear legs with crushable honeycomb aluminum shock absorbers. Touchdown was triggered by 5.6-foot lunar surface contact probes hanging from the footpads; contact lit a blue 'LUNAR CONTACT' indicator, commanding Armstrong to press the engine stop button.
   - **Curiosity Sky Crane**: Directly landing a 900-kg rover with belly thrusters would blast deep trenches and coat delicate optics in abrasive soil. The Sky Crane solved this by hovering 20 meters overhead, lowering the rover on a 7.5-meter bridle cable, deploying the rover wheels to absorb landing shock, severing the tether with pyrotechnic guillotines upon weight-off-wheels, and flying the descent stage away to crash.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 8.363805055618286s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%

**Citations:** `['Apollo_11_Technical_Information_Summary.pdf, Page 83', 'Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 1', 'Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 11']`


The provided NASA documentation does not contain sufficient data to address the detailed comparison of the descent propulsion system, guidance control, and terminal touchdown mechanics of the Apollo 11 Lunar Module (Eagle) with the Entry, Descent, and Landing (EDL) Sky Crane of Curiosity on Mars. The excerpts focus primarily on the Curiosity mission and do not provide comprehensive details about the Apollo 11 Lunar Module's descent system.

However, based on the information provided:

- The Apollo 11 Lunar Module (Eagle) had a descent propulsion system consisting of a Reaction Control System (RCS) that provided thrust capability for maneuvering during the descent. [Apollo_11_Technical_Information_Summary.pdf, Page 83]

- The Lunar Module had a descent engine and four retractable landing gear assemblies. [Apollo_11_Technical_Information_Summary.pdf, Page 83]

- The Curiosity mission utilized a unique EDL system architecture that included a Sky Crane system for precise landing. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 1]

- The Powered Descent Segment of Curiosity involved several sub-segments, including a powered approach, constant velocity accordion, constant deceleration, and the Sky Crane. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 11]

- The Sky Crane system was designed to lower the rover to the surface using cables, allowing the descent stage to fly away to a safe distance. [Mars_Curiosity_MSL_EDL_Assessment.pdf, Page 11]

For a detailed comparison, additional technical documentation on the Apollo 11 Lunar Module's descent system would be necessary. [Apollo_11_Technical_Information_Summary.pdf, Page 83]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 9.903042078018188s | **Fact Recall:** 0.0% | **Telemetry:** 0.0%


The Apollo 11 Lunar Module (LM) and the Entry, Descent, and Landing (EDL) system of the Curiosity rover on Mars, while both designed for landing on another celestial body, have distinct differences in their propulsion systems, guidance and control mechanisms, and touchdown procedures.

### Apollo 11 Lunar Module (Eagle)
**Descent Propulsion System:**
- The LM used a single descent engine for both vertical descent and lateral movement. This engine was capable of both forward and backward thrust, allowing for precise control during the landing.
- The engine was fueled by a mixture of hypergolic propellants (UDMH and Aerozine-50).

**Guidance and Control:**
- The LM's guidance and control were primarily managed by the Lunar Module Guidance Computer (LMGC). The computer provided guidance for the descent and landing.
- The LM had a system of gyros and accelerometers to provide inertial guidance. The crew also had manual control options to override the computer if necessary.
- The LM used a combination of radar and visual cues to determine its altitude and velocity during the descent.

**Terminal Touchdown Mechanics:**
- The LM had four landing legs that were deployed just before touchdown. These legs were designed to absorb the impact of landing.
- The descent engine was throttled down to a hover just before touchdown, allowing the crew to make final adjustments. The engine was then shut down, and the LM landed under its own weight.

### Curiosity Rover (Mars Science Laboratory)
**Entry, Descent, and Landing (EDL) System:**
- Curiosity used a complex EDL system that included a heat shield, parachute, and rocket-powered descent stage known as the Sky Crane.
- The heat shield protected the rover during atmospheric entry.
- The parachute system slowed the descent after the heat shield was jettisoned.
- The Sky Crane system used a retro-rockets to slow the descent further and lower the rover to the surface on cables.

**Descent Propulsion System:**
- The Sky Crane used a descent stage with eight retro-rockets for vertical descent and lateral movement.
- The descent stage was fueled by a mixture of monomethylhydrazine and nitrogen tetroxide.

**Guidance and Control:**
- The EDL system was managed by the Entry, Descent, and Landing (EDL) software on the rover's computer.
- The system used a combination of radar and cameras to determine altitude, velocity, and position.
- The EDL software had to account for the dynamic nature of the Martian atmosphere, which could differ from predictions.

**Terminal Touchdown Mechanics:**
- The Sky Crane system lowered the rover to the surface on cables. Once the rover was secure, the cables were cut, and the descent stage flew away to a safe distance.
- The rover touched down on its six wheels, ready to begin its mission.

### Key Differences:
- **Propulsion:** The LM used a single engine for both descent and lateral movement, while Curiosity's Sky Crane used a descent stage with multiple retro-rockets.
- **Guidance and Control:** The LM relied on a combination of inertial guidance and manual control, while Curiosity's EDL system was fully automated.
- **Landing Mechanism:** The LM landed under its own weight, while Curiosity used a Sky Crane to lower the rover to the surface.

These differences reflect the technological advancements in spacecraft design and the unique challenges of landing on different celestial bodies.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 2.25 / 5.0 | *Strengths:* Mentions some correct details about both missions.

- **Without-RAG Overall Score:** 3.5 / 5.0 | *Weaknesses:* Contains inaccuracies in propellant types and engine details. Omissions include specific throttle ranges, atmospheric entry speeds, and the role of human intervention in Apollo LM.


---

### NASA_Q20: Planetary Defense & Orbital Mechanics — Kinetic Impactor vs. Slow-Push Deflection Physics

**Question:** Based on the technical results of the DART mission, what is the mathematical physics of momentum transfer in kinetic impact deflection, and how does kinetic impact compare in effectiveness, warning time, and operational risk to slow-push methods like gravity tractors?

**Primary Source Document:** `DART_Planetary_Defense_Technical_Report.pdf`

<details>
<summary><b>View Ground Truth Answer</b></summary>


The DART mission provided empirical validation of kinetic impact physics, allowing planetary defense engineers to mathematically model asteroid deflection and rigorously evaluate trade-offs against alternative slow-push concepts:

1. **Mathematical Physics of Kinetic Impact Deflection**:
   - The instantaneous velocity change $\Delta \mathbf{v}_{ast}$ imparted to an asteroid of mass $M_{ast}$ by a kinetic impactor of mass $m_{sc}$ striking at relative velocity $\mathbf{v}_{rel}$ is governed by the momentum conservation equation:
$$\Delta \mathbf{v}_{ast} = \beta \left( \frac{m_{sc}}{M_{ast}} \right) \mathbf{v}_{rel}$$
where $\beta$ is the momentum enhancement factor from crater ejecta recoil.
   - For DART on Dimorphos: $m_{sc} \approx 580 \text{ kg}$, $\mathbf{v}_{rel} \approx 6.14 \text{ km/s}$, $M_{ast} \approx 4.3 \times 10^9 \text{ kg}$, and $\beta \approx 3.6$. This produced an instantaneous velocity change of $\Delta v \approx 2.7 \text{ mm/s}$ (or $\sim 2.7 \times 10^{-3} \text{ m/s}$).
   - While 2.7 mm/s appears tiny, when projected along an asteroid's heliocentric orbital path over an operational warning time of 10 years ($\Delta t = 3.15 \times 10^8 \text{ s}$), the cumulative orbital position displacement $\Delta x$ is:
$$\Delta x \approx 3 \cdot \Delta v \cdot \Delta t \approx 3 \cdot (0.0027) \cdot (3.15 \times 10^8) \approx 2.55 \times 10^6 \text{ m} \approx 2,550 \text{ km}$$
which shifts the asteroid's intersection point by thousands of kilometers, easily transforming a direct Earth collision into a safe miss.

2. **Comparison with Slow-Push Techniques (Gravity Tractor)**:
   - **Gravity Tractor Mechanism**: A massive spacecraft hovers near an asteroid without docking, using mutual gravitational attraction ($F_g = G \frac{m_{sc} M_{ast}}{r^2}$) and low-thrust ion engines canted outward to slowly tow the asteroid over years.
   - **Warning Time Requirements**:
     * **Kinetic Impactor**: High effectiveness for short-to-medium warning times (**5 to 20 years**). Delivers an instantaneous, single-impulse velocity change.
     * **Gravity Tractor**: Requires extremely long warning times (**20 to 50+ years**) because gravitational force is minuscule, producing tiny accelerations ($\Delta v \sim 10^{-5} \text{ m/s per year}$). However, it provides exquisite trajectory trim control with zero risk of fragmentation.
   - **Operational Risks & Rubble-Pile Asteroids**:
     * Kinetic impact carries the risk of asteroid disruption or fragmentation if the impact energy exceeds the specific catastrophic disruption energy ($Q^*_D$). DART proved that for a 160-meter rubble-pile asteroid, a 6.1 km/s impact deflected Dimorphos without catastrophically blowing it apart, while ejecta recoil multiplied deflection efficiency by a factor of 3.6.

</details>


<details>
<summary><b>View With-RAG Answer (Grounded)</b></summary>


**Latency:** 10.62056016921997s | **Fact Recall:** 9.1% | **Telemetry:** 0.0%

**Citations:** `['DART_Kinetic_Impactor_Deflection_Results.pdf, Page 4', 'DART_Kinetic_Impactor_Deflection_Results.pdf, Page 3', 'DART_Kinetic_Impactor_Deflection_Results.pdf, Page 17', 'DART_Planetary_Defense_Technical_Report.pdf, Page 39']`


The DART mission provided insights into the momentum transfer efficiency in kinetic impact deflection, which is a key aspect of planetary defense. The momentum transfer efficiency, denoted as \(\beta\), is a critical parameter that quantifies how the ejecta produced during a deflection attempt contributes to the momentum imparted to the target asteroid. The DART mission demonstrated that the ejecta can significantly enhance the momentum transfer, potentially making \(\beta > 1\). [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 4]

The kinetic impact method involves the impactor spacecraft depositing its own momentum on the target, but the kinetic energy liberated in the hypervelocity collision can excavate and eject a large amount of material. The recoil impulse from this ejecta can exceed the directly delivered momentum, greatly enhancing the deflection effect. [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 3]

In terms of effectiveness, the DART mission showed that the momentum transfer efficiency \(\beta\) can be constrained using the DART measurements and later results from Hera. This efficiency is crucial for predicting the ejecta response and optimizing the deflection direction for a potential Earth-impacting object. [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 3]

Regarding warning time, the DART mission demonstrated that sufficient time can be available between the impact and a potential Earth-impacting scenario to refine simulation and laboratory experiment capabilities. This allows for better predictions of the ejecta response and the design of a future kinetic impactor mission. [DART_Kinetic_Impactor_Deflection_Results.pdf, Page 17]

Operational risk is a significant factor in comparing kinetic impact to slow-push methods like gravity tractors. The DART mission highlighted that a planetary defense spacecraft may need to be built within a much shorter timeframe than DART, posing programmatic challenges. In contrast, gravity tractors operate over extended periods, which can mitigate some of the risks associated with rapid spacecraft development. [DART_Planetary_Defense_Technical_Report.pdf, Page 39]

In summary, the DART mission provided evidence that kinetic impact can be highly effective in asteroid deflection due to the momentum transfer enhancement parameter \(\beta\). However, the operational risks and time constraints for rapid mission development are significant. Gravity tractors, while slower, offer a potentially safer and more sustainable approach to planetary defense. [DART_Planetary_Defense_Technical_Report.pdf, Page 39]

</details>


<details>
<summary><b>View Without-RAG Answer (Baseline)</b></summary>


**Latency:** 8.907297849655151s | **Fact Recall:** 9.1% | **Telemetry:** 0.0%


The DART (Double Asteroid Redirection Test) mission demonstrated the kinetic impactor technique for asteroid deflection. The mathematical physics of momentum transfer in kinetic impact deflection involves the transfer of the spacecraft's momentum to the asteroid through a high-speed collision. This momentum transfer changes the asteroid's velocity, which over time can alter its orbit.

The momentum transfer equation is given by:
\[ \Delta v = \frac{m_{\text{impactor}} \cdot v_{\text{impactor}}}{m_{\text{target}}} \]
Where:
- \( \Delta v \) is the change in velocity of the asteroid
- \( m_{\text{impactor}} \) is the mass of the impactor (DART)
- \( v_{\text{impactor}} \) is the velocity of the impactor relative to the asteroid
- \( m_{\text{target}} \) is the mass of the asteroid

For DART, the impactor (DART itself) had a mass of about 600 kg and impacted Dimorphos at a relative velocity of approximately 6.6 km/s. The target asteroid Dimorphos has an estimated mass of about 130 million kg. The calculated change in velocity for Dimorphos was on the order of millimeters per second.

Kinetic impact compared to slow-push methods like gravity tractors:

1. **Effectiveness:**
   - **Kinetic Impact:** Effective for larger, more massive asteroids that require a significant change in velocity. The DART mission demonstrated a 1% change in the asteroid's orbital period, which is a significant result for a small-scale test.
   - **Gravity Tractor:** Effective for smaller asteroids or those with less mass. The gravitational force exerted by a spacecraft can gradually change the asteroid's trajectory over time.

2. **Warning Time:**
   - **Kinetic Impact:** Requires a relatively short warning time, as the impactor can be launched and reach the asteroid within a few months. This is advantageous for near-term threats.
   - **Gravity Tractor:** Requires a much longer warning time, as the gravitational force is much weaker and the change in trajectory is gradual. This method is more suitable for long-term planning.

3. **Operational Risk:**
   - **Kinetic Impact:** The risk is primarily in the successful delivery of the impactor to the asteroid. There is a risk of the impactor missing the target or failing to impact at the correct location or angle. However, the impact is a one-time event.
   - **Gravity Tractor:** The risk is in maintaining the spacecraft's position relative to the asteroid over an extended period. The spacecraft must be continuously adjusted to maintain the desired gravitational influence, which can be complex and resource-intensive.

In summary, kinetic impact is effective for rapid response to asteroid threats, requires a shorter warning time, and is a one-time event. Gravity tractors are more suitable for long-term planning, require a longer warning time, and involve continuous operation. The choice between these methods depends on the specific characteristics of the asteroid and the available time for intervention.

</details>


**Judge Analysis:**

- **With-RAG Overall Score:** 3.75 / 5.0 | *Strengths:* Accurately discusses momentum transfer efficiency and the role of ejecta, mentions key parameters and comparisons with gravity tractors.

- **Without-RAG Overall Score:** 3.75 / 5.0 | *Weaknesses:* Contains minor inaccuracies in technical details (e.g., impactor mass, velocity, and momentum transfer equation), and omits the momentum enhancement factor β and the cumulative orbital position displacement calculation.


---
