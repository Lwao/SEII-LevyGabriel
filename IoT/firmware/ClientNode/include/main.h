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

#ifndef FREERTOS_LIB_INCLUDED
    #define FREERTOS_LIB_INCLUDED
    #include "freertos/FreeRTOS.h"
    #include "freertos/task.h"
    #include "freertos/queue.h"
    #include "freertos/semphr.h"
    #include "freertos/event_groups.h"
#endif //FREERTOS_LIB_INCLUDED

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

#ifndef WIFI_LIBS_INCLUDED
    #define WIFI_LIBS_INCLUDED
    #include "esp_wifi.h"
    #include "esp_event.h"
    #include "nvs_flash.h"
    #include "esp_netif.h"
#endif //WIFI_LIBS_INCLUDED

#ifndef MQTT_LIBS_INCLUDED
    #define MQTT_LIBS_INCLUDED
    #include "mqtt_client.h"
#endif //MQTT_LIBS_INCLUDED


#define ESP_WIFI_SSID      "2018"
#define ESP_WIFI_PASS      "la06le19lu43al4606194346"
#define ESP_MAXIMUM_RETRY  10
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT      BIT1

#define MQTT_SERVER "192.168.18.45"
#define MQTT_PORT 1883
#define MQTT_USER ""
#define MQTT_PWD ""


#define GPIO_INPUT_PIN_SEL   (1ULL<<GPIO_NUM_0)  // | (1ULL<<ANOTHER_GPIO)
#define ESP_INTR_FLAG_DEFAULT 0
#define BUFFER_NUM 2
#define BUFFER_LEN 64
#define BIT_(shift) (1<<shift)

// Log tags

#define SETUP_APP_TAG "app_main"
#define WIFI_TAG "wifi_config"
#define MQTT_TAG "mqtt_config"

// Events
enum events{SYSTEM_STARTED,
            BTN_ON_TASK,
            BTN_OFF_TASK};

// config input pin - button (GPIO0 commanded by BOOT button)
gpio_config_t in_conf = {
    .intr_type    = GPIO_INTR_POSEDGE,   // interrupt on rising edge
    .mode         = GPIO_MODE_INPUT,     // set as input mode
    .pin_bit_mask = GPIO_INPUT_PIN_SEL,  // bit mask of pins to set (GPIO00)
    .pull_down_en = 1,                   // enable pull-down mode
    .pull_up_en   = 0,                   // disable pull-up mode
};

// freertos variables
TaskHandle_t xTask; // task placeholder
QueueHandle_t xQueue; // queue placeholder
EventGroupHandle_t xEvents; // event group placeholder
SemaphoreHandle_t xSemaphore; // semaphore placeholder

portMUX_TYPE spinlock = portMUX_INITIALIZER_UNLOCKED;

// buffers
float buffer1[BUFFER_LEN];
float buffer2[BUFFER_LEN];

static int s_retry_num = 0;
static EventGroupHandle_t s_wifi_event_group;

/**
 * @brief Task placeholder.
 *
 * @param pvParameters freeRTOS task parameters.
 */
void vTask(void * pvParameters);

/**
 * @brief Interrupt service routine for button pressed (associated with BOOT button a.k.a GPIO0).
 */
static void IRAM_ATTR ISR_BTN();

/**
 * @brief Initialize Wi-Fi configuration.
 */
void wifi_station_init();

/**
 * @brief Initialize MQTT configuration.
 */
static void mqtt_client_init();

/**
 * @brief Handles Wi-Fi related events
 * 
 * @param arg user data registered to the event.
 * @param event_base Event base for the handler
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */
static void wifi_event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data);

/**
 * @brief Event handler registered to receive MQTT events
 *
 * @param handler_args user data registered to the event.
 * @param base Event base for the handler(always MQTT Base in this example).
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */
static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data);

/**
 * @brief Log message in response to MQTT error
 *
 * @param message Incoming message.
 * @param error_code Error code to handle.
 */
static void log_error_if_nonzero(const char *message, int error_code);

#endif // _MAIN_H_