set(srcs "esp_hid_device.c" "esp_hid_gap.c")

idf_component_register(SRCS "${srcs}"
                    INCLUDE_DIRS "."
                    REQUIRES bt driver efuse esp_common esp_event esp_timer
                                esp_rom freertos heap log soc spiffs esp_hid
                    PRIV_REQUIRES nvs_flash)
