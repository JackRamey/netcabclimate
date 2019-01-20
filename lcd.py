from RPLCD import i2c

# Set-up some constants to initialise the LCD
lcdmode = 'i2c'
cols = 16
rows = 2
charmap = 'A00'
i2c_expander = 'PCF8574'
address = 0x27 # If you don't know what yours is, do i2cdetect -y 1
port = 1 # 0 on an older Pi

# Initialise the LCD
lcd = i2c.CharLCD(i2c_expander,address,port=port,charmap=charmap,cols=cols,rows=rows)

if __name__ == "__main__":
    lcd.clear()
    lcd.write_string("Hello world!")

