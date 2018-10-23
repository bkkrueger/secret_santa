# Imports
import copy
import getpass
import math
import random
import smtplib
import sys

import ss_parse
import ss_test_input
import ss_util

# =============================================================================
# Read input from a file

# TODO: Just call parse directly

def get_file_input(filename):
    import ss_parse
    return(ss_parse.parse(filename))

# =============================================================================
# Specify test input

# TODO: Just call get_test_input directly

def get_test_input(N,P):
    import ss_test_input
    return(ss_test_input.get_test_input(N,P))

# =============================================================================
# Verify input

def verify_input(emails, bad_pairs):

    names = sorted(emails.keys())

    # Don't need to verify that names are unique
    # -- Since we're storing the names and email addresses in a dictionary,
    #    that forces the names to be unique.  The downside is that if multiple
    #    non-unique entries are added, only the last entry will survive, and
    #    that will happen without a warning.
    ###repeats = {}
    ###for i in range(len(names)-1):
    ###    if names[i] == names[i+1]:
    ###        repeats[names[i]] = repeats.get(names[i],0) + 1
    ###if len(repeats) > 0:
    ###    print("Repeated names:")
    ###    for name, count in repeats.items():
    ###        print("  {0}: {1}".format(name, count))
    ###    raise ValueError("Non-unique names in list.")

    # Confirm that all email addresses look like email addresses
    ### TODO

    # Confirm that all entries in bad_pairs list are pairs, and that all names
    # in bad_pairs list are in names list
    for pair in bad_pairs:
        if len(pair) != 2:
            msg = "Entry in bad_pairs list is not a pair: {0}"
            raise ValueError(msg.format(pair))
        for name in pair:
            if name not in names:
                msg = "Name in bad_pairs list not in names_list: {0}"
                raise ValueError(msg.format(name))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def TEST_verify_input():
    emails = {"Bob": "bob@bob.com",
              "Susan": "susan@susan.com",
              "Bob": "robert@robert.com",
              "Sandra": "sandra@sandra.com"}
    bad_pairs = [("Sandra", "Susan")]
    try:
        print("Verify the following input:")
        print("  Names & Emails:")
        for i, (name, email) in enumerate(emails.items()):
            print("    {0}: {1} <{2}>".format(i, name, email))
        print("  Invalid Pairs:")
        for i, pair in enumerate(bad_pairs):
            print("    {0}: {1[0]} & {1[1]}".format(i, pair))
        verify_input(emails, bad_pairs)
    except ValueError as err:
        print(" ".join(["Caught error:", str(err)]))
    else:
        print("Passes verification tests.")

# =============================================================================
# Process input

def process_input(emails, bad_pairs):
    # Remove duplicates from bad_pairs list
    # -- Don't need to generate an error (TODO: although a warning might be
    #    appreciated by users)
    bad_pairs = set((pair[0],pair[1]) if pair[0] < pair[1] else
            (pair[1],pair[0]) for pair in bad_pairs)

    # Turn the list of bad pairs into a dict
    # -- Also forbid self-gifting
    forbidden = {name: set() for name in emails.keys()}
    for name in emails.keys():
        forbidden[name].add(name)
    for pair in bad_pairs:
        forbidden[pair[0]].add(pair[1])
        forbidden[pair[1]].add(pair[0])

    return(forbidden)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def TEST_process_input():
    N = 6
    P = 2
    print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    emails, bad_pairs = get_test_input(N,P)
    print("  Names:")
    for i, (name, email) in enumerate(emails.items()):
        print("    {0:{1}}: {2} <{3}>".format(
            i+1,ss_util.digits(N),name,email))
    print("  Forbidden Pairs:")
    for i, pair in enumerate(bad_pairs):
        print("    {0:{1}}: {2[0]} & {2[1]}".format(
            i+1,ss_util.digits(P),pair))
    forbidden = process_input(emails, bad_pairs)
    print("  Invalid Dict:")
    names = sorted(list(forbidden.keys()))
    for name in names:
        invalid = sorted(list(forbidden[name]))
        print("    {0}:".format(name))
        for name2 in invalid:
            print("      {0}".format(name2))

# =============================================================================
# Perform a single selection pass

def single_selection(emails, forbidden):
    sorted_names = sorted(emails.keys(), key=lambda name:len(forbidden[name]),
            reverse=True)
    not_yet_chosen = copy.copy(sorted_names)
    pairs = {}
    for giver in sorted_names:
        # Who can this person give to?
        recipients = [name for name in not_yet_chosen if name not in
                forbidden[giver]]
        # Fail if not valid recipients
        if len(recipients) == 0:
            print("  Tried the following pairs:")
            for n1, n2 in pairs.items():
                print("    {0} gives to {1}".format(n1, n2))
            print("  Not yet chosen:")
            for name in not_yet_chosen:
                print("    {0}".format(name))
            msg = "  No valid recipients remaining for {0}"
            raise ValueError(msg.format(giver))
        # Select a random recipient
        recipient = random.choice(recipients)
        # Save the giver/receiver pair
        pairs[giver] = recipient
        # Remove the recipient from the list of not_yet_chosen
        not_yet_chosen.remove(recipient)
    return(pairs)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def TEST_single_selection():
    pass

# =============================================================================
# Loop to get a valid selection

def selection_loop(emails, forbidden):
    iter_max = 1000
    # TODO: Try a reasonable number of tries (10? 30? 100?) then switch to
    #       enumerating (constrained enumeration: don't enumerate all, but
    #       instead shuffle and then iterate through valid choices.  Make a
    #       note to the user that we're switching to enumeration and that it
    #       might take a while.
    for iteration in range(iter_max):
        print("Iteration {0:0{1}d} ------------------------------".format(
            iteration, ss_util.digits(iter_max)))
        try:
            results = single_selection(emails, forbidden)
        except ValueError as error:
            print(str(error))
        else:
            print("Success!")
            break
    else:
        msg = "Failed to find a valid selection after {0} iterations."
        raise ValueError(msg.format(iter_max))
    return(results)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def TEST_selection_loop():
    pass

# =============================================================================
# Send test email to organizer

def test_email_send(pairs):
    # TODO: Add a note -- if login fails and server is GMail, tell people to
    #       check the "less secure apps" setting.
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    username = getpass.getpass("username: ")
    password = getpass.getpass("password: ")
    server.login(username,password)
    body = ["<b>{0}</b> is giving a gift to <i>{1}</i>".format(giver, receiver) for giver,
            receiver in pairs.items()]
    message = "\n".join([
        "To: {0}".format(username),
        "Content-type: text/html",
        "Subject: HTML test",
        "" ]) + "<br>".join([
        "This is a test message to demonstrate that we can send email."
        ] + body)
    server.sendmail(username, username, message)
    server.quit()

# =============================================================================
# Email

def email_login(email, url, port):
    server = smtplib.SMTP(":".join((url, port)))
    server.ehlo()
    server.starttls()
    password = getpass.getpass("password: ")
    server.login(email, password)
    return(server)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def email_logout(server):
    server.quit()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def send_email(server, sender_name, sender_email, giver_name, giver_email,
        receiver, subject, message):
    header = "\n".join([
        "To: " + giver_email,
        "From: " + sender_email,
        "Content-type: text/html",
        "Subject: " + subject,
        ])
    body = "<br>".join([message.format(gifter=giver_name, recipient=receiver),
        "",
        " ".join([
            "This message was generated automatically.  Please don't lose",
            "this email, because {0} does not have a record of who is giving",
            "a gift to whom."
            ]).format(sender_name)
        ])
    server.sendmail(sender_email, giver_email, header + "\n\n" + body)

# =============================================================================
# Main

def main():

    # Get input
    # TODO: Command line argument: generate random test input or read from a
    #       user-specified file.
    input_data = ss_parse.parse("input.txt")
    #N = 10
    #P = 14
    #print("Choose {0} names with {1} forbidden pairs:".format(N,P))
    #input_data = ss_test_input.get_test_input(N,P)
    emails = input_data["PARTICIPANTS"]
    bad_pairs = input_data["DO NOT PAIR"]
    N = len(emails.keys())
    P = len(bad_pairs)

    if __debug__:
        print("  Names:")
        for i, (name, email) in enumerate(emails.items()):
            print("    {0:{1}}: {2} <{3}>".format(
                i+1,ss_util.digits(N),name,email))
        print("  Forbidden Pairs:")
        for i, pair in enumerate(bad_pairs):
            print("    {0:{1}}: {2[0]} & {2[1]}".format(
                i+1,ss_util.digits(P),pair))

    # Process input
    if __debug__:
        print("Verify input:")
    verify_input(emails, bad_pairs)
    if __debug__:
        print("  Input valid")

    if __debug__:
        print("Process input:")
    forbidden = process_input(emails, bad_pairs)

    if __debug__:
        print("  Invalid Dict:")
        names = sorted(list(forbidden.keys()))
        for name in names:
            invalid = sorted(list(forbidden[name]))
            print("    {0}:".format(name))
            for name2 in invalid:
                print("      {0}".format(name2))

    if __debug__:
        print("Run selection loop:")
    pairs = selection_loop(emails, forbidden)
    #for giver, receiver in pairs.items():
    #    print("  {0} is giving a gift to {1}".format(giver, receiver))

    if __debug__:
        print("Writing results to a file:")
    #filename = input("filename: ")
    filename = "ss.txt"
    with open(filename,'w') as outfile:
        for giver in pairs.keys():
            outfile.write("   {0}   {1}   {2}\n".format(
                giver, emails[giver], pairs[giver]))

    #print("Send a test email to demonstrate that sending works.")
    #test_email_send(pairs)
    organizer = input_data["ORGANIZER"]
    server = email_login(organizer["email"],
            organizer["smtp url"], organizer["smtp port"])
    for giver in pairs.keys():
        # Testing -- need to change to the right email
        send_email(server, organizer["name"], organizer["email"],
                giver, emails[giver], pairs[giver],
                input_data["MESSAGE SUBJECT"], input_data["MESSAGE BODY"])
    email_logout(server)

if __name__ == "__main__":
    main()
