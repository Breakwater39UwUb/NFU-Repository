## Work Path

[Path](C:\nuvoton\NUC100SeriesBSP_v1.05.002\NuvotonPlatform_Keil\Sample\NUC1xx-LB_002\)

## Delay

    DrvSYS_Delay(500000); //delay 0.5s
    DrvSYS_Delay(100000); //delay 100000us=100ms

## Buzzer
    DrvGPIO_Open(E_GPB, 11, E_IO_OUTPUT); // initial Buzzer
    DrvGPIO_ClrBit(E_GPB,11); // turn on Buzzer
    DrvGPIO_SetBit(E_GPB,11); // turn off Buzzer
    DrvSYS_Delay(100000);


## SW_INT

    DrvGPIO_Open(E_GPB, 15, E_IO_INPUT); // initial SWINT
    SW_INT button press
    DrvGPIO_GetBit(E_GPB,15)==0

## Debounce

    if(DrvGPIO_GetBit(E_GPB,15)==0) {
		while(1){
			DrvSYS_Delay(1000);
			if(DrvGPIO_GetBit(E_GPB,15)==1) {
				break;
			}
		}
    }

---

## Keypad

Column control : GPA2, 1, 0

Raw control : GPA 3, 4, 5

| \    | GPA2 | GPA1 | GPA0 |
|--:   |:--   |:--   |:--   |
| GPA3 |   1  |   2  |  3   |
| GPA4 |   4  |   5  |  6   |
| GPA5 |   7  |   8  |  9   |

### Encode of keypad

| GPA0 | GPA1 | GPA2 | GPA3 | GPA4 | GPA5 | hex |
| :-:  | :-:  | :-:  | :-:  | :-:  | :-:  | :-: |
|  1   |  1   |  1   |  1   |  1   |  1   | 0x3f|

    Key1 = GPA3 + GPA2
    Key2 = GPA3 + GPA1
    Key3 = GPA3 + GPA0
    Key4 = GPA4 + GPA2
    Key5 = GPA4 + GPA1
    Key6 = GPA4 + GPA0
    Key7 = GPA5 + GPA2
    Key8 = GPA5 + GPA1
    Key9 = GPA5 + GPA0

---

## 7 Segment Display
    DrvGPIO_Open(E_GPE, 0, E_IO_OUTPUT);
    DrvGPIO_Open(E_GPC, 4, E_IO_OUTPUT);  4~7

| g | e | d | b | a | f | p | c | hex  | dec |
|:--|:--|:--|:--|:--|:--|:--|:--| :--  | :-- |
| 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0xff | off |
| 1 | 1 | 1 | 1 | 0 | 1 | 1 | 1 | 0xf7 |     |
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0x7f |     |
| 1 | 1 | 0 | 1 | 1 | 1 | 1 | 1 | 0xdf |     |
| 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 | 0x22 |  A  |
| 0 | 0 | 0 | 1 | 1 | 0 | 1 | 0 | 0x1a |  B  |
| 1 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0x93 |  C  |
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0x00e |  D  |
| 0 | 0 | 0 | 1 | 0 | 0 | 1 | 1 | 0x13 |  E  |
| 0 | 0 | 1 | 1 | 0 | 0 | 1 | 1 | 0x33 |  F  |

C:10010011 = 0X93
E:00010011 = 0X13

    #define SEG_N0   0x82
    #define SEG_N1   0xEE
    #define SEG_N2   0x07
    #define SEG_N3   0x46
    #define SEG_N4   0x6A
    #define SEG_N5   0x52
    #define SEG_N6   0x12
    #define SEG_N7   0xE6
    #define SEG_N8   0x02
    #define SEG_N9   0x62

---

## LCD 128*64

### Initialize GPC12~16 (SPI1 pins)

    for(i=12;i<16;i++)	DrvGPIO_Open(E_GPC, i, E_IO_OUTPUT); 

### Encode

    16*8, down to up -> left to right, upper to downer


### [ASCII table](./Notes%20of%20microprocessor_2.md)


### Custom table

```c
unsigned char Ascii[]={
    /* 虎 */
    0xF0,0X08,0X28,0XFF,0XAA,0XAA,0X0A,0X38,0XFF,0x00,0xFC,0X00,0XFC,0X80,0X80,0X00,
    /* 科 */
    0X44,0XFC,0X44,0X00,0X24,0X48,0XFE,0X00,0X0E,0X7F,0X02,0X04,0X09,0X01,0X7F,0X01,
    /* 大 */
    0x10,0x10,0x10,0xFF,0x10,0x10,0x10,0x10,0x30,0x1E,0x07,0x01,0x07,0x1E,0x30,0x40,
    /* 資 */
    0x12,0x80,0x88,0xA6,0x9B,0x9A,0x26,0x00,0x00,0xBF,0x6A,0x2A,0x6A,0xBF,0x00,0x00,
    /* 工 */
    0x00,0x10,0x10,0x10,0xF0,0x10,0x10,0x00,0x00,0x04,0x04,0x04,0x07,0x04,0x04,0x00,
    /* 系 */
    0x10,0x48,0x64,0xD2,0x49,0x24,0x10,0x00,0x00,0x22,0x13,0x82,0xFE,0x02,0x13,0x26,
    /* 許 */
    0x08,0xAA,0xAC,0x08,0x9F,0x84,0xFC,0x84,0x1C,0x22,0x22,0x1C,0x00,0x00,0x3F,0x00,
    /* 書 */
    0x00,0x08,0xAA,0xAA,0xFF,0xAA,0xBE,0x08,0x00,0x02,0xFA,0xAA,0xAB,0xAA,0xFA,0x02,
    /* 和 */
    0x90,0x88,0xFC,0x82,0xE0,0x10,0x10,0xE0,0x08,0x04,0x7F,0x04,0x0B,0x04,0x04,0x03,
    /* packman */
    0xE0,0xF0,0xF8,0xFC,0x7C,0x78,0x30,0x20,0x0F,0x1F,0x3F,0x7E,0x7C,0x3C,0x18,0x10,
}
```