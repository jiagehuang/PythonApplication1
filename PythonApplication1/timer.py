# timer.py
import time
class TimerError(Exception):
    """一个自定义异常，用于报告使用Timer类时的错误"""
 
class Timer:
    def __init__(self):
        self._start_time = None
 
    def start(self,s):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()
        if str!=None:
            self._s='\t'+s
            print(self._s+'...')
    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        elapsed_time =int() 
        elapsed_time = (time.perf_counter() - self._start_time)
        self._start_time = None
        print(self._s+f' 计时结束，耗时: {elapsed_time:0.4f} 秒.\n')
        self._s=None