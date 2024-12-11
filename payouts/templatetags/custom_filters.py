from django import template

register = template.Library()

# Define a mapping dictionary for replacements
MAPPING = {
    'bank_name': 'Bank Name',
    'ifsc_code': 'IFSC Code',
    'account_number': 'Account Number',
    'email' : 'Email',
    'wallet_address': 'Wallet Address',
    'crypto_type': 'Cryptocurrency Type',
}

@register.filter
def replace(value, arg="_"):
    """
    Replace underscores with spaces or map keys to human-readable labels.
    """
    if isinstance(value, str):
        # First check if the value is in the mapping
        if value in MAPPING:
            return MAPPING[value]
        # Otherwise, just replace the specified character (default is '_') with a space
        return value.replace(arg, " ")
    return value
