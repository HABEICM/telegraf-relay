"""
Telegraf Styles - Glassmorphism Theme
Premium styling and animations
"""

# Color palette
COLORS = {
    'primary': 'rgba(100, 150, 255, 200)',
    'secondary': 'rgba(150, 100, 255, 200)',
    'success': 'rgba(100, 200, 100, 200)',
    'danger': 'rgba(255, 100, 100, 200)',
    'warning': 'rgba(255, 180, 100, 200)',
    'info': 'rgba(100, 200, 255, 200)',

    'glass_light': 'rgba(255, 255, 255, 30)',
    'glass_medium': 'rgba(255, 255, 255, 50)',
    'glass_dark': 'rgba(30, 40, 60, 200)',

    'border_light': 'rgba(255, 255, 255, 50)',
    'border_medium': 'rgba(255, 255, 255, 100)',

    'text_primary': 'rgba(255, 255, 255, 255)',
    'text_secondary': 'rgba(255, 255, 255, 180)',
    'text_muted': 'rgba(255, 255, 255, 120)',
}

# Gradients
GRADIENTS = {
    'primary': """
        qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(100, 150, 255, 200),
            stop:1 rgba(150, 100, 255, 200))
    """,

    'success': """
        qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(100, 200, 100, 200),
            stop:1 rgba(100, 255, 150, 200))
    """,

    'background': """
        qlineargradient(x1:0, y1:0, x2:1, y2:1,
            stop:0 rgba(20, 30, 50, 250),
            stop:1 rgba(40, 20, 60, 250))
    """,

    'header': """
        qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 rgba(100, 150, 255, 180),
            stop:1 rgba(150, 100, 255, 180))
    """,
}

# Global stylesheet
GLOBAL_STYLE = """
QWidget {
    font-family: 'Segoe UI', 'San Francisco', 'Helvetica Neue', Arial, sans-serif;
}

QToolTip {
    background: rgba(30, 40, 60, 230);
    border: 1px solid rgba(255, 255, 255, 80);
    border-radius: 8px;
    padding: 8px;
    color: white;
    font-size: 12px;
}

QScrollBar:vertical {
    background: rgba(255, 255, 255, 20);
    width: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:vertical {
    background: rgba(100, 150, 255, 150);
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: rgba(120, 170, 255, 180);
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0px;
}

QScrollBar:horizontal {
    background: rgba(255, 255, 255, 20);
    height: 10px;
    border-radius: 5px;
    margin: 2px;
}

QScrollBar::handle:horizontal {
    background: rgba(100, 150, 255, 150);
    border-radius: 5px;
    min-width: 30px;
}

QScrollBar::handle:horizontal:hover {
    background: rgba(120, 170, 255, 180);
}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {
    width: 0px;
}

QMenu {
    background: rgba(30, 40, 60, 230);
    border: 1px solid rgba(255, 255, 255, 80);
    border-radius: 10px;
    padding: 5px;
}

QMenu::item {
    background: transparent;
    color: white;
    padding: 8px 20px;
    border-radius: 5px;
}

QMenu::item:selected {
    background: rgba(100, 150, 255, 150);
}

QMenu::separator {
    height: 1px;
    background: rgba(255, 255, 255, 30);
    margin: 5px 10px;
}
"""

# Animation durations (ms)
ANIMATION_DURATION = {
    'fast': 150,
    'normal': 300,
    'slow': 500,
}

# Easing curves
EASING = {
    'ease_in': 'InCubic',
    'ease_out': 'OutCubic',
    'ease_in_out': 'InOutCubic',
    'bounce': 'OutBounce',
    'elastic': 'OutElastic',
}

# Border radius
RADIUS = {
    'small': 8,
    'medium': 12,
    'large': 18,
    'xlarge': 25,
    'round': 50,
}

# Spacing
SPACING = {
    'xs': 5,
    'sm': 10,
    'md': 15,
    'lg': 20,
    'xl': 30,
}

# Shadows
SHADOWS = {
    'small': '0 2px 8px rgba(0, 0, 0, 0.1)',
    'medium': '0 4px 16px rgba(0, 0, 0, 0.15)',
    'large': '0 8px 32px rgba(0, 0, 0, 0.2)',
    'glow': '0 0 20px rgba(100, 150, 255, 0.5)',
}

# Typography
TYPOGRAPHY = {
    'h1': {'size': 32, 'weight': 'bold'},
    'h2': {'size': 24, 'weight': 'bold'},
    'h3': {'size': 20, 'weight': '600'},
    'h4': {'size': 18, 'weight': '600'},
    'body': {'size': 14, 'weight': 'normal'},
    'small': {'size': 12, 'weight': 'normal'},
    'tiny': {'size': 10, 'weight': 'normal'},
}

def get_button_style(variant='primary'):
    """Get button style by variant"""
    styles = {
        'primary': f"""
            QPushButton {{
                background: {GRADIENTS['primary']};
                border: 1px solid {COLORS['border_medium']};
                border-radius: {RADIUS['large']}px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(120, 170, 255, 220),
                    stop:1 rgba(170, 120, 255, 220));
                border: 1px solid rgba(255, 255, 255, 150);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(80, 130, 235, 200),
                    stop:1 rgba(130, 80, 235, 200));
            }}
        """,

        'secondary': f"""
            QPushButton {{
                background: {COLORS['glass_medium']};
                border: 1px solid {COLORS['border_medium']};
                border-radius: {RADIUS['large']}px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: {COLORS['glass_light']};
            }}
        """,

        'success': f"""
            QPushButton {{
                background: {GRADIENTS['success']};
                border: 1px solid {COLORS['border_medium']};
                border-radius: {RADIUS['large']}px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                font-weight: 600;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(120, 220, 120, 230),
                    stop:1 rgba(120, 255, 170, 230));
            }}
        """,
    }

    return styles.get(variant, styles['primary'])

def get_input_style():
    """Get input field style"""
    return f"""
        QLineEdit {{
            background: {COLORS['glass_light']};
            border: 1px solid {COLORS['border_light']};
            border-radius: {RADIUS['large']}px;
            padding: 12px 20px;
            color: {COLORS['text_primary']};
            font-size: 14px;
            selection-background-color: {COLORS['primary']};
        }}
        QLineEdit:focus {{
            background: {COLORS['glass_medium']};
            border: 2px solid {COLORS['primary']};
        }}
        QLineEdit::placeholder {{
            color: {COLORS['text_muted']};
        }}
    """

def get_panel_style():
    """Get glass panel style"""
    return f"""
        QFrame {{
            background: {COLORS['glass_dark']};
            border: 1px solid {COLORS['border_light']};
            border-radius: {RADIUS['medium']}px;
        }}
    """

def get_message_bubble_style(is_own=False):
    """Get message bubble style"""
    if is_own:
        return f"""
            QLabel {{
                background: {GRADIENTS['primary']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['medium']}px;
                padding: 12px 16px;
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
        """
    else:
        return f"""
            QLabel {{
                background: {COLORS['glass_dark']};
                border: 1px solid {COLORS['border_light']};
                border-radius: {RADIUS['medium']}px;
                padding: 12px 16px;
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
        """
