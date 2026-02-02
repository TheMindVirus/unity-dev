@echo off
set GCC=%CD%\mingw32\bin\gcc.exe
set PATH=%PATH%;%CD%\mingw32\bin\
set LIB=%CD%\mingw32\bin\
%GCC% -O0 -c live.c -o live.o
%GCC% -O2 live.o -o live.dll -s -shared -Wl,--subsystem,windows -L %LIB%