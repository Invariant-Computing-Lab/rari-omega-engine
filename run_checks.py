"""Run the preserved local source tests; never invoke cloud orchestration."""
from pathlib import Path
import sys,tempfile,unittest
ROOT=Path(__file__).resolve().parent
if __name__=='__main__':
    source=ROOT/'source'
    sys.path[:0]=[str(source),str(source/'reference')]
    import omega_common as common
    with tempfile.TemporaryDirectory(prefix='omega-source-tests-') as td:
        common.PKG=source; common.PROTOCOL=source/'OMEGA_PROTOCOL.json'
        common.ROOT=Path(td); common.PYTHON=Path(sys.executable)
        suite=unittest.defaultTestLoader.discover(str(source/'tests'))
        result=unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() and result.testsRun else 1)
