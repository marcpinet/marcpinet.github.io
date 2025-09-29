+++
title = "Mimimi"
description = "🎵 Self-supervised complex neural network for machine sound anomaly detection using phase-aware spectral analysis. Implements deep complex convolutions with attention mechanisms to capture both real and imaginary components from audio spectrograms, achieving near-SOTA anomaly detection through machine ID classification on industrial sound data."
date = "2025-07-20"
weight = 1

[extra]
remote_image = "/mimimi/img.png"
link_to = "https://github.com/marcpinet/mimimi"
pinned = true
pin_order = 1
+++

<style>
/* GitHub Alert Styles */
.github-alert {
    border-radius: 6px;
    margin: 16px 0;
    padding: 12px 16px;
    border-left: 4px solid;
}

.github-alert-note {
    background-color: #ddf4ff;
    border-color: #0969da;
}

.github-alert-tip {
    background-color: #dcfce7;
    border-color: #1a7f37;
}

.github-alert-important {
    background-color: #f3e8ff;
    border-color: #8250df;
}

.github-alert-warning {
    background-color: #fff8dc;
    border-color: #d1242f;
}

.github-alert-caution {
    background-color: #ffebee;
    border-color: #d1242f;
}

/* Table Wrapper */
.table-wrapper {
    overflow-x: auto;
    margin: 16px 0;
}

.table-wrapper table {
    width: 100%;
    border-collapse: collapse;
}

.table-wrapper th,
.table-wrapper td {
    border: 1px solid #d1d5da;
    padding: 8px 12px;
    text-align: left;
}

.table-wrapper th {
    font-weight: 600;
}

/* Video Styles */
video {
    max-width: 100%;
    height: auto;
    border-radius: 6px;
    margin: 16px 0;
}

/* Code Block Styles */
pre {
    background-color: #f6f8fa;
    border-radius: 6px;
    padding: 16px;
    overflow-x: auto;
    margin: 16px 0;
}

code {
    background-color: #f6f8fa;
    padding: 2px 4px;
    border-radius: 3px;
    font-family: 'SFMono-Regular', 'Monaco', 'Inconsolata', 'Liberation Mono', 'Consolas', monospace;
    font-size: 85%;
    color: #24292f;
}

pre code {
    background-color: transparent;
    padding: 0;
}

/* Dark mode support for inline code */
@media (prefers-color-scheme: dark) {
    pre {
        background-color: #161b22;
        color: #f0f6fc;
    }
    
    code {
        background-color: #21262d;
        color: #f0f6fc;
    }
    
    pre code {
        background-color: transparent;
        color: inherit;
    }
}
</style>

# 🎵 MIMIMI: Self-supervised Complex Network for Machine Sound Anomaly Detection

