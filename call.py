from modules.extraction import extract


class data:
    def __init__(self):
        pass

    def run(self):
        initial = 1514764815
        extract(initial, initial + (4) * 86385).run()

data().run()
