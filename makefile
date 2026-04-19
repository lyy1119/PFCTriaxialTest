all:
	echo 'Nothing to do. Run make clean to clean useless file.'
clean:
	rm *.csv *.his errorlog.* pfc3d.log *.temp
	rm -r Python/__pycache__

tar:
	tar -cvf archive.tar *.* Python PFC
