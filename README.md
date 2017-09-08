# README #

Repo for updated drivers and documentation for CMD recon - a branch of the CMD Robots project of 2012.

https://github.com/wallarug/cmd-robot

The aim of this repository is to create a Python driver for CMD Recon to interface with the [donkey car](https://github.com/wroscoe/donkey) code.  This will provide a second platform for testing.  

This is an extension to the existing scope of the project.

## Pin Out Mapping ##

This project relays on the Pololu Dual VNH5019 Motor Driver Shield.  It will be driven by the Raspberry Pi's GPIO Pins directly.  The Motor Shield comes ready to use on an Arduino, hence it already has Arduino pins mapped to specific inputs.

| Arduino | VNH5019 | BCM GPIO |
|---------|---------|----------|
|  D2     | M1 INA  |     17    |
|  D4     | M1 INB  |     27    |
|  D6     | M1 EN   |     23    |
|  D7     | M2 INA  |     5   |
|  D8     | M2 INB  |     6   |
|  D9     | M1 PWM  |     22   |
|  D10    | M2 PWM  |     13   |
|  D12    | M2 EN   |     24   |
|  A0     | M1 CS   |     nc   |
|  A1     | M2 CS   |     nc   |

