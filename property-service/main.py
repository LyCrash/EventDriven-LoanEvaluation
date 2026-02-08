from shared.rabbitmq import consume_event, publish_event
from shared.events import CREDIT_CHECKED, PROPERTY_EVALUATED
import random

def evaluate_property(loan):
    estimated_value = random.randint(100000, 500000)
    loan["property_value"] = estimated_value

    publish_event(PROPERTY_EVALUATED, loan)

consume_event(CREDIT_CHECKED, evaluate_property)
