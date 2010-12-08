all: ../pk/widgets/resources.py

../pk/widgets/resources.py: resources.rcc
	pyrcc4 resources.rcc -o ../pk/widgets/resources.py

resources.rcc:
	pkrcc > resources.rcc
