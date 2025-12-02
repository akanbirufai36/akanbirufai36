import json
import csv
from itertools import islice


class Grading:
    def __init__(self):
        self.BLUE = '\033[34m'
        self.GREEN = '\033[32m'
        self.YELLOW = '\033[33m'
        self.RED = '\033[31m'
        self.LIGHTBLUE_EX = '\033[94m'
        self.RESET_COLOR = '\033[0m'

    def recursion_observer(self):
        if self.recursive_count % 2 == 0:
            print("Type 'exit' to end session")
        else:
            pass

    def grade_checker(self, score, smart_score=True):
        '''Calculates grade of student if Score within range 0 and 100'''
        if smart_score == True:
            grade = ('A' if score >= 70 else
                     'B' if score >= 60 else
                     'C' if score >= 50 else
                     'D' if score >= 45 else
                     'E' if score >= 40 else
                     'F' if score >= 0 else '-')
            return grade
        else:
            return '-'

    def grade_displayer(self, grade):
        '''Return colour for each grade.'''

        if grade:
            match grade:
                case 'A':
                    return self.BLUE + grade + self.RESET_COLOR
                case 'B':
                    return self.GREEN + grade + self.RESET_COLOR
                case 'C':
                    return self.GREEN + grade + self.RESET_COLOR
                case 'D':
                    return self.YELLOW + grade + self.RESET_COLOR
                case 'E':
                    return self.YELLOW + grade + self.RESET_COLOR
                case 'F':
                    return self.RED + grade + self.RESET_COLOR
                case '-':
                    return '-'

    def remark(self, grade):
        '''Returns a remark if grade is given. '''
        match grade:
            case 'A':
                return self.BLUE + 'Excellent' + self.RESET_COLOR
            case 'B':
                return self.GREEN + 'Good' + self.RESET_COLOR
            case 'C':
                return self.GREEN + 'Good' + self.RESET_COLOR
            case 'D':
                return self.YELLOW + 'Fair' + self.RESET_COLOR
            case 'E':
                return self.YELLOW + 'Poor' + self.RESET_COLOR
            case 'F':
                return self.RED + 'Fail' + self.RESET_COLOR
            case '-':
                return '-'


