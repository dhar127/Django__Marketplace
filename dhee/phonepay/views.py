from django.shortcuts import render, get_object_or_404
import razorpay
from django.views.decorators.csrf import csrf_exempt
from item.models import Item
import pdfkit
from django.http import JsonResponse


def home(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == "POST":
        amount = 50000  # Convert to paise
        order_currency = 'INR'

        client = razorpay.Client(
            auth=("rzp_test_2gdjmciQ45GBhe", "LMeNHvU3jutDBpqmGdH9lKBh"))

        payment = client.order.create({'amount': amount, 'currency': order_currency, 'payment_capture': '1'})
        
        return render(request, 'phonepay/index.html', {
            'item': item,
            'payment': payment
        })

    return render(request, 'phonepay/index.html', {
        'item': item
    })

@csrf_exempt
def success(request):
    return render(request, "phonepay/success.html")


@csrf_exempt
def generate_bill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        payment_id = data.get('payment_id')
        name = data.get('name')
        email = data.get('email')
        item_name = data.get('item_name')
        amount = data.get('amount')

        # Generate the PDF bill
        html_content = render_to_string('bill_template.html', {
            'payment_id': payment_id,
            'name': name,
            'email': email,
            'item_name': item_name,
            'amount': amount
        })
        pdf_file = pdfkit.from_string(html_content, False)
        bill_url = f'/path/to/bills/{payment_id}.pdf'

        # Save the PDF to a file (for simplicity, save to a static location)
        with open(bill_url, 'wb') as f:
            f.write(pdf_file)

        return JsonResponse({'success': True, 'bill_url': bill_url})
    return JsonResponse({'success': False})

