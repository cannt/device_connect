import ppadb.client as adb
import flet as ft
import AdbDevice as adbDvc
import os

global client
client: adb.Client = adb.Client(host="127.0.0.1", port=5037)

global dvcs
dvcs = []

global selected
selected: adbDvc.AdbDevice = None


def on_click(e):
    print(e.control.data)
    for dvc in dvcs:
        if e.control.data == dvc.os:
            os.chdir('C:/Users/angeltrujillo/OneDrive - Ascensores ENINTER, S.L.U/Escritorio/scrcpy-win64-v1.24')
            dvc.device.shell("tcpip 5555")
            os.system('cmd /c "adb connect ' + dvc.ip + ':5555"')
            if (dvc.os == 8):
                btn26.bgcolor = ft.colors.GREEN
                btn26.color = ft.colors.WHITE
                btn26.update()
            elif (dvc.os == 9):
                btn28.bgcolor = ft.colors.GREEN
                btn28.color = ft.colors.WHITE
                btn28.update()
            elif (dvc.os == 10):
                btn29.bgcolor = ft.colors.GREEN
                btn29.color = ft.colors.WHITE
                btn29.update()
            elif (dvc.os == 12):
                btn31.bgcolor = ft.colors.GREEN
                btn31.color = ft.colors.WHITE
                btn31.update()
            unlock_btn.visible = True
            unlock_btn.update()
            display = dvc.device.shell("wm size").replace("Physical size: ", "").replace("\n", "").split("x")
            width = int(display[0])
            height = int(display[1])
            print(display)
            dvc.device.input_keyevent(26)
            dvc.device.input_swipe(width - (width/2), height - (width/2), width - 50, height - 800, 100)
            dvc.device.input_text("4444")
            dvc.device.input_keyevent(66)
            dvc.device.input_keyevent(4)
            os.system('cmd /c "scrcpy -s ' + dvc.ip + ' --window-title="Android ' + str(dvc.os) + '""')

            break


def unlock_device(e):
    for dvc in dvcs:
        display = dvc.device.shell("wm size").replace("Physical size: ", "").replace("\n", "").split("x")
        print(display)
        width = int(display[0])
        height = int(display[1])
        dvc.device.input_keyevent(26)
        dvc.device.input_swipe(width - (width/2), height - (height/2), width - 50, height - 800, 100)
        dvc.device.input_text("444444")
        dvc.device.input_keyevent(66)
        dvc.device.input_keyevent(4)


def main(page: ft.Page):
    page.title = "Adb Devices"
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window_min_width = 400
    page.window_min_height = 425
    page.window_width = 400
    page.window_height = 425
    page.theme_mode = "dark"

    client = adb.Client(host="127.0.0.1", port=5037)
    devices = client.devices()

    global dvc_btns
    dvc_btns = []

    global btn26
    btn26 = ft.ElevatedButton(text="26", on_click=on_click, data=8, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK,
                              width=50, height=50)

    global btn28
    btn28 = ft.ElevatedButton(text="28", on_click=on_click, data=9, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK,
                              width=50, height=50)

    global btn29
    btn29 = ft.ElevatedButton(text="29", on_click=on_click, data=10, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK,
                              width=50, height=50)

    global btn31
    btn31 = ft.ElevatedButton(text="31", on_click=on_click, data=12, bgcolor=ft.colors.WHITE, color=ft.colors.BLACK,
                              width=50, height=50)

    for device in devices:
        devc_os = int(
            device.shell("getprop ro.build.version.release").replace('\n', '').replace('.0', '').replace('.1', ''))
        if (devc_os == "8.0.0" or devc_os == "8.1.0"):
            devc_os = "8"
        serial = device.shell("getprop ro.boot.serialno").replace('\n', '')
        ip = device.shell("ip addr show wlan0  | grep 'inet ' | cut -d ' ' -f 6 | cut -d / -f 1").replace('\n', '')
        dvc = adbDvc.AdbDevice(device, serial, devc_os, ip, False)

        if (dvc.os == 8 and btn26 not in dvc_btns):
            dvc_btns.append(btn26)
        elif (dvc.os == 9 and btn28 not in dvc_btns):
            dvc_btns.append(btn28)
        elif (dvc.os == 10 and btn29 not in dvc_btns):
            dvc_btns.append(btn29)
        elif (dvc.os == 12 and btn31 not in dvc_btns):
            dvc_btns.append(btn31)

        print(dvc.device)
        print(dvc.serial)
        print(dvc.os)
        print(dvc.ip)
        print(dvc.state)
        dvcs.append(dvc)

    client.remote_disconnect()

    global unlock_btn
    unlock_btn = ft.ElevatedButton(
        text="Unlock devices",
        icon="LOCK_OPEN_ROUNDED",
        icon_color="white",
        bgcolor=ft.colors.GREEN,
        color=ft.colors.WHITE,
        on_click=unlock_device,
        visible=False,
    )

    page.add(
        ft.Column(
            [
                ft.Row(
                    dvc_btns,
                    alignment="center",
                    vertical_alignment="center",
                ),
                unlock_btn
            ],
            alignment="center",
            horizontal_alignment="center",
        )
    )


if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
