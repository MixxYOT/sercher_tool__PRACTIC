# -*- mode: python ; coding: utf-8 -*-
import os
from PyInstaller.utils.hooks import (
    collect_submodules, 
    collect_data_files, 
    collect_dynamic_libs
)

main_script = os.path.join('src', '__main__.py')

datas = [('src', 'src')]
binaries = []
hiddenimports = [
    'docx', 
    'openpyxl', 
    'olefile', 
    'lxml'
]

hiddenimports += collect_submodules('odf')
hiddenimports += collect_submodules('rich')
datas += collect_data_files('rich')
hiddenimports += collect_submodules('fitz')
binaries += collect_dynamic_libs('fitz')


a = Analysis(
    [main_script],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='searcher',
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