class Scorekeeper(Grading):
    def __init__(self, candidate_record={}, exit=['Exit', 'End', 'Quit', 'Nope', 'No', 'Clear']):
        self.candidate_record = candidate_record
        self.exit = exit
        self.recursive_count = 0
        self.gradingsheet = {}
        super().__init__()

    def recursion_observer(self):
        if self.recursive_count % 4 == 0:
            print(f"Type {self.RED} {'exit'} {self.RESET_COLOR} to end session")
        else:
            pass

    def start(self):

        print(f'\n\n\t{'=' * 15} Smart Score Manager {'=' * 15}')
        try:
            self.score_range = int(input(
                f'{self.LIGHTBLUE_EX}  ⚠  Tutor Should Please Write The Highest Intended Score  ⚠\n{self.RESET_COLOR}   ==>'))
        except ValueError:
            return self.start()

    def check_score(self):
        pass

    def validate_score(self, score, name):

        if self.score in self.exit:
            return
        try:
            self.score = int(score)
            if self.score > self.score_range:
                print(
                    f'{self.LIGHTBLUE_EX} Score must be between 0 and {self.score_range} {self.RESET_COLOR}.')
                self.score = input(f'Enter {name} score: ').capitalize()
                self.recursive_count += 2
                self.recursion_observer()
                return self.validate_score(self.score, self.name)
        except ValueError:
            print(self.LIGHTBLUE_EX +
                  ' Invalid Input. Score must be an integer' + self.RESET_COLOR)
            self.score = input(f'Enter {name} score: ').capitalize()
            self.recursive_count += 2
            self.recursion_observer()
            return self.validate_score(self.score, self.name)

    def record_machine(self, score=0):
        self.score = score
        self.name = input('\nEnter candidate name: ').title()

        if (not self.name.replace(' ', '').isalpha()) or self.name.startswith(' ') or self.name == '':
            print(self.LIGHTBLUE_EX + ' Please enter a candidate OR Press(exit/end/quit)\n    ',
                  self.RESET_COLOR, end=' ')
            self.recursive_count += 2
            self.recursion_observer()
            return self.record_machine()
        else:
            pass
        if self.name not in self.exit:
            self.score = input(f'Enter {self.name} score: ').capitalize()
            self.validate_score(self.score, self.name)

            if self.score not in self.exit:
                self.validate_score(self.score, self.name)
                if self.name in self.candidate_record:
                    self.candidate_record[self.name] += (self.score,)
                else:
                    self.candidate_record[self.name] = (self.score,)
                return self.record_machine()
        else:
            return self.candidate_record

    def average_and_grading(self):
        smart_score = False if self.score_range != 100 else True
        number_of_student = 0
        self.gradingsheet = {}
        for name in sorted(self.candidate_record.keys()):
            adding = 0
            counter = 0
            number_of_student += 1
            for score in self.candidate_record[name]:
                adding += score
                counter += 1

            average = round(adding / counter, 1)
            grade = self.grade_checker(average, smart_score)
            grade_display = self.grade_displayer(grade)
            python_remark = self.remark(grade)

            self.gradingsheet[number_of_student] = (
                name, average, grade_display, python_remark)

        return self.gradingsheet

    def display(self):
        print(f'\n\n {'=' * 70}')
        print(f'{'FINAL RESULTS.':^70}')
        print(
            f'\n {'No':<5}| {'CANDIDATE NAME':^25}| {'SCORE':^8} | {'GRADE':^8} | {'REMARK':^10}')
        print(f'{'-' * 70}')
        for num, (name, avg, grade_display, remark) in self.gradingsheet.items():
            print(f' {num:<5}| {name:^25}| {avg:^ 8} | {str(grade_display).center(8)} | {remark:^10}')  # noqa E231

        print('  ')

    def store_file_as_csv(self):
        name_of_file = input('What do you want to name your file: ')
        data = self.gradingsheet

        def remove_color(text):
            import re
            return re.sub(r'\x1b\[[0-9;]*m', '', str(text))

        with open(f'{name_of_file}.csv', 'w+', newline='') as file:

            writer = csv.writer(file)
            writer.writerow(['No', 'Name', 'Average', 'Grade', 'Remark'])

            for num, (name, avg, grade_display, remark) in data.items():
                writer.writerow([
                    num,
                    name,
                    avg,
                    remove_color(grade_display),
                    remove_color(remark)
                ])
        print(f'\nSaved successfully as {name_of_file}.csv')


class Help(Scorekeeper):
    def __init__(self, candidate_record={}, exit=['Exit', 'End', 'Quit', 'Nope', 'No', 'Clear']):
        super().__init__(candidate_record, exit)
        self.gradingsheet = self.gradingsheet

    def delete_candidate_data(self, candidate):
        pass

    def store_file_as_json(self):
        name_of_file = input('What do you want to name your file: ')
        data = self.gradingsheet
        data = dict(islice(data.items(), 2))
        with open(f"{name_of_file}.json", "w+") as file:
            json.dump(data, file, indent=4)

    # def store_file_as_csv(self):
    #     name_of_file = input('What do you want to name your file: ')
    #     data = self.gradingsheet

    #     def remove_color(text):
    #         import re
    #         return re.sub(r'\x1b\[[0-9;]*m', '', str(text))

    #     with open(f'{name_of_file}.json', 'w+', newline='') as file:
    #         writer = csv.writer(file)
    #         writer.writerow(['No', 'Name', 'Average', 'Grade', 'Remark'])
    #         for num, (name, avg, grade_display, remark) in data.items():
    #             writer.writerow([
    #                 num,
    #                 name,
    #                 avg,
    #                 remove_color(grade_display),
    #                 remove_color(remark)
    #             ])
    #     print(f'\nSaved successfully as {name_of_file}.csv')

    def view_and_edit_a_file(self):
        pass


start = Scorekeeper()
start.start()
start.record_machine()
start.average_and_grading()
start.display()
start.store_file_as_csv()
user = input('\n\n\n\nQuit/Exit/Ended   ')
