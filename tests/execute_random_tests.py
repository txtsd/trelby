#!/usr/bin/env python3
# ut:ignore

# Runs random operations on a Screenplay as a way of trying to find bugs.
# Note that this is not part of the normal test run, this has to be run
# manually.

import random
import sys
import traceback

# FIXME
from typing import Optional

import os
location = os.path.dirname(__file__)
sys.path.append(os.path.join(location, "../src"))

from screenplay import Screenplay


import u

# Generates, stores, saves, loads, and runs operations against a Screenplay
# object.
class Ops:
    sp: Optional[Screenplay]
    def __init__(self):
        # A list of Op objects
        self.ops = []

        # A Screenplay object
        self.sp = None

        # Index of next operation to run
        self.nextPos = 0

    # Run next operation. returns True when more operations are waiting to be
    # run, False otherwise.
    def run(self):
        self.sp = self.ops[self.nextPos].run(self.sp)
        self.nextPos += 1

        return self.nextPos < len(self.ops)

    # Add given Operation.
    def add(self, op):
        self.ops.append(op)

    # Return self.ops as a text string
    def save(self)->str:
        s = ""

        for op in self.ops:
            s += op.save() + "\n"

        return s

    # Construct a new Ops from the given string.
    @staticmethod
    def load(s):
        self = Ops()

        for line in s.splitlines():
            if not line.startswith("#"):
                self.ops.append(Op.load(line))

        return self

# A single operation
class Op:
    funcs = [
        "abort",
        "addChar",
        "deleteBackward",
        "deleteForward",
        "insertForcedLineBreak",
        "moveDown",
        "moveEnd",
        "moveLeft",
        "moveLineEnd",
        "moveLineStart",
        "moveRight",
        "moveSceneDown",
        "moveSceneUp",
        "moveStart",
        "moveUp",
        "redo",
        "selectAll",
        "selectScene",
        "setMark",
        "splitElement",
        "tab",
        "toActBreak",
        "toAction",
        "toCharacter",
        "toDialogue",
        "toNote",
        "toParen",
        "toPrevTypeTab",
        "toScene",
        "toShot",
        "toTransition",
        "undo",
        ]

    # FIXME: not tested editing commands:
    #   -removeElementTypes
    #   -cut (getSelectedAsCD(True))
    #   -paste

    def __init__(self, name = None):
        # Name of operation
        self.name = name

        # Arguments to operation. Currently, a list of ints, but it's probable
        # we need another class, Arg, that can represent an arbitrary argument.
        self.args = []

    # Run this operation against the given screenplay. returns either sp or a
    # new Screenplay object (if the operation is NEW/LOAD).
    def run(self, sp):
        if self.name == "NEW":
            return u.new()
        elif self.name == "LOAD":
            return u.load()

        if self.args:
            sp.cmd(self.name, chr(self.args[0]))
        else:
            sp.cmd(self.name)

        return sp

    # Get a random operation.
    # FIXME: this should have different probabilities for different
    #  operations.
    @staticmethod
    def getRandom():
        self = Op()

        f = self.__class__.funcs
        self.name = f[random.randint(0, len(f) - 1)]

        if self.name == "addChar":
            self.args.append(random.randint(0, 255))

        return self

    # Return self as a text string
    def save(self):
        s = self.name

        for arg in self.args:
            s += ",%s" % str(arg)

        return s

    # Construct a new Ops from the given string
    @staticmethod
    def load(s):
        vals = s.split(",")

        self = Op()
        self.name = vals[0]
        for i in range(1, len(vals)):
            self.args.append(int(vals[i]))

        return self

# Run random operations forever
def runRandomOps():
    cnt = 0
    while True:
        rounds = max(1, int(random.gauss(15000, 4000)))
        print("Count %d (%d rounds)" % (cnt, rounds))

        ops = Ops()
        failed = False

        # Every 10th time, test operations on an empty script
        if (cnt % 10) == 0:
            ops.add(Op("NEW"))
        else:
            ops.add(Op("LOAD"))

        for i in range(rounds):
            if i != 0:
                ops.add(Op.getRandom())

            try:
                ops.run()
                # FIXME: add a --validate option
                ops.sp._validate()
            except KeyboardInterrupt:
                raise
            except:
                print(" Failed, saving...")
                save(ops, cnt)
                failed = True

                break

        if not failed:
            try:
                ops.sp._validate()
                s = ops.sp.save()
                u.loadString(s.decode())
            except KeyboardInterrupt:
                raise
            except:
                print(" Failed in save/load, saving...")
                save(ops, cnt)

        cnt += 1

# Run ops from given file
def runOpsFromFile(filename):
    f = open(filename, "r")
    s = f.read()
    f.close()

    ops = Ops.load(s)

    while 1:
        more = ops.run()

        # FIXME: add a --validate option
        ops.sp._validate()

        if not more:
            break

# Save information about failed ops.
def save(ops: Ops, cnt: int):
    f = open("%d.ops" % cnt, "w")

    tbLines = traceback.format_exception(*sys.exc_info())

    for l in tbLines:
        # Traceback lines contain embedded newlines, so it gets a bit complex
        # escaping every line with # and keeping the formatting correct.
        f.write("#" + l.rstrip().replace("\n", "\n#") + "\n")

    f.write(ops.save())
    f.close()

    f = open("%d.trelby" % cnt, "wb")
    f.write(ops.sp.save())
    f.close()

def main():
    if len(sys.argv) == 1:
        runRandomOps()
    else:
        runOpsFromFile(sys.argv[1])

main()
