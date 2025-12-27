# Semantic Preservation Human Evaluation Tool

This tool is designed to conduct **human subjective evaluations** on **image semantic preservation** across different generative model exploration levels.

---

## 🛠 1. Prerequisites

### Environment Requirements

- **Python**: 3.8 or higher  
- **Library**: `Pillow (PIL)` is required for image rendering in the GUI

### Installation

Run the following command in your terminal to install the necessary dependency:

```bash
pip install Pillow
````

---

## 📂 2. Directory Structure

The evaluation script uses a **flat directory structure**.
Ensure the script (`human_eval_gui.py`) is placed in the same directory as your dataset folders:

```text
Project_Root/
├── gui.py                 # The GUI Scoring Application
├── requirements.txt       # Environment dependencies
├── README.md              # Project documentation
├── MNIST/                 # Dataset folder
│   └── class_0/           # Category subfolder
│       ├── sample_0_exp_0.png  # Reference (Base Reconstruction)
│       ├── sample_0_exp_1.png  # Exploration Level 1 (λ = 0.1)
│       ├── sample_0_exp_2.png  # Exploration Level 2 (λ = 0.2)
│       └── ...
├── FashionMNIST/
├── SVHN/
├── CIFAR10/
└── Imagenet/              # ImageNet dataset folder
```

---

## 🚀 3. How to Conduct the Experiment

### Step 1: Launch the GUI

Open your terminal in the project directory and run:

```bash
python gui.py
```

---

### Step 2: Scoring Protocol

The interface displays a **pair of images**:

* **Left**: Reference image (`exp_0`), representing the model’s best reconstruction of the original class
* **Right**: Interpolated target image generated under a given exploration level

#### Scoring Scale (1–5)

* **Score 5 – Perfect Preservation**
  The target is visually different but clearly represents the same semantic identity as the reference.

* **Score 3 – Recognizable but Distorted**
  The semantic identity is still visible, but significant distortion or style changes are present.

* **Score 1 – Identity Lost**
  The object has morphed into another class or become unrecognizable noise.

---

### Step 3: Data Output

All evaluation results are **automatically appended** after each click to:

```text
humaneval_results.csv
```

---

## 📊 4. Results Analysis

The generated `humaneval_results.csv` contains the following columns:

| Column Name | Description                  |
| ----------- | ---------------------------- |
| Dataset     | Source dataset (e.g., MNIST) |
| Class       | Category folder name         |
| Exp_Level   | Exploration level (1–5)      |
| Score       | Human evaluation score       |

You can aggregate these results (e.g., compute **mean scores per exploration level**) to assess the **semantic robustness** of your generative model under increasing exploration strength.

```
```
