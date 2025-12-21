import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import json
import re
from itertools import islice


class Grading:
    def __init__(self):
        self.BLUE = '#4A90E2'
        self.GREEN = '#7ED321'
        self.YELLOW = '#F5A623'
        self.RED = '#D0021B'

    def grade_checker(self, score, smart_score=True):
        '''Calculates grade of student if Score within range 0 and 100'''
        if smart_score:
            grade = ('A' if score >= 70 else
                     'B' if score >= 60 else
                     'C' if score >= 50 else
                     'D' if score >= 45 else
                     'E' if score >= 40 else
                     'F' if score >= 0 else '-')
            return grade
        else:
            return '-'

    def get_color_for_grade(self, grade):
        '''Return colour for each grade.'''
        match grade:
            case 'A':
                return self.BLUE
            case 'B':
                return self.GREEN
            case 'C':
                return self.GREEN
            case 'D':
                return self.YELLOW
            case 'E':
                return self.YELLOW
            case 'F':
                return self.RED
            case '-':
                return '#000000'

    def remark(self, grade):
        '''Returns a remark if grade is given.'''
        match grade:
            case 'A':
                return 'Excellent'
            case 'B':
                return 'Good'
            case 'C':
                return 'Good'
            case 'D':
                return 'Fair'
            case 'E':
                return 'Poor'
            case 'F':
                return 'Fail'
            case '-':
                return '-'


class Scorekeeper(Grading):
    def __init__(self, candidate_record=None, exit_list=None):
        '''It takes a Score Sheet and keep on recording if it's available.'''
        self.candidate_record = candidate_record if candidate_record is not None else {}
        self.exit = exit_list if exit_list is not None else ['Exit', 'End', 'Quit', 'Nope', 'No', 'Clear']
        self.recursive_count = 0
        self.gradingsheet = {}
        self.score_range = 100
        self.score = None
        self.name = None
        super().__init__()

    def validate_score(self, score, name):
        '''Checks if the Scores are Integers and within the Scorerange set by the tutor.'''
        if isinstance(score, str) and score in self.exit:
            return False
        try:
            self.score = int(score)
            if self.score > self.score_range:
                return False
            if self.score < 0:
                return False
            return True
        except ValueError:
            return False

    def add_candidate_score(self, name, score):
        '''Add a score for a candidate'''
        if not self.validate_score(score, name):
            return False
        
        if name in self.candidate_record:
            self.candidate_record[name] += (self.score,)
        else:
            self.candidate_record[name] = (self.score,)
        return True

    def average_and_grading(self):
        '''Calculate averages and grades for all candidates'''
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
            remark = self.remark(grade)

            self.gradingsheet[number_of_student] = (name, average, grade, remark)

        return self.gradingsheet

    def delete_candidate(self, candidate):
        '''Delete a candidate from the record'''
        if candidate in self.candidate_record:
            del self.candidate_record[candidate]
            self.average_and_grading()
            return True
        return False


