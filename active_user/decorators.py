# from django.contrib.auth.decorators import login_required
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required


admin_login_required_test = user_passes_test(lambda u: True if u.is_admin() else False, login_url='/login')

def admin_login_required(view_func):
    decorated_view_func = login_required(admin_login_required_test(view_func), login_url='/login')
    return decorated_view_func


hamyar_login_required_test = user_passes_test(lambda u: True if u.is_hamyar() else False, login_url='/login')

def hamyar_login_required(view_func):
    decorated_view_func = login_required(hamyar_login_required_test(view_func), login_url='/login')
    return decorated_view_func

madadkar_login_required_test = user_passes_test(lambda u: True if u.is_madadkar() else False, login_url='/login')

def madadkar_login_required(view_func):
    decorated_view_func = login_required(madadkar_login_required_test(view_func), login_url='/login')
    return decorated_view_func

madadjoo_login_required_test = user_passes_test(lambda u: True if u.is_madadjoo() else False, login_url='/login')

def madadjoo_login_required(view_func):
    decorated_view_func = login_required(madadjoo_login_required_test(view_func), login_url='/login')
    return decorated_view_func
