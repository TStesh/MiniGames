from Graphix.ppm import ppm3, ppm6, ppm_view

fn = 'c:\\users\\alexa\\downloads\\example.ppm'

img_width, img_height = 1024, 768

img_buf = []

for y in range(img_height):
    for x in range(img_width):
        img_buf.append(int(255.999 * (r / img_height)))
        img_buf.append(int(255.999 * (g / img_width)))
        img_buf.append(64)

res = ppm6(fn, img_width, img_height, img_buf)

ppm_view(fn)
