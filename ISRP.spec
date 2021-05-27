# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['c:\\Users\\melvin_venceslass\\3D Objects\\mypythons\\Automations - 2021\\Roche Packing Soln\\dev_4\\ISRP.pyw'],
             pathex=['C:\\Users\\melvin_venceslass\\3D Objects\\mypythons\\Automations - 2021\\Roche Packing Soln\\dev_4'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
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
          name='ISRP',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False , icon='c:\\Users\\melvin_venceslass\\3D Objects\\mypythons\\Automations - 2021\\Roche Packing Soln\\dev_4\\isrp_PX4_icon.ico')
