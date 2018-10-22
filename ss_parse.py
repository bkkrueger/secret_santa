import pprint

# =============================================================================

class InputError(Exception):
    pass

# =============================================================================

def parse_do_not_pair(listing):
    input_data = []
    for full_line in listing:
        if __debug__:
            print("  Line: \"{0}\"".format(full_line))
        # Line should be of the form "-- name1, name2"
        if full_line.strip()[0:2] != "--":
            msg = "Do not pair lines should start with \"--\"."
            raise InputError(msg)
        line = full_line[2:].split(",")
        if len(line) != 2:
            msg = " ".join(["Do not pair lines should be of the format",
                "\"-- name1, name2\"."])
            raise InputError(msg)
        name1 = line[0].strip()
        name2 = line[1].strip()
        # Save
        if name1 < name2:
            pair = (name1, name2)
        else:
            pair = (name2, name1)
        input_data.append(pair)
    return(input_data)

# =============================================================================

def parse_message_body(listing):
    return("<br>".join(listing))

# =============================================================================

def parse_message_subject(listing):
    if len(listing) != 1:
        raise InputError("Message subject can only be a single line.")
    return(listing[0])

# =============================================================================

def parse_organizer(listing):
    # Turn listing into dict
    input_data = {}
    for full_line in listing:
        if __debug__:
            print("  Line: \"{0}\"".format(full_line))
        # Line should be of the form "-- key: value"
        if full_line.strip()[0:2] != "--":
            msg = "Organizer lines should start with \"--\"."
            raise InputError(msg)
        line = full_line[2:].split(":")
        if len(line) != 2:
            msg = " ".join(["Organizer lines should be of the format",
                "\"-- key: value\"."])
            raise InputError(msg)
        key = line[0].strip().lower()
        value = line[1].strip()
        # Save
        input_data[key] = value
    # Make sure the relevant data is provided
    required_keys = ["name", "email", "smtp url", "smtp port"]
    for key in required_keys:
        if key not in input_data:
            msg = "Organizer section must specify key \"{0}\".".format(key)
            raise InputError(msg)
    # Make sure spurious data is not provied
    for key in input_data.keys():
        if key not in required_keys:
            msg = "Organizer section has unknown key \"{0}\".".format(key)
            raise InputError(msg)
    return(input_data)

# =============================================================================

def parse_participants(listing):
    input_data = {}
    for full_line in listing:
        if __debug__:
            print("  Line: \"{0}\"".format(full_line))
        # Line should be of the form "-- name: email"
        if full_line.strip()[0:2] != "--":
            msg = "Participants lines should start with \"--\"."
            raise InputError(msg)
        line = full_line[2:].split(":")
        if len(line) != 2:
            msg = " ".join(["Participants lines should be of the format",
                "\"-- name: email\"."])
            raise InputError(msg)
        name = line[0].strip()
        email = line[1].strip()
        # Save
        input_data[name] = email
    return(input_data)

# =============================================================================

sections = {
        "DO NOT PAIR": parse_do_not_pair,
        "MESSAGE BODY": parse_message_body,
        "MESSAGE SUBJECT": parse_message_subject,
        "ORGANIZER": parse_organizer,
        "PARTICIPANTS": parse_participants,
        }

# =============================================================================

def parse_section(section, full_listing):
    # Trim listing
    listing = []
    for full_line in full_listing:
        line = full_line.strip()
        if line == section:
            # We now know what section we're in, so we don't need this
            continue
        elif line == "" and section != "MESSAGE BODY":
            # Throw away blank lines, except in the message body
            continue
        elif len(line) > 1 and line[0] == "#":
            # Throw away comment lines
            continue
        else:
            # Save useful lines (minus leading/trailing whitespace)
            listing.append(line)

    # Parse section
    if section not in sections:
        raise InputError("Unknown section: \"{0}\".".format(section))
    if __debug__:
        print("Parsing \"{0}\" section.".format(section))
    input_data = sections[section](listing)

    return(input_data)

# TODO when verifying input:
# -- verify email addresses look like email addresses
# -- verify names in do-not-pair list are all in list of participants
# -- Add boilerplate to end of message: auto generated, no one else has this
#    info, whether or not the result was saved for resending in the future.
# -- In message body replace {gifter} and {recipient}

# =============================================================================

def parse(filename):
    # Load data file
    file_listing = []
    with open(filename,'r') as infile:
        header = True
        for line in infile:
            if header:
                if line.strip() == "":
                    # Throw away header comment lines
                    continue
                elif line.strip()[0] == "#":
                    # Throw away header blank lines
                    continue
                else:
                    header = False
            if not header:
                # Save any other lines (minus leading/trailing whitespace)
                file_listing.append(line.strip())

    # Find section indices
    if file_listing[0] not in sections:
        raise InputError("Leading non-header line not a section header.")
    start = {}
    end = {}
    index = 0
    curr_section = ""
    for line in file_listing:
        if curr_section != "":
            end[curr_section] = index
        upperline = line.upper()
        if upperline in sections:
            curr_section = upperline
            start[upperline] = index
        index = index + 1
    end[curr_section] = index

    # Split into sections
    section_listings = {}
    for section in sections:
        section_listings[section] = file_listing[start[section]:end[section]]

    # Parse sections
    user_input = {}
    for section in sections:
        user_input[section] = parse_section(section, section_listings[section])

    return(user_input)

# =============================================================================

if __name__ == "__main__":
    user_input = parse("input.txt")
    pprint.pprint(user_input)
