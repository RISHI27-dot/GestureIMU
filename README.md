# Prerequisites

1. `Python3` for running python scripts
```
sudo apt install python3
```

2. `ESP-IDF` for building the esp32 app and flashing it into esp32

    Refer - [Get Started](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/index.html)

3. `hcidump` tool for logging the data received via BLE on Host
```
sudo apt install bluez-hcidump
```

4. `clang-format` for code formatting

```
sudo apt install clang-format
```

# File Structure

The project contains two folders

## ModuleIMU
This folder contains the esp idf project. It will handle the following things
- [x] Interfacing of MPU6050
- [x] Sending the data acquired from MPU6050 to the host PC via BLE.

## Host
This folder contains the code that will run on the host. It will handle the following things
- [x] Parsing the `.txt` files where the gesture data received via BLE is dumped.
- [x] Generating data set.
- [ ] Training and running ML model on the data.

# Usage

## Clone the repo
```
git clone git@github.com:RISHI27-dot/GestureIMU.git
cd GestureIMU
```

## Sensor Data Acquisition
Connect the module to your host PC and open two terminals.

Terminal 1:
```
cd Host
chmod +x record_gesture.sh
./record_gesture.sh <gesture>
```
The `<gesture>` argument of the shell script signifies the gesture being recorded. Pass `0` to record the gesture of 0, Pass `7` to record the gesture of 7 etc.

The gesture data will be recorded in the `<gesture>.txt` file in the `Host/txt/` directory.

Terminal 2:
```
cd ModuleIMU
get_idf
idf.py flash monitor
```
After this MPU6050 will start recording gestures and ESP32 will send them to the host PC via BLE depending on the switch pressed.
```
/* Pseudo Code */

if (SWITCH_1 hold) {
    send gesture data
} else if (SWITCH_4 hold) {
    send end sequence
}
```
The shell script running in the Terminal 1 will be recording the value sent by ESP32 and received by the host PC into the corresponding `.txt` file.

## Data Set Generation
After the data for one gesture is recorded, kill the command in Terminal 1 using `Ctrl + C`. You will see `<gesture>.txt` file in the `Host/txt/` directory.

To generate CSV data, run the following command.

Terminal 1:
```
python3 parser.py <gesture>
```
The `<gesture>` argument of the python script signifies the gesture for which `.csv` are being generated. Pass `0` for gesture 0, Pass `7` for gesture of 7 etc.

This will generate multiple `.csv` of the naming convention `a_b.csv` in the `Host/csv/`directory. Here `a` is the gesture and `b` is the sequence number.

Example - File no `3` of the gesture `7` will have name `7_3.csv`