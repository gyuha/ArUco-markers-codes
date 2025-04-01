from __future__ import annotations

import cv2
import cv2.aruco as aruco
import numpy as np


def main():
    # 카메라 초기화
    cap = cv2.VideoCapture(0)
    
    # ArUco 딕셔너리 설정 (기본 6x6 마커)
    aruco_dict = aruco.Dictionary(aruco.DICT_6X6_250, 6)  # 6x6 마커 크기 지정
    parameters = aruco.DetectorParameters()
    
    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        if not ret:
            break
            
        # 그레이스케일 변환
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 마커 검출
        detector = aruco.ArucoDetector(aruco_dict, parameters)
        corners, ids, rejected = detector.detectMarkers(gray)
        
        # 마커가 검출된 경우
        if ids is not None:
            # 검출된 모든 마커에 대해 처리
            for i in range(len(ids)):
                # 마커의 코너 좌표
                corner = corners[i][0]
                
                # 마커의 중심점 계산
                center_x = int(np.mean(corner[:, 0]))
                center_y = int(np.mean(corner[:, 1]))
                
                # 마커 ID 표시
                cv2.putText(frame, f"ID: {ids[i][0]}", (center_x - 20, center_y - 20),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                # 연두색 테두리 그리기
                corner = corner.astype(np.int32)
                cv2.polylines(frame, [corner], True, (0, 255, 0), 2)
        
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
