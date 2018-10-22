import getpass
import smtplib

# =============================================================================

def email_login(username, password):
    # TODO: Make general for non-gmail senders
    server = smtplib.SMTP("smtp.gmail.com:587")
    server.ehlo()
    server.starttls()
    server.login(username, password)
    return(server)

# =============================================================================

def email_logout(server):
    server.quit()

# =============================================================================

def send_email(server, sender, giver, email, receiver):
    header = "\n".join([
        "To: " + email,
        "From: " + sender,
        "Content-type: text/html",
        "Subject: 2018 Bartie Kids Secret Santa!"
        ])
    body = "<br>".join([
        "Hello {0}!".format(giver),
        "",
        "This is your <font color=\"darkgreen\">SECRET</font> <font color=\"red\">SANTA</font> drawing!",
        "",
        "This year, you are giving a gift to <b>{0}</b>!".format(receiver),
        "",
        "-- insert discussion of rules here --"
        ])
    server.sendmail(sender, email, header + "\n\n" + body)

# =============================================================================

def notify(name, email, receiver):
    print("NOTIFY!")
    print("  giver: " + name)
    print("  email: " + email)

    my_username = input("sender's email address: ")
    my_password = getpass.getpass("email password: ")
    server = email_login(my_username, my_password)

    # Send test email: send to self but use garbage in place of receiver
    # TODO: Make a command-line argument.
    send_email(server, my_username, name, my_username, "[REDACTED]")

    # TODO: Once there's a command-line argument, we don't need this.  You'll
    #       either send a test email or the real email.
    test_success = input("Did the test work? [y/n]: ")
    if test_success.lower() == "y":
        send_email(server, my_username, name, email, receiver)

    email_logout(server)

# =============================================================================

def main():
    # TODO: Take the file name as a command-line argument
    filename = input("file name: ")
    names = []
    emails = {}
    receivers = {}
    with open(filename,'r') as fin:
        for line in fin:
            giver, email, receiver = line.split()
            #print("")
            #print("Giver: {0}".format(giver))
            #print("Email: {0}".format(email))
            #print("Receiver: {0}".format(receiver))
            names.append(giver)
            emails[giver] = email
            receivers[giver] = receiver

    # Notify who?
    # TODO: Take this as an argument.  Allow --all vs --name, and allow
    #       multiple instances of --name.
    notify_who = input("Notify who? (name or all): ")
    if notify_who.lower() == "all":
        for name in names:
            notify(name, emails[name], receivers[name])
    elif notify_who in names:
        notify(notify_who, emails[notify_who], receivers[notify_who])
    else:
        print("Cannot notify {0} -- name not found.".format(notify_who))
        print("Names found:")
        for name in names:
            print("   {0}".format(name))

if __name__ == "__main__":
    main()
