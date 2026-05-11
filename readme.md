````md id="4e0jlwm"
# AdaptiveOS — Context-Aware Behavioral Security System

## Overview

AdaptiveOS was developed as an academic Deep Learning project focused on behavioral security and contextual risk analysis.

Instead of relying only on passwords or static authentication, the system continuously observes how a user interacts with the system and dynamically adjusts security levels in real time.

In simple terms:

- normal behavior → system stays relaxed
- suspicious behavior → security level increases
- highly abnormal behavior → protected files get locked

And yes, the wallpaper changes too because cybersecurity is cooler with visual drama.

The project monitors:

* Typing behavior
* Mouse interaction patterns
* Activity context
* Application usage behavior
* Network environment
* Temporal behavioral sequences

The project combines concepts from:

* Deep Learning (LSTM)
* Behavioral Biometrics
* Context-Aware Risk Assessment
* Adaptive Baseline Modeling
* Real-Time Security Enforcement

When suspicious or abnormal behavior is detected, the system:

* Changes system security tiers
* Updates wallpaper alerts
* Locks protected files/folders
* Requests password-based reauthentication

This README contains all setup, training, and execution steps required to run the project successfully.

---

# Features

## Real-Time Telemetry Monitoring

The system continuously collects:

* Typing speed
* Mouse click rate
* Active applications
* Network information
* Behavioral transitions

Basically, your keyboard and mouse become accidental informants.

---

## Adaptive Behavioral Profiling

Each user generates their own behavioral baseline using:

* Mean behavior
* Standard deviation
* Temporal activity patterns

This allows the system to adapt to:

* Fast typists
* Slow typists
* Different usage styles
* Different workflows

So the system judges you based on your own habits, not someone else's caffeine levels.

---

## LSTM-Based Sequential Analysis

The project uses an LSTM (Long Short-Term Memory) neural network to analyze sequences of user behavior.

Unlike traditional ML models that treat samples independently, the LSTM learns:

* Temporal patterns
* Sequential behavior
* Behavioral consistency
* Context transitions

This allows the system to detect anomalies over time rather than using isolated events.

Unlike humans during exams, the LSTM actually remembers previous context.

---

## Context-Aware Risk Engine

Risk is computed using multiple factors:

* LSTM risk prediction
* Typing anomaly detection
* Mouse behavior anomaly detection
* Behavioral modes
* Network trust
* Activity smoothing

The final output is converted into:

* Green Tier
* Yellow Tier
* Red Tier

---

## Security Response System

When Red Tier is reached:

* Protected folder is locked
* Wallpaper turns aggressively Red
* High-priority password popup appears
* System remains in Red until successful authentication

At that point the system has trust issues.

---

# Project Architecture

```text
User Activity
      ↓
Telemetry Collection
      ↓
Feature Preprocessing
      ↓
Sequence Buffer
      ↓
LSTM Behavioral Analysis
      ↓
Adaptive Baseline Comparison
      ↓
Contextual Risk Engine
      ↓
Tier Generation
      ↓
Security Enforcement
````

---

# Tech Stack

## Languages

* Python

## Libraries

* PyTorch
* NumPy
* JSON
* Tkinter
* pynput
* psutil

---

# Folder Structure

```text
adaptive_os/
│
├── config.json
├── inference.py
├── train.py
├── context_model.pth
├── telemetry_logs.json
│
├── data/
│   ├── baseline.py
│   ├── baseline.json
│   └── real_dataset.py
│
├── models/
│   └── lstm_model.py
│
├── telemetry/
│   ├── collector.py
│   ├── logger.py
│   └── preprocess.py
│
├── secure_folder/
│   └── .gitkeep
│
├── crypto_manager.py
├── wallpaper_manager.py
└── README.md
```

---

# Protected Folder

The `secure_folder/` directory is the protected area monitored by AdaptiveOS.

Any files placed inside this folder may be:

* Locked during Red Tier
* Protected from unauthorized access
* Unlocked only after successful authentication

For security and privacy reasons, no personal files are included in the repository.

Users should manually place their own files inside:

```text
secure_folder/
```

before running the project.

---

# Security Tiers

## Green Tier

Normal trusted behavior.

* Low risk
* Normal user behavior
* Stable interaction patterns

The system is calm. Life is good.

---

## Yellow Tier

Moderate anomaly detected.

* Suspicious behavior
* Temporary deviation
* Monitoring intensified

The system is watching you a little more carefully now.

---

## Red Tier

High-risk behavior detected.

* Folder locked
* Wallpaper turns Red
* Authentication required
* System stays in Red until verified

You have officially made the AI uncomfortable.

---

# Model Description

## Why LSTM?

The project uses an LSTM because behavioral security depends heavily on temporal patterns.

Traditional models such as:

* CNN
* MLP
* Linear models

are less suitable because they do not effectively model long-term sequential dependencies.

The LSTM is capable of:

* Learning behavioral sequences
* Remembering previous context
* Understanding temporal consistency
* Detecting sequential anomalies

---

# Behavioral Features Used

The model learns from:

* Typing speed
* Mouse click rate
* Application switching
* Network changes
* Temporal interaction patterns
* Activity transitions

In short, the system quietly studies your digital habits like a very paranoid roommate.

---

# Adaptive Baseline System

The project uses personalized baseline modeling.

For every user:

* Mean behavior is computed
* Standard deviation is computed
* Z-score based anomaly detection is applied

This means:

* Fast typists are normal to themselves
* Slow typists are normal to themselves

The system evaluates deviation from personal behavior instead of using fixed universal thresholds.

---

# Installation

## 1. Clone Repository

```bash
git clone <repository-url>
cd adaptive_os
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