class Help(Scorekeeper):
    '''Extra functionality for file operations and data management'''

    def store_file_as_csv(self, filename):
        '''Store results as CSV'''
        if not self.gradingsheet:
            self.average_and_grading()

        try:
            with open(f'{filename}.csv', 'w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['No', 'Name', 'Average', 'Grade', 'Remark'])

                for num, (name, avg, grade, remark) in self.gradingsheet.items():
                    writer.writerow([num, name, avg, grade, remark])
            return True
        except Exception as e:
            return False

    def store_file_as_json(self, filename):
        '''Store results as JSON'''
        if not self.gradingsheet:
            self.average_and_grading()

        try:
            data = dict(islice(self.gradingsheet.items(), len(self.gradingsheet)))
            with open(f"{filename}.json", "w+") as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            return False


class ScoreKeeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Smart Score Manager')
        self.root.geometry('1000x750')
        
        self.manager = Help()
        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = ttk.Label(self.root, text='Smart Score Manager', font=('Arial', 18, 'bold'))
        title_label.pack(pady=10)

        # Max Score Frame
        config_frame = ttk.Frame(self.root)
        config_frame.pack(pady=10, padx=10, fill='x')
        
        ttk.Label(config_frame, text='Max Score:').pack(side='left', padx=5)
        self.max_score_var = tk.StringVar(value='100')
        max_score_spinbox = ttk.Spinbox(config_frame, from_=1, to=500, textvariable=self.max_score_var, width=10)
        max_score_spinbox.pack(side='left', padx=5)
        
        ttk.Button(config_frame, text='Set Max Score', command=self.set_max_score).pack(side='left', padx=5)

        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text='Add New Score', padding=10)
        input_frame.pack(pady=10, padx=10, fill='x')

        ttk.Label(input_frame, text='Student Name:').grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.name_entry = ttk.Entry(input_frame, width=25)
        self.name_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)

        ttk.Label(input_frame, text='Score:').grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.score_entry = ttk.Entry(input_frame, width=10)
        self.score_entry.grid(row=0, column=3, sticky='ew', padx=5, pady=5)

        ttk.Button(input_frame, text='Add Score', command=self.add_score).grid(row=0, column=4, padx=5, pady=5)
        input_frame.columnconfigure(1, weight=1)

        # Table Frame
        table_frame = ttk.LabelFrame(self.root, text='Results Table', padding=10)
        table_frame.pack(pady=10, padx=10, fill='both', expand=True)

        # Treeview
        columns = ('No', 'Name', 'Average', 'Grade', 'Remark', 'Actions')
        self.tree = ttk.Treeview(table_frame, columns=columns, height=20, show='headings')
        
        self.tree.column('No', width=40, anchor='center')
        self.tree.column('Name', width=150, anchor='w')
        self.tree.column('Average', width=80, anchor='center')
        self.tree.column('Grade', width=70, anchor='center')
        self.tree.column('Remark', width=120, anchor='w')
        self.tree.column('Actions', width=100, anchor='center')

        for col in columns:
            self.tree.heading(col, text=col)

        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        self.tree.bind('<Button-1>', self.on_tree_click)

        # Statistics Frame
        stats_frame = ttk.LabelFrame(self.root, text='Statistics', padding=10)
        stats_frame.pack(pady=10, padx=10, fill='x')

        self.stats_label = ttk.Label(stats_frame, text='Total: 0 | Average: 0.0 | Highest: 0 | Lowest: 0', font=('Arial', 10))
        self.stats_label.pack()

        # Button Frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10, padx=10, fill='x')

        ttk.Button(button_frame, text='Export to CSV', command=self.export_csv).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Export to JSON', command=self.export_json).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Clear All', command=self.clear_all).pack(side='left', padx=5)

    def set_max_score(self):
        """Set the maximum score range"""
        try:
            score = int(self.max_score_var.get())
            if score < 1 or score > 500:
                raise ValueError("Score must be between 1 and 500")
            self.manager.score_range = score
            messagebox.showinfo('Success', f'Max score set to {score}')
        except ValueError as e:
            messagebox.showerror('Error', f'Invalid input: {str(e)}')

    def add_score(self):
        """Add a new score"""
        name = self.name_entry.get().strip().title()
        score_str = self.score_entry.get().strip()

        # Validate name
        if not name:
            messagebox.showerror('Error', 'Please enter a student name')
            return
        
        if not name.replace(' ', '').isalpha():
            messagebox.showerror('Error', 'Name must contain only letters')
            return

        # Validate score
        if not score_str:
            messagebox.showerror('Error', 'Please enter a score')
            return

        if not self.manager.validate_score(score_str, name):
            messagebox.showerror('Error', f'Score must be between 0 and {self.manager.score_range}')
            return

        # Add score
        self.manager.add_candidate_score(name, score_str)
        self.name_entry.delete(0, tk.END)
        self.score_entry.delete(0, tk.END)
        self.update_display()
        messagebox.showinfo('Success', f'Score added for {name}')

    def update_display(self):
        """Update the table and statistics"""
        # Recalculate
        self.manager.average_and_grading()

        # Clear table
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add rows
        for num, (name, avg, grade, remark) in self.manager.gradingsheet.items():
            self.tree.insert('', 'end', iid=num, values=(num, name, avg, grade, remark, 'Edit | Delete'))

        # Update statistics
        self.update_statistics()

    def update_statistics(self):
        """Update statistics display"""
        scores = []
        for candidate_scores in self.manager.candidate_record.values():
            scores.extend(candidate_scores)

        if not scores:
            self.stats_label.config(text='Total: 0 | Average: 0.0 | Highest: 0 | Lowest: 0')
            return

        total = len(self.manager.candidate_record)
        avg = round(sum(scores) / len(scores), 1)
        highest = max(scores)
        lowest = min(scores)

        self.stats_label.config(
            text=f'Total Students: {total} | Class Average: {avg} | Highest: {highest} | Lowest: {lowest}'
        )

    def on_tree_click(self, event):
        """Handle tree click events"""
        if not self.tree.selection():
            return

        item = self.tree.selection()[0]
        col = self.tree.identify_column(event.x)
        
        if col == '#6':  # Actions column
            num = int(item)
            if num in self.manager.gradingsheet:
                name, _, _, _ = self.manager.gradingsheet[num]
                self.show_action_menu(event.x_root, event.y_root, name)

    def show_action_menu(self, x, y, name):
        """Show context menu"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label='Add Score', command=lambda: self.add_score_dialog(name))
        menu.add_command(label='Delete', command=lambda: self.delete_candidate(name))
        menu.post(x, y)

    def add_score_dialog(self, name):
        """Add additional score to existing candidate"""
        dialog = tk.Toplevel(self.root)
        dialog.title(f'Add Score for {name}')
        dialog.geometry('300x150')

        ttk.Label(dialog, text=f'Add another score for {name}:').pack(pady=10)
        score_entry = ttk.Entry(dialog, width=10)
        score_entry.pack(pady=5)

        def save():
            score_str = score_entry.get().strip()
            if not score_str:
                messagebox.showerror('Error', 'Please enter a score')
                return
            
            if not self.manager.validate_score(score_str, name):
                messagebox.showerror('Error', f'Invalid score. Must be 0-{self.manager.score_range}')
                return
            
            self.manager.add_candidate_score(name, score_str)
            self.update_display()
            dialog.destroy()
            messagebox.showinfo('Success', f'Score added for {name}')

        ttk.Button(dialog, text='Add', command=save).pack(pady=10)

    def delete_candidate(self, name):
        """Delete a candidate"""
        if messagebox.askyesno('Confirm', f'Delete all scores for {name}?'):
            if self.manager.delete_candidate(name):
                self.update_display()
                messagebox.showinfo('Success', f'{name} removed')
            else:
                messagebox.showerror('Error', f'{name} not found')

    def export_csv(self):
        """Export to CSV"""
        if not self.manager.gradingsheet:
            messagebox.showwarning('Warning', 'No data to export')
            return

        file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')])
        if not file_path:
            return

        filename = file_path.replace('.csv', '')
        if self.manager.store_file_as_csv(filename):
            messagebox.showinfo('Success', f'Exported to {filename}.csv')
        else:
            messagebox.showerror('Error', 'Failed to export')

    def export_json(self):
        """Export to JSON"""
        if not self.manager.gradingsheet:
            messagebox.showwarning('Warning', 'No data to export')
            return

        file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[('JSON files', '*.json')])
        if not file_path:
            return

        filename = file_path.replace('.json', '')
        if self.manager.store_file_as_json(filename):
            messagebox.showinfo('Success', f'Exported to {filename}.json')
        else:
            messagebox.showerror('Error', 'Failed to export')

    def clear_all(self):
        """Clear all data"""
        if messagebox.askyesno('Confirm', 'Clear all student data?'):
            self.manager.candidate_record = {}
            self.manager.gradingsheet = {}
            self.update_display()


if __name__ == '__main__':
    root = tk.Tk()
    app = ScoreKeeperGUI(root)
    root.mainloop()
