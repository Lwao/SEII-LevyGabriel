all:
	clear
	gcc -Wall -g src/foo.c -c -Iinclude -o src/foo.o
	gcc -Wall -g src/bar.c -c -Iinclude -o src/bar.o
	gcc -Wall -g src/foo.o src/bar.o src/main.c -Iinclude -o app
	-rm src/foo.o src/bar.o 
	./app 
	./app a b c d e f
	./app a b
	./app -sup 42 42
	./app -sum 42 42
	./app -sub 42 42