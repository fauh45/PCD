import PySimpleGUI as sg
import cv2 as cv
import numpy as np

IMAGE_SIZE = (500, 500)
UI_STRING_FORMAT = "Image Preview are 500x500, image are {0}x{1}"

menu_def = [
    ['&File', ['&Open', '---', 'Exit']],
    ['&Edit', ['Brightness', 'Inverse (Negative)', 'Restore']],
]

layout = [
    [sg.Menu(menu_def, tearoff=False)],
    [sg.Image(size=IMAGE_SIZE, filename="", key="image")],
    [sg.Text("Image preview are 500x500", key="ui_text")]
]

window = sg.Window("PCD", layout)

image_element = window["image"]
ui_text = window["ui_text"]

original_image = None
shown_image = None


def encode_img(img):
    resized_img = cv.resize(img, IMAGE_SIZE)

    return cv.imencode(".png", resized_img)[1].tobytes()


def brightness_window():
    global shown_image

    temp_shown_image = shown_image

    layout = [
        [sg.Text("Brightness value")],
        [sg.Slider(range=(-255, 255), default_value=0,
                   key="brightness", orientation="horizontal", enable_events=True, change_submits=True)],
        [sg.Button("Done")]
    ]

    window = sg.Window("Brightness Adjust", layout)

    slider_value = 0
    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            image_element.update(data=encode_img(shown_image))
            break
        elif event == 'Done':
            shown_image = temp_shown_image
            break
        elif slider_value != int(values["brightness"]):
            value = int(values["brightness"])
            mask = (255 - shown_image) < value

            temp_shown_image = np.where(mask, 255, shown_image + value)
            image_element.update(data=encode_img(temp_shown_image))

    window.close()


while True:
    event, values = window.read()

    print(event)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

    if event == 'Open':
        filename = sg.popup_get_file("File Gambar", file_types=(
            ("Windows Bitmaps", "*.BMP;*.DIP"), ("JPEG", "*.JPEG;*.JPG;*.JPE"), ("Portable Network Graphics", "*.PNG"), ("TIFF files", "*.TIFF;*.TIF"), ("GIF Files", "*.GIF"),))

        if filename != None and filename != '':
            file_format = filename.split(".")[-1]

            if file_format == "gif":
                cap = cv.VideoCapture(filename)
                _, image = cap.read()
                cap.release()

                shown_image = image
            else:
                shown_image = cv.imread(filename, cv.IMREAD_COLOR)

            original_image = shown_image
            ui_text.update(UI_STRING_FORMAT.format(
                shown_image.shape[0], shown_image.shape[1]))

            image_element.update(data=encode_img(shown_image))
    elif not shown_image is None:
        if event == 'Inverse (Negative)':
            shown_image = 255 - shown_image

            image_element.update(data=encode_img(shown_image))
        elif event == 'Restore':
            shown_image = original_image

            image_element.update(data=encode_img(shown_image))
        elif event == 'Brightness':
            brightness_window()

window.close()
