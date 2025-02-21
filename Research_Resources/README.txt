Quanser Research Studios:
===================================================================
src	 	         : Source folder for files used by Quanser Research Studios.
- SDCS   	      : Consists of the skills activities and user guides for the Self-Driving Car Studio.
- user_manuals    : Consists of .docx/.pdf files of user manuals for different solutions provided by Quanser.
- examples	      : Consists of software examples in either Simulink/Python/ROS for different solutions provided by Quanser.
- libraries	      : Source location for custom Python/Simulink libraries.
- setup           : Setup for different studio products. Currently setup for autonomous vehicles research studio and self driving car studio.
- concept_reviews : Consists of .docx/.pdf files for background concepts utilizes in Quanser Curriculum.
===================================================================

Getting Started:
----------------
NOTE: The setup process requires Python. If a compatible Python version is not
already installed, the user will be prompted to install it from the provided
installer (in which case please ensure to check the 'Add python.exe to PATH'
option). The setup process will also attempt to connect to the internet to
check for and download compatible python libraries needed to run the supplied
Python examples. When using a Quanser supplied Studio PC, please connect an
ethernet cable to the network interface port in the back of the PC to access
internet connection during the installation.
WARNING: DO NOT CONNECT THE INTERNET CABLE DIRECTLY TO THE PROVIDED ROUTER.
THIS MAY CAUSE UNEXPECTED BEHAVIOR DUE TO AUTOMATIC ROUTER FIRMWARE UPDATES.

If an internet connection is not available, the setup process will proceed to
finish offline. Python examples might not function properly due to potentially
missing or incompatible libraries. Please contact Quanser customer success team
(tech@quanser.com) regarding any questions or concerns with the setup process.

1. On your local machine run setup.bat which has been designed to:
   - Copy the content of src\ onto the local machine under the C:\Users\<USER>\Documents\Quanser folder
   - Define the PYTHONPATH variable on your system which points to custom
      Quanser python libraries within the src\libraries\python folder
   - Install the python3 dependencies required for users using python.
2. Based on the equipment purchased:
   - Review the user_manuals to get started with the specific products
   - Review the setup folder to see the setup guides for our studio products
   - See the examples folder to get started with product/solution specific examples
   - Review SDCS folder to get started with setting up SDCS and for student skills activities


Change Log:
===========

Quanser Research Studios v1.3.0 (2023-10-18):
---------------------------------------------
- Modifications to SDCS skills activities documentation
- Mofidied workflow for skills activities in QLabs for graceful stop when complete
- Updated traffic light user manual


Quanser Research Studios v1.2.0 (2023-09-12):
---------------------------------------------
- Included resources for the QBot Platform Alpha including:
   - IO examples
   - pal libraries
   - user manuals


Quanser Research Studios v1.1.0 (2023-08-17):
--------------------------------------------
- Included resources for the autonomous vehicles research studio


Quanser Research Studios v1.0.0 (2023-06-9):
--------------------------------------------
- Inclusion of environment interpretation skills activity for SDCS
- Inclusion of API documentation (in 'documentation' directory)
- Updated hardware examples for QCar
- Inclusion of support for Qube3


Quanser Research Studios v0.7.3 (2023-04-20):
---------------------------------------------
- Inclusion of state estimation and vehicle control skills activity for SDCS
- Documentation updates for qcar under src\user_manuals\qcar and src\examples\self_driving_car_studio\qcar\applications


Quanser Research Studios v0.5.3 (2023-03-10):
---------------------------------------------
- Updates to libraries/python/pal/utilities/scope class in hal due to version mismatch
- Updates to sensor interfacing skills activity
