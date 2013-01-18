import cv

input = 'rt.mkv'
while not input:
    input = raw_input("Enter the absolute location of the movie: ")
    try:
        open(input)
    except IOError as e:
        input = None


capture = cv.CaptureFromFile(input)
img=cv.QueryFrame(capture)
img = cv.CreateImage(img.width, img.height), cv.IPL_DEPTH_32F, 3)
cv.SaveImage('0.png', img)

i = 0
while img:
    if i > 300:
        exit(1)
    cv.WaitKey(60)
    img = cv.QueryFrame(capture)
    img = cv.CreateImage(imageScale(img.height, img.width), cv.IPL_DEPTH_32F, 3)
    cv.SaveImage('%s.png' % i, img)
    i += 1