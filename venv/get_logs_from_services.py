import itertools
from datetime import datetime, timedelta


def flatten(list_of_lists):
    return list(itertools.chain.from_iterable(list_of_lists))


def get_logs_from_service(service_name):
    try:
        file = open("/var/tmp/%s_LOCAL/logs/stdout.txt" % service_name, "r")
        logs = file.readlines()
        file.close()

        logs_with_date = []
        prev_date = datetime.now()

        for log in logs:
            service = "[" + service_name + "] "
            try:
                date_from_log = get_date_from_log(log)
                prev_date = date_from_log
                logs_with_date.append((date_from_log, service + log))
            except:
                logs_with_date.append((prev_date, service + log))

        return logs_with_date
    except:
        return []


def combine_all_logs(service_names):
    jagged_logs = []
    for service in service_names:
        try:
            jagged_logs.append(get_logs_from_service(service))
        except:
            print ("oops " + str(service))

    return flatten(jagged_logs)


def get_date_from_log(log):
    split = log.split(" ")
    date_string = split[0]
    time_string = split[1]
    date_time_obj = datetime.strptime(date_string + " " + time_string, '%Y-%m-%d %H:%M:%S,%f')
    return date_time_obj


def order_logs_by_date(logs):
    last_hour = filter(lambda x: x[0] > datetime.now() - timedelta(hours=1), logs)
    return sorted(last_hour, key=lambda x: x[0])


def apply(service_names):
    logs = combine_all_logs(service_names)
    ordered_logs = order_logs_by_date(logs)
    return map(lambda x: x[1], ordered_logs)

