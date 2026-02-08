# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('icon.ico', '.'), ('src/fonts', 'src/fonts')]
binaries = []
hiddenimports = ['src', 'src.menu', 'src.scanner', 'src.session', 'src.exporter', 'src.converter', 'src.redactor', 'src.preview', 'src.config', 'src.clipboard', 'src.chunker', 'src.token_counter', 'src.cli', 'src.utils', 'src.utils.file_filter', 'src.utils.filename', 'src.utils.encoding', 'src.utils.safety', 'gui', 'gui.app', 'gui.main_window', 'gui.scan_tab', 'gui.convert_tab', 'gui.delete_tab', 'gui.files_tab', 'gui.settings_tab', 'gui.widgets', 'gui.workers', 'gui.styles', 'chardet', 'pyperclip', 'fitz', 'pymupdf']
tmp_ret = collect_all('tiktoken')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('tiktoken_ext')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main_gui.py'],
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
    name='ContextBuilder-GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
