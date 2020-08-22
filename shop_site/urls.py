from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.HomeView, name="home"),
    url(r'^product/(?P<pk>\d+)/$', views.ItemDetailView, name="product"),
    url(r'^checkout/$', views.checkout, name="checkout"),
    url(r'^add-to-cart/(?P<pk>\d+)/$', views.add_to_Cart, name="add_to_cart"),
    url(r'^add-single-to-cart/(?P<pk>\d+)/$', views.add_single_to_Cart, name="add_single_to_cart"),
    url(r'^plus-quantity/(?P<pk>\d+)/$', views.plus_quantity, name="plus_quantity"),
    url(r'^minus-quantity/(?P<pk>\d+)/$', views.minus_quantity, name="minus_quantity"),
    url(r'^remove-from-cart/(?P<pk>\d+)/$', views.remove_from_cart, name="remove_from_cart"),
    url(r'^remove-single-item-from-cart/(?P<pk>\d+)/$', views.remove_single_item_from_cart, name="remove_single_item_from_cart"),
    url(r'^decrease-quantity/(?P<pk>\d+)/$', views.decrease_quantity, name="decrease_quantity"),
    url(r'^order-summary/$', views.OrderSummaryView, name="order-summary"),
    url(r'^reset-cart/(?P<pk>\d+)/$', views.reset_cart, name="reset-cart"),
    url(r'^payment/$', views.payment, name="payment"),
    url(r'^charge/$', views.charge, name="charge"),
    url(r'^redem-coupon/$', views.redem_coupon, name="redem-coupon"),
    url(r'^change-promo/$', views.change_promo, name="change-promo"),
    url(r'^request-refund/$', views.Request_Refund, name='request-refund'),
    url(r'^add-item/$', views.add_item, name='admin-panel'),
    url(r'^add-category/$', views.add_category, name='add-category'),
    url(r'^add-subcategory/$', views.add_subcategory, name='add-subcategory'),
    url(r'^add-coupon/$', views.add_coupon, name='add-coupon'),
    url(r'^order-history/$', views.order_history, name="order-history"),
    url(r'^invoice-action/$', views.invoice_action, name="invoice-action"),
    url(r'^invoice/(?P<pk>\d+)/$', views.invoice, name="invoice"),
    url(r'^invoice-view/(?P<pk>\d+)/$', views.Invoice_View, name="invoice-view"),
    url(r'^create-dispatch/(?P<pk>\d+)/$', views.create_dispatch, name="create-dispatch"),
    url(r'^dispatch-view/(?P<pk>\d+)/$', views.Dispatch_View, name="dispatch-view"),


    url(r'^address-select/$', views.address_select, name="address-select"),
    url(r'^checkout-system/$', views.checkout_system, name="checkout-system"),
    url(r'^get-payment-method/$', views.get_payment_method, name='get-payment-method'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)