@echo off
set PATH=%PATH%;%CD%\..\..\..\compilers\gcc_mingw\mingw32\bin\
set INCLUDE=-I C:\Python36\include\ -I %CD%\..\..\..\opencl\include\
set LIB=-L %CD%\..\..\..\compilers\gcc_mingw\mingw32\bin\ -L %CD%\..\..\..\compilers\gcc_mingw\mingw32\lib\gcc\i686-w64-mingw32\15.2.0\ -L %CD%\..\..\..\opencl\lib\ -L C:\Python36\libs\ -lopencl -fopenmp -lpython36 -lgomp -lpthread
set CC=%CD%\..\..\..\compilers\gcc_mingw\mingw32\bin\g++.exe
%CC% main.cpp -o main.pyd -shared -static -O3 %INCLUDE% %LIB%
pause