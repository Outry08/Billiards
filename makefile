CFLAGS = -Wall -std=c99 -pedantic

CC = clang

##
## We can define variables for values we will use repeatedly below
##

# LIB = libphylib.so

# OBJS = phylib.o


## top level target -- build all the dependent executables
# all : $(EXE)
all : _phylib.so

## targets for each executable, based on the object files indicated

phylib_wrap.c:
	swig -python phylib.i
	
phylib_wrap.o : phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/Library/Frameworks/Python.framework/Versions/3.11/include/python3.11/ -fPIC -o phylib_wrap.o

_phylib.so : phylib_wrap.o libphylib.so
	$(CC) $(CFLAGS) phylib_wrap.o -shared -L. -L/Library/Frameworks/Python.framework/Versions/3.11/lib -lpython3.11 -lphylib -o _phylib.so

phylib.o : phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o

libphylib.so : phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm

## convenience target to remove the results of a build
clean :
	- rm -f *.o *.so

## Magic line: export LD_LIBRARY_PATH=`pwd`
