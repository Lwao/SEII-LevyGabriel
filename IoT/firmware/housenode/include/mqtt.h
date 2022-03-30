/**
 * @file mqtt.h
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date March 20 2022
 */


#ifndef _MQTT_H_ 
#define _MQTT_H_

#ifndef C_POSIX_LIB_INCLUDED
    #define C_POSIX_LIB_INCLUDED
    #include <stdio.h>
    #include <stdlib.h>
    #include <stdint.h>
    #include <string.h>
    #include <stddef.h>
#endif //C_POSIX_LIB_INCLUDED

#ifndef MQTT_LIBS_INCLUDED
    #define MQTT_LIBS_INCLUDED
    #include "mqtt_client.h"
#endif //MQTT_LIBS_INCLUDED

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

#define MQTT_SERVER "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_USER ""
#define MQTT_PWD ""


#define USERNAME "blue"
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
 * @brief Parse incoming messages checking to what child topic the message belongs to and handling the results
 *
 * @param event event of incoming message.
 * @param client mqtt from event
 */
void topic_handler(esp_mqtt_event_handle_t event, esp_mqtt_client_handle_t client);

/**
 * @brief Log message in response to MQTT error
 *
 * @param message Incoming message.
 * @param error_code Error code to handle.
 */
void log_error_if_nonzero(const char *message, int error_code);

#endif // _MQTT_H_