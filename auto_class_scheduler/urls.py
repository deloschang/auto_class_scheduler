from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'app.views.home', name='home'),
     url(r'^logged-in/$', 'app.views.loggedin', name='loggedin'),
     url(r'', include('social_auth.urls')),

    # url(r'^auto_class_scheduler/', include('auto_class_scheduler.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
