import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTabWidget, QFrame
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QFont, QPixmap, QIcon
from View.colors import *
from View.Tabs.Overview.overviewTab import OverviewTab
from View.Tabs.Transaction.transactionsTab import TransactionsTab
from View.Tabs.userManagementTab import UserManagementTab
from View.Tabs.productManagementTab import ProductManagementTab
from Controller.overview_controller import OverviewController

class AdminTabbedView(QWidget):
    logout_signal = pyqtSignal()

    add_user_signal = pyqtSignal(str, str, str)
    delete_user_signal = pyqtSignal(str)
    reactivate_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    add_product_signal = pyqtSignal(str, float, int)
    delete_product_signal = pyqtSignal(str)
    search_products_signal = pyqtSignal(str)

    search_transactions_signal = pyqtSignal(str)
    filter_by_month_signal = pyqtSignal(int, int)

    def __init__(self, data_model):
        super().__init__()
        self.data_model = data_model

        self.overview_controller = OverviewController(data_model)

        self.init_ui()
        self._connect_tab_signals()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(285)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-right: 1px solid #E8F4F5;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(18, 18, 18, 18)
        sidebar_layout.setSpacing(12)

        logo_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "logo.png")
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            scaled_pixmap.setDevicePixelRatio(3.0)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)
        
        sidebar_layout.addSpacing(8)

        title = QLabel("Techserve")
        title.setFont(QFont("Poppins", 17, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PRIMARY};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(title)

        nav_button_style = f"""
            QPushButton {{
                background: transparent;
                color: #4B5563;
                padding: 12px 14px 12px 14px;
                border-radius: 8px;
                font-family: Poppins;
                font-size: 11pt;
                font-weight: 500;
                text-align: left;
                border: none;
            }}
            QPushButton:hover:!checked {{
                background-color: #F3F4F6;
                color: #111827;
            }}
            QPushButton:checked {{
                background-color: {PRIMARY};
                color: white;
                font-weight: bold;
            }}
        """

        self.nav_buttons = []
        nav_icon_size = QSize(24, 24)
        nav_items = [
            ("Dashboard", 0, "dashboardHomeBlue.svg", "dashboardHomeWhite.svg"),
            ("Transactions", 1, "transactionLogo.svg", "transactionLogoWhite.svg"),
            ("User Management", 2, "userLogo.svg", "userLogoWhite.svg"),
            ("Product Management", 3, "productLogo.svg", "productLogoWhite.svg"),
        ]

        for label, index, icon_name, active_icon_name in nav_items:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)
            icon_path = os.path.join(os.path.dirname(__file__), "..", "Assets", icon_name)
            active_icon_path = os.path.join(os.path.dirname(__file__), "..", "Assets", active_icon_name)
            btn.setProperty("icon_normal", icon_path)
            btn.setProperty("icon_active", active_icon_path)
            if os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))
                btn.setIconSize(nav_icon_size)
            btn.setStyleSheet(nav_button_style)
            btn.clicked.connect(lambda checked, i=index: self.tab_widget.setCurrentIndex(i))
            sidebar_layout.addWidget(btn)
            self.nav_buttons.append(btn)

        sidebar_layout.addStretch()

        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        logout_icon_path = os.path.join(os.path.dirname(__file__), "..", "Assets", "logoutRed.svg")
        if os.path.exists(logout_icon_path):
            logout_btn.setIcon(QIcon(logout_icon_path))
            logout_btn.setIconSize(QSize(LOGOUT_ICON_WIDTH, LOGOUT_ICON_HEIGHT))
        logout_btn.setFixedWidth(LOGOUT_BUTTON_WIDTH)
        logout_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {LOGOUT};
                padding: 6px {LOGOUT_BUTTON_PADDING_X}px;
                border-radius: 6px;
                font-family: Poppins;
                font-size: 13pt;
                font-weight: bold;
                text-align: center;
                border: none;
            }}
            QPushButton:hover {{ background-color: {LOGOUT_HOVER}; }}
            QPushButton:pressed {{ background-color: {LOGOUT_ACTIVE}; }}
        """)
        logout_btn.clicked.connect(self.logout_signal.emit)
        sidebar_layout.addWidget(logout_btn, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addWidget(sidebar)

        # Content
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(16, 16, 16, 16)
        content_layout.setSpacing(0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {BACKGROUND};
            }}
            QTabBar::tab {{
                background-color: #E0E0E0;
                color: #666666;
                padding: 12px 30px;
                margin-right: 2px;
                font-family: Poppins;
                font-size: 13px;
                font-weight: bold;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
            QTabBar::tab:selected {{
                background-color: {PRIMARY};
                color: white;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: #BDBDBD;
                color: #333333;
            }}
        """)

        self.overview_tab = OverviewTab(self.overview_controller)
        self.transactions_tab = TransactionsTab()
        self.user_mgmt_tab = UserManagementTab()
        self.product_mgmt_tab = ProductManagementTab()

        self.tab_widget.addTab(self.overview_tab, "Overview")
        self.tab_widget.addTab(self.transactions_tab, "Transactions")
        self.tab_widget.addTab(self.user_mgmt_tab, "User Management")
        self.tab_widget.addTab(self.product_mgmt_tab, "Product Management")

        self.tab_widget.tabBar().hide()
        content_layout.addWidget(self.tab_widget)

        main_layout.addWidget(content_widget, 1)

        if self.nav_buttons:
            self.nav_buttons[0].setChecked(True)
        self.tab_widget.currentChanged.connect(self._set_active_nav)
        self._set_active_nav(self.tab_widget.currentIndex())

    def _set_active_nav(self, index):
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == index)
            icon_path = btn.property("icon_active") if i == index else btn.property("icon_normal")
            if icon_path and os.path.exists(icon_path):
                btn.setIcon(QIcon(icon_path))

    def _connect_tab_signals(self):
        self.user_mgmt_tab.add_user_signal.connect(self.add_user_signal.emit)
        self.user_mgmt_tab.delete_user_signal.connect(self.delete_user_signal.emit)
        self.user_mgmt_tab.reactivate_user_signal.connect(self.reactivate_user_signal.emit)
        self.user_mgmt_tab.search_users_signal.connect(self.search_users_signal.emit)

        self.product_mgmt_tab.add_product_signal.connect(self.add_product_signal.emit)
        self.product_mgmt_tab.delete_product_signal.connect(self.delete_product_signal.emit)
        self.product_mgmt_tab.search_products_signal.connect(self.search_products_signal.emit)

        self.transactions_tab.search_transactions_signal.connect(self.search_transactions_signal.emit)
        self.transactions_tab.filter_by_month_signal.connect(self.filter_by_month_signal.emit)

        # ── Wire Overview → Transactions navigation ──────────────────
        self.overview_tab.navigate_to_transactions.connect(
            lambda: self.tab_widget.setCurrentIndex(1)
        )
        self.overview_tab.navigate_to_products.connect(
            lambda: self.tab_widget.setCurrentIndex(3)
        )

    def update_overview(self):
        self.overview_tab.update_overview()

    def update_users_table(self, users, current_username=None):
        self.user_mgmt_tab.update_users_table(users, current_username)

    def update_products_table(self, products):
        self.product_mgmt_tab.update_products_table(products)

    def update_transactions_table(self, transactions):
        self.transactions_tab.month_selector.set_available_years(self.data_model.transactions)
        self.transactions_tab.update_transactions_table(transactions)