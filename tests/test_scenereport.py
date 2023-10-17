import scenereport
import u
import util

# Tests scene report (just that it runs without exceptions, for now)

def testBasic():
    sp = u.load()
    report = scenereport.SceneReport(sp)
    data = report.generate()

    # Try to catch cases where generate returns something other than a PDF
    # document
    assert len(data) > 200
    assert data[:8] == util.toLatin1("%PDF-1.5")
