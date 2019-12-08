import get_running_service_names
import get_logs_from_services

service_names = get_running_service_names.get_service_names()
service_location_names = get_running_service_names.get_location_names(service_names)

old_logs = []


while True:
    all_logs = get_logs_from_services.apply(service_location_names)
    new_logs = [x for x in all_logs if x not in old_logs]
    for log in new_logs:
        print log
    old_logs = all_logs





