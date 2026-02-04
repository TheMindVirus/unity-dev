@echo off
set GPP=%CD%\..\mingw32\bin\g++.exe
set LIB=%CD%\..\mingw32\bin\
set PATH=%PATH%;%LIB%
%GPP% -c customfft.cpp -o customfft.o
%GPP% customfft.o -o customfft.exe -L %LIB%
cmd /k customfft.exe