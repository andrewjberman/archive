"""Test-support stub for PyMuPDF (not installed on this box): lets test modules that import fitz at module level be collected.
Any USE of fitz raises, so a test that needs a real PDF fails identically on both trees. Not part of either zip."""
def __getattr__(name):
    if name.startswith("__"):
        raise AttributeError(name)
    def _unavailable(*a, **k):
        raise RuntimeError("fitz stub: PyMuPDF is not installed on this box")
    return _unavailable
