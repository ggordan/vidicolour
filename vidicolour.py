from posix import getcwd
import cv
import Image
import scipy
import scipy.misc
import scipy.cluster
from glob import glob
from PIL import Image, ImageDraw
from time import time

start_time = time()

jumping = False
NUM_CLUSTERS = 20
IMG_HEIGHT = 700
COLOR_WIDTH = 100

input = None
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

# get an image every 5 minutes
fpm = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FPS) * (60*5))

# first query
img = cv.QueryFrame(capture)
#img = None

i = 1
while img:
    if not jumping:
        # dirt hack @todo need to get cv.SetCaptureProperty to work
        for j in range(fpm):
            cv.QueryFrame(capture)
    else:
        cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_POS_FRAMES, fpm * i)

    img = cv.QueryFrame(capture)
    if img:
        cv.SaveImage('sample_images/%s.png' % i, img)
        cv.WaitKey(fpm)
        i += 1


colours = []
# get all the image
images = glob("%s/sample_images/*.png" % getcwd())
# process images
for image in images:
    # open the image
    im = Image.open(image)
    im = im.resize((150, 150))
    # get PIL image
    ar = scipy.misc.fromimage(im)
    shape = ar.shape
    ar = ar.reshape(scipy.product(shape[:2]), shape[2])

    codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

    vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
    counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

    index_max = scipy.argmax(counts)                    # find most frequent
    peak = codes[index_max]
    colour = '#' + ''.join(chr(c) for c in peak).encode('hex')
    colours.append(tuple(peak))

# set the image size
image_size = tuple((len(images) * COLOR_WIDTH, IMG_HEIGHT))
# create a new image
newImage = Image.new('RGBA', image_size, (0, 0, 0, 0))
# create a new draw object
draw = ImageDraw.Draw(newImage) # Create a draw object

increment = len(colours) * COLOR_WIDTH - COLOR_WIDTH
for colour in colours:
    print colour
    print increment
    draw.rectangle((increment, 0, COLOR_WIDTH, IMG_HEIGHT), fill=colour)
#    newImage.save('sadasd%s.png' % increment)
    increment -= COLOR_WIDTH

newImage.save('vidicolour.png')