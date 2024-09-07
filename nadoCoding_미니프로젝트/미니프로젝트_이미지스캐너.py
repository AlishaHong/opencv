import cv2
import numpy as np
import sys

# 미니프로젝트 
# 반자동 문서 스캐너 만들기 


# 이미지 원근 변환 할때 
# 그림판에서 픽셀 위치값을 얻어오는 번거로움이 있었음 
# 이것을 이미지에서 직접 값을 얻을 수 있게 함 


# 마우스 이벤트 등록 


# EVENT 
# 사용 가능한 이벤트 목록:

# cv2.EVENT_MOUSEMOVE: 마우스가 움직일 때 발생
# cv2.EVENT_LBUTTONDOWN: 마우스 왼쪽 버튼을 눌렀을 때 발생
# cv2.EVENT_RBUTTONDOWN: 마우스 오른쪽 버튼을 눌렀을 때 발생
# cv2.EVENT_MBUTTONDOWN: 마우스 가운데 버튼을 눌렀을 때 발생
# cv2.EVENT_LBUTTONUP: 마우스 왼쪽 버튼을 뗐을 때 발생
# cv2.EVENT_RBUTTONUP: 마우스 오른쪽 버튼을 뗐을 때 발생
# cv2.EVENT_LBUTTONDBLCLK: 마우스 왼쪽 버튼을 더블클릭했을 때 발생


# 이벤트가 발생했을때 불러와지는 좌표를 저장하는 리스트
point_list = []
img = cv2.imread('nadoCoding/data/poker.jpg')
resized_img = cv2.resize(img, (233, 300))  # (width, height) 순으로 지정

color = (255,0,255) # 핑크색
thickness = 3   # 직선두께
drawing = False # 선을 그릴지 여부
# 일단 false로 뒀다가 클릭 뒤 선을 그리도록 True로 바꿔줄예정
def mouse_handler(event, x ,y , flags, param):
    global drawing
    dst_img = resized_img.copy()
    
    if event == cv2.EVENT_LBUTTONDOWN: # 왼쪽 버튼 Down
        drawing = True # 선을 그리기 시작
        point_list.append((x, y))
        
    if drawing: # drawing이 True면
        prev_point = None   # 직선의 시작점
        for point in point_list:
            # 도형그려보기(반지름 : 5)
            cv2.circle(dst_img, point, 3, color, cv2.FILLED )
            if prev_point:  #첫번째 점을 찍었을때는 아직 prev_point가 없음
                cv2.line(dst_img, prev_point, point, color, thickness, cv2.LINE_AA)
            prev_point = point

        # 마지막 선긋기
        next_point = (x,y)
        if len(point_list) == 4:
            show_result()   # 결과출력
            next_point = point_list[0]  # 첫번째 지점
            # point 리스트 배열에 4개가 다 차게되면 더이상 마우스를 따라오지 않고
            # 0번 인덱스의 지점으로 직선을 연결하도록 함 
        cv2.line(dst_img, next_point, point, color,thickness,cv2.LINE_AA)

    cv2.namedWindow('img',cv2.WINDOW_NORMAL)  
    cv2.imshow('img', dst_img)
    
    # 마지막 부분은 직선으로 이어지지 않음!!! 
    # 실시간 선긋기로 수정 
def show_result():
    width, height = 233,300
    src = np.float32(point_list)
    dst = np.float32([[0, 0], [width, 0], [width, height], [0, height]])
    # 좌상,우상,우하,좌하(시계방향)
    
    matrix = cv2.getPerspectiveTransform(src, dst)  #matrix얻어옴
    result = cv2.warpPerspective(resized_img, matrix, (width, height))   #matrix대로 변환
    cv2.namedWindow('result',cv2.WINDOW_NORMAL)  
    cv2.imshow('result', result)


cv2.namedWindow('img',cv2.WINDOW_NORMAL)  
#img란 이름의 윈도우를 먼저 만듬 : 여기에 마우스 이벤트를 처리하기 위한 핸들러 적용

cv2.setMouseCallback('img', mouse_handler)
cv2.imshow('img', resized_img)
cv2.waitKey()
cv2.destroyAllWindows()