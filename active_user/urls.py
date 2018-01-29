from django.conf.urls import url
from active_user import views

urlpatterns = [
    url(r'^letter_madadkar_add_madadjoo$', views.letter_madadkar_add_madadjoo, name='letter_madadkar_add_madadjoo'),
    url(r'^home_madadkar$', views.home_madadkar, name='home_madadkar'),
    url(r'^home_hamyar$', views.home_hamyar, name='home_hamyar'),
    url(r'^home_madadjoo$', views.home_madadjoo, name='home_madadjoo'),
    url(r'^home_admin$', views.home_admin, name='home_admin'),
    url(r'^show_madadjoo$', views.show_madadjoo, name='show_madadjoo'),
    url(r'^show_madadjoo_hamyar$', views.show_madadjoo_hamyar, name='show_madadjoo_hamyar'),
    url(r'^edit_madadjoo$', views.edit_madadjoo, name='edit_madadjoo'),
    url(r'^add_madadjoo', views.add_madadjoo, name='add_madadjoo'),
    url(r'^show_a_madadjoo$', views.show_a_madadjoo, name='show_a_madadjoo'),
    url(r'^show_a_madadjoo_hamyar$', views.show_a_madadjoo_hamyar, name='show_a_madadjoo_hamyar'),
    url(r'^show_a_hamyar$', views.show_a_hamyar, name='show_a_hamyar'),
    url(r'^send_letter$', views.send_letter, name='send_letter'),
    url(r'^send_delete_letter$', views.send_delete_letter, name='send_delete_letter'),
    url(r'^send_letter_hamyar$', views.send_letter_hamyar, name='send_letter_hamyar'),
    url(r'^inbox_madadkar$', views.inbox_madadkar, name='inbox_madadkar'),
    url(r'^inbox_hamyar$', views.inbox_hamyar, name='inbox_hamyar'),
    url(r'^inbox_madadjoo$', views.inbox_madadjoo, name='inbox_madadjoo'),
    url(r'^show_hamyar_hamyar$', views.show_hamyar_information, name='show_hamyar_hamyar'),
    url(r'^edit_hamyar_hamyar', views.edit_hamyar_information, name='edit_hamyar_hamyar'),
    url(r'^madadjoo_report$', views.show_madadjoo_report, name='madadjoo_report'),
    url(r'^payment_reports$', views.payment_reports, name='payment_reports'),
    url(r'^select_madadjoo$', views.select_madadjoo, name='select_madadjoo'),
    url(r'^show_hamyar$', views.show_hamyar, name='show_hamyar'),
    url(r'^show_a_hamyar_madadjoo$', views.show_a_hamyar_madadjoo, name='show_a_hamyar_madadjoo'),
    url(r'^show_a_madadkar_madadjoo$', views.show_a_madadkar_madadjoo, name='show_a_madadkar_madadjoo'),
    url(r'^payment_reports_madadjoo$', views.payment_reports_madadjoo, name='payment_reports_madadjoo'),
    url(r'^send_letter_hamyar_madadjoo', views.send_letter_hamyar_madadjoo, name='send_letter_hamyar_madadjoo'),
    url(r'^send_request_madadkar', views.send_request_madadkar, name='send_request_madadkar'),
    url(r'^send_gratitude_letter', views.send_gratitude_letter, name='send_gratitude_letter'),
    url(r'^show_madadjoo_information', views.show_madadjoo_information, name='show_madadjoo_information'),
    url(r'^show_madadjoo_admin', views.show_madadjoo_admin, name='show_madadjoo_admin'),
    url(r'^show_madadkar_admin', views.show_madadkar_admin, name='show_madadkar_admin'),
    url(r'^show_hamyar_admin', views.show_hamyar_admin, name='show_hamyar_admin'),
    url(r'^show_a_madadjoo_admin', views.show_a_madadjoo_admin, name='show_a_madadjoo_admin'),
    url(r'^show_a_madadkar_admin', views.show_a_madadkar_admin, name='show_a_madadkar_admin'),
    url(r'^show_a_hamyar_admin', views.show_a_hamyar_admin, name='show_a_hamyar_admin'),
    url(r'^edit_a_madadjoo_admin', views.edit_a_madadjoo_admin, name='edit_a_madadjoo_admin'),
    url(r'^edit_a_madadkar_admin', views.edit_a_madadkar_admin, name='edit_a_madadkar_admin'),
    url(r'^edit_a_hamyar_admin', views.edit_a_hamyar_admin, name='edit_a_hamyar_admin'),
    url(r'^add_a_madadjoo_admin', views.add_a_madadjoo_admin, name='add_a_madadjoo_admin'),
    url(r'^add_a_madadjoo_madadkar', views.add_a_madadjoo_madadkar, name='add_a_madadjoo_admin'),
    url(r'^add_a_madadkar_admin', views.add_a_madadkar_admin, name='add_a_madadkar_admin'),
    url(r'^add_a_hamyar_admin', views.add_a_hamyar_admin, name='add_a_hamyar_admin'),
    url(r'^inbox_admin', views.inbox_admin, name='inbox_admin'),
    url(r'^payment_reports_admin$', views.payment_reports_admin, name='payment_reports_admin'),
    url(r'^activity_report_admin$', views.activity_report, name='activity_report_admin'),
    url(r'^madadjoo_paid_report$', views.madadjoo_paid_report, name='madadjoo_paid_report'),
    url(r'^support_a_madadjoo_hamyar$', views.support_a_madadjoo, name='support_a_madadjoo'),
    url(r'^letter_madadjoo_content_madadkar$', views.letter_madadjoo_content_madadkar, name='letter_madadjoo_content_madadkar'),
    url(r'^letter_mtoh_content_madadkar$', views.letter_mtoh_content_madadkar, name='letter_mtoh_content_madadkar'),
    url(r'^letter_htom_content_madadkar$', views.letter_htom_content_madadkar, name='letter_htom_content_madadkar'),
    url(r'^delete_letter_madadkar$', views.delete_letter_madadkar, name='delete_letter_madadkar'),
    url(r'^delete_letter_hamyar$', views.delete_letter_hamyar, name='delete_letter_hamyar'),
    url(r'^delete_madadjoo_letter_content_hamyar', views.delete_madadjoo_letter_content_hamyar, name='delete_madadjoo_letter_content_hamyar'),
    url(r'^letter_content_hamyar$', views.letter_content_hamyar, name='letter_content_hamyar'),
    url(r'^letter_content_madadjoo$', views.letter_content_madadjoo, name='letter_content_madadjoo'),
    url(r'^confirm_madadjoo_hamyar_letter', views.confirm_madadjoo_hamyar_letter, name='confirm_madadjoo_hamyar_letter'),
    url(r'^confirm_hamyar_madadjoo_letter', views.confirm_hamyar_madadjoo_letter, name='confirm_hamyar_madadjoo_letter'),
    url(r'^madadkar_panel', views.madadkar_panel, name='madadkar_panel'),
    url(r'^hamyar_panel', views.hamyar_panel, name='hamyar_panel'),
    url(r'^madadjoo_panel', views.madadjoo_panel, name='madadjoo_panel'),
    url(r'^admin_panel', views.admin_panel, name='admin_panel'),
    url(r'^confirm_madadjoo_admin', views.confirm_madadjoo_admin, name='confirm_madadjoo_admin'),
    url(r'^urgent_need_letters', views.urgent_need_letters, name='urgent_need_letters'),
    url(r'^confirm_need_admin', views.confirm_need_admin, name='confirm_need_admin'),
    url(r'^warning_letter_admin', views.warning_letter_admin, name='warning_letter_admin'),
    url(r'^warning_content_madadkar', views.warning_content_madadkar, name='warning_content_madadkar'),
]
