# ArUco 마커 생성기 (ArUco Marker Generator)

포커 카드 인식을 위한 ArUco 마커를 생성하고 인쇄하기 위한 도구입니다.

## 기능

- 포커 카드에 대응하는 ArUco 마커 생성
- A4 용지에 마커를 출력하기 위한 PDF 생성
- 카드 모양별로 그룹화된 마커 레이아웃
- PDF에 파일명 표시

## 필요한 패키지

```
opencv-contrib-python==4.8.0.76
numpy==1.24.3
reportlab==4.0.8
```

## 사용 방법

1. 패키지 설치:
```bash
pip install -r requirements.txt
```

2. ArUco 마커 생성:
```bash
python generate_aruco_markers.py
```
이 명령어를 실행하면 `markers` 폴더에 54개의 마커 이미지가 생성됩니다:
- 52개의 표준 카드 마커 (A, 2-10, J, Q, K × 스페이드, 하트, 다이아몬드, 클럽)
- 2개의 조커 마커 (Black, Red)

3. PDF 생성:
```bash
python marker_print.py
```
이 명령어를 실행하면 `print` 폴더에 `card_markers.pdf` 파일이 생성됩니다.

## PDF 레이아웃

- 각 페이지는 4x4 그리드로 총 16개의 마커를 표시합니다.
- 카드는 모양별로 그룹화되어 있습니다 (스페이드, 하트, 다이아몬드, 클럽).
- 각 마커 아래에 파일명이 표시됩니다.
- 페이지 오른쪽 하단에 현재 모양이 표시됩니다.

## 프로젝트 구조

- `generate_aruco_markers.py`: ArUco 마커 이미지 생성
- `marker_print.py`: PDF 생성 및 인쇄 레이아웃
- `requirements.txt`: 필요한 패키지 목록
- `markers/`: 생성된 마커 이미지가 저장되는 폴더
- `print/`: 생성된 PDF가 저장되는 폴더 