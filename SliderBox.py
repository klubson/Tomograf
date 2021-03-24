from PyQt5.QtWidgets import QSlider, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt


class SliderBox(QHBoxLayout):

    def __init__(self, name, mini, maxi, step, default=180):
        super().__init__()

        self.text = QLabel()
        self.text.setText(name)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        self.slider.setValue(default)
        self.slider.setTickInterval(step)
        self.slider.setSingleStep(step)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimumWidth(200)

        self.value = QLabel()
        self.setVal()

        self.slider.valueChanged.connect(self.setVal)

        self.addWidget(self.text)
        self.addWidget(self.value)
        self.addStretch(1)
        self.addWidget(self.slider)
        self.addStretch(1)

    def setVal(self):
        self.value.setText(str(self.slider.value()))

    def getVal(self):
        return self.value
