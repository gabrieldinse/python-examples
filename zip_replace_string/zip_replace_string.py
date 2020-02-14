import sys
import shutil
import zipfile
from pathlib import Path
from PIL import Image


# O metodo process files existe apenas nas classes derivadas
class ZipProcessor:
    def __init__(self, zipname):
        self.zipname = zipname
        self.temp_directory = Path("unzipped-{}".format(zipname[:-4]))

    def process_zip(self):
        self.unzip_files()
        self.process_files()
        self.zip_files()

    def unzip_files(self):
        self.temp_directory.mkdir()  # cria o diretorio/pasta
        with zipfile.ZipFile(self.zipname) as zip:  # abre o arquivo zip no modo leitura (padrao)
            zip.extractall(str(self.temp_directory))  # extrai os arquivos no diretorio

    def zip_files(self):
        with zipfile.ZipFile(self.zipname, 'w') as file:  # abre o arquivo zip no modo escrita
            for filename in self.temp_directory.iterdir():  # itera nos arquivo do diretorio
                file.write(str(filename), filename.name)  # compacta o arquivo
        shutil.rmtree(str(self.temp_directory))


class ZipReplace(ZipProcessor):
    def __init__(self, filename, search_string, replace_string):
        super().__init__(filename)
        self.search_string = search_string  # string para procurar
        self.replace_string = replace_string  # string para substituir

    def process_files(self):
        '''perform a search and replace on all files in the
        temporary directory'''
        for filename in self.temp_directory.iterdir():  # itera nos diretorios
            with filename.open() as file:
                contents = file.read()
            contents = contents.replace(
                self.search_string, self.replace_string)
            with filename.open("w") as file:
                file.write(contents)


class ScaleZip(ZipProcessor):
    def process_files(self):
        '''Scale each image in the directory to 640x480'''
        for filename in self.temp_directory.iterdir():
            im = Image.open(str(filename))
            scaled = im.resize((640, 480))
            scaled.save(str(filename))


if __name__ == "__main__":
    ScaleZip(*sys.argv[1:4]).process_zip()
