@echo off
set GCC=%CD%\mingw32\bin\gcc.exe
set PATH=%PATH%;%CD%\mingw32\bin\
set LIB=%CD%\mingw32\bin\
%GCC% -c complicated_lib.c -o complicated_obj.o
%GCC% complicated_obj.o -o complicated_dll.dll -s -shared -Wl,--subsystem,windows -L %LIB%