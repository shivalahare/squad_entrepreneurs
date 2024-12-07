from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from io import BytesIO
from .models import Payment
from subscriptions.models import Subscription
import qrcode
import base64


@login_required
def payment_page(request, order_id):
    """
    Display the payment page with the UPI QR Code and handle the payment ID submission.
    """
    # Get the subscription details based on the order ID
    subscription = get_object_or_404(Subscription, order_id=order_id)

    # Generate the UPI QR Code dynamically
    upi_id = "your_upi_id@bank"  # Replace with your actual UPI ID
    upi_string = f"upi://pay?pa={upi_id}&pn=Your+Business+Name&am={subscription.plan.price}&cu=INR"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(upi_string)
    qr.make(fit=True)
    qr_image = qr.make_image(fill="black", back_color="white")

    # Convert the QR code image to a format usable in the template
    buffer = BytesIO()
    qr_image.save(buffer, format="PNG")
    qr_code_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # Check if a Payment record already exists
    payment = Payment.objects.filter(subscription=subscription).first()
    if not payment:
        # Create a new Payment record
        payment = Payment.objects.create(
            user=request.user,
            subscription=subscription,
            amount=subscription.plan.price,
            status='pending'
        )

    # Handle form submission for payment ID
    if request.method == "POST":
        payment_id = request.POST.get("payment_id")
        
        # Assuming you would verify the payment ID here (replace with actual verification)
        if payment_id:  # Add actual payment verification logic here
            # Update Payment record
            payment.payment_id = payment_id
            payment.status = 'completed'
            payment.save()

            # Update Subscription record
            subscription.is_active = True  # Mark the subscription as active
            subscription.payment_id = payment_id  # Save the payment ID in Subscription
            subscription.save()

            # Redirect to a subscription list or success page
            return redirect("subscription_list")  # Replace with your success page URL

    # Render the payment page
    return render(
        request,
        "payments/payment_page.html",
        {
            "subscription": subscription,
            "qr_code_data": qr_code_data,
            "upi_id": upi_id,
            "payment": payment,  # Pass payment details to the template
        },
    )


@csrf_exempt
def razorpay_webhook(request):
    """
    Handle Razorpay webhook events.
    """
    payload = json.loads(request.body)
    event = payload.get("event")

    if event == "payment.captured":
        payment_data = payload["payload"]["payment"]["entity"]
        order_id = payment_data["order_id"]
        payment_id = payment_data["id"]

        # Activate the subscription
        subscription = Subscription.objects.filter(order_id=order_id).first()
        if subscription:
            subscription.is_active = True
            subscription.start_date = now()
            subscription.payment_id = payment_id
            subscription.save()

            return JsonResponse({"status": "success"})

    return JsonResponse({"error": "Unhandled event"}, status=400)
