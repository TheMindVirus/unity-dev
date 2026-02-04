@echo off
set GCC=%CD%\..\mingw32\bin\gcc.exe
set PATH=%PATH%;%CD%\..\mingw32\bin\
set LIB=%CD%\..\mingw32\bin\
%GCC% -O0 -c blaskernel.c -o blaskernel.o
%GCC% -O2 blaskernel.o -o blaskernel.dll -s -shared -Wl,--subsystem,windows -L %LIB%