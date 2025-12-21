import os
import json
import csv
from itertools import islice
os.chdir('C:/Users/ALIYU/Documents/Score Keeper')


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
        '''It takes a Score Sheet and keep on recording if it's available. '''
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
        ''' The recording,calculation of results starts here.'''

        # print a simple header
        print("\n\n\t" + '=' * 15 + " Smart Score Manager " + '=' * 15)
        try:
            self.score_range = int(input(
                f'{self.LIGHTBLUE_EX}  ⚠  Tutor Should Please Write The Highest Intended Score  ⚠\n{self.RESET_COLOR}   ==>'))
        except ValueError:
            return self.start()

    def validate_score(self, score, name):
        '''Checks if the Scores are Integers and within the Scorerange set by the tutor.'''

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
        '''Takes name and score as input, validates and stores them in a dictionary.'''

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
        '''This where the calculations og result takes place. 
        It returns a grade and remark if the score range is 100.'''
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
        '''This section is takes cares of what python gives as output.'''

        print('\n\n ' + '=' * 70)
        print('{:^70}'.format('FINAL RESULTS.'))
        print('\n {:<5}| {:^25}| {:^8} | {:^8} | {:^10}'.format('No', 'CANDIDATE NAME', 'SCORE', 'GRADE', 'REMARK'))
        print('-' * 70)
        for num, (name, avg, grade_display, remark) in self.gradingsheet.items():
            print(' {:<5}| {:^25}| {:^8} | {:^8} | {:^10}'.format(num, name, avg, str(grade_display).center(8), remark))

        print('  ')


class Help(Scorekeeper):
    '''It does extra task aside calculation of results'''

    def __init__(self, candidate_record={}, exit=['Exit', 'End', 'Quit', 'Nope', 'No', 'Clear']):
        '''It takes a Score Sheet and keep on recording if it's available. '''

        super().__init__(candidate_record, exit)
        self.gradingsheet = self.gradingsheet

    def delete_candidate_data(self, candidate=None):
        '''Deletes a candidate data from the Scoresheet'''
        if not self.candidate_record:
            print("No candidate data available to delete.")
            return False

        if candidate is None:
            candidate = input("Enter candidate name to delete: ").title()

        if candidate in self.candidate_record:
            confirm = input(f"Are you sure you want to delete all scores for {candidate}? (y/n): ").strip().lower()
            if confirm == 'y':
                del self.candidate_record[candidate]
                # recompute gradingsheet
                self.average_and_grading()
                print(f"{candidate} has been removed from the score sheet.")
                return True
            else:
                print("Deletion cancelled.")
                return False
        else:
            print(f"{candidate} not found in the score sheet.")
            return False

    def store_file_as_json(self):
        '''It stores a file in json format.'''

        name_of_file = input('What do you want to name your file: ')
        data = self.gradingsheet
        data = dict(islice(data.items(), 2))
        with open(f"{name_of_file}.json", "w+") as file:

            json.dump(data, file, indent=4)

    def store_file_as_csv(self):
        '''It store a file as csv and makes it available for advanced editing on Word Editor'''
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
        return os.path.abspath(f'{name_of_file}.csv')

    def view_and_edit_a_file(self):
        '''Interactive view and edit of the current gradingsheet.

        Actions:
         - View current gradingsheet
         - Add a new score for a candidate
         - Replace a candidate's scores (enter comma-separated scores)
         - Delete a candidate
         - Quit editor
        '''
        if not self.gradingsheet:
            # ensure gradingsheet is prepared
            self.average_and_grading()

        def print_sheet():
            print("\nCurrent Results:")
            print('-' * 70)
            print('{:<5} {:^25} {:^8} {:^8} {:^10}'.format('No', 'Name', 'Average', 'Grade', 'Remark'))
            print('-' * 70)
            for num, (name, avg, grade_display, remark) in self.gradingsheet.items():
                # remove color codes for compact view
                stripped_grade = str(grade_display)
                stripped_remark = str(remark)
                print('{:<5} {:^25} {:^8} {:^8} {:^10}'.format(num, name, avg, stripped_grade.center(8), stripped_remark))

        while True:
            print_sheet()
            action = input("\nChoose action: [A]dd score, [R]eplace scores, [D]elete candidate, [Q]uit: ").strip().lower()
            if action == 'q':
                break
            if action not in ('a', 'r', 'd'):
                print("Unknown action, please choose A, R, D or Q.")
                continue

            name = input("Enter candidate name (exact): ").title()
            if name not in self.candidate_record and action in ('a', 'r'):
                create = input(f"{name} not found. Create new candidate? (y/n): ").strip().lower()
                if create != 'y':
                    continue
                else:
                    self.candidate_record[name] = tuple()

            if action == 'a':
                # add one new score to candidate
                raw = input(f"Enter new score to add for {name}: ").strip()
                # validate the entered score
                try:
                    # using validate_score which expects string input
                    self.validate_score(raw, name)
                    if isinstance(self.score, int):
                        if name in self.candidate_record:
                            self.candidate_record[name] += (self.score,)
                        else:
                            self.candidate_record[name] = (self.score,)
                        print(f"Added score {self.score} for {name}.")
                        self.average_and_grading()
                except Exception as e:
                    print("Could not add score:", e)
            elif action == 'r':
                # replace all scores
                raw = input(f"Enter comma separated scores for {name} (e.g. 12, 45, 78): ").strip()
                parts = [p.strip() for p in raw.split(',') if p.strip() != '']
                new_scores = []
                ok = True
                for part in parts:
                    try:
                        self.validate_score(part, name)
                        if isinstance(self.score, int):
                            new_scores.append(self.score)
                        else:
                            ok = False
                            break
                    except Exception:
                        ok = False
                        break
                if not ok or not new_scores:
                    print("Invalid scores entered. No changes made.")
                else:
                    self.candidate_record[name] = tuple(new_scores)
                    self.average_and_grading()
                    print(f"Replaced scores for {name}.")
            elif action == 'd':
                # delete candidate
                if name in self.candidate_record:
                    confirm = input(f"Delete {name}? (y/n): ").strip().lower()
                    if confirm == 'y':
                        del self.candidate_record[name]
                        self.average_and_grading()
                        print(f"{name} deleted.")
                else:
                    print(f"{name} not found.")
        print("Exited view/edit mode.")


