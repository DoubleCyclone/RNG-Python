# RNG-Python
Random number generator with Python Tkinter

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)

## 🎯 Overview
A Python app with a simple GUI to easily and quickly generate random numbers. Close enough to true random and customizable!

## ✨ Features

### Random Number Generation
- Uses Python's secrets package to generate cryptographically strong pseudo-random numbers.
- Range and the amount of numbers generated can be changed easily by using the textboxes.
- The last preset used is saved when exiting the application.

### Hotkeys
- Can use hotkeys like **alt + (any number other than 0)** to roll immediately in the range of **1 - (that number)**.
- Can use **alt + q** to roll one number in the range determined by the textboxes in the GUI or **alt + w** to roll multiple numbers according to the same textboxes.
- Hotkeys work even when the app is unfocused.

### Sound Effects + TTS
- Can enable/disable sound effects on number generation to get feedback.
- Can enable/disable TTS on number generation (works on only single rolls as theoretically you can generate 100 numbers at the same time and probably wouldn't want to hear that play) which can be used to know the outcome without looking at the GUI.

### History Tracking
- Can enable/disable history GUI which shows all the numbers generated, their ranges and the date and time they were generated.
- History information is saved to a .csv file automatically even if the GUI is turned off.

### Customization
- Some GUI elements, sound effects and hotkeys are saved to their own .json files that can be changed to customize the app.
