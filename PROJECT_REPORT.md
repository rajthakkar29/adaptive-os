# Adaptive-OS Project Report

## Executive Summary

Adaptive-OS is a proof-of-concept for a context-aware security system that uses live telemetry, a sequence model, and simple security actions to adapt the system state in real time. The core idea is strong: it tries to infer risk from user behavior and machine context, then respond by changing the wallpaper, locking a secure folder, and asking for a password when risk becomes high.

The project’s biggest strength is its end-to-end concept. It connects telemetry collection, preprocessing, model inference, and security enforcement in one pipeline. The biggest weakness is that several pieces are either incomplete, tightly coupled to Windows, or not wired together cleanly enough for reliable day-to-day use. In its current form, it reads more like an ambitious prototype than a production-ready security tool.

## What The Project Is Trying To Do

The repository implements an adaptive security monitor. At a high level, it observes the user’s behavior and system state, converts that into a feature sequence, runs the sequence through an LSTM model, and computes a risk score. Based on that score, it chooses one of three security tiers: Green, Yellow, or Red.

That decision then drives visible and protective responses:

- The wallpaper is updated to match the current tier in [wallpaper_manager.py](wallpaper_manager.py).
- The secure folder is encrypted when risk becomes Red in [crypto_manager.py](crypto_manager.py) and [inference.py](inference.py).
- A password prompt is shown when the system is in Red and an unlock is attempted in [crypto_manager.py](crypto_manager.py).

## Architecture Overview

The project is split into a few clear layers.

The model layer is in [models/lstm_model.py](models/lstm_model.py). It defines a `ContextLSTM` that outputs both a context classification and a risk score.

The training path is in [train.py](train.py) and [data/real_dataset.py](data/real_dataset.py). Training loads telemetry logs, slices them into sequences, generates labels from typing and click behavior, trains the model, and saves a `context_model.pth` checkpoint.

The runtime inference path is in [inference.py](inference.py). It collects telemetry, preprocesses it, feeds a rolling sequence of 10 samples into the model, smooths and adjusts the resulting risk score, then triggers tier changes and security actions.

Telemetry is collected in [telemetry/collector.py](telemetry/collector.py) and normalized in [telemetry/preprocess.py](telemetry/preprocess.py). Logging support exists in [telemetry/logger.py](telemetry/logger.py), but it is not integrated into the main inference loop.

The security implementation is handled by [crypto_manager.py](crypto_manager.py) and [auth_manager.py](auth_manager.py). UI feedback is split between [ui_display.py](ui_display.py) for console output and [wallpaper_manager.py](wallpaper_manager.py) for visual tier signaling.

## Strengths

The project has a clear and interesting design goal. It is not just collecting data or just training a model; it tries to close the loop between behavior observation and automated protection. That makes the architecture more compelling than a typical demo that stops at inference.

The model design is also sensible for the problem. Using an LSTM in [models/lstm_model.py](models/lstm_model.py) matches the idea that risk should depend on behavior over time rather than only a single snapshot.

The security tier idea is easy to understand. Green, Yellow, and Red provide a simple mental model, and the code in [inference.py](inference.py) uses that tiering to create concrete responses rather than only printing a score.

The project also has a modular directory structure. Telemetry, data preparation, model code, security code, and UI feedback are separated into different files, which is a good foundation for future cleanup.

## Weaknesses

The most serious weakness is integration quality. The project has the right components, but several of them do not connect cleanly.

There is a clear bug in the authentication path. [auth_manager.py](auth_manager.py) imports `decrypt_folder`, but [crypto_manager.py](crypto_manager.py) defines `unlock_folder` instead. That means the authentication module will fail as written.

The telemetry and UI code also appear partially unused. [telemetry/logger.py](telemetry/logger.py) defines a logging pipeline, but nothing in [inference.py](inference.py) calls it. Likewise, [ui_display.py](ui_display.py) defines a status table, but the live inference loop prints directly to the console instead.

There is no dependency manifest in the repository. I did not find a `requirements.txt` or equivalent file, so reproducing the environment requires guessing the package set.

## Major Upsides

