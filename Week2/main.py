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
        [sg.Text("Red", key="text-r", visible=False), sg.Slider(range=(0, 10), default_value=0,
                                                                visible=False, orientation="h", key="slider-r", enable_events=True)],
        [sg.Text("Green", key="text-g", visible=False), sg.Slider(range=(0, 10), default_value=0,
                                                                  visible=False, orientation="h", key="slider-g", enable_events=True)],
        [sg.Text("Blue", key="text-b", visible=False), sg.Slider(range=(0, 10), default_value=0,
                                                                 visible=False, orientation="h", key="slider-b", enable_events=True)]
    ]

    window = sg.Window("Week 2 PCD", layout)

    image_element = window["image"]

    img = None
    curr_slider_value = [0, 0, 0]
    while True:
        event, values = window.read()

        if event == "Load":
            filename = sg.popup_get_file("File Gambar", file_types=(
                ("Images", "*.JPG;*.JPEG;*.JPE;*.JP2;*.BMP;*.DIB"), ))

            if filename != None and filename != "":
                curr_slider_value = [0, 0, 0]

                window["slider-r"].update(visible=True)
                window["slider-g"].update(visible=True)
                window["slider-b"].update(visible=True)

                window["text-r"].update(visible=True)
                window["text-g"].update(visible=True)
                window["text-b"].update(visible=True)

                window["restore-btn"].update(visible=True)

                img = cv.imread(filename, cv.IMREAD_COLOR)

                image_element.update(data=encode_img(img))

        if event == "restore-btn":
            image_element.update(data=encode_img(img))

            window["slider-r"].update(0)
            window["slider-g"].update(0)
            window["slider-b"].update(0)

        if int(values["slider-r"]) != curr_slider_value[2] or int(values["slider-g"]) != curr_slider_value[1] or int(values["slider-b"]) != curr_slider_value[0]:
            curr_slider_value[2] = int(values["slider-r"])
            curr_slider_value[1] = int(values["slider-g"])
            curr_slider_value[0] = int(values["slider-b"])

            if not img is None:
                temp_img = np.copy(img)

                temp_img[:, :, 2] += curr_slider_value[2]
                temp_img[:, :, 1] += curr_slider_value[1]
                temp_img[:, :, 0] += curr_slider_value[0]

                image_element.update(data=encode_img(temp_img))

        if event in ("Quit", sg.WIN_CLOSED):
            break

    window.close()


main()
