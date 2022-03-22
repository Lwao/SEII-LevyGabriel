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
    // configure gpio pins
    gpio_config_t out_gpio = {
        .mode         = GPIO_MODE_OUTPUT,     // output mode
        .pin_bit_mask = GPIO_OUTPUT_PIN_SEL,  // bit mask for pins in use
        .pull_down_en = GPIO_PULLDOWN_ENABLE, // enable pull-down mode
        .pull_up_en   = GPIO_PULLUP_DISABLE,  // disable pull-up mode
        .intr_type    = GPIO_INTR_DISABLE     // no isr hooked
    };
    ESP_ERROR_CHECK(gpio_config(&out_gpio)); // initialize input pin configuration
    
    ESP_LOGI(WIFI_TAG, "ESP_WIFI_MODE_STA");
    wifi_station_init();

    ESP_LOGI(MQTT_TAG, "ESP_MQTT_MODE_CLIENT");
    mqtt_client_init();

    vTaskDelete(NULL);
}