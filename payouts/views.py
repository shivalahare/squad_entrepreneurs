from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import PaymentMethod, WithdrawalRequest, WithdrawalPolicy
from referrals.models import ReferralProfile
from .forms import PaymentMethodForm, WithdrawalRequestForm
from django.http import JsonResponse
import json

@login_required
def payout_dashboard(request):
    referral_profile = ReferralProfile.objects.get(user=request.user)
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    withdrawal_requests = WithdrawalRequest.objects.filter(user=request.user).order_by('-created_at')
    withdrawal_policy = WithdrawalPolicy.objects.first()
    
    context = {
        'available_balance': referral_profile.total_earnings,
        'payment_methods': payment_methods,
        'withdrawal_requests': withdrawal_requests,
        'withdrawal_policy': withdrawal_policy,
    }
    return render(request, 'payouts/dashboard.html', context)

@login_required
def payment_methods(request):
    payment_methods = PaymentMethod.objects.all()
    return render(request, "payouts/payment_methods.html", {"payment_methods": payment_methods})


@login_required
def add_payment_method(request):
    if request.method == 'POST':
        print("POST Data:", request.POST) 
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            print("Cleaned Data:", form.cleaned_data)
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            return redirect('payout_dashboard')  # Or wherever you want to redirect
    else:
        form = PaymentMethodForm()

    return render(request, 'payouts/add_payment_method.html', {'form': form})



# def add_payment_method(request):
#     if request.method == 'POST':
#         form = PaymentMethodForm(request.POST)
#         if form.is_valid():
#             payment_method = form.save(commit=False)
#             payment_method.user = request.user
#             payment_method.save()
#             messages.success(request, 'Payment method added successfully!')
#             return redirect('payout_dashboard')
#     else:
#         form = PaymentMethodForm()
    
#     return render(request, 'payouts/add_payment_method.html', {'form': form})


@login_required
def edit_payment_method(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            messages.success(request, "Payment method updated successfully!")
            return redirect('payout_dashboard')
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        form = PaymentMethodForm(instance=payment_method)
    
    context = {
        'form': form,
    }
    return render(request, 'payouts/edit_payment_method.html', context)

@login_required
def delete_payment_method(request, pk):
    payment_method = get_object_or_404(PaymentMethod, pk=pk, user=request.user)
    if request.method == 'POST':
        payment_method.delete()
        messages.success(request, "Payment method deleted successfully!")
        return redirect('payout_dashboard')
    
    context = {
        'payment_method': payment_method,
    }
    return render(request, 'payouts/confirm_delete.html', context)


@login_required
@transaction.atomic
def request_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                payment_method = form.cleaned_data['payment_method']
                
                # Validate withdrawal amount
                referral_profile = ReferralProfile.objects.get(user=request.user)
                if amount > referral_profile.total_earnings:
                    raise ValidationError('Insufficient balance')
                
                # Create withdrawal request
                withdrawal = WithdrawalRequest.objects.create(
                    user=request.user,
                    amount=amount,
                    payment_method=payment_method,
                    status='pending'
                )
                
                # Update available balance
                referral_profile.total_earnings -= amount
                referral_profile.save()
                
                messages.success(request, 'Withdrawal request submitted successfully!')
                return redirect('payout_dashboard')
                
            except ValidationError as e:
                messages.error(request, str(e))
    else:
        form = WithdrawalRequestForm(user=request.user)
    
    return render(request, 'payouts/request_withdrawal.html', {'form': form})

@login_required
def cancel_withdrawal(request, withdrawal_id):
    withdrawal = get_object_or_404(WithdrawalRequest, id=withdrawal_id, user=request.user)
    
    if not withdrawal.can_be_cancelled:
        messages.error(request, 'This withdrawal request cannot be cancelled.')
        return redirect('payout_dashboard')
    
    with transaction.atomic():
        # Restore the amount to user's balance
        referral_profile = ReferralProfile.objects.get(user=request.user)
        referral_profile.total_earnings += withdrawal.amount
        referral_profile.save()
        
        # Update withdrawal status
        withdrawal.status = 'cancelled'
        withdrawal.notes = 'Cancelled by user'
        withdrawal.save()
    
    messages.success(request, 'Withdrawal request cancelled successfully!')
    return redirect('payout_dashboard')