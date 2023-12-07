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

    SW_INT button press
    DrvGPIO_GetBit(E_GPB,15)==0

## Debounce

    while(1){
		DrvSYS_Delay(1000);
		if(DrvGPIO_GetBit(E_GPB,15)==1) {
			break;
		}
	}

## Keypad

    Column control : GPA2, 1, 0
    Raw control : GPA 3, 4, 5
    | \    | GPA2 | GPA1 | GPA0 |
    |:--   |:--   |:--   |:--   |
    | GPA3 |   1  |   2  |  3   |
    | GPA4 |   4  |   5  |  6   |
    | GPA5 |   7  |   8  |  9   |
           000000
    -> GPA 012345
    Key1 = GPA3 + GPA2
    Key2 = GPA3 + GPA1
    Key3 = GPA3 + GPA0
    Key4 = GPA4 + GPA2
    Key5 = GPA4 + GPA1
    Key6 = GPA4 + GPA0
    Key7 = GPA5 + GPA2
    Key8 = GPA5 + GPA1
    Key9 = GPA5 + GPA0


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
| 0 | 0 | 0 | 0 | 1 | 1 | 1 | 0 | 0x0e |  D  |
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

Vertical and Horizontal scan(7 Seg)
B3
E6

3B
6E

9B
CE