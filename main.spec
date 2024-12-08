# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('./config.json', './'),
        
        ('./extensions/entertainment.py', './extensions'),
        ('./extensions/event.py', './extensions'),
        ('./extensions/moderation.py', './extensions'),
        ('./extensions/nickname.py', './extensions'),
        
        ('./settings/config.py', './settings'),
        ('./settings/keep_alive.py', './settings'),
        ('./settings/restarter.py', './settings'),
        
        ('./utils/apiWargaming.py', './utils'),
        ('./utils/constants.py', './utils'),
        ('./utils/functions.py', './utils'),
        ('./utils/modal.py', './utils')
    ],
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
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)