from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
Puzzle0_Asays = And(AKnave, AKnight)
knowledge0 = And(
    # TODO
    Or(AKnight,AKnave),
    Not(And(AKnight,AKnave)),
    Implication(AKnave, Not(Puzzle0_Asays)),
    Implication(AKnight, Puzzle0_Asays) 
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
Puzzle1_Asays = And(AKnave,BKnave)
knowledge1 = And(
    # TODO
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Implication(AKnave,Not(Puzzle1_Asays)),
    Implication(AKnight,Puzzle1_Asays)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."

Puzzle2_Asays =Or(Biconditional(AKnight,BKnight),Biconditional(AKnave,BKnave))  
Puzzle2_Bsays = Or(Biconditional(AKnight,BKnave),Biconditional(AKnave,BKnight))  

knowledge2 = And(
    # TODO
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Implication(AKnight,Puzzle2_Asays),
    Implication(AKnave,Not(Puzzle2_Asays)),
    Implication(BKnight,Puzzle2_Bsays),
    Implication(BKnave,Not(Puzzle2_Bsays))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."

Puzzle3_Asays = And(Or(AKnight,AKnave), Not(And(AKnight,AKnave)))
Puzzle3_Csays = AKnight



knowledge3 = And(
    # TODO
    Or(AKnight,AKnave),
    Or(BKnight,BKnave),
    Not(And(AKnight,AKnave)),
    Not(And(BKnight,BKnave)),
    Or(CKnight,CKnave),
    Not(And(CKnight,CKnave)),
    BKnave,
    Implication(AKnight,Puzzle3_Asays),
    Implication(AKnave,Not(Puzzle3_Asays)),
    Implication(CKnight,Puzzle3_Csays),
    Implication(CKnave,Not(Puzzle3_Csays))
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
