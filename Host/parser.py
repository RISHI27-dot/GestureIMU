import csv
import numpy as np
import sys
import os
import argparse

from inference import get_average


def func():
   if len(sys.argv) < 2:
       print("Please provide a gesture")
       exit()

   txt_prefix = "txt/" + sys.argv[1]
   bt_txt_file_name = txt_prefix + ".txt"
   if not os.path.exists(bt_txt_file_name):
       print("The file", bt_txt_file_name, "has not been generated")
       print("Run the following command to generate it")
       print("     ./record_gesture.sh " + sys.argv[1])
       exit()
   bt_txt_file = open(bt_txt_file_name, "r")
   data = bt_txt_file.readlines()

   csv_prefix = "csv/" + sys.argv[1]
   bt_csv_file_name = csv_prefix + "_" + "0" + ".csv"
   bt_csv_file = open(bt_csv_file_name, "w")
   fields = ['ax', 'ay', 'az']
   csvwriter = csv.writer(bt_csv_file)
   csvwriter.writerow(fields)

   print("-------------------------------------")
   print("writing to the file", bt_csv_file_name)
   print("-------------------------------------")

   ax_values = []
   end_seq_flag = 0
   file_count = 1
   sr_no = 1

   for line in data:
       # Obtain the current line
       curr_line = line.split()
       curr_line_len = len(curr_line)
      
       # If not valid line skip
       if (curr_line[0] != '>' or curr_line_len != 19):
           continue

       # Convert all elements to uint8, later they will be fused to form int16
       raw_values = [np.uint8(int(curr_line[i], 16)) for i in range(13, curr_line_len)]

       if(raw_values != [0, 0, 0, 1, 0, 0]):

           if(end_seq_flag == 1):
               new_file_name = csv_prefix + "_" + str(file_count) + ".csv"
               sr_no = 1

               print("---------------------------------------------")
               print("writing to the file", new_file_name)
               print("---------------------------------------------")

               bt_csv_file = open(new_file_name, "w")
               csvwriter = csv.writer(bt_csv_file)
               csvwriter.writerow(fields)

               file_count = file_count + 1
          
           # Fusion
           ax = np.int16(((raw_values[0] << 8) + raw_values[1]))
           ay = np.int16(((raw_values[2] << 8) + raw_values[3]))
           az = np.int16(((raw_values[4] << 8) + raw_values[5]))

           # Log
           print("{:4d}: ax = {:6d} | ay = {:6d} | az = {:6d}".format(sr_no, ax, ay, az))

           # Write to the CSV
           acc_list = [ax, ay, az]
           ax_values.append(ax)
           csvwriter.writerow(acc_list)
           sr_no = sr_no + 1
           end_seq_flag = 0
       else:
           end_seq_flag = 1
           continue


if __name__ == "__main__":
   if sys.argv[1] == '-t':
       fail_count = 0
       bitmap = [0,0,0,0,0,0,0,0,0,0]
       string = sys.argv[2]
       for i in range(len(string)):
            test_file = './Host/csv/test_' + str(i) + '_' + string[i] + '.csv'
            # print(test_file, end="->")
            res = get_average(filepath=test_file, model_type='nnet', n_observations=105, average_window=15)
            # print(res)
            if(str(res) != string[i]):
                # print("Failed on " + string[i])
                fail_count += 1
                bitmap[int(string[i])] += 1
       print("Total Obs = ", len(string))
       print("Failed On = ", fail_count)
       accuracy = ((len(string) - fail_count)/len(string)) * 100
       print("Acc = ", accuracy, "%")

       print("Indices = ", [0,1,2,3,4,5,6,7,8,9])
       print("Fails   = ", bitmap)

   elif sys.argv[1] == '-d':
       func()
   else:
       raise ValueError('Invalid flag passed')
