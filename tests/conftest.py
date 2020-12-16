#one-time setup
import os
cwd = os.getcwd()
if cwd.endswith('PythonPackageSyncTool'):
    os.chdir(os.path.join(cwd, 'data'))

#see https://docs.pytest.org/en/latest/mark.html
#see https://docs.pytest.org/en/latest/example/simple.html#control-skipping-of-tests-according-to-command-line-option
def pytest_configure(config):
    config.addinivalue_line(
        "markers", "it:"
    )
