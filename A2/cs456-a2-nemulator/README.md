# CS456-A2 nEmulator

Author: Hannah Bulmer

Student ID: 20714790

## Instructions

My entire program is written in Python3, which should be installed on the commandline in order to run it. No makefile or compiling is required to run. Files can be run through provided bash scripts.

To run (assuming you are in the correct directory):

Set file permissions
```
chmod u+x receiver
chmod u+x sender
```

Open 3 different hosts.

Start the network emulator on host1. Run `./nEmulator -h` to see usage instructions.

Example:
```
./nEmulator 9991 host2 9994 9993 host3 9992 1 0.2 0
```

Start the receiver on host2. Run `./receiver -h` to see usage instructions.

Example:

```
./receiver host1 9993 9994 <output file>
```

Start the sender on host3. Run `./sender -h` to see usage instructions.

Example:

```
./sender host1 9991 9992 50 <input file>
```


## Testing / Examples

I tested my code using `ubuntu2004-002` for the nEmulator, `ubuntu2004-004` for the receiver, and `ubuntu2004-008` for the sender. Below is a list of steps I took to run the applications:

First start the nEmulator on `ubuntu2004-002`
```
ssh -Y hkbulmer@ubuntu2004-002.student.cs.uwaterloo.ca

./nEmulator 50412 ubuntu2004-004 50413 50414 ubuntu2004-008 50415 1 0.2 0
```

Next start the receiver on `ubuntu2004-004`
```
ssh -Y hkbulmer@ubuntu2004-004.student.cs.uwaterloo.ca

./receiver ubuntu2004-002 50414 50413 output
```

Finally start the sender on `ubuntu2004-008`
```
ssh -Y hkbulmer@ubuntu2004-008.student.cs.uwaterloo.ca

./sender ubuntu2004-002 50412 50415 50 input
```

At the end to check the packets transmitted correctly, I diffed the output:

```
diff input output
```

and made sure nothing was returned.

I used the file `input` to test with input that would require more than 32 packets to transmit (file is 45023 bytes), and the file `input1` to test input that requires fewer than 32 packets (file is 6130 bytes).

## Versioning

This project was built using `Python 3.6.4`, but is compatible with the `Python 3.8.10` running on school machines. Using `argparse v1.1`