from __future__ import annotations

import os

import cv2
import numpy as np


def get_card_name(marker_id):
    """
    마커 ID에 해당하는 포커 카드 이름을 반환하는 함수
    
    Args:
        marker_id (int): 마커 ID (0-53)
    
    Returns:
        tuple: (카드 모양, 카드 숫자)
    """
    if marker_id >= 52:  # 조커
        return "joker", "B" if marker_id == 52 else "R"  # B: Black Joker, R: Red Joker
    
    suits = ["spades", "hearts", "diamonds", "clubs"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    
    suit_idx = marker_id // 13
    rank_idx = marker_id % 13
    
    return suits[suit_idx], ranks[rank_idx]

def create_aruco_marker(marker_id, size=256):
    """
    ArUco 마커를 생성하는 함수
    
    Args:
        marker_id (int): 마커 ID (0-249)
        size (int): 출력 이미지 크기 (픽셀)
    
    Returns:
        numpy.ndarray: 생성된 마커 이미지
    """
    # ArUco 사전 생성
    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
    
    # 마커 이미지 생성
    marker_image = np.zeros((size, size), dtype=np.uint8)
    marker = cv2.aruco.generateImageMarker(dictionary, marker_id, size, marker_image, 1)
    
    # 흑백 이미지를 3채널로 변환
    marker_image_bgr = cv2.cvtColor(marker, cv2.COLOR_GRAY2BGR)
    
    return marker_image_bgr

def main():
    # 출력 디렉토리 생성
    output_dir = "markers"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 포커 카드 52장과 조커 2장에 대한 마커 생성 (0-53)
    for marker_id in range(54):  # 52장의 카드 + 2장의 조커
        # 마커 생성
        marker = create_aruco_marker(marker_id)
        
        # 카드 이름 가져오기
        suit, rank = get_card_name(marker_id)
        
        # 파일 저장 (마커 ID, 카드 모양, 카드 숫자 포함)
        filename = f"{output_dir}/{marker_id:02d}_{suit}_{rank}.png"
        cv2.imwrite(filename, marker)
        print(f"마커 생성 완료: {filename}")

if __name__ == "__main__":
    main() 