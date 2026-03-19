# [cite_start]Privacy-Aware Multi-Object Tracking under Anonymization [cite: 1]

[cite_start]본 연구는 CCTV 기반 다중 객체 추적(Multi-Object Tracking, MOT) 환경에서 프라이버시 보호를 위해 적용되는 비식별화 기법이 추적 성능에 미치는 영향을 체계적으로 분석합니다[cite: 3]. [cite_start]특히 고정 파라미터 기반 비식별화의 한계를 극복하기 위해 객체의 크기에 적응하는 **Adaptive Anonymization** 전략을 제안하고 그 실효성을 검증합니다[cite: 8, 16].

## 🛠 주요 특징
- [cite_start]**Adaptive Anonymization**: 객체의 바운딩 박스 크기($L$)에 비례하여 비식별화 강도를 자동 조절함으로써 보호 수준과 분석 유틸리티의 일관성을 확보합니다[cite: 14, 98].
- [cite_start]**YOLOv8 기반 검출**: YOLOv8n 및 YOLOv8s 모델을 활용하여 비식별화 환경에서의 객체 인지 능력을 평가합니다[cite: 127, 129].
- [cite_start]**다양한 실험 설계**: 얼굴(Face) 및 전신(Person)을 대상으로 Blur와 Mosaic 기법을 3단계 강도(Weak/Medium/Strong)로 적용하여 총 12개의 조합을 분석합니다[cite: 4, 71].
- [cite_start]**성능 붕괴 임계점(Breaking Point) 규명**: 비식별화 강도 증가에 따른 추적 성능 하락 및 ID 일관성(IDF1)이 급격히 붕괴되는 임계점을 실험적으로 제시합니다[cite: 6, 19].

## 📊 Adaptive 비식별화 설계 ($L$ 비례)
[cite_start]각 객체의 바운딩 박스에서 짧은 변을 $L = \min(w, h)$으로 정의하고, 이를 기준으로 파라미터를 결정합니다[cite: 100, 101].

### [cite_start]1. 적용 수식 [cite: 103, 105]
- **Gaussian Blur 커널 크기 ($k$)**: $k = 2 \times \lfloor \alpha \cdot L \rfloor + 1$
- **Mosaic 블록 크기 ($m$)**: $m = \lfloor \beta \cdot L \rfloor$

### 2. 비식별화 파라미터 계수 ($\alpha, \beta$)
| Category   | Method           | Weak  | Medium | Strong |
|:-----------|:-----------------|:------|:-------|:-------|
| **Face**   | Blur ($\alpha$)  | 0.2   | 0.4    | 0.6    |
| **Face**   | Mosaic ($\beta$) | 0.1   | 0.2    | 0.3    |
| **Person** | Blur ($\alpha$)  | 0.15  | 0.3    | 0.5    |
| **Person** | Mosaic ($\beta$) | 0.03  | 0.06   | 0.09   |

[cite_start]*전신 Mosaic의 경우 추적 성능 붕괴를 완화하기 위해 비율을 단계적으로 하향 조정하여 최적화하였습니다[cite: 92, 125].*

## 🔍 주요 실험 인사이트 (Research Insights)
- [cite_start]**ID 유지 능력**: 얼굴 비식별화는 신체 실루엣과 보행 특징을 보존하여 전신 비식별화 대비 추적 유틸리티 보존 측면에서 압도적으로 유리합니다[cite: 7, 246, 270].
- [cite_start]**카메라 구동 환경**: 이동 카메라(Moving) 환경에서는 프레임 간 상대적 운동 정보가 외형 정보의 부재를 보완하여 고정 카메라 환경보다 우수한 성능을 보입니다[cite: 196, 198, 202].
- [cite_start]**모델 체급의 영향**: 파라미터 수가 많은 YOLOv8s 모델이 왜곡된 이미지 속에서도 객체의 추상적 특징을 더 정교하게 인지하여 성능 방어력이 높습니다[cite: 135, 231, 235].
- [cite_start]**밀집도 취약성**: 고밀도 군중 환경에서는 비식별화 영역이 중첩되면서 객체 간 경계 정보가 소실되어 추적 지표(MOTA)가 급격히 하락합니다[cite: 7, 261, 263, 264].

## 🚀 실행 방법

### 1. 환경 설정
```bash
pip install -r requirements.txt
```

### 2. 데이터 준비
download_dataset.py를 실행하여 실험에 사용된 MOT17/MOT20의 핵심 6개 시퀀스를 준비합니다.
```bash
python download_dataset.py
```

### 3. 비식별화 및 추적 실행
yolov8n-face.pt 모델을 프로젝트 루트 폴더에 위치시킨 후, main.py를 실행하여 비식별화 영상을 생성합니다.
```bash
python main.py
```