class Uploadresults:
    '''It updates/uploads a result to designated portal Using Web Scrapping (basic helper).'''

    def __init__(self, scorekeeper=None):
        """
        scorekeeper: an instance of Scorekeeper (or Help) with gradingsheet available
        """
        self.scorekeeper = scorekeeper

    def _remove_color(self, text):
        import re
        return re.sub(r'\x1b\[[0-9;]*m', '', str(text))

    def export_csv(self, name_of_file='upload_export'):
        '''Export the current gradingsheet to a CSV and return its path.'''
        if not self.scorekeeper:
            raise ValueError("No scorekeeper provided to export data from.")
        data = self.scorekeeper.gradingsheet
        if not data:
            # try to build it
            self.scorekeeper.average_and_grading()
            data = self.scorekeeper.gradingsheet

        path = f'{name_of_file}.csv'
        with open(path, 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['No', 'Name', 'Average', 'Grade', 'Remark'])
            for num, (name, avg, grade_display, remark) in data.items():
                writer.writerow([
                    num,
                    name,
                    avg,
                    self._remove_color(grade_display),
                    self._remove_color(remark)
                ])
        return os.path.abspath(path)

    def upload_file(self, upload_url, file_path, file_field='file', auth=None, extra_data=None, timeout=30):
        """
        Attempt to upload a file via HTTP POST as multipart/form-data.

        upload_url: endpoint to POST to.
        file_path: path to file to upload.
        file_field: form field name used for the uploaded file.
        auth: tuple(username, password) for basic auth (optional).
        extra_data: dict additional form data (optional).
        Returns requests.Response on success, or raises informative errors.
        Note: this function requires the 'requests' package.
        """
        try:
            import requests
        except Exception:
            raise RuntimeError("requests is required for upload_file. Install it with 'pip install requests'.")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        files = {file_field: open(file_path, 'rb')}
        data = extra_data or {}
        try:
            if auth:
                resp = requests.post(upload_url, files=files, data=data, auth=auth, timeout=timeout)
            else:
                resp = requests.post(upload_url, files=files, data=data, timeout=timeout)
            return resp
        finally:
            # ensure file handle closed
            try:
                files[file_field].close()
            except Exception:
                pass


start = Scorekeeper()
start.start()
start.record_machine()
start.average_and_grading()
start.display()
user = input('\n\n\n\nQuit/Exit/Ended   ')