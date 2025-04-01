from __future__ import annotations

import cv2
import cv2.aruco as aruco
import numpy as np


def main():
    # 카메라 초기화
    cap = cv2.VideoCapture(0)
    
    # ArUco 딕셔너리 설정 (기본 6x6 마커)
    aruco_dict = aruco.Dictionary(aruco.DICT_6X6_250, 6)
    parameters = aruco.DetectorParameters()
    
    # 검출 파라미터 조정
    parameters.adaptiveThreshWinSizeMin = 3
    parameters.adaptiveThreshWinSizeMax = 23
    parameters.adaptiveThreshWinSizeStep = 10
    parameters.adaptiveThreshConstant = 7
    
    # 최소/최대 마커 크기 설정
    parameters.minMarkerPerimeterRate = 0.1  # 마커 최소 크기 증가
    parameters.maxMarkerPerimeterRate = 0.8  # 마커 최대 크기 증가
    
    # 마커 검출 정확도 향상
    parameters.polygonalApproxAccuracyRate = 0.01  # 다각형 근사 정확도 향상
    parameters.minCornerDistanceRate = 0.05  # 코너 간 최소 거리
    parameters.minDistanceToBorder = 3  # 경계까지의 최소 거리
    
    # 코너 정제 파라미터
    parameters.cornerRefinementMethod = aruco.CORNER_REFINE_SUBPIX
    parameters.cornerRefinementWinSize = 5
    parameters.cornerRefinementMaxIterations = 30
    parameters.cornerRefinementMinAccuracy = 0.005  # 정확도 향상
    
    # 오류 검출 파라미터
    parameters.errorCorrectionRate = 1.0  # 최대 오류 수정
    
    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break
            
        # 이미지 전처리
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 적응형 이진화 적용
        gray = cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2
        )
        
        # 마커 검출
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
        
        # 마커가 검출된 경우
        if ids is not None:
            # 검출된 모든 마커에 대해 처리
            for i in range(len(ids)):
                # 마커의 코너 좌표
                corner = corners[i][0]
                
                # 마커 면적 계산
                area = cv2.contourArea(corner)
                
                # 너무 작은 마커는 무시 (노이즈 제거)
                if area < 1000:  # 최소 면적 기준
                    continue
                
                # 마커의 중심점 계산
                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))
                
                # 마커 ID 표시
                cv2.putText(frame, f"ID: {ids[i][0]}", (center_x - 20, center_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # 연두색 테두리 그리기
                corner = corner.astype(np.int32)
                cv2.polylines(frame, [corner], True, (0, 255, 0), 2)
                
                # 마커의 방향 표시
                cv2.arrowedLine(frame, 
                              (int(corner[0][0]), int(corner[0][1])),
                              (int(corner[1][0]), int(corner[1][1])),
                              (0, 0, 255), 2)
        
        # 결과 표시
        cv2.imshow('ArUco Marker Detection', frame)
        
        # 'q' 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # 리소스 해제
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
