from src.schemas.artist import ArtistSchema
from src.schemas.track import TrackSchema


class TrackWithArtists(TrackSchema):
    artists: list[ArtistSchema] | None = []


class ArtistWithTracks(ArtistSchema):
    tracks: list[TrackSchema] | None = []
