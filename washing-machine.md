# Washing machine state

## START
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Start"
}

## READY
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Ready"
}

## FILLWATER
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "FillWater_ON"
}

## HEATWATER
topic:v1cdti/app/set/6310301009/model-01/sn-01
payload: {
    "action"    :   "set",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "HeatWater_ON"
}

## WASH
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Wash_ON" 
}

## RINSE
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Rinse_ON"
}

## SPIN
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Spin_ON"
}

# Operation state

## DOORCLOSE
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "set",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "DoorClose"
}

## WATERFULLLEVEL
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "WaterFullLevel"
}

## TEMPERATUREREACHED
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "TemperatureRearched"
}


# FAULT state
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Fault"
}
## TIMEOUT
topic:v1cdti/app/get/6310301009/model-01/sn-01
payload: {
    "action"    :   "get",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "TimeOut"
}

## OUTOFBALANCE
topic:v1cdti/app/set/6310301009/model-01/sn-01
payload: {
    "action"    :   "set",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "TimeOut"
}

## MOTORFAILURE
topic:v1cdti/app/set/6310301009/model-01/sn-01
payload: {
    "action"    :   "set",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "Fault"
}

## FAULTCLEARED
topic:v1cdti/app/set/6310301009/model-01/sn-01
payload: {
    "action"    :   "set",
    "project"   :   "6310301009",
    "model"     :   "model-01",
    "serial"    :   "sn-01",
    "name"      :   "Status",
    "value"     :   "FAULTCLEARED"
}