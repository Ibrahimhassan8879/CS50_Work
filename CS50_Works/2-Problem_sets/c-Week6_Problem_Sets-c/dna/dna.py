import csv
from sys import argv


def main():
    Origin_Database = []

    if len(argv) != 3:
        print("Plaese Enter 2 file path \n")
        return 1
    else:
        filename = argv[1]

        with open(filename) as file:
            columns = list(csv.DictReader(file))
            first_row = list(columns[0].keys())[1:]

            for column in columns:
                for keys in first_row:
                    column[keys] = int(column[keys])

        filename_2 = argv[2]
        with open(filename_2) as file:
            sequence = file.read()
            Result = []
            subsequence = first_row
            for j in range(len(first_row)):

                longest_match(sequence, subsequence[j])
                Result.append(longest_match(sequence, subsequence[j]))

            for patient_dna in columns:
                matchingFlag = True
                for dna_type_index in range(len(subsequence)):
                    if Result[dna_type_index] != patient_dna[subsequence[dna_type_index]]:
                        matchingFlag = False
                        break

                if (matchingFlag):
                    print(patient_dna["name"])
                    return 0

            print("No match")
            return 1


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
