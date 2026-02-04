@echo off
set GPP=%CD%\..\mingw32\bin\g++.exe
set LIB=%CD%\..\mingw32\bin\
set PATH=%PATH%;%LIB%
%GPP% -c pocketfft.cpp -o pocketfft.o
%GPP% pocketfft.o -o pocketfft.exe -L %LIB%
cmd /k pocketfft.exe