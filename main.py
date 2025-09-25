from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import ListProperty, NumericProperty, StringProperty
from kivy.animation import Animation
from kivy.uix.popup import Popup
import json
import os

# Set window size for testing (will be fullscreen on Android)
Window.size = (360, 640)

# Complete Hiragana characters data
HIRAGANA_CHART = {
    "vowels": [
        {"character": "あ", "romaji": "a", "strokes": 3},
        {"character": "い", "romaji": "i", "strokes": 2},
        {"character": "う", "romaji": "u", "strokes": 2},
        {"character": "え", "romaji": "e", "strokes": 2},
        {"character": "お", "romaji": "o", "strokes": 3}
    ],
    "k-column": [
        {"character": "か", "romaji": "ka", "strokes": 3},
        {"character": "き", "romaji": "ki", "strokes": 4},
        {"character": "く", "romaji": "ku", "strokes": 1},
        {"character": "け", "romaji": "ke", "strokes": 3},
        {"character": "こ", "romaji": "ko", "strokes": 2}
    ],
    "s-column": [
        {"character": "さ", "romaji": "sa", "strokes": 3},
        {"character": "し", "romaji": "shi", "strokes": 1},
        {"character": "す", "romaji": "su", "strokes": 2},
        {"character": "せ", "romaji": "se", "strokes": 3},
        {"character": "そ", "romaji": "so", "strokes": 1}
    ],
    "t-column": [
        {"character": "た", "romaji": "ta", "strokes": 4},
        {"character": "ち", "romaji": "chi", "strokes": 2},
        {"character": "つ", "romaji": "tsu", "strokes": 1},
        {"character": "て", "romaji": "te", "strokes": 1},
        {"character": "と", "romaji": "to", "strokes": 2}
    ],
    "n-column": [
        {"character": "な", "romaji": "na", "strokes": 4},
        {"character": "に", "romaji": "ni", "strokes": 3},
        {"character": "ぬ", "romaji": "nu", "strokes": 2},
        {"character": "ね", "romaji": "ne", "strokes": 2},
        {"character": "の", "romaji": "no", "strokes": 1}
    ],
    "h-column": [
        {"character": "は", "romaji": "ha", "strokes": 3},
        {"character": "ひ", "romaji": "hi", "strokes": 1},
        {"character": "ふ", "romaji": "fu", "strokes": 4},
        {"character": "へ", "romaji": "he", "strokes": 1},
        {"character": "ほ", "romaji": "ho", "strokes": 4}
    ],
    "m-column": [
        {"character": "ま", "romaji": "ma", "strokes": 3},
        {"character": "み", "romaji": "mi", "strokes": 2},
        {"character": "む", "romaji": "mu", "strokes": 3},
        {"character": "め", "romaji": "me", "strokes": 2},
        {"character": "も", "romaji": "mo", "strokes": 3}
    ],
    "y-column": [
        {"character": "や", "romaji": "ya", "strokes": 2},
        {"character": "ゆ", "romaji": "yu", "strokes": 2},
        {"character": "よ", "romaji": "yo", "strokes": 2}
    ],
    "r-column": [
        {"character": "ら", "romaji": "ra", "strokes": 2},
        {"character": "り", "romaji": "ri", "strokes": 2},
        {"character": "る", "romaji": "ru", "strokes": 1},
        {"character": "れ", "romaji": "re", "strokes": 2},
        {"character": "ろ", "romaji": "ro", "strokes": 1}
    ],
    "w-column": [
        {"character": "わ", "romaji": "wa", "strokes": 2},
        {"character": "を", "romaji": "wo", "strokes": 3},
        {"character": "ん", "romaji": "n", "strokes": 1}
    ],
    "g-column": [
        {"character": "が", "romaji": "ga", "strokes": 3},
        {"character": "ぎ", "romaji": "gi", "strokes": 4},
        {"character": "ぐ", "romaji": "gu", "strokes": 1},
        {"character": "げ", "romaji": "ge", "strokes": 3},
        {"character": "ご", "romaji": "go", "strokes": 2}
    ],
    "z-column": [
        {"character": "ざ", "romaji": "za", "strokes": 3},
        {"character": "じ", "romaji": "ji", "strokes": 1},
        {"character": "ず", "romaji": "zu", "strokes": 2},
        {"character": "ぜ", "romaji": "ze", "strokes": 3},
        {"character": "ぞ", "romaji": "zo", "strokes": 1}
    ],
    "d-column": [
        {"character": "だ", "romaji": "da", "strokes": 4},
        {"character": "ぢ", "romaji": "ji", "strokes": 2},
        {"character": "づ", "romaji": "zu", "strokes": 1},
        {"character": "で", "romaji": "de", "strokes": 1},
        {"character": "ど", "romaji": "do", "strokes": 2}
    ],
    "b-column": [
        {"character": "ば", "romaji": "ba", "strokes": 3},
        {"character": "び", "romaji": "bi", "strokes": 1},
        {"character": "ぶ", "romaji": "bu", "strokes": 4},
        {"character": "べ", "romaji": "be", "strokes": 1},
        {"character": "ぼ", "romaji": "bo", "strokes": 4}
    ],
    "p-column": [
        {"character": "ぱ", "romaji": "pa", "strokes": 3},
        {"character": "ぴ", "romaji": "pi", "strokes": 1},
        {"character": "ぷ", "romaji": "pu", "strokes": 4},
        {"character": "ぺ", "romaji": "pe", "strokes": 1},
        {"character": "ぽ", "romaji": "po", "strokes": 4}
    ],
    "k-combinations": [
        {"character": "きゃ", "romaji": "kya", "strokes": 4},
        {"character": "きゅ", "romaji": "kyu", "strokes": 4},
        {"character": "きょ", "romaji": "kyo", "strokes": 4}
    ],
    "s-combinations": [
        {"character": "しゃ", "romaji": "sha", "strokes": 1},
        {"character": "しゅ", "romaji": "shu", "strokes": 1},
        {"character": "しょ", "romaji": "sho", "strokes": 1}
    ],
    "t-combinations": [
        {"character": "ちゃ", "romaji": "cha", "strokes": 2},
        {"character": "ちゅ", "romaji": "chu", "strokes": 2},
        {"character": "ちょ", "romaji": "cho", "strokes": 2}
    ],
    "n-combinations": [
        {"character": "にゃ", "romaji": "nya", "strokes": 3},
        {"character": "にゅ", "romaji": "nyu", "strokes": 3},
        {"character": "にょ", "romaji": "nyo", "strokes": 3}
    ],
    "h-combinations": [
        {"character": "ひゃ", "romaji": "hya", "strokes": 1},
        {"character": "ひゅ", "romaji": "hyu", "strokes": 1},
        {"character": "ひょ", "romaji": "hyo", "strokes": 1}
    ],
    "m-combinations": [
        {"character": "みゃ", "romaji": "mya", "strokes": 2},
        {"character": "みゅ", "romaji": "myu", "strokes": 2},
        {"character": "みょ", "romaji": "myo", "strokes": 2}
    ],
    "r-combinations": [
        {"character": "りゃ", "romaji": "rya", "strokes": 2},
        {"character": "りゅ", "romaji": "ryu", "strokes": 2},
        {"character": "りょ", "romaji": "ryo", "strokes": 2}
    ],
    "g-combinations": [
        {"character": "ぎゃ", "romaji": "gya", "strokes": 4},
        {"character": "ぎゅ", "romaji": "gyu", "strokes": 4},
        {"character": "ぎょ", "romaji": "gyo", "strokes": 4}
    ],
    "z-combinations": [
        {"character": "じゃ", "romaji": "ja", "strokes": 1},
        {"character": "じゅ", "romaji": "ju", "strokes": 1},
        {"character": "じょ", "romaji": "jo", "strokes": 1}
    ],
    "b-combinations": [
        {"character": "びゃ", "romaji": "bya", "strokes": 1},
        {"character": "びゅ", "romaji": "byu", "strokes": 1},
        {"character": "びょ", "romaji": "byo", "strokes": 1}
    ],
    "p-combinations": [
        {"character": "ぴゃ", "romaji": "pya", "strokes": 1},
        {"character": "ぴゅ", "romaji": "pyu", "strokes": 1},
        {"character": "ぴょ", "romaji": "pyo", "strokes": 1}
    ]
}

