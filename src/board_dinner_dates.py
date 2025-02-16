import random
import csv
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    random.seed(42)
    members_file = os.getenv('MEMBERS_FILE')
    initial_values_file = os.getenv('INITIAL_VALUES_FILE')
    output_file = os.getenv('OUTPUT_FILE')

    if not members_file or not initial_values_file or not output_file:
        raise ValueError("Please ensure that MEMBERS_FILE, INITIAL_VALUES_FILE, and OUTPUT_FILE are set in the .env file.")

    dinner_dates = BoardDinnerDates(members_file, 4, 12, skip_weeks=['03/16/25'])
    dinner_dates.load_initial_values(initial_values_file)
    dinner_dates.run(display=True, save=True, output_file=output_file)
    dinner_dates.calculate_statistics()
    

class BoardDinnerDates:
    def __init__(self, filename: str, group_size: int, weeks: int, skip_weeks = None):
        self.filename = filename
        self.group_size = group_size
        self.weeks = weeks
        self.members = self.load_members()
        self.reach_out_count = Counter()
        self.dinner_history = defaultdict(Counter)
        self.start_date = None
        self.skip_weeks = [datetime.strptime(date, '%m/%d/%y') for date in skip_weeks] if skip_weeks else []

    def load_members(self):
        with open(self.filename, 'r') as file:
            members = [name.strip() for name in file.readlines()]
        return members

    def load_initial_values(self, initial_values_file: str):
        if not initial_values_file:
            raise ValueError("Initial values file is not provided.")

        with open(initial_values_file, 'r') as file:
            reader = csv.reader(file)
            dates = next(reader)
            dates = [date for date in dates if date != '']
            self.start_date = datetime.strptime(dates[len(dates)-1], '%m/%d/%y')
            first_row = next(reader)
            first_row = [element.replace(' ', '\t') for element in first_row if (element != '' and not element[0].isdigit())]
            groups = [[h] for h in first_row]
            for row in reader:
                row = [element for element in row]
                for i, member in enumerate(row):
                    if member and not member[0].isdigit():
                        groups[i].append(member)
            for group in groups:
                if group:
                    leader = group[0]
                    if leader:
                        self.reach_out_count[leader] += 1
                    for member in group:
                        if member and member != leader:
                            self.dinner_history[leader][member] += 1
                            self.dinner_history[member][leader] += 1

    def generate_groups(self):
        groups = []
        max_groups = len(self.members) // self.group_size 
        for _ in range(self.weeks):
            random.shuffle(self.members)
            week_groups = []
            available_members = self.members[:]
            while available_members and len(week_groups) < max_groups:
                group = []
                while len(group) < self.group_size and available_members:
                    member = self.select_member(available_members, group)
                    group.append(member)
                    available_members.remove(member)
                week_groups.append(group)
            # remaining members
            for i in range(len(available_members)):
                week_groups[i % len(week_groups)].append(available_members[i])

            self.assign_group_leaders(week_groups)
            groups.append(week_groups)
        return groups
    
        #naive approach
        def randomized(board: list, date_size:int):
            permutation = random.shuffle(board)
            counter = -1
            for name in board:
                if counter == date_size - 1:
                        counter = -1
                        print()
                print(name)
                counter += 1
            pass

    def select_member(self, available_members, current_group):
        # Select a member who has had the least dinners with the current group members
        min_dinners = float('inf')
        selected_member = None
        for member in available_members:
            dinners_with_group = sum(self.dinner_history[member][m] for m in current_group)
            if dinners_with_group < min_dinners:
                min_dinners = dinners_with_group
                selected_member = member
        return selected_member

    def assign_group_leaders(self, groups):
        for group in groups:
            eligible_leaders = [member for member in group if self.reach_out_count[member] == min(self.reach_out_count[m] for m in group)]
            leader = random.choice(eligible_leaders)
            print(leader)
            leader_index = group.index(leader)
            group[0], group[leader_index] = group[leader_index], group[0]
            self.reach_out_count[leader] += 1
            for member in group:
                for other_member in group:
                    if member != other_member:
                        self.dinner_history[member][other_member] += 1

    def display_groups(self, groups):
        for week, week_groups in enumerate(groups, start=1):
            print(f"Week {week}:")
            for i, group in enumerate(week_groups):
                leader = group[0]  
                print(f"  Group {i + 1}: {', '.join(group)} (Leader: {leader})")

    def save_generated_dates(self, groups, output_file: str):
        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            # Calculate the dates for each week, skipping specified weeks
            if self.start_date:
                dates = []
                week_counter = 1
                while len(dates) < self.weeks:
                    current_date = self.start_date + timedelta(weeks=week_counter)
                    if current_date not in self.skip_weeks:
                        dates.append(current_date)
                    week_counter += 1
                date_row = []
                for date in dates:
                    date_row.extend([date.strftime('%m/%d/%y')] + [''] * (self.group_size))
                writer.writerow(date_row)
            else:
                week_row = []
                for week in range(1, self.weeks + 1):
                    week_row.extend([f"Week {week}"] + [''] * (self.group_size))
                writer.writerow(week_row)
            max_group_size = max(len(group) for week_groups in groups for group in week_groups)
            for i in range(max_group_size):
                row = []
                for week_groups in groups:
                    for group in week_groups:
                        if i < len(group):
                            row.append(group[i])
                        else:
                            row.append('')
                writer.writerow(row)

    def calculate_statistics(self):
        num_dinners = []
        for member in self.members:
            history = self.dinner_history[member]
            dinners = sum(history.values())
            num_dinners.append(dinners)
            avg_dinners = np.mean(list(history.values()))
            var_dinners = np.var(list(history.values()))
            min_dinners = np.min(list(history.values()))
            max_dinners = np.max(list(history.values()))
            min_dinners_freq = list(history.values()).count(min_dinners)
            max_dinners_freq = list(history.values()).count(max_dinners)
            print(f"{member} had dinner with each person on average {avg_dinners:.2f} times, variance {var_dinners:.2f}, minimum {min_dinners} (frequency: {min_dinners_freq}), maximum {max_dinners} (frequency: {max_dinners_freq}).")

    def run(self, display = True, save = True, output_file = None):
        groups = self.generate_groups()
        if display:
            self.display_groups(groups)
        if save and output_file:
            self.save_generated_dates(groups,output_file)


if __name__ == '__main__':
    main()