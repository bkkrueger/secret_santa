# Imports
import random
import sys

# =============================================================================
# Specify test input

def get_test_input(N,P):

    manufactured_input = {}

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate participants

    # TODO: Move this to a separate subroutine (and this whole fake input stuff
    #       to a separate module)

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

    # Build random email addresses for the users
    emails = {name: "test-{0}@somedomain.com".format(name) for name in names}

    # Add emails dict to input
    manufactured_input["PARTICIPANTS"] = emails

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate invalid pairs

    # TODO: Move this to a separate subroutine (and this whole fake input stuff
    #       to a separate module)

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

    # To help demonstrate later processing: swap order of some pairs
    bad_pairs = [(pair[0],pair[1]) if random.randint(0,1) == 0 else
            (pair[1],pair[0]) for pair in bad_pairs]

    # Add pairs to input
    manufactured_input["DO NOT PAIR"] = bad_pairs

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate message

    # TODO: Move this to a separate subroutine (and this whole fake input stuff
    #       to a separate module)

    manufactured_input["MESSAGE SUBJECT"] = "test email for secret_santa.py"

    manufactured_input["MESSAGE BODY"] = "<br>".join([
        "This is a test email for the secret_santa.py software.",
        "",
        "You are {gifter}.  You are giving a gift to {recipient}.",
        "",
        "This email was automatically generated.",
        ])

    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    # Generate organizer

    # TODO: Move this to a separate subroutine (and this whole fake input stuff
    #       to a separate module)

    organizer = {
            "name": "Brendan K. Krueger",
            "email": "bkkrueger@gmail.com",
            "smtp url": "smtp.gmail.com",
            "smtp port": 587,
            }

    manufactured_input["ORGANIZER"] = organizer

    return(manufactured_input)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def TEST_get_test_input():
    N = 6
    P = 2
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    emails, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, (name, email) in enumerate(emails.items()):
        print("    {0:{1}}: {2} <{3}>".format(i+1,digits(N),name,email))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(i+1,digits(P),pair))
    print("")
    N = 60
    P = 60
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    emails, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, (name, email) in enumerate(emails.items()):
        print("    {0:{1}}: {2} <{3}>".format(i+1,digits(N),name,email))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(i+1,digits(P),pair))


# =============================================================================
# Main

# TODO This is no longer a reasonable main.  It should probably just call the
# test method?

def main():
    N = 10
    P = 14
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    emails, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, (name, email) in enumerate(emails.items()):
        print("    {0:{1}}: {2} <{3}>".format(i+1,digits(N),name,email))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(i+1,digits(P),pair))

    print("Verify input:")
    verify_input(emails, bad_pairs)
    print("  Input valid")

    print("Process input:")
    forbidden = process_input(emails, bad_pairs)
    print("  Invalid Dict:")
    names = sorted(list(forbidden.keys()))
    for name in names:
        invalid = sorted(list(forbidden[name]))
        print("    {0}:".format(name))
        for name2 in invalid:
            print("      {0}".format(name2))

    print("Run selection loop:")
    pairs = selection_loop(emails, forbidden)
    #for giver, receiver in pairs.items():
    #    print("  {0} is giving a gift to {1}".format(giver, receiver))

    print("Writing results to a file:")
    filename = input("filename: ")

    with open(filename,'w') as outfile:
        for giver in pairs.keys():
            outfile.write("   {0}   {1}   {2}\n".format(
                giver, emails[giver], pairs[giver]))

    #print("Send a test email to demonstrate that sending works.")
    #test_email_send(pairs)

if __name__ == "__main__":
    main()
