# from django.contrib.auth
# @login_required(login_url='login')
# def count_notification(request):
#     noti_count = Notification.objects.filter(
#         receiver=request.user, is_viewed=False).count()
#     return render(request, "groups/group_detail.html", {
#         "noti_count": noti_count
#     })
