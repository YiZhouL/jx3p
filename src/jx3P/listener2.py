import typing as tp

from pynput import keyboard


class MultiKbListener:
    def _on_release(self, key: tp.Union[keyboard.KeyCode, keyboard.Key]):
        self._do(key)

    def _do(self, key):
        pass

    def mainloop(self):
        listener = keyboard.Listener(on_release=self._on_release)
        listener.start()
        try:
            listener.join()
        finally:
            listener.stop()

    def start(self):
        listener = keyboard.Listener(on_release=self._on_release)
        listener.start()


if __name__ == "__main__":
    l = MultiKbListener()
    l.mainloop()
