'''
File: SecretSantaGenerator.py
Last Updated: 12/25/21
----------
This file writes to .txt files for anonymous secret santa assignments!

INSTRUCTIONS:
	1. Within the SecretSanta_v2021 folder, populate the secret_santa_participants.txt file with the participants names,
	   each on their own line
	2. In the terminal window, run python3 SecretSantaGenerator.py
	3. Check the ASSIGNMENTS folder to ensure that each participant has a .txt file
	4. WITHOUT opening the .txt files, text or email each .txt file to the appropriate person.
	5. Enjoy!
'''

import random
import collections

EMPTYFILE_ERR = "No names exist into the secret_santa_participants.txt file. Type participants' names (each name on its own line) to use this program."

# secret_santa_participants.txt should contain names of participants, each on a separate line
names_file = 'secret_santa_participants.txt'


def pluralize(singular, times):
    if times == 1: 
        return singular
    else: 
        return singular + 's'


def read_names(filename):
    names = []
    with open(filename, 'r') as f:
        for name in f:
            if name.strip() == '':
                continue
            names.append(name.strip())
    f.close()
    return names

# Generate Secret Santa assignments.
#   debug       :   When set to true, print out assignments to terminal for error checking.
#   allowPairs  :   When set to false, restart the algorithm if a pair-wise assignment is created.
def generate_assignemnts(names, debug=False, allowPairs=True, lowPrice=30, highPrice=40):
    print('\n' + '*'*20 + 'Secret Santa Generator is starting, stay tuned...' + '*'*20)

    generate_from_start = True                  # Create variable used to determine whether we end up with an issue assigning the final person
    unassigned_names = names                    # Create a list of unassigned names
    assignments = collections.defaultdict(int)  # Create an empty dictionary for assigned names

    first = True
    num_iters = 0
    while generate_from_start == True:
        num_iters += 1
        if debug:
            print('*'*10, 'Running from start...', '*'*10, '\n')

        # Reset the algorithm to run from the start
        generate_from_start = False
        unassigned_names = names
        assignments = collections.defaultdict(int)

        # Iterate over all the names
        for name in names:
            # if first:
            #     print('*')
            with open('ASSIGNMENTS/' + name + '.txt', 'w') as f:
                # Determine valid assignment choices given the allowPairs parameter
                if allowPairs:
                    valid_choices = [
                        person for person in unassigned_names if person != name]
                else:
                    valid_choices = [
                        person for person in unassigned_names if person != name and person != assignments[name]]

                # If there are no valid choices, restart the matching algorithm
                if len(valid_choices) == 0:
                    generate_from_start = True
                    break

                # Obtain an assignment, and write to file
                assignment = valid_choices[random.randrange(0, len(valid_choices))]
                if not allowPairs:
                    assignments[name] = assignment
                f.write('Subject: Secret Santa Assignment for %s\nMessage: You will be giving a gift to %s. The recommended price range is $%d-$%d. Happy gifting!' %
                        (name.upper(), assignment, lowPrice, highPrice))
                if debug:
                    print('Subject: Secret Santa Assignment for %s\nMessage: You will be giving a gift to %s. The recommended price range is $%d-$%d. Happy gifting!\n' %
                        (name.upper(), assignment, lowPrice, highPrice))
                unassigned_names = [
                    person for person in unassigned_names if person != assignment]
            f.close()
        first = False

    print('*'*8, 'Secret Santa Generator is finished running (required %d %s). Check files for assignments.' % (num_iters, pluralize("iteration", num_iters)), '*'*8, '\n')


def main():
    names = read_names(names_file)
    random.shuffle(names)
    if len(names) == 0:
        raise Exception(EMPTYFILE_ERR)
    generate_assignemnts(names, debug=False, allowPairs=False, lowPrice=30, highPrice=40)

if __name__ == "__main__":
    main()
