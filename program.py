from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
import sys
from setup_db import *
import os

def normalize_path(path):
    # Convert path separators to system-specific format
    normalized = os.path.normpath(path)
    # Check if path exists, if not try to find it relative to current directory
    if not os.path.exists(normalized):
        # Try relative to current directory
        relative_path = os.path.join(os.getcwd(), normalized)
        if os.path.exists(relative_path):
            return relative_path
    return normalized

class MessageBox():
    def success_box(self, message) :
        box = QMessageBox()
        box.setWindowTitle("Success")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Information)
        box.exec()

    def error_box(self, message) :
        box = QMessageBox()
        box.setWindowTitle("Error")
        box.setText(message)
        box.setIcon(QMessageBox.Icon.Critical)
        box.exec()

class Login(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi("ui/Login.ui", self)

        self.email = self.findChild(QLineEdit,"txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_eye_p = self.findChild(QPushButton, "btn_eye_p")

        self.btn_login.clicked.connect(self.login)
        self.btn_register.clicked.connect(self.show_register)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
    
    def hiddenOrShow(self,input:QLineEdit, button:QPushButton) :
        if input.echoMode() == QLineEdit.EchoMode.Password :
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else :
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))

    def login(self):
        msg = MessageBox()
        email = self.email.text().strip()
        password = self.password.text()

        if email == "":
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        
        if password == "" :
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        user = get_user_by_email_and_password(email, password)
        if user is not None :
            msg.success_box("Đăng nhập thành công")
            self.show_home(user["id"])
            return
        
        msg.error_box("Email hoặc mật khẩu không đúng")

    def show_home(self, user_id) :
        self.home = Home(user_id)
        self.home.show()
        self.close()

    def show_register(self) :
        self.register = Register()
        self.register.show()
        self.close()

class Register(QMainWindow) :
    def __init__(self) :
        super().__init__()
        uic.loadUi("ui/Register.ui", self)

        self.name = self.findChild(QLineEdit, "txt_name")
        self.email = self.findChild(QLineEdit, "txt_email")
        self.password = self.findChild(QLineEdit, "txt_password")
        self.confirm_password = self.findChild(QLineEdit, "txt_conf_pwd")
        self.btn_register = self.findChild(QPushButton, "btn_register")
        self.btn_login = self.findChild(QPushButton, "btn_login")
        self.btn_eye_p = self.findChild(QPushButton,"btn_eye_p")
        self.btn_eye_cp = self.findChild(QPushButton,"btn_eye_cp")

        self.btn_register.clicked.connect(self.register)
        self.btn_login.clicked.connect(self.show_login)
        self.btn_eye_p.clicked.connect(lambda: self.hiddenOrShow(self.password, self.btn_eye_p))
        self.btn_eye_cp.clicked.connect(lambda: self.hiddenOrShow(self.confirm_password, self.btn_eye_cp))
    
    def hiddenOrShow(self,input:QLineEdit, button:QPushButton) :
        if input.echoMode() == QLineEdit.EchoMode.Password :
            input.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setIcon(QIcon("img/eye-solid.svg"))
        else :
            input.setEchoMode(QLineEdit.EchoMode.Password)
            button.setIcon(QIcon("img/eye-slash-solid.svg"))
    
    def register(self) :
        msg = MessageBox()
        name = self.name.text().strip()
        email = self.name.text().strip()
        password = self.password.text().strip()
        confirm_password = self.confirm_password.text().strip()

        if name == "" :
            msg.error_box("Họ tên không được để trống")
            self.name.setFocus()
            return

        if email == "" :
            msg.error_box("Email không được để trống")
            self.email.setFocus()
            return
        
        if password == "" :
            msg.error_box("Mật khẩu không được để trống")
            self.password.setFocus()
            return
        
        if confirm_password == "" :
            msg.error_box("Xác nhận mật khẩu không được để trống")
            self.confirm_password.setFocus()
            return
        
        if password != confirm_password :
            msg.error_box("Mật khẩu không trùng khớp")
            self.confirm_password.setText("")
            self.password.setFocus()
            return
        
        if not self.validate_email(email) :
            msg.error_box("Email không hợp lệ")
            self.email.setFocus()
            return
        
        check_email = get_user_by_email(email)
        if check_email is not None:
            msg.error_box("Email đã tồn tại")
            return
        
        create_user(name, email, password)
        msg.success_box("Đăng ký thành công")
        self.show_login()

    def show_login(self) :
        self.login = Login()
        self.login.show()
        self.close()

    def validate_email(self,s):
            idx_at = s.find('@')
            if idx_at == -1 :
                return False
            return '.' in s[idx_at+1:]
        
