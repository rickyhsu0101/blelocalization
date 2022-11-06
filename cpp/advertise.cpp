
#include "mbed.h"
#include "mbed_i2c.h"
#include "inv_mpu.h"
#include "inv_mpu_dmp_motion_driver.h"
#include "nrf51.h"
#include "nrf51_bitfields.h"

#include "BLE.h"
#include "DFUService.h"
#include "UARTService.h"


#define LOG(...)    { pc.printf(__VA_ARGS__); }

#define LED_GREEN   p21
#define LED_RED     p22
#define LED_BLUE    p23
#define BUTTON_PIN  p17
#define BATTERY_PIN p1

#define MPU6050_SDA p12
#define MPU6050_SCL p13

#define UART_TX     p9
#define UART_RX     p11
#define UART_CTS    p8
#define UART_RTS    p10

/* Starting sampling rate. */
#define DEFAULT_MPU_HZ  (100)

Serial pc(UART_TX, UART_RX);
BLEDevice ble;

int main(void)
{
    wait(1);
    LOG("Initialising the nRF51822\n");
    ble.init();

    /* setup advertising */
    ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED);
    ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.accumulateAdvertisingPayload(GapAdvertisingData::SHORTENED_LOCAL_NAME,
                                     (const uint8_t *)"aedis", sizeof("aedis"));
    ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_128BIT_SERVICE_IDS,
                                     (const uint8_t *)UARTServiceUUID_reversed, sizeof(UARTServiceUUID_reversed));
                                     
    Gap::AddressType_t addr_type;
    Gap::Address_t addr;
    ble.gap().getAddress(&addr_type, addr);
    LOG("Device address: %02x:%02x:%02x:%02x:%02x:%02x\r\n",
           addr[5], addr[4], addr[3], addr[2], addr[1], addr[0]);

    ble.setAdvertisingInterval(160); /* 100ms; in multiples of 0.625ms. */
    ble.gap().startAdvertising();
        
}