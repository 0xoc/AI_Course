from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
asaid = And(AKnight, AKnave)

knowledge0 = And(
    # a is knave
    Biconditional(AKnave, Not(asaid)),
    # a is knight
    Biconditional(AKnight, asaid),
    # game rules
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
asaid = And(AKnave, BKnave)
knowledge1 = And(
    # a is knave
    Biconditional(AKnave, Not(asaid)),
    # a is knight
    Biconditional(AKnight, asaid),
    # game rules
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
asaid = Or(And(AKnight, BKnight), And(AKnave, BKnave))
bsaid = Or(And(AKnight, BKnave), And(AKnave, BKnight))
knowledge2 = And(
    # a is knave
    Biconditional(AKnave, Not(asaid)),
    # a is knight
    Biconditional(AKnight, asaid),

    # b is knave
    Biconditional(BKnave, Not(bsaid)),
    # b is knight
    Biconditional(BKnight, bsaid),

    # game rules
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

def xor(s1, s2):
    return And(
        Or(s1,s2),
        Not(And(s1,s2))
    )

asaid = xor(AKnight, AKnave)
bsaid = And(AKnave, CKnight)
csaid = AKnight

knowledge3 = And(
    # a
    Biconditional(AKnave, Not(asaid)),
    Biconditional(AKnight, asaid),

    # b
    Biconditional(BKnave, Not(bsaid)),
    Biconditional(BKnight, bsaid),

    # c
    Biconditional(CKnave, Not(csaid)),
    Biconditional(CKnight, csaid),

    # game rules
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(AKnave, Not(AKnight)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(BKnave, Not(BKnight)),
    Biconditional(CKnight, Not(CKnave)),
    Biconditional(CKnave, Not(CKnight)),

)

def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