> A PyTorch implementation of the EUSIPCO 2021 paper ["Self-supervised Complex Network for Machine Sound Anomaly Detection"](https://eurasip.org/Proceedings/Eusipco/Eusipco2021/pdfs/0000586.pdf) by Kim et al.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Overview

**MIMIMI** implements a novel deep complex neural network for machine sound anomaly detection using phase-aware spectral analysis. The model leverages complex-valued convolutions and attention mechanisms to capture both magnitude and phase information from audio spectrograms, achieving superior performance over traditional magnitude-only approaches.

### Features

- **Complex-valued Neural Networks**: Full complex arithmetic throughout the network
- **Phase-aware Processing**: Utilizes both magnitude and phase information
- **Attention Mechanism**: Adaptive weighting of magnitude vs. complex features
- **Self-supervised Learning**: Trains on normal sounds only using machine ID classification
- **Multi-branch Architecture**: Separate processing paths for magnitude, complex, and combined features

## 🏗️ Architecture

The network consists of three main components:

1. **Complex Convolutional Backbone**: 5 complex convolution blocks with PReLU activation
2. **Dual-path Processing**: Separate branches for magnitude and complex features
3. **Attention Fusion**: Channel attention to weight magnitude vs. complex contributions

![Architecture Overview](https://raw.githubusercontent.com/marcpinet/mimimi/main/./assets/architecture.png)

## 📊 Results

### Performance Comparison

<div class="github-alert github-alert-important" style="border-left: 4px solid #8250df; background-color: #8250df10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">❗</span>

<div style="flex: 1;">
            <strong style="color: #8250df; text-transform: uppercase; font-size: 14px; font-weight: 600;">IMPORTANT</strong>

<div style="margin-top: 4px;"><p>The following table compares the paper's results, which used the complete MIMII dataset (30+ GB), compared to mine which uses only the development subset (~4 GB).</p></div>
        </div>
    </div>
</div>
<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Machine Type</p></th><th><p>Paper (%)</p></th><th><p>Best Machine ID (%)</p></th><th><p>Average of all IDs (%)</p></th></tr>
</thead>
<tbody>
<tr><td><p>Fan</p></td><td><p>96.40</p></td><td><p>88.33</p></td><td><p>83.43</p></td></tr>
<tr><td><p>Pump</p></td><td><p>98.75</p></td><td><p>99.48</p></td><td><p>87.15</p></td></tr>
<tr><td><p>Slider</p></td><td><p>96.87</p></td><td><p>99.84</p></td><td><p>92.35</p></td></tr>
<tr><td><p>Valve</p></td><td><p>96.87</p></td><td><p>93.06</p></td><td><p>85.22</p></td></tr>
<tr><td><p><strong>Average</strong></p></td><td><p><strong>97.22</strong></p></td><td><p><strong>95.18</strong></p></td><td><p><strong>87.04</strong></p></td></tr>
</tbody>
</table>
</div>

<div class="github-alert github-alert-note" style="border-left: 4px solid #0969da; background-color: #0969da10; padding: 12px 16px; margin: 16px 0; border-radius: 6px;">

<div style="display: flex; align-items: flex-start;">
        <span style="margin-right: 8px; font-size: 16px;">💡</span>

<div style="flex: 1;">
            <strong style="color: #0969da; text-transform: uppercase; font-size: 14px; font-weight: 600;">NOTE</strong>

<div style="margin-top: 4px;"><p>The paper didn't mention if it highlighted the best performing machine ID or the average across all IDs.
Therefore, I decided to show both.</p></div>
        </div>
    </div>
</div>

### Detailed Results by Machine ID

#### Fan (4 Machine IDs)

- Overall AUC: **83.43%**
- Best performing ID: **88.33%** (ID 1)
- Range: 73.48% - 88.33%

#### Pump (4 Machine IDs)

- Overall AUC: **87.15%**
- Best performing ID: **99.48%** (ID 2)
- Range: 51.69% - 99.48%

#### Slider (4 Machine IDs)

- Overall AUC: **92.35%**
- Best performing ID: **99.84%** (ID 2)
- Range: 73.94% - 99.84%

#### Valve (4 Machine IDs)

- Overall AUC: **85.22%**
- Best performing ID: **93.06%** (ID 0)
- Range: 79.94% - 93.06%

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (mandatory)

```bash
pip install -r requirements.txt
```

### Dataset Download

The implementation uses the MIMII dataset (development subset) from [Zenodo](https://zenodo.org/records/3678171):

```bash
cd data
python download_data.py
```

The script will automatically download and extract:

- `dev_data_fan.zip`
- `dev_data_pump.zip`
- `dev_data_slider.zip`
- `dev_data_valve.zip`

### Training

Train models for all machine types:

```bash
python main.py --mode train
```

Or train a specific machine type:

```bash
python train.py  # Will train all types in config.MACHINE_TYPES
```

### Evaluation

Evaluate trained models:

```bash
python main.py --mode evaluate
```

## 📁 Project Structure

```txt
mimimi/
├── src/
│   ├── model/
│   │   ├── __init__.py           # Model package initialization
│   │   ├── model.py              # Main complex anomaly detector
│   │   ├── complex_layers.py     # Complex convolution, batch norm, PReLU
│   │   ├── attention.py          # Channel attention mechanism
│   │   ├── dataset.py            # MIMII dataset loader with complex STFT
│   │   ├── train.py              # Training pipeline with mixup support
│   │   ├── evaluate.py           # Comprehensive evaluation metrics
│   │   ├── config.py             # Configuration parameters
│   │   └── utils.py              # Utility functions (Youden threshold)
│   ├── main.py                   # Main entry point for training/evaluation
├── data/
│   └── download_data.py      # Automated dataset download
├── models/                   # Saved models and metrics
```

## 🔬 Technical Implementation

### Complex Neural Network Components

#### 1. Complex Convolution

Complex multiplication follows the mathematical rule:

$(a + bi) \times (c + di) = (ac - bd) + (ad + bc)i$

Where:
- Real output: $conv_{real}(real) - conv_{imag}(imag)$
- Imaginary output: $conv_{real}(imag) + conv_{imag}(real)$

#### 2. Complex Batch Normalization

For complex input $z = x + iy$, normalization is applied separately to real and imaginary components:

- Real part: $x_{\text{norm}} = \frac{x - \mu_x}{\sigma_x + \epsilon}$
- Imaginary part: $y_{\text{norm}} = \frac{y - \mu_y}{\sigma_y + \epsilon}$
- Output: $z_{\text{norm}} = x_{\text{norm}} + iy_{\text{norm}}$

#### 3. Attention Mechanism

Channel-wise attention to balance magnitude vs. complex features:

$F_{\text{out}} = A(F_t) \odot F_t + F_t$

Where:
- $A(F_t) = \text{softmax}(\text{FC}_2(\text{ReLU}(\text{FC}_1(\text{GAP}(F_t)))))$
- $\odot$ denotes element-wise multiplication
- $\text{GAP}$ is Global Average Pooling

### Training Strategy

- **Self-supervised Learning**: Machine ID classification on normal sounds only
- **Multi-loss Training**: Combined losses from magnitude, complex, and fused branches
- **Complex STFT**: Input preprocessing preserves phase information
- **Data Augmentation**: Spectral masking, noise injection, frequency shifting

### Key Hyperparameters

<div class="table-wrapper">
<table>
<thead>
<tr><th><p>Parameter</p></th><th><p>Value</p></th><th><p>Description</p></th></tr>
</thead>
<tbody>
<tr><td><p>Sample Rate</p></td><td><p>16 kHz</p></td><td><p>Audio sampling frequency</p></td></tr>
<tr><td><p>FFT Size</p></td><td><p>1024</p></td><td><p>STFT window size</p></td></tr>
<tr><td><p>Hop Length</p></td><td><p>512</p></td><td><p>STFT hop size</p></td></tr>
<tr><td><p>Frames</p></td><td><p>64</p></td><td><p>Time frames per sample</p></td></tr>
<tr><td><p>Learning Rate</p></td><td><p>1e-4</p></td><td><p>Adam optimizer learning rate</p></td></tr>
<tr><td><p>Batch Size</p></td><td><p>32</p></td><td><p>Training batch size</p></td></tr>
<tr><td><p>Epochs</p></td><td><p>30</p></td><td><p>Maximum training epochs</p></td></tr>
<tr><td><p>Patience</p></td><td><p>20</p></td><td><p>Early stopping patience</p></td></tr>
</tbody>
</table>
</div>

## 🎯 Anomaly Detection Strategy

The model detects anomalies through **classification confidence scoring**:

1. **Training Phase**: Learn to classify machine IDs of normal sounds
2. **Test Phase**: High cross-entropy loss indicates inability to classify → anomaly
3. **Threshold**: Optimal threshold found using Youden's J statistic

```python
def get_anomaly_score(self, x, true_class):
    _, _, logits_total = self.forward(x)
    return F.cross_entropy(logits_total, true_class, reduction='none')
```

## 📈 Evaluation Metrics

The implementation provides comprehensive evaluation:

- **AUC-ROC**: Area under receiver operating characteristic curve
- **Precision/Recall/F1**: Binary classification metrics at optimal threshold
- **Per-Machine Analysis**: Individual machine ID performance
- **Confusion Matrices**: Classification and anomaly detection confusion matrices
- **Score Distributions**: Visualization of normal vs. anomalous score distributions

## 🔍 Analysis & Insights

### Strengths of the Implementation

1. **Complete Complex Processing**: Full complex arithmetic pipeline maintained
2. **Faithful Architecture**: Closely follows paper specifications
3. **Comprehensive Evaluation**: Detailed metrics and visualizations
4. **Robust Training**: Early stopping, validation monitoring, model checkpointing

### Performance Analysis

- **Slider machines**: Best performance (92.35%), demonstrating clear phase differences
- **Pump machines**: Moderate performance (87.15%), some IDs excel (99.48%)
- **Valve machines**: Good performance (85.22%), consistent across most IDs (93.06% best)
- **Fan machines**: Most challenging performance (83.43%), ID-dependent variations
- **Individual Excellence**: Several machine IDs achieve >99% AUC, showing model capability

### Potential Improvements

1. **Data Augmentation**: Enhanced spectral augmentation strategies
2. **Architecture Tuning**: Hyperparameter optimization for each machine type
3. **Ensemble Methods**: Combining multiple model predictions
4. **Advanced Complex Operations**: Exploring additional complex layer types

## 📚 References

1. Kim, M., Ho, M. T., & Kang, H. G. (2021). Self-supervised Complex Network for Machine Sound Anomaly Detection. *EUSIPCO 2021*.
2. Purohit, H., et al. (2019). MIMII Dataset: Sound dataset for malfunctioning industrial machine investigation and inspection. *arXiv preprint*.
3. Choi, H. S., et al. (2018). Phase-aware speech enhancement with deep complex u-net. *ICLR 2018*.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/marcpinet/mimimi/tree/main/LICENSE) file for details.

## 🙏 Acknowledgments

- Original paper authors for the innovative complex network approach
- MIMII dataset creators for providing high-quality industrial sound data
- PyTorch community for excellent deep learning framework

---

**Note**: This implementation demonstrates the practical feasibility of complex-valued neural networks for audio anomaly detection, achieving competitive results while providing insights into phase-aware signal processing for industrial applications.