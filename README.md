
# ARCSim
This is AVR Random Instruction generator and Simulator (ARCSim). A handy tool to generate completely random and executable codes for AVR micro-controllers. The main purpose of this tool is too generate dataset to train a deep learning model for profiling side-channel attacks. I have designed it during my master thesis to gather my own dataset.

# Main Features
- Supports all instructions from [AVR instruction set](http://atmel-studio-doc.s3-website-us-east-1.amazonaws.com/webhelp/GUID-0B644D8F-67E7-49E6-82C9-1B2B9ABE6A0D-en-US-1/index.html?GUID-7383E2A4-AFC3-4ED1-B462-589CC8453073)
- Simulation and labeling using a customized version of [simavr](https://github.com/buserror/simavr)
- Two different types of code generation including one-cycle instructions and multi-cycle instructions
- Easily extendable for multiple AVR cores just by defining the desired core's instruction set in Cores.py"file

# Running the Software
The software is written using [PyQt5](https://pypi.org/project/PyQt5/). Thus, you first need to install it on your system. I have tested the software on Ubuntu 20 and using anaconda environment, which I strongly recommend. After cloning the repository, you can lunch the software by running Main.py file.

# Contact Information
Feel free to use the this tool our manipulate it. For more information and feedback you can mail me to pouyanarimani.kh@gmail.com. I appreciate your kind suggestions.
