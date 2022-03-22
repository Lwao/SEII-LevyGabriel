/**
 * @file mqtt.c
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date March 20 2022
 */

#include "mqtt.h"

char port_map[] = {13,14,15,16,17,18,19,21,22,23,25,26,27,32,33}; // port1 to port15

void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data)
{
    ESP_LOGD(MQTT_TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    esp_mqtt_event_handle_t event = event_data;
    esp_mqtt_client_handle_t client = event->client;
    int msg_id;
    switch ((esp_mqtt_event_id_t)event_id) {
    case MQTT_EVENT_CONNECTED:
        ESP_LOGI(MQTT_TAG, "MQTT_EVENT_CONNECTED");
        msg_id = esp_mqtt_client_subscribe(client, USERNAME "/#", 2);
        ESP_LOGI(MQTT_TAG, "sent subscribe successful, msg_id=%d", msg_id);
        msg_id = esp_mqtt_client_publish(client, USERNAME "/status", "online", 0, 2, 0);
        ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);

        // initialize pins to zero
        char* topic_back;
        for(int port=0; port<15; port++)
        {
            gpio_set_level(port_map[port], 0);
            asprintf(&topic_back, USERNAME "/devices/port%d", port+1);
            msg_id = esp_mqtt_client_publish(client, topic_back, "offline", 0, 2, 0);
            ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);
        }
        break;
    case MQTT_EVENT_DISCONNECTED:
        ESP_LOGI(MQTT_TAG, "MQTT_EVENT_DISCONNECTED");
        msg_id = esp_mqtt_client_publish(client, USERNAME "/status", "offline", 0, 2, 0);
        ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);
        break;
    case MQTT_EVENT_SUBSCRIBED:
        break;
    case MQTT_EVENT_UNSUBSCRIBED:
        break;
    case MQTT_EVENT_PUBLISHED:
        break;
    case MQTT_EVENT_DATA:
        ESP_LOGI(MQTT_TAG, "MQTT_EVENT_DATA");
        printf("TOPIC=%.*s\r\n", event->topic_len, event->topic);
        printf("DATA=%.*s\r\n", event->data_len, event->data);
        topic_handler(event, client);
        break;
    case MQTT_EVENT_ERROR:
        ESP_LOGI(MQTT_TAG, "MQTT_EVENT_ERROR");
        if (event->error_handle->error_type == MQTT_ERROR_TYPE_TCP_TRANSPORT) {
            log_error_if_nonzero("reported from esp-tls", event->error_handle->esp_tls_last_esp_err);
            log_error_if_nonzero("reported from tls stack", event->error_handle->esp_tls_stack_err);
            log_error_if_nonzero("captured as transport's socket errno",  event->error_handle->esp_transport_sock_errno);
            ESP_LOGI(MQTT_TAG, "Last errno string (%s)", strerror(event->error_handle->esp_transport_sock_errno));
        }
        break;
    default:
        ESP_LOGI(MQTT_TAG, "Other event id:%d", event->event_id);
        break;
    }
}

void topic_handler(esp_mqtt_event_handle_t event, esp_mqtt_client_handle_t client)
{
    char* topic;
    char* data;
    char* token; 
    int port, msg_id;

    asprintf(&topic, "%.*s", event->topic_len, event->topic);
    asprintf(&data, "%.*s", event->data_len, event->data);
    
    token = strtok(topic, "/");
    if((token != NULL) && (strcmp(token,USERNAME)==0)
    ) // extracts USERNAME
    {
        token = strtok(NULL, "/");
        if(token != NULL) // parse first level child /status or /devices
        {
            if(strcmp(token,"status")==0) // get status
            {
                if(strcmp(data,"online")!=0) // if not online status force to it
                {
                    msg_id = esp_mqtt_client_publish(client, USERNAME "/status", "online", 0, 2, 0);
                    ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);
                }                
            } else if(strcmp(token,"devices")==0) // get port
            {
                token = strtok(NULL, "/port"); 
                port = strtol(token, NULL, 10); // convert port number to int

                char* topic_back;
                asprintf(&topic_back, USERNAME "/devices/port%d", port);

                if(strcmp(data,"on")==0) // receive the on command
                {
                    gpio_set_level(port_map[port-1], 1);
                    // once the on command pass, it publishes back online into port
                    msg_id = esp_mqtt_client_publish(client, topic_back, "online", 0, 2, 0);
                    ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);
                } else if(strcmp(data,"off")==0) // receive the off command
                {
                    gpio_set_level(port_map[port-1], 0);
                    // once the on command pass, it publishes back offline into port
                    msg_id = esp_mqtt_client_publish(client, topic_back, "offline", 0, 2, 0);
                    ESP_LOGI(MQTT_TAG, "sent publish successful, msg_id=%d", msg_id);
                }                
            } else printf("Invalid topic!\n");
        }
    }

}

void mqtt_client_init()
{
    esp_mqtt_client_config_t mqtt_cfg = {
        .host = MQTT_SERVER,
        .port = MQTT_PORT,
        .username = MQTT_USER,
        .password = MQTT_PWD,
        .lwt_topic = USERNAME "/status",
        .lwt_msg = "offline",
        .lwt_qos = 2,
        .lwt_retain = 1,
        .keepalive = 5,
    };

    esp_mqtt_client_handle_t client = esp_mqtt_client_init(&mqtt_cfg);
    /* The last argument may be used to pass data to the event handler, in this example mqtt_event_handler */
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, NULL);
    esp_mqtt_client_start(client);
}

void log_error_if_nonzero(const char *message, int error_code)
{
    if (error_code != 0) {
        ESP_LOGE(MQTT_TAG, "Last error %s: 0x%x", message, error_code);
    }
}