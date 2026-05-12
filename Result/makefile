FILE = *.sav *.csv ../input.ini ../log.txt

default: 7z

targz:
	tar -zcf Result.tar.gz $(FILE)

tar:
	tar -cvf Result.tar $(FILE)

7z:
	7z a Result.7z $(FILE)