import PyQt5
from PyQt5 import QtWidgets, uic
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget
import arcpy
import os
import sys

class MyWindow(QMainWindow): 
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi("Ui file.ui", self)

        # show app
        self.show()

        self.ENTER.clicked.connect(self.SetDirectory)
        self.pushButton.clicked.connect(self.Extraction)

    # function for accessing the data
    def SetDirectory(self):
        myWorking_Directory = self.plainTextEdit.toPlainText()
        arcpy.env.workspace = (myWorking_Directory)
        Featurelist = arcpy.ListFeatureClasses()
        self.country_comb.addItems(Featurelist)
        self.comboBox_2.addItems(Featurelist)

    # extraction function
    def Extraction(self):
        countries = self.country_comb.currentText()
        shop = self.comboBox_2.currentText()
        Country = self.lineEdit_4.text()
        shopType = self.lineEdit_5.text()
        outpath = self.lineEdit.text()
        shop_layer = arcpy.MakeFeatureLayer_management(shop, 'shops_layer')
        country_layer = arcpy.MakeFeatureLayer_management(countries, 'countries_layer')
        # selection by attribute
        country = arcpy.SelectLayerByAttribute_management(country_layer, 'NEW_SELECTION', "NAME= '" + Country + "'")
        # selection by location
        #  Select Layer By Location
        shops_out = arcpy.SelectLayerByLocation_management(shop_layer, "INTERSECT", country, "", "NEW_SELECTION", "NOT_INVERT")
        # selection by attribute
        myShops = arcpy.SelectLayerByAttribute_management(shop_layer, 'SUBSET_SELECTION', "shop= '" + shopType + "'")
        # Writting selected outputs
        output = arcpy.FeatureClassToFeatureClass_conversion(myShops, outpath, 'shops')

app = QtWidgets.QApplication([])
Welcome = MyWindow()
Welcome.show()
sys.exit(app.exec())
