import os.path
import time
import typing as tp
import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from loguru import logger
from pynput.keyboard import KeyCode

from .listener2 import MultiKbListener
from .press import DDPresser
from .cfg2 import Micro


class MicroPresser(MultiKbListener):
    def __init__(self, dd_path: str = os.path.join(os.path.dirname(__file__), "DD.dll")):
        super().__init__()
        self._sche: tp.Optional[BackgroundScheduler] = None

        self._presser = DDPresser(dd_path)
        self._cfg: tp.Optional[Micro] = None
        self._keys = None
        self._is_running = False
        self._already_triggers = set()

    def load(self, cfg_path):
        logger.info(f"[LOAD]{cfg_path}")
        if self._sche:
            self._sche.remove_all_jobs()
            self._already_triggers.clear()
            self._sche.shutdown()
        self._cfg = Micro.parse_file(cfg_path)
        self._keys = self._cfg.keys

    def _do(self, key):
        if isinstance(key, KeyCode):
            key = key.char
        else:
            key = key.name
        if key == self._cfg.switch and self._is_running:
            logger.info(f"[CLOSE]{key}")
            self._sche.remove_all_jobs()
            self._already_triggers.clear()
            self._is_running = False
            self._sche.shutdown()
        elif key in self._already_triggers:
            pass
        elif key in self._keys:
            logger.info(f"[PRESS]{key}")
            if self._is_running:
                if self._sche is not None:
                    self._sche.remove_all_jobs()
                    self._already_triggers.clear()
                    self._sche.shutdown()

            self._sche = BackgroundScheduler()
            self._sche.start()
            self._is_running = True
            max_secs = 300
            s = 0
            last, next_ = "", key
            now = datetime.datetime.now()

            self._sche.add_job(
                self._press,
                "date",
                run_date=now, args=(last, next_,)
            )

            item = self._cfg.data[next_]
            next_, last = item[3], next_
            s += item[2]
            while s < max_secs and next_:
                item = self._cfg.data[next_]
                next_, last = item[3], next_
                self._sche.add_job(
                    self._press,
                    "date",
                    run_date=now + datetime.timedelta(seconds=s), args=(last, next_, )
                )
                s += item[2]

    def _press(self, last, next_):
        if last in self._already_triggers:
            self._already_triggers.remove(last)
        self._already_triggers.add(next_)
        logger.info(f"[REMOVE]{last}, [ADD]{next_}")
        while next_ in self._already_triggers:
            self._presser.press(next_)

    def mainloop(self, ignore_dll=False):
        if ignore_dll or self._presser.init():
            if not ignore_dll:
                logger.info("dd导入成功")
            else:
                logger.warning("dd未init")
            super().mainloop()
        else:
            logger.error("dd导入失败")

    def start(self, ignore_dll=False):
        if ignore_dll or self._presser.init():
            if not ignore_dll:
                logger.info("dd导入成功")
            else:
                logger.warning("dd未init")
            super().start()
        else:
            logger.error("dd导入失败")
