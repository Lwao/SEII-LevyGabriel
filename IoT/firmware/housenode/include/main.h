/**
 * @file main.h
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date February 22 2022
 */

#ifndef _MAIN_H_ 
#define _MAIN_H_

#ifndef C_POSIX_LIB_INCLUDED
    #define C_POSIX_LIB_INCLUDED
    #include <stdio.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include <string.h>
    #include <stddef.h>
#endif //C_POSIX_LIB_INCLUDED

#ifndef DRIVERS_INCLUDED
    #define DRIVERS_INCLUDED
    #include "driver/gpio.h"
#endif //DRIVERS_INCLUDED

#ifndef ESP_MANAGEMENT_LIBS_INCLUDED
    #define ESP_MANAGEMENT_LIBS_INCLUDED
    #include "esp_err.h" // error codes and helper functions
    #include "esp_log.h" // logging library
    #include "esp_system.h" // esp system functions
#endif //ESP_MANAGEMENT_LIBS_INCLUDED

#include "wifi.h"
#include "mqtt.h"

#define GPIO_OUTPUT_PIN_SEL   (1ULL<<GPIO_NUM_13) | (1ULL<<GPIO_NUM_14) | (1ULL<<GPIO_NUM_15) | (1ULL<<GPIO_NUM_16) | (1ULL<<GPIO_NUM_17) | (1ULL<<GPIO_NUM_18) | (1ULL<<GPIO_NUM_19) | (1ULL<<GPIO_NUM_21) | (1ULL<<GPIO_NUM_22) | (1ULL<<GPIO_NUM_23) | (1ULL<<GPIO_NUM_25) | (1ULL<<GPIO_NUM_26) | (1ULL<<GPIO_NUM_27) | (1ULL<<GPIO_NUM_32) | (1ULL<<GPIO_NUM_33)
#define ESP_INTR_FLAG_DEFAULT 0

#define SETUP_APP_TAG "app_main"

#endif // _MAIN_H_