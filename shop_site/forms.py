from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from shop_site.models import Item, Coupon, Address, Category, subcategory, Dispatch, Invoice

PAYMENT_CHOICES = (
    ('S', 'Credit Or Debit Card'),
    ('CD', 'Cash On Delivery')
)

class PaymentMethodForm(forms.Form):
    payment_method = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('street_address', 'apartment_address', 'country', 'zip')
    

class CouponeForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'Promo Code',
        'aria-label' : 'Recipient\'s username',
        'aria-describedby' : 'basic-addon2'
    }))

class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()


class AddItem(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('title','price','discount_price','category','sub_category','label','item_image','description')

class AddCategory(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('category_title',)

class AddCoupon(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ('code','discount_percentage')

class AddSubcategory(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = ('category',"subcategory_title")

class DispatchForm(forms.ModelForm):
    class Meta:
        model = Dispatch
        fields = ('transpoter_name','delivery_date','invoice','order')
        
