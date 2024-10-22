import os#provides a way to interact with the operating system, directory manipulation and other system related functionalities

# Function to display the main menu and prompt the user for a menu option
def display_main_menu():
    print("\nNI Electoral System")
    print("***********************")
    print("1. Setup polling station votes file")
    print("2. Enter polling booth")
    print("3. Review statistics")
    print("4. Exit")

    while True:
        option = input("Enter menu option: ").lower()

        if option in {'1', '2', '3', '4'}:
            return option #returns the chosen menu option
        else:
            print("|***Invalid option. Please enter a number between 1-4!***|.")


# Function to create or load the votes file and returns the password and the file name given
def setup_votes_file():
    file_name = input("Enter the name of the polling station file: ")

    # Check if the file already exists
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            lines = file.readlines()
            if len(lines) >= 7:  # Check if the file has at least 7 lines
                while True:
                    overwrite_confirmation = input(
                        f"The file '{file_name}' already exists. Do you want to continue to the polling booth? (y/n): ").lower()
                    if overwrite_confirmation == 'y':
                        # If the user wants to continue, return the existing password and file name
                        password = file_name
                        return password, file_name
                    elif overwrite_confirmation == 'n':
                        print("Exiting setup.")
                        return None, None
                    else:
                        print("|***Invalid input. Please enter (Y/N)***|")
            else:
                print(f"|***Invalid file format. The file '{file_name}' does not have the expected number of lines.***|")
                return None, None

    # Create a secret password based on the file name
    password = file_name
    #initializes a new file with default values set
    with open(file_name, 'w') as file:
        for _ in range(5):
            file.write("0.0\n")  # Sets votes for each candidate to zero
        file.write("0\n")  # Sets the male tally to zero
        file.write("0\n")  # Sets the female tally to zero

    return password, file_name


# Function to enter polling booth and cast votes, also updates the votes file with whatever votes have been casted
def enter_polling_booth(password, file_name):
    # Read existing data from the file
    with open(file_name, 'r') as file:
        lines = file.readlines()

    # Initialize these male and female variables
    male_tally = int(lines[5])
    female_tally = int(lines[6])

    used_votes = set()  # Set to store used votes
    #prompts for the users gender of either male or female
    while True:
        gender = input("\nWhat is your gender? (M/F): ").lower()
        if gender == 'm' or gender == 'f':
            break
        else:
            print("|***Invalid input. Please enter 'M' or 'F'***|")

    for i in range(5):
        print(f"Vote for {candidates[i]}:")
        while True:
            vote = input("Enter a valid vote (0, 1, 2, 3, 4, or 5): ")
            if not vote or (vote.isdigit() and 0 <= int(vote) <= 5):
                if not vote:
                    vote = '0'
                if int(vote) == 0 or (int(vote) not in used_votes):
                    used_votes.add(int(vote))
                    break
                else:
                    print("|***Vote already used. Please enter an unused vote between 0 and 5!***|")
            else:
                print("|***Invalid vote. Please enter a vote between 0 and 5!***|")
        #updates the votes based on the users choices
        update_votes(vote, i, male_tally, female_tally, lines)

    # Update gender tally
    if gender == 'm':
        lines[5] = str(male_tally + 1) + "\n"
    elif gender == 'f':
        lines[6] = str(female_tally + 1) + "\n"

        # Prompt for the secret password which is the name of the file
        while True:
            entered_password = input("\nEnter the secret password to leave the polling station: ")
            if entered_password == password:
                break
            else:
                print("|***Incorrect password. Please enter the correct password to leave the polling booth!***|")

    print("|***Votes recorded and finalized successfully.***|")

    # Write updated data to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)


# Function to update votes and gender tally based on whatever the user has input
def update_votes(vote, candidate_votes, male_tally, female_tally, lines):
    vote = int(vote)
    #updates based on the users input
    if vote == 1:
        lines[candidate_votes] = str(float(lines[candidate_votes]) + 1.0) + "\n"
    elif vote == 2:
        lines[candidate_votes] = str(float(lines[candidate_votes]) + 0.5) + "\n"
    elif vote == 3:
        lines[candidate_votes] = str(float(lines[candidate_votes]) + 0.33) + "\n"
    elif vote == 4:
        lines[candidate_votes] = str(float(lines[candidate_votes]) + 0.25) + "\n"
    elif vote == 5:
        lines[candidate_votes] = str(float(lines[candidate_votes]) + 0.2) + "\n"