class MovieItemWidget(QWidget):
    signal_detail_movie = pyqtSignal(int)
    signal_play_movie = pyqtSignal(int)
    signal_favorite_changed = pyqtSignal()  # New signal for favorite changes
    
    def __init__(self, movie_id, title, banner_path, video_path, description):
        super().__init__()
        self.movie_id = movie_id
        self.user_id = 1  # We'll get this from Main class
        
        # Load UI
        uic.loadUi('ui/movie_item.ui', self)
        
        # Set data
        self.titleLabel.setText(title)
        
        # Set banner with normalized path
        banner_path = normalize_path(banner_path)
        pixmap = QPixmap(banner_path)
        self.bannerLabel.setPixmap(pixmap)
        
        # Connect signals
        self.infoButton.clicked.connect(self.show_detail)
        self.playButton.clicked.connect(self.play_movie)
        self.btn_favorite.clicked.connect(self.toggle_favorite)
        
        # Set favorite icon
        self.update_favorite_icon()
        
    def set_user_id(self, user_id):
        self.user_id = user_id
        self.update_favorite_icon()
        
    def update_favorite_icon(self):
        is_fav = is_favorite(self.user_id, self.movie_id)
        icon = QIcon("img/heart-solid.svg" if is_fav else "img/heart-regular.svg")
        self.btn_favorite.setIcon(icon)
        
    def show_detail(self):
        self.signal_detail_movie.emit(self.movie_id)
        
    def play_movie(self):
        self.signal_play_movie.emit(self.movie_id)
        
    def toggle_favorite(self):
        is_fav = is_favorite(self.user_id, self.movie_id)
        if is_fav:
            remove_from_favorites(self.user_id, self.movie_id)
        else:
            add_to_favorites(self.user_id, self.movie_id)
        self.update_favorite_icon()
        self.signal_favorite_changed.emit()  # Emit signal when favorite status changes
        
