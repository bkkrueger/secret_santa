# Imports
import math
import random
import sys

# =============================================================================
# Miscellaneous support functions

def digits(N):
    return(math.floor(math.log10(N))+1)

# =============================================================================
# Read input from a file

# =============================================================================
# Specify test input

def get_test_input(N,P):

    # Verify that the arguments are valid
    if int(N) != N or N <= 0:
        raise ValueError(" ".join(["Argument N to",
            sys._getframe().f_code.co_name, "must be a positive integer."]))
    if N < 6:
        raise ValueError(" ".join(["Argument N to",
            sys._getframe().f_code.co_name,
            "must be at least 6 for sane testing."]))
    if int(P) != P or P <= 0:
        raise ValueError(" ".join(["Argument P to",
            sys._getframe().f_code.co_name, "must be a positive integer."]))
    if P > (N-1)*(N+1)/4 - N:
        # N(N-1) possible pairs
        # this includes [A,B] and [B,A] -- only (1/2)(N-1)^2 unique pairs
        # must still have N possible pairs
        # upper bound is (N^2-4N+1)/2
        # for the same of being safe, let's limit further by cutting this in
        #   half again
        print("N = {0}, P = {1}".format(N,P))
        print("(N-1)(N+1)/4 - N = {0}".format((N-1)*(N+1)/4-N))
        raise ValueError(" ".join(["Argument P to",
            sys._getframe().f_code.co_name,
            "cannot be greater than (N-1)(N+1)/4-N."]))

    # Select some names at random
    name_list = ["Alicia"   , "Alexander",
                 "Bronwyn"  , "Bartholomew",
                 "Catherine", "Charles",
                 "Danielle" , "Duncan",
                 "Elspeth"  , "Edwin",
                 "Fern"     , "Fergus",
                 "Georgina" , "Gus",
                 "Helene"   , "Harry",
                 "Isola"    , "Ivan",
                 "Jennifer" , "Jackson",
                 "Kelly"    , "Kevin",
                 "Lois"     , "Liam",
                 "Maude"    , "Malcolm",
                 "Nolwenn"  , "Noel",
                 "Ophelia"  , "Oscar",
                 "Penelope" , "Peter",
                 "Queenie"  , "Quincy",
                 "Rosalyn"  , "Roland",
                 "Samantha" , "Samuel",
                 "Tanya"    , "Theodore",
                 "Ulrike"   , "Ulysses",
                 "Veronica" , "Victor",
                 "Wendy"    , "William",
                 "Xanthippe", "Xavier",
                 "Yasmina"  , "Yannick",
                 "Zelda"    , "Zachariah"]
    if N <= len(name_list):
        random.shuffle(name_list)
        names = name_list[0:N]
    else:
        names = []
        for i in range(1,N+1):
            name = "{i:0{w}d}-{name}".format(
                    i=i,w=digits(N),name=random.choice(name_list))
            names.append(name)

    # Build some disallowed pairs at random
    bad_pairs = []
    i = 0
    while True:
        n1 = random.choice(names)
        n2 = random.choice(names)
        if n1 < n2:
            pair = (n1, n2)
        elif n1 == n2:
            continue
        else:
            pair = (n2, n1)
        if pair not in bad_pairs:
            bad_pairs.append(pair)
        i = i + 1
        if i == P:
            break

    return(names, bad_pairs)

def TEST_get_test_input():
    N = 6
    P = 2
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    names, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, name in enumerate(names):
        print("    {0:{1}}: {2}".format(i+1,digits(N),name))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(i+1,digits(P),pair))
    N = 60
    P = 60
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    names, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, name in enumerate(names):
        print("    {0:{1}}: {2}".format(i+1,digits(N),name))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(i+1,digits(P),pair))

# =============================================================================
# Verify input

def verify_input():
    pass

# =============================================================================
# Process input

# =============================================================================
# Perform a single selection pass

# =============================================================================
# Loop to get a valid selection

# =============================================================================
# Main

def main():
    TEST_get_test_input()

if __name__ == "__main__":
    main()
