/**
 * @file main.c
 * @brief 
 *
 * @author Levy Gabriel & Pedro Santos
 * @date February 22 2022
 */

#include "main.h"

void app_main(void)
{
    printf("Hello World!");

    //BaseType_t xReturnedTask[1];

    // configure gpio pins
    ESP_ERROR_CHECK(gpio_config(&in_conf));                              // initialize input pin configuration
    ESP_ERROR_CHECK(gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT));    // install gpio isr service
    ESP_ERROR_CHECK(gpio_isr_handler_add(GPIO_NUM_0, ISR_BTN, NULL)); // hook isr handler for specific gpio pin

    // create semaphores/event groups
    xEvents     = xEventGroupCreate();
    xSemaphore  = xSemaphoreCreateBinary();
    xQueue      = xQueueCreate(BUFFER_NUM,BUFFER_LEN*sizeof(float)); 
    
    
    if(xEvents == NULL){ // tests if event group creation fails
        ESP_LOGE(SETUP_APP_TAG, "Failed to create event group.\n");
        while(1);
    }
    if(xSemaphore == NULL){ // tests if semaphore creation fails
        ESP_LOGE(SETUP_APP_TAG, "Failed to create binary semaphore.\n");
        while(1);
    }  
    if(xQueue == NULL){ // tests if queue creation fails
        ESP_LOGE(SETUP_APP_TAG, "Failed to create data queue.\n");
        while(1);
    }

    // create tasks
    // xReturnedTask[0] = xTaskCreatePinnedToCore( vTask, 
    //                                             "taskTest", 
    //                                             configMINIMAL_STACK_SIZE+128, 
    //                                             NULL, 
    //                                             configMAX_PRIORITIES-1, 
    //                                             &xTask, PRO_CPU_NUM); // APP_CPU_NUM
    
    // if(xReturnedTask[0] == pdFAIL){ // tests if task creation fails
    //     ESP_LOGE(SETUP_APP_TAG, "Failed to create task %d.\n", 0);
    //     while(1);
    // }

    // set flag informing that the recording is stopped
    // xEventGroupClearBits(xEvents, BIT_(SYSTEM_STARTED));
    xEventGroupSetBits(xEvents, BIT_(SYSTEM_STARTED));

    ESP_LOGI(SETUP_APP_TAG, "Successful BOOT!");

    wifi_station_init();

    vTaskDelete(NULL);
}

void vTask(void * pvParameters)
{
    while(1)
    {
        if(xEventGroupWaitBits(xEvents, BIT_(BTN_ON_TASK), pdFALSE, pdTRUE, portMAX_DELAY) & BIT_(BTN_ON_TASK))
        {
            // while(xQueue!=NULL && xQueueReceive(xQueue, &buffer2, 0)==pdTRUE)
            // {
            //     vTaskDelay(pdMS_TO_TICKS(1000));
            //     xQueueSend(xQueue,&buffer1,portMAX_DELAY);
            // }
        }
        vTaskDelay(pdMS_TO_TICKS(1000));     
    }
}

static void IRAM_ATTR ISR_BTN()
{
    portENTER_CRITICAL_ISR(&spinlock);
    if(xEventGroupGetBitsFromISR(xEvents) & BIT_(SYSTEM_STARTED))
    {
        xEventGroupSetBits(xEvents, BIT_(BTN_OFF_TASK)); 
    } 
    else{xEventGroupSetBits(xEvents, BIT_(BTN_ON_TASK));} 
    portEXIT_CRITICAL_ISR(&spinlock);
}

static void event_handler(void* arg, esp_event_base_t event_base, int32_t event_id, void* event_data)
{
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        if (s_retry_num < ESP_MAXIMUM_RETRY) {
            esp_wifi_connect();
            s_retry_num++;
            ESP_LOGI(WIFI_TAG, "retry to connect to the AP");
        } else {
            xEventGroupSetBits(s_wifi_event_group, WIFI_FAIL_BIT);
        }
        ESP_LOGI(WIFI_TAG,"connect to the AP fail");
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t* event = (ip_event_got_ip_t*) event_data;
        ESP_LOGI(WIFI_TAG, "got ip:" IPSTR, IP2STR(&event->ip_info.ip));
        s_retry_num = 0;
        xEventGroupSetBits(s_wifi_event_group, WIFI_CONNECTED_BIT);
    }
}

void wifi_station_init()
{
    s_wifi_event_group = xEventGroupCreate();

    ESP_ERROR_CHECK(esp_netif_init());

    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT,
                                                        ESP_EVENT_ANY_ID,
                                                        &event_handler,
                                                        NULL,
                                                        &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT,
                                                        IP_EVENT_STA_GOT_IP,
                                                        &event_handler,
                                                        NULL,
                                                        &instance_got_ip));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = ESP_WIFI_SSID,
            .password = ESP_WIFI_PASS,
            /* Setting a password implies station will connect to all security modes including WEP/WPA.
             * However these modes are deprecated and not advisable to be used. Incase your Access point
             * doesn't support WPA2, these mode can be enabled by commenting below line */
	     .threshold.authmode = WIFI_AUTH_WPA2_PSK,

            .pmf_cfg = {
                .capable = true,
                .required = false
            },
        },
    };
    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA) );
    ESP_ERROR_CHECK(esp_wifi_set_config(WIFI_IF_STA, &wifi_config) );
    ESP_ERROR_CHECK(esp_wifi_start() );

    ESP_LOGI(WIFI_TAG, "wifi_init_sta finished.");

    /* Waiting until either the connection is established (WIFI_CONNECTED_BIT) or connection failed for the maximum
     * number of re-tries (WIFI_FAIL_BIT). The bits are set by event_handler() (see above) */
    EventBits_t bits = xEventGroupWaitBits(s_wifi_event_group,
            WIFI_CONNECTED_BIT | WIFI_FAIL_BIT,
            pdFALSE,
            pdFALSE,
            portMAX_DELAY);

    /* xEventGroupWaitBits() returns the bits before the call returned, hence we can test which event actually
     * happened. */
    if (bits & WIFI_CONNECTED_BIT) {
        ESP_LOGI(WIFI_TAG, "connected to ap SSID:%s password:%s",
                 ESP_WIFI_SSID, ESP_WIFI_PASS);
    } else if (bits & WIFI_FAIL_BIT) {
        ESP_LOGI(WIFI_TAG, "Failed to connect to SSID:%s, password:%s",
                 ESP_WIFI_SSID, ESP_WIFI_PASS);
    } else {
        ESP_LOGE(WIFI_TAG, "UNEXPECTED EVENT");
    }

    /* The event will not be processed after unregister */
    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(IP_EVENT, IP_EVENT_STA_GOT_IP, instance_got_ip));
    ESP_ERROR_CHECK(esp_event_handler_instance_unregister(WIFI_EVENT, ESP_EVENT_ANY_ID, instance_any_id));
    vEventGroupDelete(s_wifi_event_group);
}