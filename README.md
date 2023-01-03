### Drobo-Status
Drobo Status is a python program that will connect to your Drobo and return JSON data regarding your Drobo. You can then use this data to get real time status from your Drobo. This is only tested on Drobo FS 8 Bay. Please let me know if it works on others. 

#### Donate to get me geek stuff(sorry no beer here)

[![paypal](https://www.paypalobjects.com/en_US/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=TWRQVYJWC77E6)

#### Set up Application
1. Clone this repo
2. Edit drobo-status.cfg Set you DROBO IP (do not use quotes)
```
[drobo]
host = IP of your DROBO
```
#### Update Docker file if needed on line 3
```
Please note you can change the TZ to a more specific location listed [Here](https://en.m.wikipedia.org/wiki/List_of_tz_database_time_zones) .
```


3. docker build -t drobo-status:latest .
4. docker run -d --name drobo-status -p 192.168.1.126:5000:5000 drobo-status:latest

#### In a browser go to host that is running this program on port 5000 I.E.(192.168.1.126:5000)
You should see output like 
```
{"name":"Storage", "serial": "0db1135c014012","firmware-version": "2.1.8 [7.38.12635]","disk-total": "12 TB","disk-used": "1 TB","disk-free": "10 TB", "drives": [{"sid": 0, "status": 3, "capacity": "2.73 TB"}, {"sid": 1, "status": 3, "capacity": "2.73 TB"}, {"sid": 2, "status": 3, "capacity": "2.73 TB"}, {"sid": 3, "status": 3, "capacity": "2.73 TB"}, {"sid": 4, "status": 3, "capacity": "2.73 TB"}, {"sid": 5, "status": 3, "capacity": "2.73 TB"}, {"sid": 6, "status": 3, "capacity": "2.73 TB"}, {"sid": 7, "status": 129, "capacity": "0 B"}]}
```

##### Home Assistant (The reason I made this, I might make it a plugin for HACS)
Using the Scrape plugin add this to your configuration (Need to add more in the template but its a start)

```
platform: rest
    name: tfam-storage
    # This is the ip of the host running drobo-status.py
    resource: http://192.168.1.126:5000
    json_attributes:
      - name
      - serial
      - firmware
      - disk-total
      - disk-used
      - disk-free
    value_template: "OK"
  - platform: template
    sensors:
      storage_name:
        value_template: "{{ state_attr('sensor.tfam-storage', 'name')['name'] }}"
      storage_serial:
        value_template: "{{ state_attr('sensor.tfam-storage', 'serial')['serial'] }}"
      storage_firmware:
        value_template: "{{ state_attr('sensor.tfam-storage', 'firmware')['firmware'] }}"
      storage_disk_total:
        value_template: "{{ state_attr('sensor.tfam-storage', 'disk-total')['disk-total'] }}"
```



