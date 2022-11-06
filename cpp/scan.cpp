
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

#define NRF_RADIO_FREQUENCY (*(uint32_t*)(0x40001508UL))

#define CHANNEL_1 2
#define CHANNEL_2 26
#define CHANNEL_3 80

#define SAMPLE_SIZE 10

InterruptIn button(BUTTON_PIN);

Serial pc(UART_TX, UART_RX);

BLEDevice ble;

int channel_to_rssi[3][2];

int channel_counter[3];

int counter = 0;

void initialize(){
    for(int i = 0; i < 3; ++i){
        for(int j = 0; j < 2; ++j){
            channel_to_rssi[i][j] = 0;
        }
        channel_counter[i] = 0;
    }
}

int getChannelIndex(uint32_t v){
    if(v == CHANNEL_1){
        return 0;
    }else if(v == CHANNEL_2){
        return 1;
    }else{
        return 2;        
    }
}

void scanCallback(const Gap::AdvertisementCallbackParams_t *params){
   
    const char * addr = "d3:7b:3e:8f:c5:57";
    char p[30];
    sprintf(p, "%02x:%02x:%02x:%02x:%02x:%02x\0",
       params->peerAddr[5], params->peerAddr[4], params->peerAddr[3], params->peerAddr[2], params->peerAddr[1], params->peerAddr[0]);
    if(strcmp(p, addr) == 0){
        if(channel_counter[getChannelIndex(NRF_RADIO_FREQUENCY)] < SAMPLE_SIZE){
            channel_to_rssi[getChannelIndex(NRF_RADIO_FREQUENCY)][0] += (int)params->rssi;
            ++channel_to_rssi[getChannelIndex(NRF_RADIO_FREQUENCY)][1];
            ++channel_counter[getChannelIndex(NRF_RADIO_FREQUENCY)];
           //  LOG("Channel:%d RSSI: %d\n", NRF_RADIO_FREQUENCY, (int)params->rssi);
        }
       
    }
   
}


void start(){
    ble.init();
    ble_error_t error;

    error = ble.setScanParams(160, 100, 3, false);
     if(error){
        LOG("Param Error \n");
        LOG("%d\n", (int)error);
    }
}
void print(const char * s){
    LOG(s);
}


bool pull_data = false;
void ButtonPressed(void){
    LOG("%d\n", counter);
    ++counter;
    pull_data = true;
}
int main()
{
    
    wait(1);
    

    LOG("Initialising the nRF51822 Scan ? \n");

    button.fall(ButtonPressed);
    start();
    while(1){
        
        if(pull_data){
            initialize();
            ble_error_t error;
            while(channel_counter[0] != SAMPLE_SIZE || channel_counter[1] != SAMPLE_SIZE || channel_counter[2] != SAMPLE_SIZE){
                error = ble.gap().startScan(&scanCallback);
                if(error){
                    LOG("Start Scan Error \n");
                    LOG("%d\n", (int)error);
                }
                wait_ms(5000);
                
                ble.gap().stopScan();
                if(channel_counter[0] == SAMPLE_SIZE && channel_counter[1] == SAMPLE_SIZE && channel_counter[2] == SAMPLE_SIZE){
                    LOG("%f,%f,%f\n", (double)channel_to_rssi[getChannelIndex(CHANNEL_1)][0] / channel_to_rssi[getChannelIndex(CHANNEL_1)][1], (double)channel_to_rssi[getChannelIndex(CHANNEL_2)][0] / channel_to_rssi[getChannelIndex(CHANNEL_2)][1], (double)channel_to_rssi[getChannelIndex(CHANNEL_3)][0] / channel_to_rssi[getChannelIndex(CHANNEL_3)][1]);
                    pull_data = false;
                }
            }
            
        }
    
    }
        
    return 0;
}
