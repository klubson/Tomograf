from PyQt5.QtWidgets import QSlider, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import numpy as np


class SliderBox(QHBoxLayout):

    def __init__(self, name, mini, maxi, step, toSet):
        super().__init__()

        self.text = QLabel()
        self.text.setText(name)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(mini)
        self.slider.setMaximum(maxi)
        self.slider.setValue(toSet)
        self.slider.setTickInterval(step)
        self.slider.setSingleStep(step)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMinimumWidth(200)

        self.value = QLabel()
        self.__setVal()

        self.slider.valueChanged.connect(self.__setVal)

        self.addWidget(self.text)
        self.addWidget(self.value)
        self.addStretch(1)
        self.addWidget(self.slider)
        self.addStretch(1)

    def __setVal(self):  # "__" przed funkcją w klasie robi ją prywatną w pythonie
        self.value.setText(str(self.slider.value()))

    def getVal(self):
        return self.slider.value()
