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


    ESP_LOGI(WIFI_TAG, "ESP_WIFI_MODE_STA");
    wifi_station_init();

    ESP_LOGI(MQTT_TAG, "ESP_MQTT_MODE_CLIENT");
    mqtt_client_init();

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