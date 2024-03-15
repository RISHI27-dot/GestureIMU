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

static const char *TAG = "mpu_example";
struct acc_values *data;

void app_main()
{
    while (1)
    {
    // Enable the MPU-6050 Sensor and check for error
      if (enable_mpu() == ESP_OK)
      {
          // Setting up the result arrays, time difference and initial conditions
          int16_t acce_raw_value[BUFF_SIZE / 2], gyro_raw_value[BUFF_SIZE / 2];
          setup(); // Setup BLE
          while (read_mpu_raw(acce_raw_value, gyro_raw_value) == ESP_OK)
          {
            ESP_LOGI(TAG, "acce_raw_value = %d %d %d",acce_raw_value[0],acce_raw_value[1],acce_raw_value[2]);
            data = malloc(sizeof(struct acc_values));
            data->ax = acce_raw_value[0];
            data->ay = acce_raw_value[1];
            data->az = acce_raw_value[2];
            ble_hid_task(data);
            free(data);
          }
      }
    }

    ESP_LOGE(TAG, "%s", "Error reading values!");
}
