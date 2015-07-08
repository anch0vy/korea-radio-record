#Korea Radio Recoder

##Source

- radio_util.py
	- core file for parsing and download radio streaming file

- concat.py
	- group file by timestamp
	- run ffmpeg for concatenating stream files

- 1radio.py , cbs.py , channelm.py , coolfm.py , happyfm.py , lovefm.py , mbcfm4u.py , mbcradio.py , powerfm.py
	- set some value(m3u8 url, useragent, save folder , etc...) and run radio_util

##Requirements

- Python
	- Python 2.7
	- [m3u8](https://pypi.python.org/pypi/m3u8/0.2.4)
	- [pycrypto](https://pypi.python.org/pypi/pycrypto)(for lovefm.py and powerfm.py)

- ffmpeg(compiled with flag --enable-libfdk-aac, [link](https://trac.ffmpeg.org/wiki/Encode/AAC))

##Env setting

- make '/radio' folder
- make '/radio/error' folder
- edit crontab
```
* * * * * PYTHON_PATH SCRIPT_FOLDER/1radio.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/cbs.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/channelm.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/coolfm.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/happyfm.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/lovefm.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/mbcfm4u.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/mbcradio.py
* * * * * PYTHON_PATH SCRIPT_FOLDER/powerfm.py
0 0 * * * PYTHON_PATH SCRIPT_FOLDER/concat.py
```

##Usage

After env setting, check '/radio/CHANNEL_NAME' folder.

Streaming files are in /radio/CHANNEL_NAME/raw folder.

Concatenated file wiil be saved at /radio/CHANNEL_NAME folder. (yy-mm-dd_HHHH.*, first HH is start hour, next HH is end hour.)

If ffmpeg fail to concatenate stream file, stream files are remained at /radio/CHANNEL_NAME/raw/DATETIME folder. (check streaming file size)

If you want to use lovefm.py and powerfm.py, you should find DES decrypt key.