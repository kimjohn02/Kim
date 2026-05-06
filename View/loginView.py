import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QMessageBox, QSizePolicy
)
from PyQt6.QtGui import QPixmap, QFont, QColor, QPainter, QIcon
from PyQt6.QtCore import Qt, pyqtSignal, QByteArray
from PyQt6.QtSvg import QSvgRenderer
from View.components import FieldLabel


# ── Blue palette for login only ──────────────────────────────────────────────
_BG        = "#EAF3FB"       # light blue background
_CARD_BG   = "#FFFFFF"
_BORDER    = "#B3D4F5"
_PRIMARY   = "#1565C0"       # deep blue
_PRIMARY2  = "#1976D2"       # mid blue  (gradient end)
_SUBTITLE  = "#1976D2"       # teal-blue subtitle
_ICON_CLR  = "#333333"
# ─────────────────────────────────────────────────────────────────────────────


_SVG_PERSON = b"""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='#6B7280' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  <path d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/>
  <circle cx='12' cy='7' r='4'/>
</svg>
"""

_SVG_LOCK = b"""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='#6B7280' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  <rect x='3' y='11' width='18' height='11' rx='2' ry='2'/>
  <path d='M7 11V7a5 5 0 0 1 10 0v4'/>
</svg>
"""

_SVG_EYE = b"""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='#6B7280' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  <path d='M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z'/>
  <circle cx='12' cy='12' r='3'/>
</svg>
"""

_SVG_EYE_OFF = b"""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='#6B7280' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  <path d='M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8
           a18.45 18.45 0 0 1 5.06-5.94'/>
  <path d='M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8
           a18.5 18.5 0 0 1-2.16 3.19'/>
  <line x1='1' y1='1' x2='23' y2='23'/>
</svg>
"""

_SVG_LOGIN = b"""
<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'
     fill='none' stroke='white' stroke-width='2'
     stroke-linecap='round' stroke-linejoin='round'>
  <g transform='translate(0, 1.5)'>
    <path d='M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4'/>
    <polyline points='10 17 15 12 10 7'/>
    <line x1='15' y1='12' x2='3' y2='12'/>
  </g>
</svg>
"""

# Scale factor for HiDPI — render at 3× then scale down for crispness
_ICON_SCALE = 3


def _svg_pixmap(svg_bytes: bytes, display_size: int = 20) -> QPixmap:
    """Render SVG at 3× resolution then scale for sharp, HiDPI-quality icons."""
    render_size = display_size * _ICON_SCALE
    renderer = QSvgRenderer(QByteArray(svg_bytes))
    hi_res = QPixmap(render_size, render_size)
    hi_res.fill(Qt.GlobalColor.transparent)
    painter = QPainter(hi_res)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
    renderer.render(painter)
    painter.end()
    
    hi_res.setDevicePixelRatio(float(_ICON_SCALE))
    return hi_res
# ─────────────────────────────────────────────────────────────────────────────


