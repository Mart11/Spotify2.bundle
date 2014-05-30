from objects import Objects
from utils import ViewMode, normalize


class Containers(object):
    def __init__(self, host):
        self.host = host

        self.objects = Objects(host)

    @property
    def sp(self):
        return self.host.sp

    # TODO list singles?
    def artist(self, artist, callback):
        oc = ObjectContainer(
            title2=normalize(artist.name),
            content=ContainerContent.Albums
        )

        album_uris = [al.uri for al in artist.albums if al is not None]

        @self.sp.metadata(album_uris)
        def on_albums(albums):
            for album in albums:
                oc.add(self.objects.album(album))

            callback(oc)

    def album(self, album, callback):
        oc = ObjectContainer(
            title2=normalize(album.name),
            content=ContainerContent.Tracks,
            view_group=ViewMode.Tracks
        )

        track_uris = [tr.uri for tr in album.tracks]

        @self.sp.metadata(track_uris)
        def on_tracks(tracks):
            for track in tracks:
                oc.add(self.objects.track(track))

            callback(oc)

    def playlists(self, playlists, group=None, name=None):
        oc = ObjectContainer(
            title2=normalize(name) or L("MENU_PLAYLISTS"),
            content=ContainerContent.Playlists,
            view_group=ViewMode.Playlists
        )

        for item in playlists.fetch(group):
            oc.add(self.objects.playlist(item))

        return oc

    def playlist(self, playlist):
        name = normalize(playlist.name)

        if playlist.uri.type == 'starred':
            name = L("MENU_STARRED")

        oc = ObjectContainer(
            title2=name,
            content=ContainerContent.Tracks,
            view_group=ViewMode.Tracks
        )

        for track in playlist.fetch():
            oc.add(self.objects.track(track))

        return oc

    def metadata(self, track):
        oc = ObjectContainer()
        oc.add(self.objects.track(track))

        return oc
