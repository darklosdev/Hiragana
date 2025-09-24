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

# Hiragana characters data
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

# Login Screen
class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        title = Label(text="Hiragana Practice", font_size=40, size_hint_y=0.3)
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
        
        title = Label(text="Hiragana Chart", font_size=30, size_hint_y=0.1)
        self.layout.add_widget(title)
        
        self.scroll_layout = GridLayout(cols=5, spacing=10, size_hint_y=0.9)
        self.scroll_layout.bind(minimum_height=self.scroll_layout.setter('height'))
        
        # Add vowels
        for char_data in HIRAGANA_CHART["vowels"]:
            btn = Button(text=char_data["character"], font_size=30)
            btn.character_data = char_data
            btn.bind(on_press=self.show_character_detail)
            self.scroll_layout.add_widget(btn)
        
        # Add k-column
        for char_data in HIRAGANA_CHART["k-column"]:
            btn = Button(text=char_data["character"], font_size=30)
            btn.character_data = char_data
            btn.bind(on_press=self.show_character_detail)
            self.scroll_layout.add_widget(btn)
        
        # Add more buttons for other characters as needed
        
        self.layout.add_widget(self.scroll_layout)
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