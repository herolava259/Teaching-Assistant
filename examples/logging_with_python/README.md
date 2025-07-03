# Logging cheetsheet
## Basic

```python
import logging
logging.warning("Remain calm!")
```
## 2. Log Level 

| Log Level |  Function         | Description 
|-----------|-------------------|
|  DEBUG    | logging.debug()   | Provides detailed information that's valuable to you as a developer 
|  INFO     | logging.info()    | Provides general infomation about what's going on with your program
|  WARNING  | logging.warning() | Indicates that there's something you look into.
|  ERROR    | logging.error()   | alerts you to an unexpected problem that's occured in your program.
| CRITICAL  | logging.critical()| Tells you that a serious error has occured and may have crashed your app.

## 3. Adjusting the Log Level 
- To set up basic logging configuration and adjust the log level, the logging module come with a basicConfig()

- Ex: 

```python
import logging 
logging.basicConfig(level=logging.Debug)
logging.debug("This will get logged.")
#DEBUG:root:This will get logged.
```

## 4. Formatting the Output

```python
import logging
logging.basicConfig(format="%(levelname)s:%(name)s:%(message)s")
logging.warning("Hello, Warning!")
##Output: "WARNING:root:Hello, Warning!"
```

- Keynote: [template-string-url](https://docs.python.org/3/library/string.html#string.Template)

## 4. Logging to a file

```python
import logging
logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

logging.warning("Save me!")

#Output: "2025-06-28 09:55 - WARNING - Save me!"
```

## 5. Displaying Variable Data 

```python
import logging 
logging.basicConfig(
    format="{asctime} - {levelname} - {message}",
    style="{"
    datefmt="%Y-%m-%d %H-%m",
    level=logging.DEBUG
)

name="Samara"
logging.debug(f"{name=}")
#OUPUT: 2025-30-06 9:40 - DEBUG - name='Samira'
```


## 6. Capturing Stack Traces
- The logging module also allows you to capture the full stack traces in an application. Exception information can be captured if exc_info parameters is passed as True, and the logging functions are called like this:


```python
>>> import logging
>>> logging.basicConfig(
...     filename="app.log",
...     encoding="utf-8",
...     filemode="a",
...     format="{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> donuts = 5
>>> guests = 0
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.error("DonutCalculationError", exc_info=True)
...
```

- app.log

```text
2024-07-22 15:04 - ERROR - DonutCalculationError
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
ZeroDivisionError: division by zero
```

- If exc_info isn’t set to True, the output of the above program wouldn’t tell you anything about the exception, which, in a real-world scenario, might not be as simple as a ZeroDivisionError.


- Since logging errors is such a common task, logging comes with a function that can save you some typing. If you’re logging from an exception handler, which you’ll learn more about later, then you can use the logging.exception() function. This function logs a message with the level ERROR and adds exception information to the message.

Here’s an example of how you’ll get the same output as above using logging.exception():

```python
>>> try:
...     donuts_per_guest = donuts / guests
... except ZeroDivisionError:
...     logging.exception("DonutCalculationError")
...
```
- Calling logging.exception() is like calling logging.error(exc_info=True). Since the logging.exception() function always dumps exception information, you should only call logging.exception() from an exception handler.

 - When you use logging.exception(), it shows a log at the level of ERROR. If you don’t want that, you can call any of the other logging functions from debug() to critical() and pass the exc_info parameter as True.

## 7. Creating a Custom Logger

*1. Instantiating Your Logger

```python
>>> import logging
>>> logger = logging.getLogger(__name__)
>>> logger.warning("Look at my logger!")
Look at my logger!
```

*2. Using Handlers
- Handlers come into the picture when you want to configure your own loggers. For example, when you want to send the log messages to different destinations like the standard output stream or a file.

```python
import logging
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
```

- and:
```python
>>> logger.addHandler(console_handler)
>>> logger.addHandler(file_handler)
>>> logger.handlers
[
  <StreamHandler <stderr> (NOTSET)>,
  <FileHandler /Users/RealPython/Desktop/app.log (NOTSET)>
]
```

*3. Adding Formaters to Your Handlers

```python
>>> import logging
>>> logger = logging.getLogger(__name__)
>>> console_handler = logging.StreamHandler()
>>> file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
>>> logger.addHandler(console_handler)
>>> logger.addHandler(file_handler)
>>> formatter = logging.Formatter(
...    "{asctime} - {levelname} - {message}",
...     style="{",
...     datefmt="%Y-%m-%d %H:%M",
... )

>>> console_handler.setFormatter(formatter)
>>> logger.warning("Stay calm!")
2024-07-22 15:58 - WARNING - Stay calm!
```

*4. Setting the Log Levels of Custom Loggers

```python
>>> import logging
>>> logger = logging.getLogger(__name__)
>>> logger.level
0

>>> logger
<Logger __main__ (WARNING)>

>>> logger.parent
<RootLogger root (WARNING)>
```

*5. Setting Log Level of Custom Logger

```python
>>> import logging
>>> logger = logging.getLogger(__name__)
>>> logger.level
0

>>> logger
<Logger __main__ (WARNING)>

>>> logger.parent
<RootLogger root (WARNING)>
>>> logger.getEffectiveLevel()
30
>>> logger.setLevel(10)
>>> logger
<Logger __main__ (DEBUG)>

>>> logger.setLevel("INFO")
>>> logger
<Logger __main__ (INFO)>
>>> formatter = logging.Formatter("{levelname} - {message}", style="{")
>>> console_handler = logging.StreamHandler()
>>> console_handler.setFormatter(formatter)
>>> logger.addHandler(console_handler)
>>> logger.debug("Just checking in!")
>>> logger.info("Just checking in, again!")
INFO - Just checking in, again!
```

## 8. Filtering Logs
In other words, there are three approaches to creating filters for logging. You can create a:

    1.Subclass of logging.Filter() and overwrite the .filter() method
    2.Class that contains a .filter() method
    3.Callable that resembles a .filter() method 
```python
>>> import logging
>>> def show_only_debug(record):
...     return record.levelname == "DEBUG"
...

>>> logger = logging.getLogger(__name__)
>>> logger.setLevel("DEBUG")
>>> formatter = logging.Formatter("{levelname} - {message}", style="{")

>>> console_handler = logging.StreamHandler()
>>> console_handler.setLevel("DEBUG")
>>> console_handler.setFormatter(formatter)
>>> console_handler.addFilter(show_only_debug)
>>> logger.addHandler(console_handler)

>>> file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
>>> file_handler.setLevel("WARNING")
>>> file_handler.setFormatter(formatter)
>>> logger.addHandler(file_handler)

>>> logger.debug("Just checking in!")
DEBUG - Just checking in!

>>> logger.warning("Stay curious!")
>>> logger.error("Stay put!")
```
## End and further: Source and Guide
- [Modern-Python-Logging](https://www.youtube.com/watch?v=9L77QExPmI0&t=648s)
- [Basic-Logging-Python](https://realpython.com/python-logging/)
- [Logging-Python-doc](https://docs.python.org/3/library/logging.html)
- [logging-with-logstash](https://pypi.org/project/python-elastic-logstash/)
- [Logging-Cookbook](https://docs.python.org/3/howto/logging-cookbook.html)
- [Regular-Expression](https://quantrimang.com/hoc/regex-trong-python-165471)