class Home(QMainWindow) :
    def __init__(self, user_id) :
        super().__init__()
        uic.loadUi("ui/mainwindow.ui", self)

        self.user_id = user_id
        self.user = get_user_by_id(user_id)
        self.loadAccountInfo()
        
        self.main_widget = self.findChild(QStackedWidget, "main_widget")
        self.btn_nav_home = self.findChild(QPushButton, "btn_nav_home")
        self.btn_nav_play = self.findChild(QPushButton, "btn_nav_play")
        self.btn_watch = self.findChild(QPushButton, "btn_watch")
        self.btn_nav_profile = self.findChild(QPushButton, "btn_nav_profile")
        self.btn_logout = self.findChild(QPushButton, "btn_logout")
        self.btn_radioMale = self.findChild(QRadioButton, "radio_male")
        self.btn_radioFemale = self.findChild(QRadioButton, "radio_female")
        self.btn_avatar = self.findChild(QPushButton,"btn_avatar")
        self.lb_avatar = self.findChild(QLabel,"lb_avatar")
        self.btn_save = self.findChild(QPushButton, "btn_save")
        self.btn_avatar.clicked.connect(self.update_avatar)

        self.main_widget.setCurrentIndex(0)
        self.btn_nav_home.clicked.connect(lambda: self.navMainScreen(0))
        self.btn_nav_play.clicked.connect(lambda: self.navMainScreen(1))
        self.btn_watch.clicked.connect(lambda: self.navMainScreen(2))
        self.btn_nav_profile.clicked.connect(lambda: self.navMainScreen(3))
        self.btn_logout.clicked.connect(self.show_login)
        self.btn_save.clicked.connect(self.save_info)
    


    def navMainScreen(self, index):
        self.main_widget.setCurrentIndex(index)
        
    def loadAccountInfo(self):
        self.txt_name = self.findChild(QLineEdit, "txt_name")
        self.txt_email = self.findChild(QLineEdit, "txt_email")
        self.txt_telephone = self.findChild(QLineEdit, "txt_telephone")
        self.date_birthday = self.findChild(QDateEdit, "date_birthday")
        self.radio_male = self.findChild(QRadioButton, "radio_male")
        self.radio_female = self.findChild(QRadioButton, "radio_female")
        self.lb_avatar = self.findChild(QLabel, "lb_avatar")

        self.txt_name.setText(self.user["name"])
        self.txt_email.setText(self.user["email"])
        self.txt_telephone.setText(str(self.user["telephone"]))

        birthday_str = self.user.get("birthday", "")
        birthday = QDate.fromString(birthday_str, "dd-MM-yyyy")
        self.date_birthday.setDate(birthday if birthday.isValid() else QDate.currentDate())

        gender = self.user.get("gender", "").lower()
        self.radio_male.setChecked(gender == "male")
        self.radio_female.setChecked(gender == "female")

        avatar = self.user.get("avatar", "")
        if avatar:
            pixmap = QPixmap(avatar)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(self.lb_avatar.width(), self.lb_avatar.height(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.lb_avatar.setPixmap(pixmap)

    def show_login(self) :
        self.login = Login()
        self.login.show()
        self.close()    

    def save_info(self):
        name = self.txt_name.text()
        email = self.txt_email.text()
        telephone = self.txt_telephone.text()
        birthday = self.date_birthday.date().toString("dd-MM-yyyy")

        if self.radio_male.isChecked():
            gender = "Male"
        elif self.radio_female.isChecked():
            gender = "Female"
        else:
            gender = "Other"

        self.user["name"] = name
        self.user["gender"] = gender
        self.user["email"] = email
        self.user["telephone"] = telephone
        self.user["birthday"] = birthday
        

        update_user_in_db(self.user_id, name, gender, email, telephone, birthday)
        QMessageBox.information(self, "Cập nhật", "Thông tin người dùng đã được lưu.")
    
    def update_avatar(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select Image","","Image Files(*.png *.jpg *.jpeg *.bmp)")
        if file :
            self.user["avatar"] = file
            self.lb_avatar.setPixmap(QPixmap(file))
            update_user_avatar(self.user_id, file)
    
    def setupUI(self):
        # Setup movie container
        self.movieList = QScrollArea()
        self.movieList.setStyleSheet("""
            QScrollArea {
                background-color: black;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgb(45, 45, 45);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(80, 80, 80);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.movieItem = QWidget()
        self.gridLayout = QGridLayout(self.movieItem)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(10)

        self.movieItem.setLayout(self.gridLayout)
        self.movieList.setWidget(self.movieItem)
        self.movieList.setWidgetResizable(True)
        
        # Add movie list to video container
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.movieList)
        self.video_container.setLayout(containerLayout)
        
        # Setup favorite container with scroll area
        self.favoriteList = QScrollArea()
        self.favoriteList.setStyleSheet("""
            QScrollArea {
                background-color: black;
                border: none;
            }
            QScrollBar:vertical {
                border: none;
                background: rgb(45, 45, 45);
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(80, 80, 80);
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        self.favoriteItem = QWidget()
        self.favoriteLayout = QGridLayout(self.favoriteItem)
        self.favoriteLayout.setContentsMargins(10, 10, 10, 10)
        self.favoriteLayout.setSpacing(10)
        
        self.favoriteItem.setLayout(self.favoriteLayout)
        self.favoriteList.setWidget(self.favoriteItem)
        self.favoriteList.setWidgetResizable(True)
        
        # Add favorite list to favorite container
        favoriteContainerLayout = QVBoxLayout()
        favoriteContainerLayout.addWidget(self.favoriteList)
        self.favorite_container.setLayout(favoriteContainerLayout)
        
        self.txt_search = self.findChild(QLineEdit, 'txt_search')
        self.btn_search = self.findChild(QPushButton, 'btn_search')
        self.btn_search.clicked.connect(self.search_movie)
        
        # Setup media player components
        self.setupMediaPlayer()
    
    def setupMediaPlayer(self):
        # Setup media player
        self.lbl_title = self.findChild(QLabel, 'videoName')
        self.volumeBtn = self.findChild(QPushButton, 'volumeBtn')
        self.timeLabel = self.findChild(QLabel, 'timeLabel')
        self.durationBar = self.findChild(QSlider, 'durationBar')
        self.volumeBar = self.findChild(QSlider, 'volumeBar')
        self.videoName = self.findChild(QLabel, 'videoName')
        self.playBtn = self.findChild(QPushButton, 'playBtn')
        
        # Load icons
        self.playIcon = QIcon("img/play-solid.svg")
        self.pauseIcon = QIcon("img/pause-solid.svg")
        self.volumeHighIcon = QIcon("img/volume-high-solid.svg")
        self.volumeLowIcon = QIcon("img/volume-low-solid.svg")
        self.volumeOffIcon = QIcon("img/volume-off-solid.svg")
        
        # Setup video player buttons
        self.playBtn.setIcon(self.playIcon)
        self.volumeBtn.setIcon(self.volumeHighIcon)
        
        # Setup volume control
        self.current_volume = 50
        self.volumeBar.setValue(self.current_volume)
        self.volumeBar.setRange(0, 100)
        self.volumeBar.setValue(50)
        
        # Connect signals
        self.playBtn.clicked.connect(self.play)
        self.volumeBtn.clicked.connect(self.toggleMute)
        
        # Setup video widget
        placeholder = self.findChild(QWidget, 'videoWidget')
        self.videoWidget = QVideoWidget()
        self.videoWidget.setGeometry(placeholder.geometry())
        self.videoWidget.setParent(placeholder.parentWidget())
        placeholder.hide()
        
        # Setup media player
        self.mediaPlayer = QMediaPlayer(self)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.audioOutput = QAudioOutput(self)
        self.mediaPlayer.setAudioOutput(self.audioOutput)

    def loadMovies(self):
        # Get all movies from database
        movies = get_all_videos()
        if movies:
            self.renderMovieList(movies)
        
    def renderMovieList(self, movie_list: list):
        # Clear previous search results
        for i in reversed(range(self.gridLayout.count())):
            widgetToRemove = self.gridLayout.itemAt(i).widget()
            if widgetToRemove:
                self.gridLayout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
            
        row = 0
        column = 0
        for movie in movie_list:
            itemWidget = MovieItemWidget(
                movie["id"], 
                movie["title"], 
                movie["banner"],  
                movie["video_path"],  
                movie.get("description", "")
            )
            itemWidget.set_user_id(self.user_id)  # Set user_id for the widget
            itemWidget.signal_detail_movie.connect(self.catch_detail_movie)
            itemWidget.signal_play_movie.connect(self.catch_play_movie)
            itemWidget.signal_favorite_changed.connect(self.on_favorite_changed)  # Connect new signal
            self.gridLayout.addWidget(itemWidget, row, column)
            column += 1
            if column == 3:
                row += 1
                column = 0
    
    def search_movie(self):
        name = self.txt_search.text()
        movie_list = get_video_by_name(name)
        self.renderMovieList(movie_list)

    def detail_movie(self, movie_id):
        movie = get_video_by_id(movie_id)
        if not movie:
            return
            
        # Find all the label widgets
        self.lbl_name = self.findChild(QLabel, "lbl_detail_name")
        self.lbl_director = self.findChild(QLabel, "lbl_detail_director")
        self.lbl_release_date = self.findChild(QLabel, "lbl_detail_release_date")
        self.lbl_genre = self.findChild(QLabel, "lbl_detail_genre")
        self.lbl_description = self.findChild(QLabel, "lbl_detail_description")
        self.lbl_rating = self.findChild(QLabel, "lbl_detail_rating")
        self.lbl_duration = self.findChild(QLabel, "lbl_detail_duration")
        self.lbl_age_rating = self.findChild(QLabel, "lbl_detail_age_rating")
        self.lbl_main_actor = self.findChild(QLabel, "lbl_detail_main_actor")
        self.lbl_image = self.findChild(QLabel, "lbl_detail_image")
        
        # Set the text for each label
        self.lbl_name.setText(movie["title"])
        self.lbl_director.setText(f"Director: {movie.get('director', 'N/A')}")
        self.lbl_release_date.setText(f"Release Date: {movie.get('release_date', 'N/A')}")
        self.lbl_genre.setText(f"Genre: {movie.get('genre', 'N/A')}")
        self.lbl_rating.setText(f"Rating: {movie.get('rating', 'N/A')}")
        self.lbl_duration.setText(f"Duration: {movie.get('duration', 'N/A')}")
        self.lbl_age_rating.setText(f"Age Rating: {movie.get('age_rating', 'N/A')}")
        self.lbl_main_actor.setText(f"Main Actor: {movie.get('main_actor', 'N/A')}")
        
        # Set the banner image
        if movie.get('banner'):
            self.lbl_image.setPixmap(QPixmap(movie["banner"]))
        
        # Format and set the description with word wrapping
        description = movie.get("description", "No description available")
        split_description = description.split(" ")
        description = "\n".join([" ".join(split_description[i:i+10]) for i in range(0, len(split_description), 10)])
        self.lbl_description.setText(f"Description: {description}")
        
        # Find and setup favorite button
        self.btn_favorite = self.findChild(QPushButton, "btn_favorite")
        if self.btn_favorite:
            is_fav = is_favorite(self.user_id, movie_id)
            icon = QIcon("img/heart-solid.svg" if is_fav else "img/heart-regular.svg")
            self.btn_favorite.setIcon(icon)
            self.btn_favorite.clicked.connect(lambda: self.toggle_favorite(movie_id))
        
        # Switch to detail page
        self.stackedWidget.setCurrentIndex(1)
        
    def toggle_favorite(self, movie_id):
        is_fav = is_favorite(self.user_id, movie_id)
        if is_fav:
            remove_from_favorites(self.user_id, movie_id)
            self.btn_favorite.setIcon(QIcon("img/heart-regular.svg"))
        else:
            add_to_favorites(self.user_id, movie_id)
            self.btn_favorite.setIcon(QIcon("img/heart-solid.svg"))
        
    def loadVideo(self):
        if self.movie_id is None:
            return
        try:
            movie = get_video_by_id(self.movie_id)
            # Normalize video path
            video_path = normalize_path(movie["video_path"])
            self.mediaPlayer.setSource(QUrl.fromLocalFile(video_path))
            self.mediaPlayer.play()
            self.lbl_title.setText(movie["title"])
            self.durationBar.sliderMoved.connect(self.setPosition)
            self.volumeBar.sliderMoved.connect(self.setVolume)
            self.mediaPlayer.playbackStateChanged.connect(self.mediaStateChanged)
            self.mediaPlayer.positionChanged.connect(self.positionChanged)
            self.mediaPlayer.durationChanged.connect(self.durationChanged)
            self.mediaPlayer.errorOccurred.connect(self.handleError)
            self.stackedWidget.setCurrentIndex(3)
        except Exception as e:
            print(f"Error loading video: {e}")
            self.msg.error_message(f"Could not load video: {str(e)}")
        
    def mediaStateChanged(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.playBtn.setIcon(self.pauseIcon)
        else:
            self.playBtn.setIcon(self.playIcon)

    def positionChanged(self, position):
        self.durationBar.setValue(position)
        current_time = self.formatTime(position)
        total_time = self.formatTime(self.mediaPlayer.duration())
        self.timeLabel.setText(f"{current_time}/{total_time}")
        
    def durationChanged(self):
        self.durationBar.setRange(0, self.mediaPlayer.duration())
    
    def handleError(self):
        self.playBtn.setEnabled(False)
        error_message = self.mediaPlayer.errorString()
        self.playBtn.setText(f"Error: {error_message}")
        print(f"Media Player Error: {error_message}")
        
    def play(self):
        if self.mediaPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()
    
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
        
    def setVolume(self, volume):
        volume = volume / 100.0
        self.audioOutput.setVolume(volume)
        if volume == 0.0:
            self.volumeBtn.setIcon(self.volumeOffIcon)
        elif volume < 0.5:
            self.audioOutput.setMuted(False)
            self.volumeBtn.setIcon(self.volumeLowIcon)
        else:
            self.volumeBtn.setIcon(self.volumeHighIcon)
            self.audioOutput.setMuted(False)
    
    def toggleMute(self):
        if self.audioOutput.isMuted():
            self.audioOutput.setMuted(False)
            if self.current_volume >= 50:
                self.volumeBtn.setIcon(self.volumeHighIcon)
            elif self.current_volume < 50:
                self.volumeBtn.setIcon(self.volumeLowIcon)
            else:
                self.volumeBtn.setIcon(self.volumeOffIcon)
            self.volumeBar.setValue(self.current_volume)
        else:
            self.audioOutput.setMuted(True)
            self.volumeBtn.setIcon(self.volumeOffIcon)
            self.current_volume = self.volumeBar.value()
            self.volumeBar.setValue(0)
    
    def toggleFullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def formatTime(self, milliseconds):
        total_seconds = milliseconds // 1000
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"
    
    def catch_play_movie(self, movie_id):
        self.movie_id = movie_id
        self.loadVideo()

    def catch_detail_movie(self, movie_id):
        self.movie_id = movie_id
        self.detail_movie(self.movie_id)
        self.stackedWidget.setCurrentIndex(1)
                
    def navigateScreen(self, page:int):
        self.stackedWidget.setCurrentIndex(page)

    def showFavorites(self):
        # Get favorite movies
        favorite_movies = get_user_favorites(self.user_id)
        
        # Clear previous items
        for i in reversed(range(self.favoriteLayout.count())):
            widgetToRemove = self.favoriteLayout.itemAt(i).widget()
            if widgetToRemove:
                self.favoriteLayout.removeWidget(widgetToRemove)
                widgetToRemove.setParent(None)
                
        if not favorite_movies:
            # Show empty message
            label = QLabel("You haven't added any titles to your list yet.")
            label.setStyleSheet("color: white; font-family: Geist; font-size: 16px;")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.favoriteLayout.addWidget(label)
        else:
            # Add movies to grid
            row = 0
            column = 0
            for movie in favorite_movies:
                itemWidget = MovieItemWidget(
                    movie["id"], 
                    movie["title"], 
                    movie["banner"],  
                    movie["video_path"],  
                    movie.get("description", "")
                )
                itemWidget.set_user_id(self.user_id)  # Set user_id for the widget
                itemWidget.signal_detail_movie.connect(self.catch_detail_movie)
                itemWidget.signal_play_movie.connect(self.catch_play_movie)
                itemWidget.signal_favorite_changed.connect(self.on_favorite_changed)  # Connect new signal
                self.favoriteLayout.addWidget(itemWidget, row, column)
                column += 1
                if column == 3:
                    row += 1
                    column = 0
        
        # Switch to favorites page
        self.stackedWidget.setCurrentIndex(2)
        
    def on_favorite_changed(self):
        # If we're on the favorites page, refresh it
        if self.stackedWidget.currentIndex() == 2:
            self.showFavorites()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec())