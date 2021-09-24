import PySimpleGUI as sg

layout = [
    [sg.Text("A simple dropdown below!")],
    [sg.Combo(["Hello", "World", "I'm", "A", "Dropdown!"], enable_events=True)]
]

window = sg.Window("Week 1 PCD", layout)

while True:
    event, values = window.read()

    print(event)
    if event in ("Quit", sg.WIN_CLOSED):
        break

window.close()
