from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem
 #thêm code từ các file khác
from PyQt6 import uic #thêm code từ file khác


class main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("flashcard/flashcard.ui",self) #sử dụng file thiết kế
        self.show() #hiện thị file thiết kế
        self.queslist = [{'mot':'one'},{'hai':'two'}]
        self.flip = 0
        self.display()
        self.btnAdd.clicked.connect(self.addingcard)
        self.btnFlip.clicked.connect(self.flipingcard)
        self.btnNext.clicked.connect(self.nextcard)
        self.btnPrev.clicked.connect(self.backcard)
    def display(self):
        for key in self.queslist[0].keys():
            self.labelFlashcard.setText(key)

    def addingcard(self):
        ques = self.txtQuestion.text()
        asw = self.txtAnswer.toPlainText()
        self.queslist.append({ques:asw})
        # self.labelFlashcard.setText(self.queslist[len(self.queslist)])
        for key in self.queslist[len(self.queslist)-1]:
            self.labelFlashcard.setText(key)
            self.flip = 0
    def flipingcard(self):
        key = ""
        value = ""      
        data, ke, lis = self.logic()
        if self.flip == 0:
            self.labelFlashcard.setText(data)
            self.flip = 1
        else:
            self.labelFlashcard.setText(data)
            self.flip = 0
    def logic(self):
        key = ""
        value = ""
        if self.flip == 0:
            key = self.labelFlashcard.text()
            for i in range(len(self.queslist)): 
                for j in self.queslist[i].keys():
                    if j == key:
                        value = self.queslist[i][key]
                        return value, j, i
        else:
            value = self.labelFlashcard.text()
            for i in range(len(self.queslist)):
                for j in self.queslist[i].keys():
                    if value == self.queslist[i][j]:
                        key = j
                        return key, j, i
            
        
    def nextcard(self):
        data, ke, lis = self.logic()
        if (lis+1) < (len(self.queslist)):
            output = list(self.queslist[lis+1].keys())
            self.labelFlashcard.setText(output[0])
            self.flip = 0
        else:
            lis = 0
            output = list(self.queslist[lis].keys())
            self.labelFlashcard.setText(output[0])
            self.flip = 0

    def backcard(self):
        data, ke, lis = self.logic()
        if (lis-1) >= 0:
            output = list(self.queslist[lis-1].keys())
            self.labelFlashcard.setText(output[0])
            self.flip = 0
        else:
            lis = (len(self.queslist)-1)
            output = list(self.queslist[lis].keys())
            self.labelFlashcard.setText(output[0])
            self.flip = 0

            
        



app = QApplication([])
flashcard = main()
app.exec()