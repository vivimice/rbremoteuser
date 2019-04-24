import logging
import re
from django import forms
from django.contrib import auth
from djblets.siteconfig.forms import SiteSettingsForm
from djblets.siteconfig.models import SiteConfiguration
from django.utils.translation import ugettext_lazy as _
from reviewboard.accounts.models import User
from reviewboard.accounts.backends import AuthBackend

class RemoteUserMiddleware(object):
    """Middleware that authenticates a user using REMOTE_USER CGI variable.
    """
    def process_request(self, request):
        siteconfig = SiteConfiguration.objects.get_current()

        if siteconfig.get('auth_backend') != RemoteUserBackend.backend_id:
            return

        try:
            username = request.META['REMOTE_USER']
        except KeyError:
            if request.user.is_authenticated():
                self._remove_invalid_user(request)
            return

        if request.user.is_authenticated():
            if request.user.get_username() == username:
                return
            else:
                self._remove_invalid_user(request)

        user = auth.authenticate(remote_user=username)
        if user:
            request.user = user
            auth.login(request, user)

    def _remove_invalid_user(self, request):
        auth.logout(request)

class RemoteUserBackend(AuthBackend):
    """Authenticate a user using REMOTE_USER CGI variable

    This backend relies on the RemoteUserMiddleware to extract REMOTE_USER 
    variable from django request
    """

    backend_id = 'remoteuser'
    name = _('RemoteUser')

    settings_form = RemoteUserSettingsForm
    supports_registration = False
    supports_change_name = True
    supports_change_email = True
    supports_change_password = False

    _siteconfig = SiteConfiguration.objects.get_current()

    def authenticate(self, remote_user, **kwargs):
        username = remote_user.strip()

        """Check white list"""
        if (self._is_user_in_whitelist(username)):
            return None

        return self.get_or_create_user(username)

    def get_or_create_user(self, username):
        """Get an existing user, or create one if not exist"""
        try:
            return User.objects.get(username=username.strip())

        except User.DoesNotExist:
            user = User(username=username, password='')
            user.is_staff = False
            user.is_superuser = False
            user.set_unusable_password()
            user.save()
            return user

    def _is_user_in_whitelist(self, username):
        whitelist = self._siteconfig.get('auth_rbremoteuser_whitelist_users')
        try:
            return whitelist.index(username) >= 0
        except:
            return False

class RemoteUserSettingsForm(SiteSettingsForm):

    whitelist_users = forms.CharField(
        label='LocalUsers',
        help_text='A comma-seperated list of users '
            'which are by-passed by this module. '
            '(So built-in modules will be used '
            'against these users)',
        required=False
    )

    def load(self):
        super(RemoteUserSettingsForm, self).load()
        try:
            self.fields['whitelist_users'].initial = ', '.join(self.siteconfig.get('auth_rbremoteuser_whitelist_users'))
        except Exception, e:
            logging.error(e)
            self.fields['whitelist_users'].initial = 'admin'


    def save(self):
        self.siteconfig.set('auth_rbremoteuser_whitelist_users', re.split(r',\s*', self.cleaned_data['whitelist_users']))
        super(RemoteUserSettingsForm, self).save()

    class Meta:
        title = 'RemoteUser Authentication Settings'
        save_blacklist = ('whitelist_users',)
