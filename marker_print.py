from __future__ import annotations

import os

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def group_cards_by_suit(marker_files):
    """
    카드 파일을 모양별로 그룹화하는 함수
    
    Args:
        marker_files (list): 마커 파일 목록
    
    Returns:
        dict: 모양별로 그룹화된 카드 파일 목록
    """
    # 카드 순서 정의
    rank_order = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, 
                  '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    
    def get_sort_key(filename):
        # 파일명에서 카드 정보 추출 (예: "00_spades_A.png" -> "A")
        parts = filename.split('_')
        if len(parts) == 3:
            rank = parts[2].split('.')[0]
            return rank_order[rank]
        return 999  # 조커는 마지막에
    
    # 일반 카드와 조커 분리
    regular_cards = [f for f in marker_files if not f.startswith("52_") and not f.startswith("53_")]
    jokers = [f for f in marker_files if f.startswith("52_") or f.startswith("53_")]
    
    # 모양별로 그룹화
    cards_by_suit = {}
    for card in regular_cards:
        suit = card.split('_')[1]
        if suit not in cards_by_suit:
            cards_by_suit[suit] = []
        cards_by_suit[suit].append(card)
    
    # 각 모양별로 정렬
    for suit in cards_by_suit:
        cards_by_suit[suit] = sorted(cards_by_suit[suit], key=get_sort_key)
    
    # 조커 추가
    if jokers:
        cards_by_suit['joker'] = jokers
    
    return cards_by_suit

def create_marker_pdf():
    """
    A4 용지에 카드 마커를 프린트하기 위한 PDF를 생성하는 함수
    """
    # 출력 디렉토리 생성
    output_dir = "print"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # PDF 생성
    pdf_path = os.path.join(output_dir, "card_markers.pdf")
    c = canvas.Canvas(pdf_path, pagesize=A4)
    
    # A4 용지 크기 (pt)
    page_width, page_height = A4
    
    # 마커 이미지 크기 (pt)
    marker_size = 40 * 2
    
    # 여백 설정 (pt)
    margin = 50  # 마진 더 줄임
    
    # 그리드 설정 - 4x4 유지
    grid_rows = 4
    grid_cols = 4
    markers_per_page = grid_rows * grid_cols
    
    # 사용 가능한 영역 계산
    available_width = page_width - 2 * margin
    available_height = page_height - 2 * margin
    
    # 마커 사이의 간격 계산
    h_spacing = (available_width - grid_cols * marker_size) / (grid_cols - 1)
    v_spacing = (available_height - grid_rows * marker_size) / (grid_rows - 1)
    
    # 필요하다면 마커 크기 조정
    if h_spacing < 5 or v_spacing < 5:  # 최소 5pt 간격
        h_spacing = 5
        v_spacing = 5
        marker_size = min(
            (available_width - (grid_cols - 1) * h_spacing) / grid_cols,
            (available_height - (grid_rows - 1) * v_spacing) / grid_rows
        )
    
    # 마커 파일 목록 가져오기
    marker_files = [f for f in os.listdir("markers") if f.endswith(".png")]
    
    # 카드를 모양별로 그룹화
    cards_by_suit = group_cards_by_suit(marker_files)
    
    # 각 모양별로 출력
    for suit, cards in cards_by_suit.items():
        # 카드 출력
        for i in range(0, len(cards), markers_per_page):
            # 현재 페이지의 마커
            current_markers = cards[i:i + markers_per_page]
            
            # 각 마커 출력
            for idx, marker_file in enumerate(current_markers):
                # 그리드 위치 계산 (0,1,2,3,4,5,6,7 순서로)
                row = idx // grid_cols
                col = idx % grid_cols
                
                # 마커 이미지 경로
                marker_path = os.path.join("markers", marker_file)
                
                # 마커 위치 계산 - 균등 간격 적용
                x = margin + col * (marker_size + h_spacing)
                y = page_height - margin - (row + 1) * marker_size - row * v_spacing
                
                # 마커 이미지 추가
                c.drawImage(marker_path, x, y, marker_size, marker_size)
                
                # 파일명 추가 (확장자 제외) - 폰트 크기 2배로 키움
                filename = os.path.splitext(marker_file)[0]
                text_y = y - 15  # 간격도 조정
                c.setFont("Helvetica", 12)  # 6pt -> 12pt
                c.drawCentredString(x + marker_size / 2, text_y, filename)
            
            # 모양 제목 출력 (오른쪽 하단) - 폰트 크기 2배로 키움
            c.setFont("Helvetica", 24)  # 12pt -> 24pt
            title_text = f"{suit.upper()}"
            title_width = c.stringWidth(title_text, "Helvetica", 24)
            c.drawString(page_width - margin - title_width, margin - 30, title_text)
            
            c.showPage()
    
    # PDF 저장
    c.save()
    print(f"PDF 생성 완료: {pdf_path}")

if __name__ == "__main__":
    create_marker_pdf() 