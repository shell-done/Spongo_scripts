from PIL import Image

def percentageOfOverlapping(area, el_tl, el_br):
    area_tl = [area[0], area[1]]
    area_br = [area[2], area[3]]

    el_size = (el_br[0] - el_tl[0])*(el_br[1] - el_tl[1])
    dx = min(area_br[0], el_br[0]) - max(area_tl[0], el_tl[0])
    dy = min(area_br[1], el_br[1]) - max(area_tl[1], el_tl[1])
    
    if (dx>=0) and (dy>=0):
        return (dx*dy)/el_size

    return 0

def contains(area, point):
    if point[0] > area[0] and point[0] < area[2] and point[1] > area[1] and point[1] < area[3]:
        return True

    return False

DIV_IMG_BY = 2

with open("data.csv") as f:
    categories = ["Porifera_ball", "Porifera_vase", "grey", "red", "Porifera_corona"]

    lines = [l.rstrip("\n") for l in f.readlines()]
    images = {}
    renamed_img = {}

    for i,l in enumerate(lines):
        params = l.split(";")

        if params[2] in categories:
            center = [float(p) for p in params[13][1:-1].split(",")][0:2]
            radius = float(params[13][1:-1].split(",")[2])
            img_width = int(params[14][2:-2].split(",")[2].split(":")[1])
            img_height = int(params[14][2:-2].split(",")[3].split(":")[1])

            data = {
                'orig_filename': params[8],
                'label_name': params[2],
                'center': center,
                'radius': radius,
                'top_left': [max(center[0] - radius, 0), max(center[1] - radius, 0)],
                'bottom_right': [min(center[0] + radius, img_width), min(center[1] + radius, img_height)],
                'img_width': img_width,
                'img_height': img_height
            }

            arr = images.get(params[8].rstrip("\n"), [])
            arr.append(data)

            images[params[8].rstrip("\n")] = arr

    img_index = 0
    for k,v in images.items():
        new_name = str(img_index).rjust(5, '0') + ".jpg"
        renamed_img[new_name] = v

        img_index += 1

    data_keeped = 0
    data_lost_on_cropping = 0
    for k,v in renamed_img.items():
        img_width = v[0]["img_width"]
        img_height = v[0]["img_height"]
        if(img_width//DIV_IMG_BY < 416 or img_height//DIV_IMG_BY < 416):
            print("Image %s (%s) should not be cropped by %d, it would have a resolution smaller than 416x416px" % (k, v[0]["orig_filename"], DIV_IMG_BY))
            continue

        areas = []
        x_div = img_width//DIV_IMG_BY
        y_div = img_height//DIV_IMG_BY
        for y in range(0, DIV_IMG_BY):
            for x in range(0, DIV_IMG_BY):
                top_left = [x_div*x, y_div*y]

                endx = 0
                endy = 0
                if x == DIV_IMG_BY - 1:
                    endx = img_width - 1
                else:
                    endx = x_div*(x+1) - 1

                if y == DIV_IMG_BY - 1:
                    endy = img_height - 1
                else:
                    endy = y_div*(y+1) - 1

                bottom_right = [endx, endy]

                areas.append([top_left[0], top_left[1], bottom_right[0], bottom_right[1]])

        for pos,area in enumerate(areas):
            area_w = area[2] - area[0]
            area_h = area[3] - area[1]
            elements_in_area = []

            for element in v:
                if(contains(area, element["center"])):
                    if percentageOfOverlapping(area, element["top_left"], element["bottom_right"]) > 0.8:
                        data_keeped += 1
                        elements_in_area.append(element)
                    else:
                        data_lost_on_cropping += 1

            if len(elements_in_area) == 0:
                continue

            orig = Image.open("pre_data/" + elements_in_area[0]["orig_filename"])
            new_img = orig.crop(area)
            new_img.save("data/" + k.rstrip(".jpg") + "-d" + str(DIV_IMG_BY) + "-a" + str(pos) + ".jpg")
            print("New img : %s (old name : %s)" % (k.rstrip(".jpg") + "-d" + str(DIV_IMG_BY) + "-a" + str(pos) + ".jpg", elements_in_area[0]["orig_filename"]))

            with open("data/" + k.rstrip(".jpg") + "-d" + str(DIV_IMG_BY) + "-a" + str(pos) + ".txt", "w") as o:
                for e in elements_in_area:
                    class_id = categories.index(e["label_name"])
                    x_center, y_center = (e["center"][0] - area[0])/area_w, (e["center"][1] - area[1])/area_h
                    radius = e["radius"]
                    width = min(radius, abs(e["center"][0] - area[0]), abs(area_w - e["center"][0] + area[0]))/area_w
                    height = min(radius, abs(e["center"][1] - area[1]), abs(area_h - e["center"][1] + area[1]))/area_h
                    o.write("%d %.6f %.6f %.6f %.6f\n" % (class_id, x_center, y_center, width, height))

    print("Data keeped : %d" % data_keeped)
    print("Data lost on cropping : %d" % data_lost_on_cropping)