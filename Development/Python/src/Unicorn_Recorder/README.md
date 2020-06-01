# Unicorn Recorder

## Quick-Guide to making a recording:
*SetUp:*
1. import the recorder
2. Create an instance of the unicorn_recorder
3. Call connect
4. Call startRecording

*Online Data Acquisition:*

1. Call refresh
2. Call getData
3. Repeat

*Stop and save:*
1. Call stopRecording
2. Call save

## Using a Dummy EEG:
The Unicorn recorder allows you to use a dummy Interface should the actual device not be available.
To use it follow the following procedure:
1. import the dummy module. You can find preimplemented dummies in the Dummies folder
2. import the Unicorn_Recorder FOLDER
3. On the FOLDER call set_backend(dummy), where dummy is the import of the module from step 1

This all needs to happen before importing the Unicorn Recorder module for the first time.
You can find an example of the functionality in the Examples under set_a_dummy

## Using a Plot with the Recorder
The Unicorn Recorder allows for automatic plotting of newly acquired data.
To use a plot create an instance of a Plotter and call toggle_plot(plot) with the plot instance you created.
See also the use_a_plot example

## Examples:  
Examples of how to use the Unicorn Recorder can be found in the Examples folder.

## References

MNE : https://mne.tools/stable/overview/index.html

## Issues
- IsDeviceLibraryLoaded() has an argument that is not specified in the documentation.
- The Amplifiers Unit returns "ÂµV". What does that even mean?

- Unpacking the float values is rather slow. Bad for online applications
- Use the Unicorn Dummy at your own risk, it is not an an accurate representation of the EEG
- It is not sure that the signal quality check actually works