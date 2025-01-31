#!/usr/bin/env python3
# coding=utf-8
import ipywidgets.widgets as widgets
from IPython.display import display
from DOGZILLALib import DOGZILLA

class DogzillaController:
    def __init__(self):
        self.g_dog = DOGZILLA()
        self.g_ENABLE_CHINESE = False

        self.Name_widgets = {
            'Reset':("Reset", "恢复默认姿态"),
            'Shoulder': ("Shoulder", "肩部"),
            'Thigh': ("Thigh", "大腿"),
            'Calf': ("Calf", "小腿"),
            'Left_front': ("Left_front", "左前腿"),
            'Right_front': ("Right_front", "右前腿"),
            'Right_rear': ("Right_rear", "右后腿"),
            'Left_rear': ("Left_rear", "左后腿"),
            'Load':("Load", "已加载"),
            'Unload':("Unload", "已卸载"),
            'Load_ALL':("Load_ALL", "加载全部舵机"),
            'Unload_ALL':("Unload_ALL", "卸载全部舵机"),
            'Motor_speed':("Motor_speed", "舵机速度")
        }

        # Create buttons and sliders
        self.create_widgets()
        self.setup_callbacks()

        # Create display layout
        self.output = widgets.Output()
        self.layout_widgets()

    def create_widgets(self):
        # Buttons
        self.button_Reset = widgets.Button(description=self.Name_widgets['Reset'][self.g_ENABLE_CHINESE], button_style='info', icon='uncheck')
        self.button_Load_ALL = widgets.Button(description=self.Name_widgets['Load_ALL'][self.g_ENABLE_CHINESE], button_style='info', icon='uncheck')
        self.button_Unload_ALL = widgets.Button(description=self.Name_widgets['Unload_ALL'][self.g_ENABLE_CHINESE], button_style='info', icon='uncheck')
        
        self.button_leg1 = widgets.Button(description=self.Name_widgets['Left_front'][self.g_ENABLE_CHINESE], button_style='success', layout=widgets.Layout(width='100%'), icon='check')
        self.button_leg2 = widgets.Button(description=self.Name_widgets['Right_front'][self.g_ENABLE_CHINESE], button_style='success', layout=widgets.Layout(width='100%'), icon='check')
        self.button_leg3 = widgets.Button(description=self.Name_widgets['Right_rear'][self.g_ENABLE_CHINESE], button_style='success', layout=widgets.Layout(width='100%'), icon='check')
        self.button_leg4 = widgets.Button(description=self.Name_widgets['Left_rear'][self.g_ENABLE_CHINESE], button_style='success', layout=widgets.Layout(width='100%'), icon='check')

        # Sliders
        self.slider_motor_speed = widgets.IntSlider(description=self.Name_widgets['Motor_speed'][self.g_ENABLE_CHINESE]+':', value=50, min=0, max=255, step=5)
        self.sliders = {
            'leg1': [widgets.IntSlider(description=self.Name_widgets['Shoulder'][self.g_ENABLE_CHINESE]+':', value=0, min=-31, max=31, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Thigh'][self.g_ENABLE_CHINESE]+':', value=48, min=-66, max=93, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Calf'][self.g_ENABLE_CHINESE]+':', value=14, min=-73, max=57, step=1)],
            'leg2': [widgets.IntSlider(description=self.Name_widgets['Shoulder'][self.g_ENABLE_CHINESE]+':', value=0, min=-31, max=31, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Thigh'][self.g_ENABLE_CHINESE]+':', value=48, min=-66, max=93, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Calf'][self.g_ENABLE_CHINESE]+':', value=14, min=-73, max=57, step=1)],
            'leg3': [widgets.IntSlider(description=self.Name_widgets['Shoulder'][self.g_ENABLE_CHINESE]+':', value=0, min=-31, max=31, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Thigh'][self.g_ENABLE_CHINESE]+':', value=48, min=-66, max=93, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Calf'][self.g_ENABLE_CHINESE]+':', value=14, min=-73, max=57, step=1)],
            'leg4': [widgets.IntSlider(description=self.Name_widgets['Shoulder'][self.g_ENABLE_CHINESE]+':', value=0, min=-31, max=31, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Thigh'][self.g_ENABLE_CHINESE]+':', value=48, min=-66, max=93, step=1),
                     widgets.IntSlider(description=self.Name_widgets['Calf'][self.g_ENABLE_CHINESE]+':', value=14, min=-73, max=57, step=1)]
        }

    def setup_callbacks(self):
        # Button callbacks
        self.button_Reset.on_click(self.on_button_clicked)
        self.button_Load_ALL.on_click(self.on_button_clicked)
        self.button_Unload_ALL.on_click(self.on_button_clicked)
        self.button_leg1.on_click(self.on_button_clicked)
        self.button_leg2.on_click(self.on_button_clicked)
        self.button_leg3.on_click(self.on_button_clicked)
        self.button_leg4.on_click(self.on_button_clicked)
        
        # Slider callbacks
        for leg, sliders in self.sliders.items():
            widgets.interactive(self.on_slider_leg, a3=sliders[0], a2=sliders[1], a1=sliders[2])
        widgets.interactive(self.on_slider_motor_speed, speed=self.slider_motor_speed)

    def on_button_clicked(self, b):
        with output:
            print("Button clicked:", b.description)
        if b.description == self.Name_widgets['Reset'][self.g_ENABLE_CHINESE]:
            self.g_dog.load_allmotor()
            self.g_dog.reset()
            slider_a11.value = 14
            slider_a12.value = 48
            slider_a13.value = 0
            slider_a21.value = 14
            slider_a22.value = 48
            slider_a23.value = 0
            slider_a31.value = 14
            slider_a32.value = 48
            slider_a33.value = 0
            slider_a41.value = 14
            slider_a42.value = 48
            slider_a43.value = 0
            self.slider_motor_speed.value = 30
            self.button_leg1.icon = 'check'
            self.button_leg1.button_style='success'
            self.button_leg2.icon = 'check'
            self.button_leg2.button_style='success'
            self.button_leg3.icon = 'check'
            self.button_leg3.button_style='success'
            self.button_leg4.icon = 'check'
            self.button_leg4.button_style='success'
        
        elif b.description == self.Name_widgets['Load_ALL'][self.g_ENABLE_CHINESE]:
            self.g_dog.load_allmotor()
            self.button_leg1.icon = 'check'
            self.button_leg1.button_style='success'
            self.button_leg2.icon = 'check'
            self.button_leg2.button_style='success'
            self.button_leg3.icon = 'check'
            self.button_leg3.button_style='success'
            self.button_leg4.icon = 'check'
            self.button_leg4.button_style='success'
        elif b.description == self.Name_widgets['Unload_ALL'][self.g_ENABLE_CHINESE]:
            self.g_dog.unload_allmotor()
            self.button_leg1.icon = 'uncheck'
            self.button_leg1.button_style=''
            self.button_leg2.icon = 'uncheck'
            self.button_leg2.button_style=''
            self.button_leg3.icon = 'uncheck'
            self.button_leg3.button_style=''
            self.button_leg4.icon = 'uncheck'
            self.button_leg4.button_style=''
            
        elif b.description == self.Name_widgets['Left_front'][self.g_ENABLE_CHINESE]:
            if b.icon == 'check':
                b.icon = 'uncheck'
                b.button_style=''
                self.g_dog.unload_motor(1)
                with output:
                    print(self.Name_widgets['Unload'][self.g_ENABLE_CHINESE] + ":", b.description)
            else:
                b.icon = 'check'
                b.button_style='success'
                self.g_dog.load_motor(1)
                with output:
                    print(self.Name_widgets['Load'][self.g_ENABLE_CHINESE] + ":", b.description)
        elif b.description == self.Name_widgets['Right_front'][self.g_ENABLE_CHINESE]:
            if b.icon == 'check':
                b.icon = 'uncheck'
                b.button_style=''
                self.g_dog.unload_motor(2)
                with output:
                    print(self.Name_widgets['Unload'][self.g_ENABLE_CHINESE] + ":", b.description)
            else:
                b.icon = 'check'
                b.button_style='success'
                self.g_dog.load_motor(2)
                with output:
                    print(self.Name_widgets['Load'][self.g_ENABLE_CHINESE] + ":", b.description)
        elif b.description == self.Name_widgets['Right_rear'][self.g_ENABLE_CHINESE]:
            if b.icon == 'check':
                b.icon = 'uncheck'
                b.button_style=''
                self.g_dog.unload_motor(3)
                with output:
                    print(self.Name_widgets['Unload'][self.g_ENABLE_CHINESE] + ":", b.description)
            else:
                b.icon = 'check'
                b.button_style='success'
                self.g_dog.load_motor(3)    
                with output:
                    print(self.Name_widgets['Load'][self.g_ENABLE_CHINESE] + ":", b.description)
        elif b.description == self.Name_widgets['Left_rear'][self.g_ENABLE_CHINESE]:
            if b.icon == 'check':
                b.icon = 'uncheck'
                b.button_style=''
                self.g_dog.unload_motor(4)
                with output:
                    print(self.Name_widgets['Unload'][self.g_ENABLE_CHINESE] + ":", b.description)
            else:
                b.icon = 'check'
                b.button_style='success'
                self.g_dog.load_motor(4)  
                with output:
                    print(self.Name_widgets['Load'][self.g_ENABLE_CHINESE] + ":", b.description)


    def on_slider_leg(self, a3, a2, a1):
        # Implement slider event handling for each leg here
        pass


    def on_slider_leg1(self, a3, a2, a1):
        print("ID 11~13:" , (a3, a2, a1))
        # button_leg1.icon = 'check'
        # button_leg1.button_style='success'
        motor_id = [11, 12, 13]
        angle_id = [a1, a2, a3]
        self.g_dog.motor(motor_id, angle_id)
    
    def on_slider_leg2(self, a3, a2, a1):
        print("ID 21~23:" , (a3, a2, a1))
        # button_leg2.icon = 'check'
        # button_leg2.button_style='success'
        motor_id = [21, 22, 23]
        angle_id = [a1, a2, a3]
        self.g_dog.motor(motor_id, angle_id)
        
    def on_slider_leg3(self, a3, a2, a1):
        print("ID 31~33:" , (a3, a2, a1))
        # button_leg3.icon = 'check'
        # button_leg3.button_style='success'
        motor_id = [31, 32, 33]
        angle_id = [a1, a2, a3]
        self.g_dog.motor(motor_id, angle_id)
        
    def on_slider_leg4(self, a3, a2, a1):
        print("ID 41~43:" , (a3, a2, a1))
        # button_leg4.icon = 'check'
        # button_leg4.button_style='success'
        motor_id = [41, 42, 43]
        angle_id = [a1, a2, a3]
        self.g_dog.motor(motor_id, angle_id)


    def on_slider_motor_speed(self, speed):
        # Implement motor speed slider handling
        print("   motor_speed:", speed)
        self.g_dog.motor_speed(speed)
        pass

    def layout_widgets(self):
        # Arrange and display widgets
        box_leg1 = widgets.VBox([self.button_leg1, widgets.VBox(self.sliders['leg1'])])
        box_leg2 = widgets.VBox([self.button_leg2, widgets.VBox(self.sliders['leg2'])])
        box_leg3 = widgets.VBox([self.button_leg3, widgets.VBox(self.sliders['leg3'])])
        box_leg4 = widgets.VBox([self.button_leg4, widgets.VBox(self.sliders['leg4'])])
        box_h1 = widgets.HBox([box_leg1, box_leg2])
        box_h2 = widgets.HBox([box_leg4, box_leg3])
        box_h = widgets.HBox([self.button_Reset, self.button_Load_ALL, self.button_Unload_ALL])
        
        box_display = widgets.VBox([box_h, self.slider_motor_speed, box_h1, box_h2, self.output])
        display(box_display)

# Initialize and display the Dogzilla Controller
controller = DogzillaController()

