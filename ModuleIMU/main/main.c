#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>

#include "freertos/portmacro.h"
#include "mpu.h"
#include "pindefs.h"
#include "switch_pindefs.h"
#include "switches.h"
#include "sdkconfig.h"
#include "esp_hid_gap.h"
#include "esp_hid_device.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define MAX_SAMPLES 300
#define MAX_END_SEQ_COUNT 3

static const char *TAG = "MAIN";
int16_t end_seq[3] = {0, 1, 0};

void app_main()
{
  int16_t acce_raw_value[BUFF_SIZE / 2], gyro_raw_value[BUFF_SIZE / 2];
  int ret = 0;

  while (1)
  {
    /* Setup MPU6050 */
    if(enable_mpu() != ESP_OK)
    {
      ESP_LOGE(TAG, "Error setting up MPU6050");
      goto err;
    }

    /* Setup switches */
    if(enable_switches() != ESP_OK)
    {
      ESP_LOGE(TAG, "Error setting up switches");
      goto err;
    }

    /* Setup BLE */
    setup_ble();

    if (!ret)
    {
      while (read_mpu_raw(acce_raw_value, gyro_raw_value) == ESP_OK)
      {
        if(read_switch(SWITCH_1))
        {
          if (ble_hid_task(acce_raw_value) != ESP_OK)
          {
            ESP_LOGE(TAG, "%s", "Failed to send acc values !!");
            goto err;
          }
        }
        else if (read_switch(SWITCH_4)) {
          if (ble_hid_task(end_seq) != ESP_OK)
          {
            ESP_LOGE(TAG, "%s", "Failed to send end sequence !!");
            goto err;
          }
        }
        else
        {
          ESP_LOGI(TAG, ". . . . .");
        }

        vTaskDelay(100 / portTICK_PERIOD_MS);
      }
    }
  }

err :
  ESP_LOGE(TAG, "%s", "Error !!!!!");
}
