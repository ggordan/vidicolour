import cv

jumping = False

input = 'pir.mp4'
while not input:
    input = raw_input("Enter the absolute location of the movie: ")
    try:
        open(input)
    except IOError as e:
        input = None

def imageScale(height, width):
    '''
    Scales the image based on the maxWidth and maxHeight
    '''
    maxWidth = 640.0
    maxHeight = 480.0

    if width >= height:
        if width <= maxWidth and height <= maxHeight:
            return tuple((width, height))

        widthRatio = maxWidth / width
        heightRatio = maxHeight / height
    else:
        if height <= maxHeight and width <= maxWidth:
            return tuple((width, height))

        widthRatio = maxWidth / width
        heightRatio = maxHeight / height

    return tuple((int(width*widthRatio), int(height*heightRatio)))

# load video
capture = cv.CaptureFromFile(input)

currentFrame = cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT)
cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, 25.0)

# testing frame jumping. Couldn't get CV_CAP_PROP_POS_FRAMES to work on
# the videos i tried
# not sure if related to this issue: http://code.opencv.org/issues/1419
# nonetheless, in case it doesn't work, dirty fallback
if currentFrame != cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_COUNT):
    jumping = True
    cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, float(currentFrame))

# get an image every minute
fpm = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS) * 60)

# first query
img = cv.QueryFrame(capture)

i = 1
while img:
    if not jumping:
        for j in range(fpm):
            cv.QueryFrame(capture)
    else:
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, fpm * i)

    img = cv.QueryFrame(capture)
    cv.SaveImage('%s.png' % i, img)
    i += 1