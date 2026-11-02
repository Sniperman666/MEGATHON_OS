import sys


def _preflight() -> None:
    """
    Fail with a clear message when run on an unsupported OS or with missing dependencies
    """
    if sys.platform != "darwin":
        sys.exit("OpenCore Legacy Patcher only runs on macOS (detected: {}).".format(sys.platform))

    missing = []
    for module, package in (("packaging", "packaging"), ("wx", "wxpython"), ("requests", "requests")):
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        sys.exit("Missing dependencies: {}\nInstall with: python3 -m pip install -r requirements.txt".format(", ".join(missing)))


_preflight()

from .application_entry import main