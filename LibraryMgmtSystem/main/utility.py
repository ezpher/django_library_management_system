from django.utils import timezone

#TODO: to use a formula to generate a fixed-length unique transaction ref; 
# currently based on timestamp which is not guaranteed to be unique e.g. parallel-execution environment
# also display of transaction ref will not reflect current time, but time that transaction ref was generated
def get_transaction_ref():

    tz_datetime = timezone.now().strftime('%Y-%m%d-%H%M%S')

    return f'T{tz_datetime}'