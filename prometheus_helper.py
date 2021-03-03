import string
import random
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway,Counter


class prometheus_helper:
    def __init__(self):
        self.registry = CollectorRegistry()
        self.sns_failure_counter = Counter('sns_failures', 'SNS Failure counter',registry=self.registry)
        self.dynamo_db_failure_counter = Counter('sns_failures', 'SNS Failure counter', registry=self.registry)
        self.sns_success_counter = Counter('sns_success','SNS Success counter',registry=self.registry)
        self.dynamo_db_success_counter = Counter('dynamo_db_counter','dynamo_db',registry=self.registry)
        self.char_set = string.ascii_uppercase + string.digits

    def increment_sns_counters(self,success=True):
        if success:
            self.sns_success_counter.inc(1)
        else:
            self.sns_failure_counter.inc(1)


    def increment_dynamo_db_counters(self,success=True):
        if success:
            self.dynamo_db_success_counter.inc(1)
        else:
            self.dynamo_db_failure_counter.inc(1)

    def push_metric(self):
        result_str = ''.join(random.choice(self.char_set) for i in range(6))
        push_to_gateway('localhost:9091', job=result_str, registry=self.registry)