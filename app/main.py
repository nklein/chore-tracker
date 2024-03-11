import test.buttons as btest

from semma_qt.factory import LEDButtonFactory
from sim.factory import LEDButtonFactory as SimLEDButtonFactory

def main():
    print("Making button factory")
    if False:
        factory = LEDButtonFactory()
    else:
        factory = SimLEDButtonFactory()
    print("Trying buttons")
    btest.tryButtons(factory)

if __name__ == "__main__":
    main()
