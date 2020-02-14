import abc


class MediaLoader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def play(self):
        pass

    @abc.abstractproperty
    def ext(self):
        pass
    
    @property
    @abc.abstractmethod
    def prop(self):
        pass

    # It is basically saying that any class that supplies concrete
    # implementations of all the abstract attributes of this ABC should be
    # considered a subclass of MediaLoader.
    # This special method is called by the Python interpreter to answer the
    # question, Is the class C a subclass of this class?
    @classmethod
    def __subclasshook__(cls, C):
        if cls is MediaLoader:
            # pega todos os atributos da classe
            attrs = set(dir(C))
            # verifica se a classe tem os todos atributos de cls e talvez mais.
            # OBS: 'duck typing' (tem atributos de uma classe mesmo sem
            # heranca? -> PERTENCE A CLASSE!)
            if attrs.issuperset(set(cls.__abstractmethods__)):
                return True

        return NotImplemented


class NotExplicitlyDerived:
    ext = '.format'

    def play(self):
        print('defined')
        
    @property
    def prop(self):
        return [1, 2, 3]


# DUCK TYPING
# Diz que a classe e derivada de MediaLoader sem ser explicitamente derivada,
# e sim por apresentar todos os metodos e atributos que devem ser implementados
# em qualquer classe derivada de MediaLoader
print(issubclass(NotExplicitlyDerived, MediaLoader))
print(isinstance(NotExplicitlyDerived(), MediaLoader))

