/**
 * @file mqtt.h
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date March 20 2022
 */


#ifndef _MQTT_H_ 
#define _MQTT_H_

#ifndef MQTT_LIBS_INCLUDED
    #define MQTT_LIBS_INCLUDED
    #include "mqtt_client.h"
#endif //MQTT_LIBS_INCLUDED

#ifndef ESP_MANAGEMENT_LIBS_INCLUDED
    #define ESP_MANAGEMENT_LIBS_INCLUDED
    #include "esp_err.h" // error codes and helper functions
    #include "esp_log.h" // logging library
    #include "esp_system.h" // esp system functions
#endif //ESP_MANAGEMENT_LIBS_INCLUDED

#define MQTT_SERVER "192.168.18.45"
#define MQTT_PORT 1883
#define MQTT_USER ""
#define MQTT_PWD ""

#define MQTT_TAG "mqtt_config"

/**
 * @brief Initialize MQTT configuration.
 */
void mqtt_client_init();

/**
 * @brief Event handler registered to receive MQTT events
 *
 * @param handler_args user data registered to the event.
 * @param base Event base for the handler(always MQTT Base in this example).
 * @param event_id The id for the received event.
 * @param event_data The data for the event, esp_mqtt_event_handle_t.
 */
void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data);

/**
 * @brief Log message in response to MQTT error
 *
 * @param message Incoming message.
 * @param error_code Error code to handle.
 */
void log_error_if_nonzero(const char *message, int error_code);

#endif // _MQTT_H_