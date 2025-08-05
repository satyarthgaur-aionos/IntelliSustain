from utils import *

# Sample test calls

def test_get_alarms():
    building = "Tower A"
    result = get_critical_alarms(building)
    print("\n[TEST] get_critical_alarms:", result)

def test_ack_alarm():
    alarm_id = "replace_with_actual_alarm_id"
    result = acknowledge_alarm(alarm_id)
    print("\n[TEST] acknowledge_alarm:", result)

def test_temperature():
    entity_type = "DEVICE"
    entity_id = "replace_with_device_id"
    result = get_temperature(entity_type, entity_id)
    print("\n[TEST] get_temperature:", result)

def test_device_publish():
    device_id = "replace_with_device_id"
    result = get_device_publish_status(device_id)
    print("\n[TEST] get_device_publish_status:", result)

if __name__ == "__main__":
    test_get_alarms()
    # test_ack_alarm()
    # test_temperature()
    # test_device_publish()