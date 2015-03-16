SET PASYVAT=%CD%
C:
CD "\Program Files (x86)\Microsoft Visual Studio 9.0\Common7\Tools"
CALL vsvars32.bat

CD %PASYVAT%
SET PATH=C:\Python27;C:\MinGW\bin;C:\SDK\Bin;%PATH%

python pasyvat

pause