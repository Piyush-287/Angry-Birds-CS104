import cv2

img=cv2.imread("Screenshot 2025-04-15 234204.png")
blur=cv2.blur(img,(35,35))

cv2.imshow("Blurred image",blur)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("new_blur.png",blur)