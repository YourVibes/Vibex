import enum




# Section controls in which section of the file the emitter should write
class Section(enum.Enum):
    HEADER    = 'header'
    FUNCTIONS = 'functions'
    CODE      = 'code'