# https://github.com/underbluewaters/secret-santa
# https://pymotw.com/2/getpass/

import copy
import random
import sys

def main():
    #names = ["Erin", "Brendan", "Kristin", "Olivia", "Anika", "Odin"]
    #dont_pair = [["Erin", "Brendan"]]
    names = []
    dont_pair0 = []
    for n in range(5):
        for x in ["a","b"]:
            names.append("{0}{1}".format(n+1,x))
        dont_pair0.append([names[-2],names[-1]])
    dont_pair0.append(["2a","4a"])
    dont_pair0.append(["2b","3b"])
    dont_pair0.append(["3b","4a"])
    dont_pair0.append(["4a","5a"])

    # Verify
    if len(names) != len(set(names)):
        print("Name set not unique!")
    dont_pair = []
    for couple in dont_pair0:
        dont_pair.append(sorted(couple))
    dont_pair.sort()
    for i in range(len(dont_pair)-1):
        if dont_pair[i] == dont_pair[i+1]:
            print("\"don't-pair\" set not unique!")
    for couple in dont_pair:
        if len(couple) != 2:
            print("Entry in \"don't pair\" list does not have two names.")
        for name in couple:
            if name not in names:
                print("Name in \"don't pair\" list not in names list.")

    # Forbid self-gifting
    for name in names:
        if [name, name] not in dont_pair:
            dont_pair.append([name,name])

    # Build dont_pair dict
    forbidden = dict()
    for name in names:
        temp_list = []
        for couple in dont_pair:
            if name == couple[0]:
                temp_list.append(couple[1])
            elif name == couple[1]:
                temp_list.append(couple[0])
        forbidden[name] = temp_list

    # Print
    print("Names:")
    for n, name in enumerate(names,1):
        print("{0:1}   {1}".format(n, name))
    print("Don't-Pair List:")
    for n, couple in enumerate(dont_pair,1):
        sys.stdout.write("{0:1}".format(n))
        for name in couple:
            sys.stdout.write("   {0}".format(name))
        sys.stdout.write("\n")
    print("Forbidden Dict:")
    for k, v in forbidden.items():
        print("   {0} cannot be paired with:".format(k))
        for name in v:
            print("      {0}".format(name))

    # Generate giver/receiver pairs
    valid = False
    iteration = 0
    sorted_names = copy.copy(names)
    sorted_names.sort(key=lambda name:len(forbidden[name]), reverse=True)
    print("Sorted Names:")
    for name in sorted_names:
        print("   {0}   {1}".format(len(forbidden[name]), name))
    # Loop until a valid solution is found
    while not valid:
        iteration = iteration + 1
        print("iteration {0} ------------------------------".format(iteration))
        not_yet_receiving = copy.copy(sorted_names)
        pairs = []
        # Try to select pairs
        for giver in names:
            # Generate list of possible receivers
            receivers = [name for name in not_yet_receiving if name not in
                    forbidden[giver]]
            print("   possible receivers for {0}:".format(giver))
            for receiver in receivers:
                print("      {0}".format(receiver))
            # Restart selection if no valid receivers
            if len(receivers) == 0:
                msg = "iteration {0}: failed because no allowed receivers remaining for {1}"
                print(msg.format(iteration, giver))
                print("remaining possibilities:")
                for name in not_yet_receiving:
                    sys.stdout.write("   {0}".format(name))
                sys.stdout.write("\n")
                valid = False
                break
            # Select a random receiver
            receiver = random.choice(receivers)
            print("   select {0}".format(receiver))
            # Save the giver/receiver pair
            pairs.append([giver, receiver])
            # Remove the receiver from the list of not_yet_receiving
            not_yet_receiving.remove(receiver)
        # If the selection worked, then there will be one pair per name
        valid = len(pairs) == len(names)
    print("finished in {0} iterations".format(iteration))

    # Print giver/receiver pairs
    print("Results:")
    for pair in pairs:
        print("   {0[0]} is giving a gift to {0[1]}".format(pair))


if __name__ == "__main__":
    main()
