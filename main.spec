# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[('C:\\Users\\서상혁\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sdl2dll\\dll\\SDL2.dll', 'pico2d'), ('C:\\Users\\서상혁\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sdl2dll\\dll\\SDL2_image.dll', 'pico2d'), ('C:\\Users\\서상혁\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sdl2dll\\dll\\SDL2_ttf.dll', 'pico2d'), ('C:\\Users\\서상혁\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sdl2dll\\dll\\SDL2_mixer.dll', 'pico2d'), ('C:\\Users\\서상혁\\AppData\\Local\\Programs\\Python\\Python313\\Lib\\site-packages\\sdl2dll\\dll\\SDL2_gfx.dll', 'pico2d')],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
