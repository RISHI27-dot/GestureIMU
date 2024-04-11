#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#include "mpu.h"
#include "sdkconfig.h"
#include "esp_hid_gap.h"
#include "esp_hid_device.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define MAX_SAMPLES 100

#pragma pack(1)

static const char *TAG = "mpu_example";
struct acc_values *data;

int16_t acce_raw_value[BUFF_SIZE / 2], gyro_raw_value[BUFF_SIZE / 2];
int16_t max_acc_values[3] = {INT16_MIN, INT16_MIN, INT16_MIN}; // Initialize max accelerometer values to smallest possible
int16_t min_acc_values[3] = {INT16_MAX, INT16_MAX, INT16_MAX}; // Initialize min accelerometer values to largest possible
float normalized_values[3];

void app_main()
{
    // Enable the MPU-6050 Sensor and check for error
    if (enable_mpu() != ESP_OK)
    {
        ESP_LOGE(TAG, "%s", "Error enabling MPU!");
        return; // Exit the function if there's an error enabling the MPU
    }

    setup(); // Setup BLE

    while (1)
    {
        for (int i = 0; i < MAX_SAMPLES; i++)
        {
            // Read MPU raw data
            if (read_mpu_raw(acce_raw_value, gyro_raw_value) != ESP_OK)
            {
                ESP_LOGE(TAG, "%s", "Error reading MPU!");
                return; // Exit the loop if there's an error reading the MPU
            }

            // Update max and min values
            for (int j = 0; j < 3; j++)
            {
                if (acce_raw_value[j] > max_acc_values[j])
                    max_acc_values[j] = acce_raw_value[j];
                if (acce_raw_value[j] < min_acc_values[j])
                    min_acc_values[j] = acce_raw_value[j];
            }
        }

        // Normalize accelerometer values while preserving sign
        for (int i = 0; i < 3; i++)
        {
            if (acce_raw_value[i] >= 0)
            {
                normalized_values[i] = (float)(acce_raw_value[i] - min_acc_values[i]) / (max_acc_values[i] - min_acc_values[i]);
            }
            else
            {
                normalized_values[i] = (float)(acce_raw_value[i] - min_acc_values[i]) / (min_acc_values[i] - max_acc_values[i]);
                normalized_values[i] *= -1.0f;
            }
        }

        // Print all the normalized values 
        ESP_LOGI(TAG, "Normalized values: %f, %f, %f", normalized_values[0], normalized_values[1], normalized_values[2]);

        // Reset max and min values for next batch
        for (int i = 0; i < 3; i++)
        {
            max_acc_values[i] = INT16_MIN;
            min_acc_values[i] = INT16_MAX;
        }

        // Send normalized accelerometer values to BLE task
        data = malloc(sizeof(struct acc_values));
        data->ax = normalized_values[0];
        data->ay = normalized_values[1];
        data->az = normalized_values[2];

        ble_hid_task(data);
        free(data);
    }
}
