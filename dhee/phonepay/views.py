from django.shortcuts import render, get_object_or_404
import razorpay
from django.views.decorators.csrf import csrf_exempt
from item.models import Item
from django.http import JsonResponse
from django.conf import settings
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import json

@csrf_exempt
def generate_bill(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        item_name = data.get('item_name')
        amount = data.get('amount')

        # Generate PDF using ReportLab
        pdf_path = os.path.join(settings.MEDIA_ROOT, 'bills', f'bill_{name}_{item_name}.pdf')
        os.makedirs(os.path.dirname(pdf_path), exist_ok=True)

        # Create a canvas
        c = canvas.Canvas(pdf_path, pagesize=letter)

        # Set font styles
        c.setFont('Helvetica-Bold', 16)
        c.setLineWidth(1)
        
        # Add page title and address
        c.drawString(50, 770, "Invoice")
        c.setFont('Helvetica', 12)
        c.drawString(50, 750, "Dhee Fashions")
        c.drawString(50, 735, "No 123, Perambur, Chennai, TamilNadu, 600010")
        c.line(50, 725, 565, 725)  # Horizontal line under address

        # Add customer details
        c.setFont('Helvetica-Bold', 12)
        c.drawString(50, 700, "Customer Details:")
        c.setFont('Helvetica', 12)
        c.drawString(50, 680, f"Name: {name}")
        c.drawString(50, 660, f"Email: {email}")

        # Add item details
        c.setFont('Helvetica-Bold', 12)
        c.drawString(50, 630, "Item Details:")
        c.setFont('Helvetica', 12)
        c.drawString(50, 610, f"Item Name: {item_name}")
        c.drawString(50, 590, f"Amount to be Paid: {amount} INR")

        # Add delivery instructions
        c.setFont('Helvetica-Bold', 12)
        c.drawString(50, 560, "Instructions for Delivery:")
        c.setFont('Helvetica', 12)
        c.drawString(50, 540, "This bill must be shown to the delivery person upon receipt of products.")

        # Add footer with company information
        c.setFont('Helvetica', 10)
        c.drawString(50, 50, "Contact: +91-12345 45672 | Email: dheefashions@gmail.com")

        # Save the PDF
        c.save()

        bill_url = os.path.join(settings.MEDIA_URL, 'bills', f'bill_{name}_{item_name}.pdf')

        return JsonResponse({
            'success': True,
            'name': name,
            'email': email,
            'item_name': item_name,
            'amount': amount,
            'bill_url': bill_url
        })
    return JsonResponse({'success': False})



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
