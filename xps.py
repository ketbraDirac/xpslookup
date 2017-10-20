# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 15:06:43 2017

@author: kgord
"""

import numpy as np
import sys
from qtpy import QtWidgets, QtGui, QtCore


def print_lines(e_cen, e_width):
    if e_cen < 0:
        return "E Center is negative!"
    with open('xps_data.csv') as xps_table:
        header = xps_table.readline()
        header = header.strip().split(',')
        orbitals = header[3:]
        elements = []
        for line in xps_table:
            line = line.strip().split(',')
            elements.append(line[0:3])
    energies = np.genfromtxt('xps_data.csv', delimiter=',', skip_header=1, usecols=range(3, 27))
    energies[np.isnan(energies)] = -np.inf
    condition = np.abs(energies - e_cen) < e_width  # type: np.ndarray
    output = "Name\tOrbital\tEnergy\n"
    for match in np.argwhere(condition):
        elem = match[0]
        orb = match[1]
        output = output + str(elements[int(elem)][2]) + \
            "\t" + str(orbitals[int(orb)]) + \
            "\t" + str(energies[int(elem), int(orb)]) + \
            "\n"
    return output


class QtXPS(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.e_cen_txt = QtWidgets.QLineEdit()
        self.e_cen_txt.setValidator(QtGui.QDoubleValidator())
        self.e_width_txt = QtWidgets.QLineEdit()
        self.e_width_txt.setValidator(QtGui.QDoubleValidator())
        self.output = QtWidgets.QPlainTextEdit()
        self.output.setReadOnly(True)
        self.output.setFocusPolicy(QtCore.Qt.NoFocus)
        self.init_ui()

    def run_calc(self):
        if self.e_cen_txt.hasAcceptableInput() and self.e_width_txt.hasAcceptableInput():
            e_cen = float(self.e_cen_txt.text())
            e_width = float(self.e_width_txt.text())
            self.output.setPlainText(print_lines(e_cen, e_width))
        else:
            self.output.setPlainText("")

    def init_ui(self):
        go_button = QtWidgets.QPushButton("Calculate")
        return_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Return), self)
        enter_shortcut = QtWidgets.QShortcut(QtCore.Qt.Key_Enter, self)
        return_shortcut.activated.connect(self.run_calc)
        enter_shortcut.activated.connect(self.run_calc)
        go_button.clicked.connect(self.run_calc)
        e_cen_label = QtWidgets.QLabel("E Center (eV)")
        e_width_label = QtWidgets.QLabel("E Width (eV)")

        grid = QtWidgets.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(e_cen_label, 0, 0)
        grid.addWidget(self.e_cen_txt, 0, 1)
        grid.addWidget(e_width_label, 1, 0)
        grid.addWidget(self.e_width_txt, 1, 1)
        grid.addWidget(go_button, 2, 1)
        grid.addWidget(self.output, 3, 0, 1, 2)

        self.setLayout(grid)

        self.setWindowTitle("XPS")


# The Qt application execution begins here
app = None


def main():
    global app
    app = QtWidgets.QApplication(sys.argv)
    qt_xps = QtXPS()
    qt_xps.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
