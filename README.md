# Dinner Groups Project

This project generates randomized dinner groups of 4-5 people for a semester, ensuring that each person has dinner with everyone roughly the same number of times and shares the responsibility of reaching out within their group.

## Project Structure

```
dinner-groups
├── src
│   └── board_dinner_dates.py      # Main logic for generating randomized dinner groups
├── data
│   ├── members.txt                # List of board members
│   ├── initialdata.csv            # Initial dinner dates 
│   └── generated_dinner_dates.csv # Generated dinner dates for the semester
├── .env                           # Environment variables for file paths
├── .gitignore                     # Git ignore file
└── README.md                      # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd dinner-groups
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```
   # Path to the members file
   MEMBERS_FILE=./data/members.txt

   # Path to the initial values file
   INITIAL_VALUES_FILE=./data/initialdata.csv

   # Path to the output file for generated dinner dates
   OUTPUT_FILE=./data/generated_dinner_dates.csv
   ```

4. Ensure that the `data/members.txt` file contains the names of the board members, each on a new line.

## Usage

To generate dinner groups and save them to a CSV file, run the main script:
```
python src/board_dinner_dates.py
```

This will read the member data from `members.txt`, create randomized groups, and save the results to `generated_dinner_dates.csv`.

## Group Generation Logic

The project uses a randomized approach to create groups of 4-5 members. Each member is assigned to a group where they will have the opportunity to dine with different members throughout the semester. The group leader is also assigned for outreach responsibilities, ensuring that communication within the group is maintained.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.