If something breaks here, it is probably Python being Python.

---

# Configuration

Create:

```text
config.json
```

Example:

```json
{
    "trusted_networks": [
        "YourWifiName"
    ],

    "red_threshold": 3,

    "prompt_interval": 15,

    "sequence_length": 20
}
```

---

# How to Train the System for a New User

The system is behavior-adaptive.

Each user should train the model on their own behavioral data.

Because apparently humans are all different.

---

## STEP 1 — Configure Trusted Network

Edit:

```text
config.json
```

Add your trusted WiFi name.

---

## STEP 2 — Collect Behavioral Logs

Run:

```bash
python inference.py
```

Use the system normally for:

* 2–4 hours minimum
* Regular workflow
* Natural interaction patterns

This generates:

```text
telemetry_logs.json
```

The more natural the behavior, the smarter the system becomes.

---

## STEP 3 — Generate Baseline

Run:

```bash
python data/baseline.py
```

This creates:

```text
data/baseline.json
```

The baseline contains:

* Mean typing speed
* Standard deviation
* Mouse behavior profile
* Switching behavior profile

---

## STEP 4 — Train LSTM Model

Run:

```bash
python train.py
```

This creates:

```text
context_model.pth
```

The trained model now becomes personalized for that user.

Congratulations. The AI now knows your habits.

---

## STEP 5 — Start Real-Time Monitoring

Run:

```bash
python inference.py
```

The system now performs:

* Personalized behavioral monitoring
* Real-time risk assessment
* Adaptive anomaly detection
* Security enforcement

---

# Workflow Example

```text
User starts typing normally
        ↓
Telemetry collected
        ↓
Features preprocessed
        ↓
LSTM analyzes behavioral sequence
        ↓
Risk score generated
        ↓
Risk adjusted using adaptive baseline
        ↓
Tier selected
        ↓
Security action triggered if required
```

---

# Limitations

## Behavioral Mimicry

If an attacker closely mimics the legitimate user’s behavior, detection may become difficult.

This is a known limitation of behavioral biometric systems.

So yes, a very determined clone version of you could still be a problem.

---

## Manual Personalization Required

Each user should:

* Generate their own baseline
* Train their own model

for optimal performance.

---



# Academic Domains

This project combines concepts from:

* Artificial Intelligence
* Deep Learning
* Cryptography
* Behavioral Biometrics
* Context-Aware Computing
* Human-Computer Interaction
* Adaptive Systems

---

# Final Description

AdaptiveOS is a hybrid AI-based contextual behavioral security framework that combines deep learning and adaptive anomaly detection to continuously evaluate user behavior and dynamically enforce system security.

Or in simpler words:

It watches how you use your computer and gets suspicious when things start feeling weird.