The strongest upside is the concept itself. The repository combines behavioral telemetry, contextual inference, and an active response layer. That is a valid and interesting direction for adaptive security.

Another upside is the separation between training and inference. [train.py](train.py) and [inference.py](inference.py) are distinct, which makes the project easier to reason about than a single monolithic script.

The use of visible tier feedback is also practical for a demo. Wallpaper changes are immediate and obvious, so the system’s state is easy to observe without reading logs.

## Major Downsides

The biggest downside is portability. [telemetry/collector.py](telemetry/collector.py) depends on Windows-specific APIs for active process detection and network lookup, and [wallpaper_manager.py](wallpaper_manager.py) uses `ctypes.windll`, which is also Windows-specific. On macOS, the project is not expected to run correctly without platform-specific replacements.

Another downside is the amount of hardcoded state. Trusted networks are hardcoded in [inference.py](inference.py), the model checkpoint path is hardcoded, the unlock timing is fixed, and the password hash placeholder in [auth_manager.py](auth_manager.py) is not set up for real use.

The security implementation is also brittle. [crypto_manager.py](crypto_manager.py) stores the encryption key locally, encrypts files directly in place, and suppresses decryption errors with a bare `except`. That is acceptable for a prototype, but it is not robust enough for a real security product.

## Technical Risks And Gaps

The telemetry pipeline is fragile. [telemetry/collector.py](telemetry/collector.py) starts keyboard and mouse listeners at import time, which creates side effects before the rest of the application is ready. That is risky for debugging and reuse.

The training data path is also weak. [data/real_dataset.py](data/real_dataset.py) derives labels from heuristics based on typing and click averages, which means the model is learning from rule-based pseudo-labels rather than verified ground truth. That limits how trustworthy the resulting model can be.

The inference loop is tightly coupled to runtime behavior. [inference.py](inference.py) continuously runs, adjusts risk with a few hand-written heuristics, and locks or unlocks the secure folder immediately. There is little separation between model logic, policy logic, and OS action logic.

There is also no visible testing layer. I did not find unit tests, integration tests, or a setup script. That makes regression risk much higher when any file changes.

## File-By-File Assessment

[models/lstm_model.py](models/lstm_model.py) is the cleanest piece of the project. The model is small, understandable, and appropriate for a prototype.

[train.py](train.py) is straightforward, but it assumes the dataset already exists and the model can be trained without validation or evaluation reporting.

[inference.py](inference.py) is the most important file and also the most fragile. It does the real work, but it combines model loading, telemetry collection, tier selection, security actions, and output formatting in one loop.

[telemetry/collector.py](telemetry/collector.py) contains useful ideas, but it is strongly tied to a Windows environment.

[telemetry/preprocess.py](telemetry/preprocess.py) is simple and readable, though its category lists are fixed and limited.

[telemetry/logger.py](telemetry/logger.py) is useful in principle, but currently looks like a supporting module waiting to be connected.

[crypto_manager.py](crypto_manager.py) is the central security module, but it needs better error handling and a clearer key-management story.

[auth_manager.py](auth_manager.py) currently looks incomplete because of the import mismatch and the placeholder password hash.

[wallpaper_manager.py](wallpaper_manager.py) is fine as a demo effect, but it should be treated as a Windows-only feature.

## Overall Verdict

Adaptive-OS is a strong concept with a real prototype shape, but it is not yet a dependable application. The upside is the architecture: it has a meaningful end-to-end story, a temporal model, and a visible response system. The downside is implementation maturity: platform lock-in, hardcoded values, missing wiring, and a few concrete bugs prevent it from being robust.

If this is being presented as a project report, the honest conclusion is that the project demonstrates a good design direction and a working prototype path, but it still needs cleanup, portability work, testing, and integration fixes before it can be considered production-ready.

## Recommended Next Steps

1. Fix the crypto/auth mismatch in [auth_manager.py](auth_manager.py) and [crypto_manager.py](crypto_manager.py).
2. Add a dependency file and setup instructions.
3. Separate Windows-specific code from the core ML logic.
4. Wire logging and UI output into the live inference loop.
5. Add tests for telemetry preprocessing, tier selection, and crypto state transitions.