# Function for the polling officer to review statistics, displaying a menu with prompts to enter specific areas of statistics
def review_statistics(file_name):
    while True:
        try:
            lines = []
            with open(file_name, 'r') as file:
                for _ in range(7):
                    lines.append(float(file.readline().strip("\n")))

            print("\nReview Statistics - Votes Analysis")
            print("***************************************")
            print("1. Display votes tally (ordered by party name)")
            print("2. Display votes tally (ordered in descending order of votes)")
            print("3. Overall winner, with percentage share of the total votes")
            print("4. Percentage breakdown of male to female split")
            print("5. Return to main menu")

            option = input("Enter menu option: ")

            if option == '1':
                display_votes_tally(lines)#display the votes tally order
            elif option == '2':
                display_votes_tally(lines, order='desc')  #display votes tally in descending order
            elif option == '3':
                display_overall_winner(lines)#displays the overall winner
            elif option == '4':
                display_gender_percentage(lines)#displays the gender percentage split
            elif option == '5':
                return#returns back to the main menu
            else:
                print("\n|***Invalid option. Please enter a number between 1-5***|")
        except ValueError:
            print("|***Invalid input. Please try again!***|")


# Function to display votes tally in either ascending or descending order
def display_votes_tally(lines, order='asc'):
    # Create a list of tuples with candidate names and their respective votes
    candidates_votes = [(candidates[i], float(lines[i])) for i in range(5)]
    # Sort the list based on the second element of each tuple (votes), in ascending or descending order
    candidates_votes.sort(key=lambda x: x[1], reverse=(order == 'desc'))

    print("\n|***Votes Tally***|")
    for candidate, votes in candidates_votes:
        print(f"{candidate} - {votes} votes")


# Function to display overall winner and their percentage share of the total votes recorded
def display_overall_winner(lines):
    def get_vote(candidate_tuple):#function to help take the candidate tuple and return the votes value - used as 'key' argument in the 'sort' function
        return float(candidate_tuple[1])

    candidates_votes = [(candidates[i], lines[i]) for i in range(5)]
    candidates_votes.sort(key=get_vote, reverse=True)#sorts the candidate_votes list based on the vote values in descending order

    total_votes = sum(float(line) for line in lines[:5])#calculates the total votes by summing votes of all candidates
    overall_winner = candidates_votes[0]#extracts the overall winner from the sorted list
    percentage_share = (float(overall_winner[1]) / total_votes) * 100#calculates the percentage share of total votes for the overall winner

    print(f"\n|***Overall Winner***|\n {overall_winner[0]} with {percentage_share:.2f}% of the votes")


# Function to display gender percentage breakdown of the male to female split
def display_gender_percentage(lines):
    total_votes = int(lines[5]) + int(lines[6])#calculate total votes through the summing of votes for male and female
    male_percentage = (int(lines[5]) / total_votes) * 100#calculate percentage of the male votes
    female_percentage = (int(lines[6]) / total_votes) * 100#calculate the percentage of the female votes

    print(f"\n|***Percentage breakdown of male to female split***|")#displays the percentage breakdown of the male and female split
    print(f"Male: {male_percentage:.2f}%")
    print(f"Female: {female_percentage:.2f}%")


# Main program
candidates = ["Bert Navy", "Luke Lime", "Sally Tangerine", "Rose Burgundy", "Edward Yoke"]

#Main function that runs the NI Electoral System
def main():
    global candidates#accesses the global variable 'candidates' from above
    votes_file = None#initializes the votes file name as none
    password = None#initializes the password as none

    while True:
        option = display_main_menu()#gets the users choice from the main menu

        if option == '1':
            password, votes_file = setup_votes_file()#set up or load the votes file
        elif option == '2':
            if votes_file:
                enter_polling_booth(password, votes_file)#enters the pooling booth in order to cast votes
            else:
                print("\n|***Please set up the votes file first!***|")
        elif option == '3':
            if votes_file:
                review_statistics(votes_file)#reviews and displays the statistics
            else:
                print("|***Please set up the votes file first!***|")
        elif option == '4':
            break#exits the program if the user enters 4


main()
