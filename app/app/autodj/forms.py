from django import forms
from django.contrib.admin.helpers import ActionForm

from common.forms import AudioAssetDownloadableCreateFormBase

from .models import AudioAsset, Playlist, Rotator


class PlaylistActionForm(ActionForm):
    playlist = forms.ModelChoiceField(Playlist.objects.all(), required=False, label=' ', empty_label='--- Playlist ---')


class RotatorActionForm(ActionForm):
    rotator = forms.ModelChoiceField(Rotator.objects.all(), required=False, label=' ', empty_label='--- Rotator ---')


class AudioAssetCreateForm(AudioAssetDownloadableCreateFormBase):
    class Meta(AudioAssetDownloadableCreateFormBase.Meta):
        model = AudioAsset


class AudioAssetUploadForm(forms.Form):
    audios = forms.FileField(
        widget=forms.FileInput(attrs={'multiple': True}), required=True, label='Audio files',
        help_text='Select multiple audio files to upload using Shift, CMD, and/or Alt in the dialog.')

    def __init__(self, *args, **kwargs):
        if Playlist.objects.exists():
            # Needs to be in base_fields because of the way AudioAssetAdmin.upload_view() passes context to template
            self.base_fields['playlists'] = forms.ModelMultipleChoiceField(
                Playlist.objects.all(), required=False, widget=forms.CheckboxSelectMultiple(),
                label='Playlist(s)', help_text="Optionally select playlists to these audio assets to. If you don't "
                'select a playlist, this asset will not be scheduled for playout by the AutoDJ')
        super().__init__(*args, **kwargs)
