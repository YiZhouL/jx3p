import ctypes
import time
import typing as tp

_usercode2ddcode: tp.Dict[str, int] = {
    "shift": 500,
    "f1": 101,
    "f2": 102,
    "f3": 103,
    "f4": 104,
    "f5": 105,
    "f6": 106,
    "f7": 107,
    "f8": 108,
    "f9": 109,
    "f10": 110,
    "~": 200,
    "1": 201,
    "2": 202,
    "3": 203,
    "4": 204,
    "q": 301,
    "z": 501,

}


class DDPresser:
    def __init__(self, dll_path: str):
        self._dll = ctypes.windll.LoadLibrary(dll_path)
        self._DD_key = self._dll.DD_key

    def init(self) -> bool:
        ret = self._dll.DD_btn(0)
        return ret == 1

    def press_down(self, code: str):
        self._DD_key(_usercode2ddcode[code], 1)

    def press_up(self, code: str):
        self._DD_key(_usercode2ddcode[code], 2)

    def press(self, code: str):
        self._DD_key(_usercode2ddcode[code], 1)
        time.sleep(0.005)
        self._DD_key(_usercode2ddcode[code], 2)
        time.sleep(0.005)
