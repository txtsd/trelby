import screenplay
import pml

# Used to iteratively add PML pages to a document
class Pager:
    def __init__(self, cfg):
        self.doc = pml.Document(cfg.paperWidth, cfg.paperHeight)

        # Used in several places, so keep around.
        self.charIndent = cfg.getType(screenplay.CHARACTER).indent
        self.sceneIndent = cfg.getType(screenplay.SCENE).indent

        # Current scene number
        self.scene = 0

        # Number of CONTINUED:'s lines added for current scene
        self.sceneContNr = 0
