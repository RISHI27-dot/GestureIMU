import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import sys

def avg_acc(data, vts):
    if vts:
        return data['ax'][vts:-vts].mean(), data['ay'][vts:-vts].mean(), data['az'][vts:-vts].mean() 
    else:
        return data['ax'].mean(), data['ay'].mean(), data['az'].mean() 

# get the data in the CSV file in the form of a dictionary 
def get_data(file_path):
    data = pd.read_csv(file_path, header='infer')
    return data

def plot(data):
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel('avg X')
    ax.set_ylabel('avg Y')
    ax.set_zlabel('avg Z')
    ax.set_title('3D Scatter Plot')

    for digit, acc_data in data.items():
        if digit == '0':
            ax.scatter(acc_data[0], acc_data[1], acc_data[2], color='r', label=digit)
        if digit == '2':
            ax.scatter(acc_data[0], acc_data[1], acc_data[2], color='g', label=digit)
        if digit == '9':
            ax.scatter(acc_data[0], acc_data[1], acc_data[2], color='b', label=digit)
        if digit == '8':
            ax.scatter(acc_data[0], acc_data[1], acc_data[2], color='y', label=digit)

    ax.legend()
    plt.show()

# def interpolate(data):
     # new_data_list = []
    # num_zeros = 3
    # for col in data.columns:
    #     # values = data[col].values
    #     # new_values = np.repeat(values, num_zeros +1)
    #     # new_values[1::num_zeros + 1] = 0
    #     # data[col] = new_values

def driver(csv_path):
    num_files = int(sys.argv[1]) 
    gesture_files = {
        '0': [f"{csv_path}/0_{i}.csv" for i in range(num_files)],
        '2': [f"{csv_path}/2_{i}.csv" for i in range(num_files)],
        '9': [f"{csv_path}/9_{i}.csv" for i in range(num_files)],
        '8': [f"{csv_path}/8_{i}.csv" for i in range(num_files)]
    }

    gesture_data = {
        '0': [],
        '2': [],
        '9': [],
        '8': []
    }

    for digit, files in gesture_files.items():
        avg_ax = avg_ay = avg_az = 0
        avg_ax_list = [] 
        avg_ay_list = [] 
        avg_az_list = []

        for file in files:
            data = get_data(file)

            # interpolate(data)
            avg_ax, avg_ay, avg_az = avg_acc(data, 0)
            avg_ax_list.append(avg_ax)
            avg_ay_list.append(avg_ay)
            avg_az_list.append(avg_az)
            print("ax = {:6f} | ay = {:6f} | az = {:6f}".format(avg_ax, avg_ay, avg_az))

        gesture_data[digit].append(avg_ax_list)
        gesture_data[digit].append(avg_ay_list)
        gesture_data[digit].append(avg_az_list)
    
    plot(gesture_data)
    
# Entry point of the program
if __name__ == "__main__":
    csv_path = "csv"  # Replace with the path to your CSV files directory
    if len(sys.argv) < 2:
        print("Please provide number of csv files to read")
        exit()
    driver(csv_path)
