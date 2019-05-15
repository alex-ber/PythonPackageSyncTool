#one-time setup
import os
cwd = os.getcwd()
if cwd.endswith('PythonPackageSyncTool'):
    os.chdir(os.path.join(cwd, 'data'))

