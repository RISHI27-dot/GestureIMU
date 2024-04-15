#ifndef PINDEFS
#define PINDEFS

#define MPU6050_INT 23
#define MPU6050_SDA 22
#define MPU6050_SCL 21

#define CHECK(x)                        \
	do {                            \
		esp_err_t __;           \
		if ((__ = x) != ESP_OK) \
			return __;      \
	} while (0)

#endif
