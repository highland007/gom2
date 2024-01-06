# scene/settings.py
# Defines the Settings class for storing various settings, including colors

class Settings:
    def __init__(self):
        # Default colors
        self.background_color = 'black'
        self.element_color = 'light gray'
        self.ray_color = 'your_ray_color'  # Replace with your desired color
        self.assembly_color = 'your_assembly_color'  # Replace with your desired color
        self.label_color = 'your_label_color'  # Replace with your desired color

    def set_colors(self, background, element, ray, assembly, label):
        # Set colors based on user preferences
        self.background_color = background
        self.element_color = element
        self.ray_color = ray
        self.assembly_color = assembly
        self.label_color = label
