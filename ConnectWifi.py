def connect():
    import network
 
    ssid = "Llama Speed"
    password =  "9542942625"
 
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
        print("ESP32-001 ALREADY ONLINE")
        return
 
    station.active(True)
    station.connect(ssid, password)
    print("Handshake")
    station.ifconfig(("10.0.0.195","255.255.255.0","10.0.0.1","10.0.0.1"))
    while station.isconnected() == False:
        pass
 
    print("ESP32-001 NOW ONLINE")
    print(station.ifconfig())
