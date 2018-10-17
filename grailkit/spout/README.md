
This is binding to Spout Library. 
Spout available only on Windows, for Mac OS use Syphon instead.

Compile using Microsoft Visual Studio 2014 or later, and
don't forget to copy SpoutLibrary.dll to same folder where _spout.pyd is located.

When compiling library include `pybind11` and `python`, 
usually they located in `$PYTHON/include` (if pybind installed using pip), 
and SpoutSDK located in `$PROGRAMFILES/Spout2/SPOUTSDK/SpoutSDK`
Also add `$PYTHON/Libs` to Visual Studio project libraries path.

Summary:

    includes:
        `$PYTHON/includes`
        `$PROGRAMFILES/Spout2/SPOUTSDK/SpoutSDK`

    libraries:
        `$PYTHON/libs`
        `$PROGRAMFILES/Spout2/SPOUTSDK/SpoutLibrary/Binaries/x64` (SpoutLibrary.dll needed in final distribution)

    Linker -> input:
        `$PROGRAMFILES\Spout2\SPOUTSDK\SpoutLibrary\Binaries\x64\SpoutLibrary.lib`
        