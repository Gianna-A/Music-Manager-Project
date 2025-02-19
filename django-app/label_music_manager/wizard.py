# If you wish to use data_wizard during development and testing, please feel 
# free to do so. This does not carry any marks but may help you as you work on
# the project.

#import data_wizard
import data_wizard
from .models import Song, Album, AlbumTrackListItem, MusicManagerUser

data_wizard.register(Song)
data_wizard.register(Album)
data_wizard.register(AlbumTrackListItem)
data_wizard.register(MusicManagerUser)