class _IconInput(QFrame):
    """Input field wrapper with an SVG left icon and optional right widget."""

    def __init__(self, placeholder: str, icon_pixmap: QPixmap,
                 echo_mode=QLineEdit.EchoMode.Normal,
                 right_widget=None):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #EEF2F6;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
            }}
            QFrame:focus-within {{
                border: 1px solid #1565C0;
                background-color: #ffffff;
            }}
        """)
        self.setFixedHeight(42)

        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 10, 0)
        row.setSpacing(8)

        icon_lbl = QLabel()
        icon_lbl.setPixmap(icon_pixmap)
        icon_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_lbl.setStyleSheet("background: transparent; border: none;")
        
        icon_container = QFrame()
        icon_container.setFixedWidth(40)
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.addWidget(icon_lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        icon_container.setStyleSheet("border: none; border-right: 1px solid #D1D5DB; border-radius: 0px;")
        
        row.addWidget(icon_container)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.setEchoMode(echo_mode)
        self.line_edit.setStyleSheet("""
            QLineEdit {
                background: transparent;
                border: none;
                font-family: Poppins;
                font-size: 13px;
                color: #1a1a2e;
            }
        """)
        row.addWidget(self.line_edit)

        if right_widget:
            row.addWidget(right_widget)


class LoginView(QWidget):
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self._password_visible = False
        self.init_ui()

    # ── background colour ────────────────────────────────────────────────────
    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QLinearGradient
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0.0, QColor("#D6EAF8"))
        gradient.setColorAt(1.0, QColor("#EBF5FB"))
        painter.fillRect(self.rect(), gradient)
        painter.end()

    # ── UI ───────────────────────────────────────────────────────────────────
    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ── Card ──────────────────────────────────────────────────────────
        card = QFrame()
        card.setFixedWidth(420)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {_CARD_BG};
                border-radius: 18px;
                border: 1px solid #C9DCF0;
            }}
        """)
        # subtle drop-shadow via a slightly larger coloured frame behind
        shadow = QFrame()
        shadow.setFixedWidth(426)
        shadow.setStyleSheet("""
            QFrame {
                background-color: #B8CEDE;
                border-radius: 20px;
            }
        """)
        shadow_layout = QVBoxLayout(shadow)
        shadow_layout.setContentsMargins(3, 3, 3, 6)
        shadow_layout.addWidget(card)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(40, 36, 40, 40)
        layout.setSpacing(0)

        # ── Logo ──────────────────────────────────────────────────────────
        logo_label = QLabel()
        icon_path = os.path.join(
            os.path.dirname(__file__), "..", "Assets", "logo.png"
        )
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                330, 330,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            scaled.setDevicePixelRatio(3.0)
            logo_label.setPixmap(scaled)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # The swoosh adds weight to the right, so we add a little left padding to visually center the monitor.
        logo_label.setStyleSheet("background: transparent; border: none; padding-left: 16px;")
        layout.addWidget(logo_label)
        layout.addSpacing(15)

        # ── Title ─────────────────────────────────────────────────────────
        title = QLabel("TechServe")
        title.setFont(QFont("Poppins", 16, QFont.Weight.Bold))
        title.setStyleSheet(
            "color: #111827; background: transparent; border: none;"
        )
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(24)

        # ── Username ──────────────────────────────────────────────────────
        lbl_user = FieldLabel("Username")
        lbl_user.setStyleSheet(
            "color: #4B5563; font-family: Poppins; font-size: 13px;"
            "font-weight: normal; background: transparent; border: none;"
        )
        layout.addWidget(lbl_user)
        layout.addSpacing(6)

        self._user_wrapper = _IconInput("Enter username", _svg_pixmap(_SVG_PERSON, 20))
        self.username_input = self._user_wrapper.line_edit
        layout.addWidget(self._user_wrapper)
        layout.addSpacing(14)

        # ── Password ──────────────────────────────────────────────────────
        lbl_pass = FieldLabel("Password")
        lbl_pass.setStyleSheet(
            "color: #4B5563; font-family: Poppins; font-size: 13px;"
            "font-weight: normal; background: transparent; border: none;"
        )
        layout.addWidget(lbl_pass)
        layout.addSpacing(6)

        from PyQt6.QtCore import QSize
        self._eye_btn = QPushButton()
        self._eye_icon     = QIcon(_svg_pixmap(_SVG_EYE, 20))
        self._eye_off_icon = QIcon(_svg_pixmap(_SVG_EYE_OFF, 20))
        self._eye_btn.setIcon(self._eye_icon)
        self._eye_btn.setIconSize(QSize(20, 20))
        self._eye_btn.setFixedSize(30, 30)
        self._eye_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self._eye_btn.setStyleSheet(
            "QPushButton { background: transparent; border: none; }"
        )
        self._eye_btn.clicked.connect(self._toggle_password)

        self._pass_wrapper = _IconInput(
            "Enter password", _svg_pixmap(_SVG_LOCK, 20),
            echo_mode=QLineEdit.EchoMode.Password,
            right_widget=self._eye_btn,
        )
        self.password_input = self._pass_wrapper.line_edit
        self.password_input.returnPressed.connect(self.on_login)
        layout.addWidget(self._pass_wrapper)
        layout.addSpacing(22)

        sign_in_btn = QPushButton("Sign In")
        login_icon = QIcon(_svg_pixmap(_SVG_LOGIN, 20))
        sign_in_btn.setIcon(login_icon)
        from PyQt6.QtCore import QSize
        sign_in_btn.setIconSize(QSize(20, 20))
        sign_in_btn.setFixedHeight(44)
        sign_in_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        sign_in_btn.setFont(QFont("Poppins", 11, QFont.Weight.Bold))
        sign_in_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: #1565C0;
                color: white;
                border: none;
                border-radius: 6px;
                text-align: center;
            }}
            QPushButton:hover {{
                background-color: #1976D2;
            }}
            QPushButton:pressed {{
                background-color: #0D47A1;
            }}
        """)
        sign_in_btn.clicked.connect(self.on_login)
        layout.addWidget(sign_in_btn)

        outer.addWidget(shadow)

    # ── helpers ──────────────────────────────────────────────────────────────
    def _toggle_password(self):
        self._password_visible = not self._password_visible
        if self._password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self._eye_btn.setIcon(self._eye_off_icon)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self._eye_btn.setIcon(self._eye_icon)

    def showEvent(self, event):
        super().showEvent(event)
        if not event.spontaneous():
            self.center_on_screen()

    def center_on_screen(self):
        window = self.window()
        screen = window.screen().availableGeometry()
        window_geometry = window.frameGeometry()
        window_geometry.moveCenter(screen.center())
        window.move(window_geometry.topLeft())

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.login_signal.emit(username, password)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()

    def show_error(self, title, message):
        """Display error message to user"""
        QMessageBox.warning(self, title, message)

    def show_question(self, title, message):
        """Display question dialog and return user's choice"""
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes
