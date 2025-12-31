from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QTableWidgetItem, QBoxLayout, QVBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt6 import uic
import json
import os

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # ====== CHỈ CẦN 1 DÒNG loadUi ======
        # Sửa thành:
        import os
        
        # Tìm file UI
        ui_file = None
        possible_paths = [
            "flashcard.ui",  # Cùng thư mục
            os.path.join(os.path.dirname(__file__), "flashcard.ui"),  # Tuyệt đối
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                ui_file = path
                print(f"✅ Tìm thấy UI: {ui_file}")
                break
        
        if ui_file:
            try:
                uic.loadUi(ui_file, self)
                print(f"✅ Đã load UI từ: {ui_file}")
            except Exception as e:
                print(f"❌ Lỗi load UI: {e}")
                self.setup_basic_ui()
        else:
            print("⚠️ Không tìm thấy file UI, tạo giao diện thủ công")
            self.setup_basic_ui()
            return  # Quan trọng: return ngay nếu không có UI
        
        self.show()
        # ... phần còn lại ...
        
        # ĐỌC DATA TỪ FILE JSON (THAY THẾ DATA MẪU)
        self.load_from_json()
        
        # Nếu không có data, dùng mẫu
        if not self.queslist:
            self.queslist = [{'mot':'one'}, {'hai':'two'}]
            self.save_to_json()  # Lưu data mẫu
        
        self.flip = 0
        self.display()
        self.btnAdd.clicked.connect(self.addingcard)
        self.btnFlip.clicked.connect(self.flipingcard)
        self.btnNext.clicked.connect(self.nextcard)
        self.btnPrev.clicked.connect(self.backcard)
        self.btnDelete.clicked.connect(self.deletecard)
        
        # KẾT NỐI MENU ACTIONS
        self.actionNew.triggered.connect(self.new_deck)
        self.actionOpen.triggered.connect(self.open_deck)
        self.actionSave.triggered.connect(self.save_deck)
        self.actionExit.triggered.connect(self.close)
        self.actionAbout.triggered.connect(self.about_app)
    def setup_basic_ui(self):
        # """Tạo UI cơ bản khi không có file .ui"""
        # print("📝 Tạo UI cơ bản...")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Tạo widget cơ bản
        self.labelCounter = QLabel("跟俊德学习")
        self.labelCounter.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.labelFlashcard = QLabel("Câu hỏi sẽ hiển thị ở đây")
        self.labelFlashcard.setMinimumSize(400, 250)
        self.labelFlashcard.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelFlashcard.setStyleSheet("border: 2px solid blue; padding: 20px;")
        
        # Nút điều khiển
        self.btnPrev = QPushButton("◀ Trước")
        self.btnFlip = QPushButton("Lật thẻ")
        self.btnNext = QPushButton("Sau ▶")
        self.btnDelete = QPushButton("Xóa thẻ")
        
        # Ô nhập liệu
        self.txtQuestion = QLineEdit()
        self.txtQuestion.setPlaceholderText("Câu hỏi")
        
        self.txtAnswer = QTextEdit()
        self.txtAnswer.setPlaceholderText("Câu trả lời")
        self.txtAnswer.setMaximumHeight(100)
        
        self.btnAdd = QPushButton("Thêm thẻ")
        
        # Thêm vào layout
        layout.addWidget(self.labelCounter)
        layout.addWidget(self.labelFlashcard)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btnPrev)
        button_layout.addWidget(self.btnFlip)
        button_layout.addWidget(self.btnNext)
        button_layout.addWidget(self.btnDelete)
        layout.addLayout(button_layout)
        
        layout.addWidget(QLabel("Câu hỏi:"))
        layout.addWidget(self.txtQuestion)
        layout.addWidget(QLabel("Câu trả lời:"))
        layout.addWidget(self.txtAnswer)
        layout.addWidget(self.btnAdd)
        
        central_widget.setLayout(layout)
        self.setWindowTitle("Flashcard Học Tập")
        
        # ====== QUAN TRỌNG: KẾT NỐI SIGNAL NGAY TẠI ĐÂY ======
        self.connect_signals()
    
    def connect_signals(self):
        """Kết nối tất cả signal"""
        print("🔗 Kết nối signal...")
        
        # Kết nối nút
        if hasattr(self, 'btnAdd'):
            self.btnAdd.clicked.connect(self.addingcard)
            print("✅ Kết nối btnAdd")
        
        if hasattr(self, 'btnFlip'):
            self.btnFlip.clicked.connect(self.flipingcard)
            print("✅ Kết nối btnFlip")
        
        if hasattr(self, 'btnNext'):
            self.btnNext.clicked.connect(self.nextcard)
            print("✅ Kết nối btnNext")
        
        if hasattr(self, 'btnPrev'):
            self.btnPrev.clicked.connect(self.backcard)
            print("✅ Kết nối btnPrev")
        
        if hasattr(self, 'btnDelete'):
            self.btnDelete.clicked.connect(self.deletecard)
            print("✅ Kết nối btnDelete")
    # ========== JSON HANDLING ==========
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
    def load_from_json(self):
        """Đọc dữ liệu từ file flashcards.json"""
        try:
            if os.path.exists("flashcards.json"):
                with open("flashcards.json", "r", encoding="utf-8") as f:
                    self.queslist = json.load(f)
                print(f"✅ Đã đọc {len(self.queslist)} thẻ từ file")
            else:
                print("📁 Chưa có file data, sẽ tạo mới")
                self.queslist = []
        except Exception as e:
            print(f"❌ Lỗi khi đọc file: {e}")
            self.queslist = []
    
    def save_to_json(self):
        """Lưu dữ liệu vào file flashcards.json"""
        try:
            with open("flashcards.json", "w", encoding="utf-8") as f:
                json.dump(self.queslist, f, ensure_ascii=False, indent=2)
            print(f"✅ Đã lưu {len(self.queslist)} thẻ vào file")
        except Exception as e:
            print(f"❌ Lỗi khi lưu file: {e}")
    
    # ========== MENU ACTIONS ==========
    
    def new_deck(self):
        """Tạo bộ thẻ mới"""
        reply = QMessageBox.question(
            self, "Tạo mới",
            "Bạn có chắc muốn tạo bộ thẻ mới?\nDữ liệu hiện tại sẽ bị mất!",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.queslist = []
            self.save_to_json()
            self.display()
            QMessageBox.information(self, "Thành công", "Đã tạo bộ thẻ mới!")
    
    def open_deck(self):
        """Mở file flashcard khác"""
        from PyQt6.QtWidgets import QFileDialog
        
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Mở file flashcard", "", "JSON Files (*.json)"
        )
        
        if file_name:
            try:
                with open(file_name, "r", encoding="utf-8") as f:
                    self.queslist = json.load(f)
                self.save_to_json()  # Lưu vào file mặc định
                self.display()
                QMessageBox.information(self, "Thành công", 
                    f"Đã mở {len(self.queslist)} thẻ từ file!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể mở file:\n{str(e)}")
    
    def save_deck(self):
        """Lưu dữ liệu vào file"""
        if not self.queslist:
            QMessageBox.warning(self, "Cảnh báo", "Không có thẻ nào để lưu!")
            return
        
        self.save_to_json()
        QMessageBox.information(self, "Thành công", 
            f"Đã lưu {len(self.queslist)} thẻ vào file!")
    
    def about_app(self):
        """Hiển thị thông tin ứng dụng"""
        QMessageBox.about(
            self, 
            "Về Flashcard App",
            """<b>Flashcard Học Tập v1.0</b>
            <p>Ứng dụng học tập bằng flashcard đơn giản.</p>
            <p>Phát triển by junde</p>
            <p>© 2024 - Hỗ trợ học tập</p>"""
        )
    
    # ========== CÁC HÀM CÓ SẴN (SỬA NHẸ) ==========
    
    def display(self):
        if self.queslist:
            for key in self.queslist[0].keys():
                self.labelFlashcard.setText(key)
            self.flip = 0
        else:
            self.labelFlashcard.setText("📭 Chưa có thẻ nào")
            self.flip = 0
    
    def addingcard(self):
        ques = self.txtQuestion.text()
        asw = self.txtAnswer.toPlainText()
        
        # KIỂM TRA INPUT
        if ques.strip() and asw.strip():
            self.queslist.append({ques: asw})
            
            # LUU VAO FILE NGAY
            self.save_to_json()
            
            # Hiển thị và xóa form
            for key in self.queslist[-1]:
                self.labelFlashcard.setText(key)
                self.flip = 0
            
            self.txtQuestion.clear()
            self.txtAnswer.clear()
            
            QMessageBox.information(self, "Thành công", "Đã thêm thẻ mới!")
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập cả câu hỏi và câu trả lời!")
    
    def deletecard(self):
        data, ke, lis = self.logic()
        
        # KIỂM TRA KẾT QUẢ LOGIC
        if lis == -1 or lis is None:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy thẻ để xóa!")
            return
        
        if 0 <= lis < len(self.queslist):
            # XÁC NHẬN XÓA
            card = self.queslist[lis]
            question = list(card.keys())[0]
            
            reply = QMessageBox.question(
                self, "Xác nhận xóa",
                f"Bạn có chắc muốn xóa thẻ này?\n\nCâu hỏi: {question}",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                del self.queslist[lis]
                
                # LUU VAO FILE NGAY
                self.save_to_json()
                
                # Hiển thị lại
                self.display()
                
                QMessageBox.information(self, "Thành công", "Đã xóa thẻ!")
        else:
            QMessageBox.warning(self, "Lỗi", "Index không hợp lệ!")
    
    # SỬA HÀM logic() để trả về giá trị mặc định
    def logic(self):
        if self.flip == 0:
            key = self.labelFlashcard.text()
            for i in range(len(self.queslist)): 
                for j in self.queslist[i].keys():
                    if j == key:
                        value = self.queslist[i][key]
                        return value, j, i
            return None, None, -1  # THÊM DÒNG NÀY
        else:
            value = self.labelFlashcard.text()
            for i in range(len(self.queslist)):
                for j in self.queslist[i].keys():
                    if value == self.queslist[i][j]:
                        key = j
                        return key, j, i
            return None, None, -1  # THÊM DÒNG NÀY

app = QApplication([])
flashcard = main()
app.exec()