from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt


def home(request):
    if request.method == "POST":
        
        amount = 50000
        order_currency='INR'

        client = razorpay.Client(
            auth=("rzp_test_2gdjmciQ45GBhe", "LMeNHvU3jutDBpqmGdH9lKBh"))

        payment = client.order.create({'amount': amount, 'currency': 'INR',
                                       'payment_capture': '1'})
    return render(request, 'phonepay/index.html')

@csrf_exempt
def success(request):
    return render(request, "phonepay/success.html")