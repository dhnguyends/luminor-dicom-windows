# PyInstaller build recipe for Luminor.exe
#   pyinstaller --noconfirm --clean luminor.spec
#
# One-folder build (dist\Luminor\Luminor.exe + _internal\): starts faster and
# triggers fewer antivirus false positives than a single-file exe.
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

HERE = Path(SPECPATH)
SOURCE = HERE.parent / "Claude-Radio"  # Luminor source code (server.py, static/, docs/)

a = Analysis(
    [str(HERE / "luminor_app.py")],
    pathex=[str(SOURCE)],
    datas=[
        (str(SOURCE / "static"), "static"),
        (str(SOURCE / "docs"), "docs"),
        (str(SOURCE / "LICENSE"), "."),
        (str(SOURCE / "NOTICE"), "."),
    ],
    # server.py is imported at run time; pydicom loads pixel decoders as plugins
    hiddenimports=["server", *collect_submodules("pydicom.pixels")],
    excludes=["matplotlib", "scipy", "pandas", "IPython", "pytest", "PIL"],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="Luminor",
    icon=str(HERE / "assets" / "luminor.ico"),
    version=str(HERE / "assets" / "version_info.txt"),
    console=False,  # windowed app; output goes to %APPDATA%\Luminor\luminor.log
    upx=False,      # UPX compression causes antivirus false positives
)

coll = COLLECT(exe, a.binaries, a.datas, name="Luminor", upx=False)
