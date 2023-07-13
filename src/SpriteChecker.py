import os
import cv2

# this is for standalone
# current_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
# this is for source
current_dir = os.getcwd()
files = os.listdir(current_dir)
files = [f for f in files if os.path.isfile(current_dir + '/' + f) and f.endswith(".png")]
corrected_dir = current_dir + '/' + "corrected"
if os.path.exists(corrected_dir) is False:
    os.mkdir(corrected_dir)

print("Found {0} png files in current folder.".format(len(files)))

# HSV standard colors
white = [0, 0, 255]
black = [0, 0, 0]


def correct_color(color, transparent_color):
    # if value is lower than 255/2, it is black
    if color[2] < 255 / 2:
        return black, color[2] == 0
    else:
        # if saturation is lower than 255/2, it should be white
        # pass white directly if it is an icon
        if transparent_color is None or color[1] < 255 / 2:
            return white, color[1] == 0 and color[2] == 255
        else:
            return transparent_color, color[1] == transparent_color[1] and color[2] == transparent_color[2]


for f in files:
    print("processing " + f + "...")
    # Ignore alpha since it will be forced to 1 (255)
    img = cv2.imread(current_dir + '/' + f)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    shape = img.shape
    print("image dimension : " + str(shape))
    # if it is an icon, don't pick transparency color
    transparency_ignore = shape[0] <= 8 and shape[1] <= 8
    if transparency_ignore:
        transparent = None
    else:
        transparent = img[shape[0] - 1][0]
        print("transparent color is : " + str(transparent))
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            pixel = img[i][j]
            corrected, color_matched = correct_color(pixel, transparent)
            if not color_matched:
                print("color correction for pixel [{0},{1}] : {2} -> {3}".format(i, j, pixel, corrected))
                img[i][j] = corrected
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    corrected_img_path = corrected_dir + '/' + f
    if os.path.exists(corrected_img_path):
        os.remove(corrected_img_path)
    cv2.imwrite(corrected_img_path, img)
    print("Saved corrected image to " + corrected_img_path)

input('Done. Press any key to quit.')
