# Adaptive-OS Project Report

## Project Title

Adaptive-OS: Context-Aware Security Monitoring and Adaptive Folder Protection Using Deep Learning

## Problem Statement and Objective

Adaptive-OS addresses the problem of adapting security behavior to live user context instead of applying one fixed policy for every situation. A static policy cannot distinguish between productive work, browsing, gaming, or idle behavior, so it can either create unnecessary friction or miss elevated risk.

The objective of the project is to observe behavioral and system telemetry, infer a security risk level with a deep learning model, and trigger adaptive protection when the risk changes. The system responds by changing the wallpaper as a visual indicator and by locking or unlocking a protected folder when risk becomes high.

## Selected Deep Learning Approach

The selected approach is a Long Short-Term Memory network implemented as `ContextLSTM` in `lstm_model.py`. This is a suitable choice because the problem depends on patterns over time rather than a single snapshot.

The model produces two outputs:

- a three-class context prediction,
- a continuous risk prediction in the range 0 to 1.

This dual-output design allows the system to represent both the current context and the estimated threat level.

## Dataset Description

The dataset is derived from telemetry logs stored in `telemetry_logs.json`. The training pipeline in `real_dataset.py` loads the logs, divides them into 20-step sequences, and converts each record into a 14-feature vector using the preprocessing logic in `preprocess.py`.

The feature set includes:

- CPU usage
- Hour of day
- Typing speed
- Click rate
- One-hot encoded application category
- One-hot encoded network category

The current implementation adds a robust baseline generation step through `baseline.py`. That script computes outlier-resistant statistics from telemetry logs using interquartile-range filtering and stores them in `baseline.json`.

The dataset labels are now more adaptive than before. Instead of relying only on fixed typing and click thresholds, the training set uses baseline-normalized z-scores and an anomaly score derived from typing and click deviations. This makes the risk labels more responsive to the user’s actual behavior profile.

## Methodology

### Data Preprocessing Steps

The preprocessing pipeline performs the following steps:

1. CPU and hour values are normalized to the range 0 to 1.
2. Typing speed and click rate are normalized.
3. The active application is converted into a one-hot vector.
4. The network name is converted into a one-hot vector.
5. The final feature vector is assembled into a 14-dimensional representation.

The updated training flow first requires telemetry logs to be collected and then computes a baseline from those logs. The baseline generation step removes outliers before computing the mean and standard deviation for typing speed, click rate, and application switching behavior. During inference, the system buffers 20 consecutive feature vectors before sending them to the model.

### Model Architecture

The architecture in `lstm_model.py` is compact and suitable for sequence classification. It uses the following structure:

- Input size: 14 features per time step
- Recurrent layer: LSTM with 32 hidden units
- Output head 1: Linear layer followed by softmax for context classification
- Output head 2: Linear layer followed by sigmoid for risk estimation

This design allows the model to learn temporal dependencies and produce both categorical and continuous outputs.

### Tools and Technologies Used

The main tools and technologies used in the project are:

- Python
- PyTorch for training and inference
- NumPy for numerical processing
- psutil for system telemetry
- pynput for keyboard and mouse monitoring
- cryptography for file encryption
- tkinter for password prompts
- rich for console-based status display
- Matplotlib for diagram generation in the report

### Training Procedure

The training routine in `train.py` follows this sequence:

1. Run inference first so telemetry logs exist.
2. Generate the baseline statistics using `baseline.py`.
3. Load the telemetry dataset from `real_dataset.py`.
4. Build the `ContextLSTM` model.
5. Use Adam optimization.
6. Train for 20 epochs.
7. Optimize the model using a combined loss consisting of cross-entropy for context prediction and mean squared error for risk prediction.
8. Save the trained weights as `context_model.pth`.

### Hyperparameter Settings

| Setting | Value |
|---|---:|
| Input size | 14 |
| Sequence length | 20 |
| Hidden size | 32 |
| Number of context classes | 3 |
| Training epochs | 20 |
| Optimizer | Adam |
| Learning rate | 0.001 |
| Security prompt interval | 15 seconds |
| Unlock hold duration | 10 seconds |
| Red threshold | 3 consecutive red cycles |

### Evaluation Metrics

The training objectives are cross-entropy loss for context classification and mean squared error for continuous risk estimation. For runtime behavior, the practical metric is whether the system transitions into the correct security tier, whether the red-tier hysteresis prevents unnecessary lock churn, and whether the folder lock or unlock action matches the inferred risk.

## Results and Output Screenshots / Graphs

The project produces visible results in two ways. First, the runtime loop prints the current risk, tier, active mode, network name, typing speed, and click rate. Second, the wallpaper changes according to the tier, which gives the user an immediate visual signal.

The project uses four diagrams in the report:

- `Architecture_Diagram.png`
- `Runtime_Flow_Diagram.png`
- `Security_State_Machine.png`
- `Training_Pipeline.png`

These figures summarize the overall architecture, the runtime decision flow, the security state machine, and the training pipeline.

## Performance Analysis / Discussion

Adaptive-OS performs well as a prototype because it connects telemetry collection, sequence modeling, and adaptive security actions in a single loop. The LSTM is a reasonable choice because it can model temporal behavior, which is important for detecting suspicious changes over time.

The strongest aspect of the system is the closed loop between prediction and action. The model does not only generate a score; that score directly affects the security state. This makes the project more meaningful than a passive classification demo.

However, several limitations remain. The project is strongly tied to Windows-specific behavior in `collector.py` and `wallpaper_manager.py`. The labels are now more adaptive, but they still depend on a learned baseline from local logs rather than ground-truth annotations. There is little separation between policy logic and runtime logic in `inference.py`. The crypto/authentication path still uses local key storage and a password hash file in `auth_manager.py`. There is also no dedicated test suite or dependency file.

As a result, the performance is acceptable for demonstration purposes but not yet strong enough for production deployment.

## Conclusion

Adaptive-OS is a promising adaptive-security prototype that combines deep learning, telemetry analysis, and encrypted folder protection. Its biggest value is the idea that the system reacts to user context rather than applying a fixed policy.

At the same time, the project still has important implementation gaps. The current version needs better portability, cleaner integration, stronger error handling, and more rigorous evaluation before it can be considered production-ready.

Overall, the project is best described as a solid proof of concept with a clear research direction and visible security behavior.

## Appendix: Source Code

The main source files used in this project are:

- `train.py`
- `inference.py`
- `auth_manager.py`
- `crypto_manager.py`
- `wallpaper_manager.py`
- `ui_display.py`
- `lstm_model.py`
- `real_dataset.py`
- `baseline.py`
- `baseline.json`
- `generate_data.py`
- `collector.py`
- `preprocess.py`
- `logger.py`
