## SiftSee

### Overview

**SiftSee** is a feature detection and matching toolkit that extracts keypoints from grayscale and color images using **Harris corner detection** and **SIFT (Scale-Invariant Feature Transform)**. It then computes descriptors and performs **template matching** using **SSD (Sum of Squared Differences)** and **Normalized Cross Correlation**. Designed for image understanding tasks, the app supports visual and timing-based analysis through an interactive GUI.

> This project blends classical feature detection with modern scale-invariant descriptors, providing insights into feature extraction pipelines used in biometrics, medical imaging, and computer vision research.

![SiftSee Overview](https://github.com/user-attachments/assets/c9dced42-db09-4306-a60b-84c498ebf52c)

---

### 🔍 Features & Visual Examples

Each section below includes visual comparisons for feature detection, descriptor generation, and template matching.

---

#### Harris Corner Detection

Detects high-curvature image regions (corners) based on local intensity changes.

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>Harris Keypoints</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/dd1ea27f-bc25-493d-a5cd-c805f3bafca8" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/9ab2ef51-1f3a-4fcf-9b36-bc08012f3298" width="250"/></td>
</tr>
</table>

> **Insight:** Harris operator efficiently captures sharp changes in local gradients. A 20% threshold was applied to filter weaker responses and highlight only the strongest corner features.

---

#### SIFT Keypoints & Descriptors

Computes scale- and rotation-invariant descriptors for robust object matching.

<table>
<tr>
<td><b>Original Image</b></td>
<td><b>SIFT Features</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/db1d1489-d2a8-403a-94e4-79ad51a41748" width="250"/></td>
<td><img src="https://github.com/user-attachments/assets/8b76998b-d929-44a7-b36c-09a141013e4d" width="250"/></td>
</tr>
</table>

> **Insight:** SIFT captures robust keypoints across scale and orientation shifts, enabling accurate matching across image pairs.



---

#### SSD-Based Feature Matching

Matches descriptors using the **Sum of Squared Differences** metric.

<table>
<tr>
<td><b>Image 1</b></td>
<td><b>Image 2</b></td>
<td><b>Matched Pairs (SSD)</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/db1d1489-d2a8-403a-94e4-79ad51a41748" width="250" height="250"/></td>
<td><img src="https://github.com/user-attachments/assets/79ecbe3e-171d-412a-a1de-65a003b15cd0" width="250" height="250"/></td>
<td><img src="https://github.com/user-attachments/assets/c642d724-5459-4152-9f99-0084cbeff143" width="250"/></td>
</tr>
</table>

> **Insight:** SSD identifies the most visually similar patches, but is sensitive to lighting and contrast variations.

---

#### Normalized Cross-Correlation Matching

Performs template matching that’s robust to intensity shifts.

<table>
<tr>
<td><b>Template</b></td>
<td><b>Target Image</b></td>
<td><b>Matched Result (NCC)</b></td>
</tr>
<tr>
<td><img src="https://github.com/user-attachments/assets/db1d1489-d2a8-403a-94e4-79ad51a41748" width="250" height="250"/></td>
<td><img src="https://github.com/user-attachments/assets/79ecbe3e-171d-412a-a1de-65a003b15cd0" width="250" height="250"/></td>
<td><img src="https://github.com/user-attachments/assets/4316e7c2-c627-4f34-94f9-e036a7e34e68" width="250"/></td>
</tr>
</table>

> **Insight:** NCC normalizes brightness, making it suitable for scenes with lighting inconsistencies.

---

### Installation

```bash
git clone https://github.com/YassienTawfikk/SiftSee.git
cd SiftSee
pip install -r requirements.txt
python main.py
```

---

### Use Cases

* Biometric matching (e.g., fingerprints, irises)
* Template detection in cluttered images
* Educational demos of keypoint detection methods
* Benchmarking of SSD vs. NCC in varying lighting conditions

---

## Contributions

<div>
  <table align="center">
    <tr>
      <td align="center">
        <a href="https://github.com/YassienTawfikk" target="_blank">
          <img src="https://avatars.githubusercontent.com/u/126521373?v=4" width="150px;" alt="Yassien Tawfik"/><br/>
          <sub><b>Yassien Tawfik</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/nancymahmoud1" target="_blank">
          <img src="https://avatars.githubusercontent.com/u/125357872?v=4" width="150px;" alt="Nancy Mahmoud"/><br/>
          <sub><b>Nancy Mahmoud</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/nariman-ahmed" target="_blank">
          <img src="https://avatars.githubusercontent.com/u/126989278?v=4" width="150px;" alt="Nariman Ahmed"/><br/>
          <sub><b>Nariman Ahmed</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/madonna-mosaad" target="_blank">
          <img src="https://avatars.githubusercontent.com/u/127048836?v=4" width="150px;" alt="Madonna Mosaad"/><br/>
          <sub><b>Madonna Mosaad</b></sub>
        </a>
      </td>
    </tr>
  </table>
</div>

---
