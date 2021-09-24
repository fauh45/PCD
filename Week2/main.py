import PySimpleGUI as sg
import cv2 as cv
import numpy as np


def encode_img(img):
    return cv.imencode(".png", img)[1].tobytes()


def main():
    sg.theme("Black")

    layout = [
        [sg.Image(filename="", key="image")],
        [sg.Button("Load", size=(10, 1)), sg.Button(
            "Restore", key="restore-btn", size=(10, 1), visible=False)],
        [sg.Slider(range=(0, 10), default_value=0,
                   visible=False, orientation="h", key="slider-r", enable_events=True)]
    ]

    window = sg.Window("Week 2 PCD", layout)

    image_element = window["image"]

    img = None
    curr_slider_value = [0, 0, 0]
    while True:
        event, values = window.read()
        print(event)
        print(values)

        if event == "Load":
            filename = sg.popup_get_file("File Gambar", file_types=(
                ("Images", "*.JPG;*.JPEG;*.JPE;*.JP2;*.BMP;*.DIB"), ))

            if filename != None and filename != "":
                curr_slider_value = [0, 0, 0]

                window["slider-r"].update(visible=True)
                window["restore-btn"].update(visible=True)

                img = cv.imread(filename)

                image_element.update(data=encode_img(img))

        if event == "restore-btn":
            image_element.update(data=encode_img(img))

        if int(values["slider-r"]) != curr_slider_value[2]:
            curr_slider_value[2] = int(values["slider-r"])

            if not img is None:
                temp_img = np.copy(img)
                temp_img[:, :, 2] = curr_slider_value[2]

                image_element.update(data=encode_img(temp_img))

        if event in ("Quit", sg.WIN_CLOSED):
            break

    window.close()


main()
