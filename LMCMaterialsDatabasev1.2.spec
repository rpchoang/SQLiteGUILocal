# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['SQLiteGUI.py'],
             pathex=['C:\\Users\\RonaldHoang\\SQLite'],
             binaries=[],
             datas=[],
             hiddenimports=['multiprocesing'],
             hookspath=[],
             runtime_hooks=['getsysdirectory.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='LMCMaterialsDatabasev1.2',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='Lordstown.ico')
