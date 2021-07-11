# CS456-A2 nEmulator

The network emulator requires Python 3. You can use the emulator either by executing the provided nEmulator script or by running `python3 network_emulator.py` directly. 
Find usage instructions using ./nEmulator -h

# Testing

```
ssh -Y hkbulmer@ubuntu2004-002.student.cs.uwaterloo.ca

./nEmulator 50412 ubuntu2004-004 50413 50414 ubuntu2004-008 50415 1 0.2 0

ssh -Y hkbulmer@ubuntu2004-004.student.cs.uwaterloo.ca

./receiver ubuntu2004-002 50414 50413 output

ssh -Y hkbulmer@ubuntu2004-008.student.cs.uwaterloo.ca

./sender ubuntu2004-002 50412 50415 50 input
```