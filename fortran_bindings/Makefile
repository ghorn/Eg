all : blah.o libblah.a run_me

blah.o : blah.f
	gfortran -Wall -Wextra -c blah.f -o blah.o

libblah.a : blah.o
	ar -rcs libblah.a blah.o

run_me : run_me.c blah.h libblah.a
	gcc run_me.c -L. -lblah -Wall -Wextra -o run_me

clean ::
	rm -f blah.o
	rm -f libblah.a
	rm -f run_me
