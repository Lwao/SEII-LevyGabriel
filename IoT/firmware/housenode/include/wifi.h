/**
 * @file wifi.h
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date March 20 2022
 */

#ifndef _WIFI_H_ 
#define _WIFI_H_

#ifndef WIFI_LIBS_INCLUDED
    #define WIFI_LIBS_INCLUDED
    #include "esp_wifi.h"
    #include "esp_event.h"
    #include "esp_netif.h"
    #include "nvs_flash.h"
#endif //WIFI_LIBS_INCLUDED

#ifndef ESP_MANAGEMENT_LIBS_INCLUDED
    #define ESP_MANAGEMENT_LIBS_INCLUDED
    #include "esp_err.h" // error codes and helper functions
    #include "esp_log.h" // logging library
    #include "esp_system.h" // esp system functions
#endif //ESP_MANAGEMENT_LIBS_INCLUDED

#include "freertos/event_groups.h"

#define ESP_WIFI_SSID      "Oriole"
#define ESP_WIFI_PASS      "boapergunta"
#define ESP_MAXIMUM_RETRY  10
#define WIFI_CONNECTED_BIT BIT0
#define WIFI_FAIL_BIT      BIT1

#define WIFI_TAG "wifi_config"

extern int s_retry_num;
extern EventGroupHandle_t s_wifi_event_group;

/**
 * @brief Initialize Wi-Fi configuration.
 */
void wifi_station_init();

/**
 * @brief Handles Wi-Fi related events
 * 
 * @param arg user data registered to the event.
 * @param event_base Event base for the handler
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */
void wifi_event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data);

#endif // _WIFI_H_