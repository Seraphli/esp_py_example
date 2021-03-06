from appdirs import *
import codecs
import json
import asyncio
import socketio
import uuid
import sys

APP_NAME = "electron-spirit"
PLUGIN_NAME = "ES Plugin Example"
SHORT_NAME = "example"
PLUGIN_SETTING = "plugin.setting.json"
DEFAULT_CONFIG = {
    "input_hook": "g",
    "css": ".car { position: relative; width: 100%; height: 100%; padding: 10px; background-color: rgba(250, 250, 250, 1); border: 1px solid black; text-align: center; box-sizing: border-box; overflow: auto; }",
    "basic-1": "<div class='car'>Hello</div>",
    "basic-2": "<div class='car'>World</div>",
    "basic_bound": {"x": 200, "y": 200, "w": 100, "h": 50},
    "view-1": "https://www.baidu.com",
    "view-2": "https://www.w3.org/",
    "view_bound": {"x": 300, "y": 300, "w": 300, "h": 300},
}


o_print = print


def print_flush(*args, **kwargs):
    o_print(*args, **kwargs)
    sys.stdout.flush()


print = print_flush


class PluginApi(socketio.AsyncClientNamespace):
    def __init__(self, parent):
        super().__init__()
        self.elem_count = 0
        self.parent = parent
        self.connected = False

    async def on_connect(self):
        print("Connected")
        if self.connected:
            print("Disconnect because already connected")
            asyncio.get_running_loop().stop()
            return
        await self.parent.setup_connect()
        self.connected = True

    def on_disconnect(self):
        print("Disconnected")
        asyncio.get_running_loop().stop()

    def on_echo(self, data):
        print("Echo:", data)

    def on_addInputHook(self, data):
        print("Add input hook:", data)

    def on_delInputHook(self, data):
        print("Del input hook:", data)

    def on_insertCSS(self, data):
        print("Insert css:", data)

    def on_removeCSS(self, data):
        print("Remove css:", data)

    def on_addElem(self, data):
        print("Add elem:", data)
        self.elem_count += 1

    def on_delElem(self, data):
        print("Remove elem:", data)
        self.elem_count -= 1

    def on_showElem(self, data):
        print("Show view:", data)

    def on_hideElem(self, data):
        print("Hide view:", data)

    def on_setBound(self, data):
        print("Set bound:", data)

    def on_setContent(self, data):
        print("Set content:", data)

    def on_setOpacity(self, data):
        print("Set opacity:", data)

    def on_execJSInElem(self, data):
        print("Exec js in elem:", data)

    def on_notify(self, data):
        print("Notify:", data)

    def on_updateBound(self, key, bound):
        print("Update bound:", key, bound)
        self.parent.update_bound(key, bound)

    def on_updateOpacity(self, key, opacity):
        print("Update opacity:", key, opacity)

    def on_processContent(self, content):
        print("Process content:", content)

    def on_modeFlag(self, flags):
        print("Mode flag:", flags)

    def on_elemRemove(self, key):
        print("Elem remove:", key)
        # prevent remove elem
        return True

    def on_elemRefresh(self, key):
        print("Elem refresh:", key)
        # prevent refresh elem
        return True


class Plugin(object):
    def __init__(self) -> None:
        self.load_config()
        self.api = PluginApi(self)

    def load_config(self):
        path = user_config_dir(APP_NAME, False, roaming=True)
        with codecs.open(path + "/api.json") as f:
            config = json.load(f)
        self.port = config["apiPort"]
        try:
            with codecs.open(PLUGIN_SETTING) as f:
                self.cfg = json.load(f)
            for k in DEFAULT_CONFIG:
                if k not in self.cfg or type(self.cfg[k]) != type(DEFAULT_CONFIG[k]):
                    self.cfg[k] = DEFAULT_CONFIG[k]
        except:
            self.cfg = DEFAULT_CONFIG
        self.save_cfg()

    def save_cfg(self):
        with codecs.open(PLUGIN_SETTING, "w") as f:
            json.dump(self.cfg, f)

    def update_bound(self, key, bound):
        if key == "ex-1":
            self.cfg["basic_bound"] = bound
        elif key == "ex-2":
            self.cfg["view_bound"] = bound
        self.save_cfg()

    async def wait_for_elem(self):
        while self.api.elem_count < 2:
            await asyncio.sleep(0.1)

    async def setup_connect(self):
        await sio.emit("echo", ("Hello World!"))
        # get input 'foo' from like '!g foo'
        await sio.emit("addInputHook", data=(self.cfg["input_hook"]))
        catKey = "ex-1"
        basic_elem = {
            "type": 0,
            "bound": self.cfg["basic_bound"],
            "content": self.cfg["basic-1"],
        }
        await sio.emit(
            "addElem",
            data=(
                catKey,
                basic_elem,
            ),
        )
        css = self.cfg["css"]
        await sio.emit("insertCSS", data=(catKey, css))
        catKey = "ex-2"
        view_elem = {
            "type": 1,
            "bound": self.cfg["view_bound"],
            "content": self.cfg["view-1"],
        }
        await sio.emit(
            "addElem",
            data=(
                catKey,
                view_elem,
            ),
        )
        await sio.start_background_task(self.wait_for_elem)
        await sio.sleep(2)
        await sio.emit(
            "hideElem",
            data=(
                catKey,
                view_elem,
            ),
        )
        await sio.sleep(1)
        await sio.emit(
            "showElem",
            data=(
                catKey,
                view_elem,
            ),
        )
        await sio.emit(
            "execJSInElem",
            data=(
                catKey,
                "1 + 2",
            ),
        )
        catKey = "ex-1"
        basic_elem = {
            "type": 0,
            "bound": self.cfg["basic_bound"],
            "content": self.cfg["basic-2"],
        }
        await sio.emit(
            "addElem",
            data=(
                catKey,
                basic_elem,
            ),
        )
        catKey = "ex-2"
        view_elem = {
            "type": 1,
            "bound": self.cfg["view_bound"],
            "content": self.cfg["view-2"],
        }
        await sio.emit(
            "addElem",
            data=(
                catKey,
                view_elem,
            ),
        )
        await sio.sleep(5)
        await sio.emit("delInputHook", data=(self.cfg["input_hook"]))
        catKey = "ex-2"
        await sio.emit("setOpacity", data=(catKey, 0.5))
        await sio.emit(
            "notify",
            data=(
                {
                    "text": "Demo complete. Use `ctrl + c` to exit.",
                    "title": PLUGIN_NAME,
                },
            ),
        )
        await sio.sleep(1)
        print("Demo complete. Use `ctrl + c` to exit.")

    async def loop(self):
        print("Run loop")
        await sio.connect(f"http://127.0.0.1:{self.port}")
        print("Sio Connected")
        await sio.wait()
        print("Loop end")


if __name__ == "__main__":
    while True:
        try:
            # asyncio
            sio = socketio.AsyncClient()
            p = Plugin()
            sio.register_namespace(p.api)
            asyncio.run(p.loop())
        except RuntimeError:
            import traceback

            print(traceback.format_exc())
        except:
            import traceback

            print(traceback.format_exc())
            break
