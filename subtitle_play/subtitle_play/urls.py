from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'patch_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^$',  'django.contrib.auth.views.login',   {'template_name':'login.html'}), 
    url(r'^accounts/login/$',   'django.contrib.auth.views.login',  {'template_name':'login.html'}), 
)



urlpatterns += patterns('subtitle_play.views',
    url(r'^auth_login/$',  'auth_login'), 
    url(r'^auth_logout/$',  'auth_logout'), 
    #upload
    url(r'^upload_file/(?P<target>(mv|subtitle))/$',  'upload_file'), 
    url(r'^dispatch/$',  'dispatch'), 
    url(r'^config/$',  'config'), 
    url(r'^controllor/$',  'controllor'), 
    url(r'^show/$',  'show'), 
    url(r'^get_mv_template/$',  'get_mv_template'), 
    url(r'^get_subtitle_template/$',  'get_subtitle_template'), 
    url(r'^post_music/$',  'post_music'), 
)

















