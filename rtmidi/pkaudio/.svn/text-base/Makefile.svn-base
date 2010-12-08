all: 

clean:
	rm -rf build `find . -name "*.pyc"` `find . -name "*~"` `find . -name "*.pyo"` `find . -name build`

uninstall:
	rm -rf `python -c "import distutils.sysconfig, os.path; print os.path.join(distutils.sysconfig.get_python_lib(),'pk')"`
	rm -rf `python -c "import distutils.sysconfig, os.path; print os.path.join(distutils.sysconfig.get_python_lib(),'rtaudio.so')"`
	rm -rf `python -c "import distutils.sysconfig, os.path; print os.path.join(distutils.sysconfig.get_python_lib(),'rtmidi.so')"`	
	rm -rf `python -c "import distutils.sysconfig, os.path; print os.path.join(distutils.sysconfig.get_python_lib(),'soundtouch.so')"`
	rm -rf `python -c "import distutils.sysconfig, os.path; print os.path.join(distutils.sysconfig.get_python_lib(),'dsptools')"`
