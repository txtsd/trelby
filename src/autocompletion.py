import config
import mypickle
import screenplay
import util

# Manages auto-completion information for a single script
class AutoCompletion:
    def __init__(self):
        # Type configs, key = line type, value = Type
        self.types = {}

        # Element types
        t = Type(screenplay.SCENE)
        self.types[t.ti.lt] = t

        t = Type(screenplay.CHARACTER)
        self.types[t.ti.lt] = t

        t = Type(screenplay.TRANSITION)
        t.items = [
            "BACK TO:",
            "CROSSFADE:",
            "CUT TO:",
            "DISSOLVE TO:",
            "FADE IN:",
            "FADE OUT",
            "FADE TO BLACK",
            "FLASHBACK TO:",
            "JUMP CUT TO:",
            "MATCH CUT TO:",
            "SLOW FADE TO BLACK",
            "SMASH CUT TO:",
            "TIME CUT:"
            ]
        self.types[t.ti.lt] = t
        
        t = Type(screenplay.SHOT)
        self.types[t.ti.lt] = t

        self.refresh()

    # Load config from string 's'
    # Does not throw any exceptions
    # Silently ignores any errors
    # Always leaves config in an okay state
    def load(self, s):
        vals = mypickle.Vars.makeVals(s)

        for t in self.types.values():
            t.load(vals, "AutoCompletion/")

        self.refresh()

    # Save config into a string and return that
    def save(self):
        s = ""

        for t in self.types.values():
            s += t.save("AutoCompletion/")

        return s

    # Fix up invalid values and uppercase everything
    def refresh(self):
        for t in self.types.values():
            tmp = []

            for v in t.items:
                v = util.upper(util.toInputStr(v)).strip()

                if len(v) > 0:
                    tmp.append(v)

            t.items = tmp

    # Get type's Type, or None if it doesn't exist
    def getType(self, lt):
        return self.types.get(lt)

# Auto-completion info for one element type
class Type:
    cvars = None

    def __init__(self, lt):

        # Pointer to TypeInfo
        self.ti = config.lt2ti(lt)

        if not self.__class__.cvars:
            v = self.__class__.cvars = mypickle.Vars()

            v.addBool("enabled", True, "Enabled")
            v.addList("items", [], "Items",
                      mypickle.StrLatin1Var("", "", ""))

            v.makeDicts()

        self.__class__.cvars.setDefaults(self)

    def save(self, prefix):
        prefix += "%s/" % self.ti.name

        return self.cvars.save(prefix, self)

    def load(self, vals, prefix):
        prefix += "%s/" % self.ti.name

        self.cvars.load(vals, prefix, self)
