from shutil import copyfile

EXTRACT_IMAGES = True
EXTRACT_DATA = True

DIV_IMG_BY = 2

with open("data.csv") as f:
    categories = ["Porifera_ball", "Porifera_vase", "grey", "red", "Porifera_corona"]
    lines = [l.rstrip("\n") for l in f.readlines()]

    for i,l in enumerate(lines):
        if i == 0:
            continue

        params = l.split(";")

        if params[2] in categories:
            if EXTRACT_IMAGES:
                copyfile("PL07/" + params[8], "pre_data/" + params[8])

            if EXTRACT_DATA:
                o = open("pre_data/" + params[8].rstrip(".jpg") + ".txt", "a")
                points = params[13][1:-1].split(",")
                points = [float(p) for p in points]

                attr = params[14][2:-2].split(",")
                img_width = int(attr[2].split(":")[1])
                img_height = int(attr[3].split(":")[1])

                class_id = categories.index(params[2])
                x_center, y_center = points[0], points[1]
                width = height = points[2]

                o.write("%d %.6f %.6f %.6f %.6f\n" % (class_id, x_center/img_width, y_center/img_height, width/img_width, height/img_height))
                
                o.close()