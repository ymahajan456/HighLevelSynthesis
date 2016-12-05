#!/bin/bash

echo "ROOT Access needed. Please enter your password when prompted!"
echo "Checking and Installing Python3"
sudo apt-get install python3
echo "Checking and Installing Pip3"
sudo apt-get install python3-pip
echo "Upgrading pip"
sudo -H pip3 install --upgrade pip
echo "Checking and Installing PYQT5"
sudo -H pip3 install pyqt5
sudo -H pip3 install --upgrade pyqt5
echo "Checking and Installing GRAPHVIZ"
sudo apt-get install graphviz
sudo -H pip3 install graphviz
sudo -H pip3 install --upgrade graphviz
echo "Checking and Installing PYDOT"
sudo -H pip3 install pydot
sudo -H pip3 install --upgrade pydot
