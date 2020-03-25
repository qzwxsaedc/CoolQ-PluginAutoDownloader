import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

import CustomException as ce


class WatchDog:
    def __init__(self, file_name, m_path):
        self._b_lock_modified = True
        self._b_lock_moved = True
        self.__file_name = file_name
        self.__observer = Observer()
        self.__observer.schedule(self.FileMonitor(self), m_path, True)
        self.__observer.start()

    def get_file_name(self) -> str:
        return self.__file_name

    class FileMonitor(FileSystemEventHandler):
        def __init__(self, instance):
            self.__instance = instance

        def on_modified(self, event):
            # print("modified " + os.path.basename(event.src_path))
            if (not event.is_directory) and os.path.basename(event.src_path) == self.__instance.get_file_name():
                print("modified unlocked")
                self.__instance._b_lock_modified = False
                pass

        def on_moved(self, event):
            # print("moved " + os.path.basename(event.dest_path))
            if (not event.is_directory) and os.path.basename(event.dest_path) == self.__instance.get_file_name():
                print("moved unlocked")
                self.__instance._b_lock_moved = False
                pass

        def on_any_event(self, event):
            pass

        def on_deleted(self, event):
            pass

        def on_created(self, event):
            pass

    def get_interrupt(self):
        count = 100 * 30
        while self._b_lock_modified or self._b_lock_moved:
            count -= 1
            time.sleep(0.01)
            if not count:
                self.__observer.stop()
                self.__observer.join()
                raise ce.WatchdogTimeoutWarning()
        self.__observer.stop()
        self.__observer.join()
        time.sleep(0.5)
        return True

    def __del__(self):
        self.__observer.stop()
        self.__observer.join()
