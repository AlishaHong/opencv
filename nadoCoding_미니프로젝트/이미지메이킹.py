import cv2
import numpy as np
import imageio

# 여러 개의 임의 이미지 생성 함수
def create_random_image(width=400, height=400, color=None):
    if color is None:
        # 무작위 배경 색상 생성
        color = np.random.randint(0, 256, size=(3,), dtype=np.uint8)
    # 지정된 색상으로 채워진 이미지 생성
    image = np.full((height, width, 3), color, dtype=np.uint8)
    return image

# 이미지 저장 및 GIF를 만들기 위한 이미지 리스트 생성
image_list = []

# 텍스트 추가 함수
def add_text_to_image(image, text="sesac", position=(50, 50), font=cv2.FONT_HERSHEY_SIMPLEX, 
                      font_scale=2, color=(255, 255, 255), thickness=3):
    image_with_text = image.copy()
    cv2.putText(image_with_text, text, position, font, font_scale, color, thickness)
    return image_with_text

# 임의 이미지 5개 생성 및 텍스트 추가
for i in range(10):
    img = create_random_image()
    img_with_text = add_text_to_image(img)
    image_list.append(cv2.cvtColor(img_with_text, cv2.COLOR_BGR2RGB))  # RGB로 변환하여 GIF에 적합

    # 생성된 이미지 저장 (옵션)
    cv2.imwrite(f'image_{i}.jpg', img_with_text)

# GIF 생성
imageio.mimsave('output.gif', image_list, fps=2)  # 초당 2 프레임으로 설정