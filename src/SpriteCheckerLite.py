import os
import numpy as np
import imageio as iio
import colorsys

current_dir = os.getcwd()
files = os.listdir(current_dir)
files = [f for f in files if os.path.isfile(current_dir + '/' + f) and f.endswith(".png")]
corrected_dir = current_dir + '/' + "corrected"
if os.path.exists(corrected_dir) is False:
    os.mkdir(corrected_dir)

print("Found {0} png files in current folder.".format(len(files)))

# HSV standard colors
white = np.array([0, 0, 100])
black = np.array([0, 0, 0])
light_purple = np.array([300, 74, 100])
dark_purple = np.array([300, 100, 75])
# RGB standard colors
rgb_white = np.array([255, 255, 255])
rgb_black = np.array([0, 0, 0])
rgb_light_purple = np.array([255, 64, 255])
rgb_dark_purple = np.array([192, 0, 192])

# Hue value that falls in 300+-threshold will be considered purple
purple_threshold = 20

# these will have transparency color
char_sizes = np.array(
    [[256, 288],
     [105, 57],
     [171, 214],
     [195, 164]]
)


def should_ignore_transparency_color(sizes, fname):
    fname_lower = fname.lower()
    if "event" in fname_lower or "evt" in fname_lower:
        return True
    img_size = np.array([sizes[1], sizes[0]])
    for s in char_sizes:
        if (s == img_size).all():
            return False
    return True


def hue_within_reserved_purple_range(color_hsv):
    return 300 - purple_threshold < color_hsv[0] * 360 < 300 + purple_threshold


def compare_to_purple(color, color_hsv):
    rgb = np.array([color[0], color[1], color[2]])
    if not hue_within_reserved_purple_range(color_hsv):
        return color, None
    k = color_hsv[2] / color_hsv[1]
    if k > 1:
        return rgb_light_purple, (rgb == rgb_light_purple).all()
    else:
        return rgb_dark_purple, (rgb == rgb_dark_purple).all()


def correct_color_character(color, transparent_color, t_hsv, purple_err):
    r, g, b, a = [x / 255 for x in color]
    hsv = colorsys.rgb_to_hsv(r, g, b)
    # if value is lower than 0.5, it is black
    if hsv[2] < 0.5:
        return rgb_black, hsv[2] == 0
    elif transparent_color is None and hue_within_reserved_purple_range(hsv):
        return compare_to_purple(color, hsv)
    elif transparent_color is None or hsv[1] < 0.5:
        return rgb_white, hsv[1] == 0 and hsv[2] == 1
    elif purple_err or not hue_within_reserved_purple_range(hsv):
        return transparent_color, hsv[1] == t_hsv[1] and hsv[2] == t_hsv[2]
    else:
        return compare_to_purple(color, hsv)


def print_transparent_color_warning(t_hsv):
    if hue_within_reserved_purple_range(t_hsv):
        print("WARNING: transparent color hue falls within reserved purple color range. You should "
              "not use this color as transparent color when drawing 2-bit compatible sprite !")
        return True
    if t_hsv[1] < 0.5:
        print("WARNING: transparent color is not sufficiently saturated! ")
        return False
    if t_hsv[2] < 0.5:
        print("WARNING: transparent color is too dark! ")
        return False


for f in files:
    print("processing " + f + "...")
    # Ignore alpha since it will be forced to 1 (255)
    img = iio.imread_v2(current_dir + '/' + f)
    shape = img.shape
    print("image dimension : " + str(shape))
    # if it is an icon, don't pick transparency color
    transparency_ignore = should_ignore_transparency_color(shape, f)

    if transparency_ignore:
        transparent = None
        t = None
        err = False
    else:
        transparent = img[shape[0] - 1][0]
        print("transparent color is : " + str(transparent))
        tr, tg, tb, ta = [x / 255 for x in transparent]
        t = colorsys.rgb_to_hsv(tr, tg, tb)
        err = print_transparent_color_warning(t)

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            pixel = img[i][j]
            alpha = 0 if pixel[3] < 255 / 2 else 255
            corrected, color_matched = correct_color_character(pixel, transparent, t, err)
            if len(corrected) == 3:
                corrected = np.append(corrected, alpha)
            else:
                corrected[3] = alpha
            if not color_matched:
                print("color correction for pixel [{0},{1}] : {2} -> {3}".format(i, j, pixel, corrected))
            img[i][j] = corrected
    corrected_img_path = corrected_dir + '/' + f
    if os.path.exists(corrected_img_path):
        os.remove(corrected_img_path)
    iio.imwrite(corrected_img_path, img)
    print("Saved corrected image to " + corrected_img_path)

input('Done. Press any key to quit.')
