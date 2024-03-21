var sensor_data = {}
var alarm_data = {
    "temp": [0, 0],
    "humi":[0,0],
    "co2":[0,0],
    "ill":[0,0],
}
var setAlarm = false
var led_state = "OFF"


var socket = io('http://10.2.24.16:8000')

socket.on('connect', function () {
console.log('Connected to server')
})

socket.on('msgFromSerial', function (data) {
console.log('Received message from server:', data.sensor_data)
sensor_data = data.sensor_data
var temp = document.getElementById('temp')
var humi = document.getElementById('humi')
var co2 = document.getElementById('co2')
var ill = document.getElementById('ill')
    
var tempBar = document.getElementById('temp-bar')
var humiBar = document.getElementById('humi-bar')
var co2Bar = document.getElementById('co2-bar')
var illBar = document.getElementById('ill-bar')
// var newMessage = document.createElement('p')
// newMessage.textContent = data.message
temp.innerHTML = "온도[°C] : " + sensor_data.temp
humi.innerHTML = "습도[%] : "+sensor_data.humi
co2.innerHTML = "이산화 탄소[ppm] : "+sensor_data.co2
ill.innerHTML = "조명[lx] : " + sensor_data.ill
    
tempBar.style.width = sensor_data.temp * 100 / 100 + "%"
    tempBar.innerHTML = sensor_data.temp
    
    humiBar.style.width = sensor_data.humi * 100 / 100 + "%"
    humiBar.innerHTML = sensor_data.humi
    
    co2Bar.style.width = sensor_data.co2 * 100 / 400 + "%"
    co2Bar.innerHTML = sensor_data.co2
    
    illBar.style.width = sensor_data.ill * 100 / 100 + "%"
    illBar.innerHTML = sensor_data.ill
    

    if (setAlarm) {
        alarmHandler(sensor_data.temp, alarm_data.temp[0], alarm_data.temp[1], "온도")
        alarmHandler(sensor_data.humi, alarm_data.humi[0], alarm_data.humi[1], "습도")
        alarmHandler(sensor_data.co2, alarm_data.co2[0], alarm_data.co2[1], "이산화탄소")
        alarmHandler(sensor_data.ill, alarm_data.ill[0], alarm_data.ill[1], "조도")
     
        
    }

})

socket.on('ledState', function (data) {
    led_state = data
    //console.log("LED State : " + data)

    var color = { "ON": "#FFD43B", "MOOD": "#F9DE95", "OFF": "" }
   document.getElementById("lightbulb").style.color = color[data]
    
    
})



function ledHandler(e) {
    
    var lightbulb = document.getElementById("lightbulb")
    var [ledState,color] = e.target.value.split(",")
    lightbulb.style.color = color;

    socket.emit('message',ledState)


    //console.log("LED State : "+ledState)
}



function set_alarm() {
    var tempMin = document.getElementById('temp-min').value
    var tempMax = document.getElementById('temp-max').value
    alarm_data.temp[0] = tempMin
    alarm_data.temp[1] = tempMax

    var humiMin = document.getElementById('humi-min').value
    var humiMax = document.getElementById('humi-max').value
    alarm_data.humi[0] = humiMin
    alarm_data.humi[1] = humiMax

    var co2Min = document.getElementById('co2-min').value
    var co2Max = document.getElementById('co2-max').value
    alarm_data.co2[0] = co2Min
    alarm_data.co2[1] = co2Max

    var illMin = document.getElementById('ill-min').value
    var illMax = document.getElementById('ill-max').value
    alarm_data.ill[0] = illMin
    alarm_data.ill[1] = illMax

    if (tempMin == "" || tempMin == "" || humiMin == "" || humiMax == "" || co2Min == "" || co2Max == "" || illMin == "" || illMax == "") {
        alert("Cannot set Alarm!\n[Reason] Fill all the Alarm value and try again!")
    } else {
        
        setAlarm = true
    }

    //alert("setAlarm?"+setAlarm)

}
function reset_alarm() {
    setAlarm = false

    reset_alarm_value()
}

function reset_alarm_value() {
    if (setAlarm == false) {
        document.getElementById('temp-min').value = ""
        document.getElementById('temp-max').value = ""

        document.getElementById('humi-min').value = ""
        document.getElementById('humi-max').value = ""
        
        document.getElementById('co2-min').value = ""
        document.getElementById('co2-max').value = ""
        
        document.getElementById('ill-min').value = ""
        document.getElementById('ill-max').value = ""
    }
}

function alarmHandler(sensor_val, min_val, max_val, data_type) {
    var comment = '';
    if (sensor_val <= min_val) {
        comment = data_type + "가 너무 낮습니다";

        alert(comment);
        
    } else if (sensor_val >= max_val) {
        
        comment = data_type + "가 너무 높습니다";

        alert(comment)

    }
    setAlarm = false

}