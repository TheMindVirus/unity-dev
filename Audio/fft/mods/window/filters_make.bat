@echo off
set GCC=%CD%\..\mingw32\bin\gcc.exe
set PATH=%PATH%;%CD%\..\mingw32\bin\
set INCLUDE=-I C:\Python36\include\
set LIB=-L %CD%\..\mingw32\bin\ -L %CD%\..\mingw32\lib\gcc\i686-w64-mingw32\15.2.0\ -L C:\Python36\libs\ -lpython36 -fopenmp -lgomp -lpthread -ffast-math
echo -fopenmp
%GCC% -O3 filters.c -o filters.cp36-win32.pyd -s -shared -static -Wl,--subsystem,windows %INCLUDE% %LIB%