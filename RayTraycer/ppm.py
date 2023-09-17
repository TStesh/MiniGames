"""
Generate simplest ppm-file for image
Please see https://en.wikipedia.org/wiki/Netpbm#File_formats for more information
"""
from tkinter import *
from array import array


def ppm3(fn: str, img_width: int, img_height: int, rgb: [int]) -> int:
    if len(rgb) == 0:
        print('Error: image buffer is empty!')
        return -1
    if img_width * img_height * 3 != len(rgb):
        print('Error: image buffer is incorrect!')
        return -1
    ppm_header = f'P3 {img_width} {img_height} 255\n'
    with open(fn, 'w') as f:
        f.write(ppm_header)
        [f.write(str(_) + ' ') for _ in rgb]
    return 0


def ppm6(fn: str, img_width: int, img_height: int, rgb: [int]) -> int:
    if len(rgb) == 0:
        print('Error: image buffer is empty!')
        return -1
    if img_width * img_height * 3 != len(rgb):
        print('Error: image buffer is incorrect!')
        return -1
    ppm_header = f'P6 {img_width} {img_height} 255\n'
    image = array('B', rgb)
    with open(fn, 'wb') as f:
        f.write(bytearray(ppm_header, 'ascii'))
        image.tofile(f)
    return 0


def ppm_view(fn: str) -> None:
    root = Tk()
    img = PhotoImage(file=fn)
    l = Label(root, image=img)
    # l.grid(row=0, column=0, sticky=W + E + N + S)
    l.pack()
    root.mainloop()
