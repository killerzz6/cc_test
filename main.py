from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.clock import Clock

class CountdownFloatingWindow(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.countdown_time = 60  # 倒计时秒数
        self.timer_event = None
        
    def build(self):
        # 设置窗口大小
        Window.size = (200, 100)
        
        # 创建布局
        layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        
        # 倒计时标签
        self.countdown_label = Label(
            text=str(self.countdown_time),
            font_size='48sp',
            bold=True,
            color=(1, 1, 1, 1)  # 白色字体
        )
        
        # 应用标签
        app_label = Label(
            text='倒计时',
            font_size='12sp',
            size_hint_y=0.3,
            color=(0.8, 0.8, 0.8, 1)
        )
        
        layout.add_widget(self.countdown_label)
        layout.add_widget(app_label)
        
        # 设置背景颜色
        with layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.2, 0.2, 0.2, 0.9)  # 深灰色透明背景
            self.rect = Rectangle(size=layout.size, pos=layout.pos)
            layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # 启动倒计时
        self.start_countdown()
        
        return layout
    
    def _update_rect(self, instance, value):
        """更新背景矩形"""
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def start_countdown(self):
        """启动倒计时"""
        self.timer_event = Clock.schedule_interval(self.update_countdown, 1)
    
    def update_countdown(self, dt):
        """更新倒计时显示"""
        if self.countdown_time > 0:
            self.countdown_time -= 1
            self.countdown_label.text = str(self.countdown_time)
        else:
            # 倒计时完成
            self.countdown_label.text = '完成'
            if self.timer_event:
                self.timer_event.cancel()

if __name__ == '__main__':
    CountdownFloatingWindow().run()
