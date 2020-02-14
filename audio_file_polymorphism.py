class AudioFile:
    def __init__(self, filename):
        if not filename.endswith(self.extension):
            raise Exception('Invalid file format.')

        self.filename = filename

    def play(self):
        raise NotImplementedError()


class MP3File(AudioFile):
    extension = 'mp3'

    def play(self):
        print('Playing {} audio name {}'.format(self.__class__.extension,
                                                self.filename))


class WavFile(AudioFile):
    extension = 'wav'

    def play(self):
        print('Playing {} audio name {}'.format(self.__class__.extension,
                                                self.filename))


a = MP3File('musica.mp3')
b = WavFile('musica.wav')
# c = MP3File('musica.mp4') # errado!
# d = WavFile('musica.mp3') # errado!
a.play()
b.play()
