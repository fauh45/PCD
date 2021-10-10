from PIL import Image
import PySimpleGUI as sg
import cv2 as cv
import numpy as np


IMAGE_SIZE = (500, 500)
UI_STRING_FORMAT = "Image Preview are 500x500, image are {0}x{1}"


def quantize_image(img, k: int):
    pil_img = Image.fromarray(cv.cvtColor(img, cv.COLOR_BGR2RGB))
    pil_img = pil_img.quantize(k)

    pil_img = np.array(pil_img)

    return cv.cvtColor(pil_img, cv.COLOR_RGB2BGR)


def encode_img(img):
    resized_img = cv.resize(img, IMAGE_SIZE)

    return cv.imencode(".png", resized_img)[1].tobytes()


def main():
    sg.theme("Black")

    layout = [
        [sg.Image(size=IMAGE_SIZE, filename="", key="image")],
        [sg.Button("Load", size=(10, 1)), sg.Text("Image preview are 500x500", key="ui_text"), sg.Button(
            "Restore", key="restore-btn", size=(10, 1), visible=False)],
        [sg.Button("Downsample By 0.5", key="downsample", size=(15, 1), visible=False), sg.Button(
            "Upsample By 1.5", key="upsample", size=(15, 1), visible=False)],
        [sg.Input("256", size=(10, 1), key="k_quantize", visible=False),
         sg.Button("Quantize", size=(10, 1), key="quantize", visible=False)]
    ]

    window = sg.Window("Week 2 PCD", layout)

    image_element = window["image"]
    ui_text = window["ui_text"]

    ori_img = None
    img = None
    while True:
        event, values = window.read()

        if event == "Load":
            filename = sg.popup_get_file("File Gambar", file_types=(
                ("Windows Bitmaps", "*.BMP;*.DIP"), ("JPEG", "*.JPEG;*.JPG;*.JPE"), ("Portable Network Graphics", "*.PNG"), ("TIFF files", "*.TIFF;*.TIF"), ("GIF Files", "*.GIF"),))

            if filename != None and filename != "":
                file_format = filename.split(".")[-1]

                print(file_format)

                if file_format == "gif":
                    cap = cv.VideoCapture(filename)
                    _, image = cap.read()
                    cap.release()

                    img = image
                else:
                    img = cv.imread(filename, cv.IMREAD_COLOR)

                ori_img = img
                ui_text.update(UI_STRING_FORMAT.format(
                    img.shape[0], img.shape[1]))

                window["restore-btn"].update(visible=True)
                window["upsample"].update(visible=True)
                window["downsample"].update(visible=True)
                window["quantize"].update(visible=True)
                window["k_quantize"].update(visible=True)

                image_element.update(data=encode_img(img))

        if event == "restore-btn":
            img = ori_img
            image_element.update(data=encode_img(img))

            ui_text.update(UI_STRING_FORMAT.format(img.shape[0], img.shape[1]))

        if event == "downsample":
            img = cv.resize(
                img, (int(img.shape[0] / 2), int(img.shape[1] / 2)), interpolation=cv.INTER_AREA)

            image_element.update(data=encode_img(img))
            ui_text.update(UI_STRING_FORMAT.format(img.shape[0], img.shape[1]))

        if event == "upsample":
            img = cv.resize(
                img, (int(img.shape[0] * 1.5), int(img.shape[1] * 1.5)), interpolation=cv.INTER_AREA)

            image_element.update(data=encode_img(img))
            ui_text.update(UI_STRING_FORMAT.format(img.shape[0], img.shape[1]))

        if event == "quantize":
            img = quantize_image(img, int(values["k_quantize"]))

            image_element.update(data=encode_img(img))

        if event in ("Quit", sg.WIN_CLOSED):
            break

    window.close()


main()
