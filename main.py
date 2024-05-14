from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QDialog,QDialogButtonBox,QMessageBox, QTabWidget, QApplication,QMainWindow, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QLineEdit, QToolBar
import sys

class Course():
    def __init__(self, name) -> None:
        self.__name = name
        self.__outputs = {}
        self.__total_weight = 0
        self.__grade = 0
        
    def add_output(self,output: str, score: float, weight: float):
        self.__outputs[output.upper()] = {"Score": score, "Weight": round(weight,2)}
        
    def compute_grade(self):
        total_weight = self.get_total_weight()
        outputs = list(self.__outputs.keys())
        grade = 0
        for output in outputs:
            grade += self.__outputs[output]["Score"]*self.__outputs[output]["Weight"]
        grade /= total_weight
            
        return round(grade,2)
            
    def __str__(self) -> str:   
        course_summary = f"Course Name: {self.__name}\n"

        return course_summary
    
    def set_name(self,str):
        self.__name = str
        
    def set_indiv_weight(self,weight, output_name):
        self.__outputs[output_name]["Weight"] = weight
        
        
    def set_grade(self,grade):
        self.__grade = grade
        
    def get_output_list(self):
        return list(self.__outputs.keys())
        
    def get_name(self):
        return self.__name
    
    def get_total_weight(self):
        total_weight = 0
        output_list = list(self.__outputs.keys())
        for output in output_list:
            total_weight += self.__outputs[output]["Weight"]
        return total_weight
    
    def get_grade(self):
        return self.__grade
    
    def clear_outputs(self):
        self.__outputs = {}

class CourseField(QWidget):
    def __init__(self,parent,name):
        super(CourseField, self).__init__(parent)
        
        self.newcourse = Course(name)
        self.total_score = 0
        self.total_weight = 0

        self.outputs = {}
        self.fullwindow = QHBoxLayout()
        
        self.output_table = QGroupBox()
        self.output_table.setTitle(f"{name} Outputs")
        
        self.output_table_layout = QHBoxLayout()
        self.output_fields_column = QVBoxLayout()
        self.score_fields_column = QVBoxLayout()
        self.weight_fields_column = QVBoxLayout()
        self.output_texts_column = QVBoxLayout()
        self.score_nums_column = QVBoxLayout()
        self.weight_nums_column = QVBoxLayout()
        ###
        output_label = QLabel("Output Name:")
        score_label = QLabel("Score (%):")
        weight_label = QLabel("Weight:")
        self.output_fields_column.addWidget(output_label)
        self.output_fields_column.addLayout(self.output_texts_column)
        self.output_fields_column.addStretch()
        self.score_fields_column.addWidget(score_label)
        self.score_fields_column.addLayout(self.score_nums_column)
        self.score_fields_column.addStretch()
        self.weight_fields_column.addWidget(weight_label)
        self.weight_fields_column.addLayout(self.weight_nums_column)
        self.weight_fields_column.addStretch()
        ###

        ###
        self.output_table_layout.addLayout(self.output_fields_column)
        self.output_table_layout.addLayout(self.score_fields_column)
        self.output_table_layout.addLayout(self.weight_fields_column)
        self.output_table.setLayout(self.output_table_layout)
        ###
        


        self.functions_layout = QVBoxLayout()
        self.set_up_buttons()
        self.set_up_summary()
        self.functions_layout.addStretch()

        self.fullwindow.addWidget(self.output_table)
        self.fullwindow.addLayout(self.functions_layout)
        
        self.setLayout(self.fullwindow)
        
    def set_up_buttons(self):
        buttons = QGroupBox()
        buttons.setFixedSize(QSize(100,80))
        buttons_layout = QVBoxLayout()
        add_button = QPushButton("Add Output")
        add_button.clicked.connect(self.add_output)
        compute_button = QPushButton("Compute")
        compute_button.clicked.connect(self.compute)
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(compute_button)
        buttons.setLayout(buttons_layout)
        self.functions_layout.addWidget(buttons)
    def set_up_summary(self):
        summary = QGroupBox()
        summary_layout = QVBoxLayout()
        summary.setFixedSize(QSize(100,100))
        total_weight_label = QLabel("Total Weight: ")
        self.weight_placeholder = QLabel("")
        grade_average_label = QLabel("Average Grade (%): ")
        self.grade_placeholder = QLabel("")
        summary_layout.addWidget(total_weight_label)
        summary_layout.addWidget(self.weight_placeholder)
        summary_layout.addWidget(grade_average_label)
        summary_layout.addWidget(self.grade_placeholder)
        summary.setLayout(summary_layout)
        self.functions_layout.addWidget(summary)
    def add_output(self):
        output_line = QLineEdit()
        score_line = QLineEdit()
        weight_line = QLineEdit()
        self.output_texts_column.addWidget(output_line)
        self.output_texts_column.addStretch()
        self.score_nums_column.addWidget(score_line)
        self.score_nums_column.addStretch()
        self.weight_nums_column.addWidget(weight_line)
        self.weight_nums_column.addStretch()    
        
        
    def compute(self):
        self.newcourse.clear_outputs()
        message = QMessageBox()
        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        for i in range(self.output_texts_column.count()):
            if self.output_texts_column.itemAt(i).widget() == None:
                continue
            if self.output_texts_column.itemAt(i).widget().text() == "":
                continue
            if self.score_nums_column.itemAt(i).widget().text() == "":
                message.setText("Missing score from output!")
                message.exec()
                return
            if self.weight_nums_column.itemAt(i).widget().text() == "":
                message.setText("Missing weight from output!")
                message.exec()
                return
            try:
                output_name = str(self.output_texts_column.itemAt(i).widget().text())
                score = float(self.score_nums_column.itemAt(i).widget().text())
                weight = float(self.weight_nums_column.itemAt(i).widget().text())
            except ValueError:
                message.setText("Put numbers in the Score and Weight fields!")
                message.exec()
                return
            else:
                self.newcourse.add_output(output_name,score,weight)
        try:
            self.weight_placeholder.setText(str(self.newcourse.get_total_weight()))
            self.grade_placeholder.setText(str(self.newcourse.compute_grade()))
        except ZeroDivisionError:
            self.weight_placeholder.setText("N/A")
            self.grade_placeholder.setText("N/A")

        
     
class MainWindow(QMainWindow):
    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)
        self.show()
        self.setWindowFlags(self.windowFlags() | Qt.Dialog)
        self.app = app
        self.setWindowTitle("Grade Computation")
        self.setMinimumWidth(700)
        self.courses = {}
        self.tab_widget = QTabWidget(self)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.tab_widget.removeTab)
        
        
        ##########
        # Menu Bar
        menu_bar = self.menuBar()
        # File
        file_menu = menu_bar.addMenu("File")
        import_from_file = file_menu.addAction("Import a file") #can take csv, json, and excel file
        export_to_file = file_menu.addAction("Export to...") #can export to csv, json, and excel file
        quit_app = file_menu.addAction("Save and Close")
        # View
        view_menu = menu_bar.addMenu("View")
        view_menu.addAction("Show")
        
        
        ############
        # Tool Bar
        toolbar = QToolBar("Toolbar")
        toolbar.setIconSize(QSize(16,16))
        self.addToolBar(toolbar)
        # Tool Bar for adding course
        add_course = QAction("Add New Course", self)
        add_course.setStatusTip("Add additional course to compute")
        add_course.triggered.connect(self.addcourse)
        
        toolbar.addAction(quit_app)
        toolbar.addAction(add_course)
        
        
        
    def importfile(self):
        pass
    def exportfile(self):
        pass
    def saveclose(self):
        pass
    def addcourse(self):
        get_course_name = QDialog()
        get_course_name.setWindowTitle("Adding New Course")
        
        get_course_layout = QVBoxLayout()
        get_course_message = QHBoxLayout()
        
        course_label = QLabel("Course Name:")
        course_field = QLineEdit()

        get_course_message.addWidget(course_label)
        get_course_message.addWidget(course_field)
        
        buttonbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        
        buttonbox.accepted.connect(get_course_name.accept)
        buttonbox.rejected.connect(get_course_name.reject)
        
        
        get_course_layout.addLayout(get_course_message)
        get_course_layout.addWidget(buttonbox)
        
        get_course_name.setLayout(get_course_layout)

        if get_course_name.exec() and course_field.text() != '':
            course_name = course_field.text().upper()
            if course_name in self.courses:
                return
        else:
            return
        
        course = CourseField(self, course_name)
        
        self.tab_widget.addTab(course, course_name)
        self.courses[course_name] = course
        self.setCentralWidget(self.tab_widget)

    def coursename(self,str):
        print(str)


def main():
    app = QApplication(sys.argv)
    window = MainWindow(app)
    window.show()
    app.exec()

if __name__ == "__main__":
    main()