# User data management
def load_user_data():
    if os.path.exists('user_data.json'):
        with open('user_data.json', 'r') as f:
            return json.load(f)
    return {"users": {}}

def save_user_data(data):
    with open('user_data.json', 'w') as f:
        json.dump(data, f)

# Japanese font setup
JAPANESE_FONT = None
JAPANESE_FONT_OPTIONS = [
    'fonts/NotoSansJP-Regular.ttf',
    'NotoSansCJKjp-Regular',
    'MotoyaLCedar',
    'DroidSansJapanese',
    'MS Gothic',
    'Hiragino Sans',
    'Arial Unicode MS'
]

def get_japanese_font():
    """Try to find a Japanese font that works"""
    for font_option in JAPANESE_FONT_OPTIONS:
        try:
            if font_option.startswith('fonts/') and os.path.exists(font_option):
                return font_option
            Label(font_name=font_option)
            return font_option
        except:
            continue
    return None

JAPANESE_FONT = get_japanese_font()

# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text="Hiragana Practice", font_size=40, size_hint_y=0.3)
        if JAPANESE_FONT:
            title.font_name = JAPANESE_FONT
        layout.add_widget(title)
        
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.4)
        
        self.username = TextInput(hint_text="Username", multiline=False, size_hint_y=None, height=50)
        self.password = TextInput(hint_text="Password", password=True, multiline=False, size_hint_y=None, height=50)
        
        form_layout.add_widget(self.username)
        form_layout.add_widget(self.password)
        layout.add_widget(form_layout)
        
        btn_layout = BoxLayout(spacing=10, size_hint_y=0.2)
        login_btn = Button(text="Login", on_press=self.login)
        register_btn = Button(text="Register", on_press=self.register)
        
        btn_layout.add_widget(login_btn)
        btn_layout.add_widget(register_btn)
        layout.add_widget(btn_layout)
        
        self.add_widget(layout)
    
    def login(self, instance):
        user_data = load_user_data()
        username = self.username.text
        password = self.password.text
        
        if username in user_data["users"] and user_data["users"][username]["password"] == password:
            self.manager.current = 'chart'
            self.manager.get_screen('chart').username = username
        else:
            popup = Popup(title='Error', content=Label(text='Invalid username or password'), size_hint=(0.8, 0.4))
            popup.open()
    
    def register(self, instance):
        user_data = load_user_data()
        username = self.username.text
        password = self.password.text
        
        if username in user_data["users"]:
            popup = Popup(title='Error', content=Label(text='Username already exists'), size_hint=(0.8, 0.4))
            popup.open()
        elif username and password:
            user_data["users"][username] = {"password": password, "progress": {}}
            save_user_data(user_data)
            popup = Popup(title='Success', content=Label(text='Registration successful! Please login.'), size_hint=(0.8, 0.4))
            popup.open()
        else:
            popup = Popup(title='Error', content=Label(text='Please enter username and password'), size_hint=(0.8, 0.4))
            popup.open()

# Hiragana Chart Screen
class HiraganaChartScreen(Screen):
    username = StringProperty("")
    
    def __init__(self, **kwargs):
        super(HiraganaChartScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        title = Label(text="Hiragana Chart", font_size=14, size_hint_y=0.1)
        if JAPANESE_FONT:
            title.font_name = JAPANESE_FONT
        self.layout.add_widget(title)
        
        # Create a scroll view for the chart
        from kivy.uix.scrollview import ScrollView
        scroll_view = ScrollView(size_hint_y=0.9)
        
        self.scroll_layout = GridLayout(cols=6, spacing=5, size_hint_y=None)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        
        # Helper function to create Japanese character buttons
        def create_japanese_button(char_data):
            btn = Button(
                text=char_data["character"], 
                font_size=15, # Slightly smaller font to fit all characters
                size_hint_y=None, 
                height=40
            )
            if JAPANESE_FONT:
                btn.font_name = JAPANESE_FONT
            btn.character_data = char_data
            btn.bind(on_press=self.show_character_detail)
            return btn
        
        # Add all hiragana groups
        groups_order = [
            "vowels", "k-column", "s-column", "t-column", "n-column",
            "h-column", "m-column", "y-column", "r-column", "w-column",
            "g-column", "z-column", "d-column", "b-column", "p-column",
            "k-combinations", "s-combinations", "t-combinations", "n-combinations",
            "h-combinations", "m-combinations", "r-combinations", "g-combinations",
            "z-combinations", "b-combinations", "p-combinations"
        ]
        
        # Add section headers and characters
        for group_name in groups_order:
            if group_name in HIRAGANA_CHART:
                # Add section header
                header_text = group_name.replace("-", " ").title()
                if "combinations" in group_name:
                    header_text = header_text.replace("Combinations", "Combinations (Yōon)")
                
                section_layout = BoxLayout(orientation='vertical', size_hint_y=None)
                section_layout.bind(minimum_height=section_layout.setter('height'))
                
                header = Label(
                    text=header_text, 
                    font_size=15, 
                    size_hint_y=None, 
                    height=40,
                    bold=True
                )
                self.scroll_layout.add_widget(header)
                
                char_grid = GridLayout (cols=6, spacing=5, size_hint_y=None)
                char_grid.bind(minimum_height=char_grid.setter('height'))
                                
                # Add characters for this group
                for char_data in HIRAGANA_CHART[group_name]:
                    char_grid.add_widget(create_japanese_button(char_data))
                
                section_layout.add_widget(char_grid)
                self.scroll_layout.add_widget(section_layout)
        
        scroll_view.add_widget(self.scroll_layout)
        self.layout.add_widget(scroll_view)
        self.add_widget(self.layout)
    
    def show_character_detail(self, instance):
        self.manager.get_screen('detail').character_data = instance.character_data
        self.manager.current = 'detail'

# Drawing Canvas for practice
class DrawingCanvas(Widget):
    line_width = NumericProperty(3)
    line_color = ListProperty([1, 0, 0, 1])
    
    def __init__(self, **kwargs):
        super(DrawingCanvas, self).__init__(**kwargs)
        self.lines = []
        self.current_line = None
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            with self.canvas:
                Color(*self.line_color)
                self.current_line = Line(points=(touch.x, touch.y), width=self.line_width)
            return True
        return super(DrawingCanvas, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        if self.current_line and self.collide_point(*touch.pos):
            self.current_line.points += [touch.x, touch.y]
            return True
        return super(DrawingCanvas, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):
        if self.current_line:
            self.lines.append(self.current_line)
            self.current_line = None
            return True
        return super(DrawingCanvas, self).on_touch_up(touch)
    
    def clear_canvas(self):
        self.canvas.clear()
        self.lines = []

# Character Detail Screen
class CharacterDetailScreen(Screen):
    character_data = None
    
    def __init__(self, **kwargs):
        super(CharacterDetailScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Header with character info
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        back_btn = Button(text="Back", size_hint_x=0.2)
        back_btn.bind(on_press=self.go_back)
        
        self.char_label = Label(text="", font_size=50)
        self.romaji_label = Label(text="", font_size=20)
        
        if JAPANESE_FONT:
            self.char_label.font_name = JAPANESE_FONT
        
        char_info = BoxLayout(orientation='vertical')
        char_info.add_widget(self.char_label)
        char_info.add_widget(self.romaji_label)
        
        header.add_widget(back_btn)
        header.add_widget(char_info)
        header.add_widget(Widget(size_hint_x=0.2)) # Spacer
        
        self.layout.add_widget(header)
        
        # Stroke order demonstration area
        self.stroke_demo = Image(size_hint_y=0.3)
        self.layout.add_widget(self.stroke_demo)
        
        # Practice area
        practice_label = Label(text="Practice Area", size_hint_y=0.1)
        self.layout.add_widget(practice_label)
        
        self.drawing_canvas = DrawingCanvas(size_hint_y=0.4)
        self.layout.add_widget(self.drawing_canvas)
        
        # Controls
        controls = BoxLayout(size_hint_y=0.1)
        clear_btn = Button(text="Clear")
        clear_btn.bind(on_press=self.clear_canvas)
        
        controls.add_widget(clear_btn)
        self.layout.add_widget(controls)
        
        self.add_widget(self.layout)
    
    def on_enter(self):
        if self.character_data:
            self.char_label.text = self.character_data["character"]
            self.romaji_label.text = self.character_data["romaji"]
            # In a real app, you would load the stroke order images here
            # self.stroke_demo.source = f"strokes/{self.character_data['romaji']}.gif"
    
    def go_back(self, instance):
        self.manager.current = 'chart'
    
    def clear_canvas(self, instance):
        self.drawing_canvas.clear_canvas()

# Screen Manager
class HiraganaApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(HiraganaChartScreen(name='chart'))
        sm.add_widget(CharacterDetailScreen(name='detail'))
        return sm

if __name__ == '__main__':
    HiraganaApp().run()