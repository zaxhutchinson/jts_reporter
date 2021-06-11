import sys
import game
import logging
import display
import tkinter as tk

def main():
    #----------------------------------
    # VARIABLES
    gamedir = None
    mygame = None
    #----------------------------------
    # SET UP THE LOGGER
    LGFORMAT = '%(levelname)s   %(message)s'
    logging.basicConfig(
        #filename=time.strftime("%Y%m%d%H%M%S")+'_jtsrep.log',
        filename='jtsrep.log',
        filemode='w',
        format=LGFORMAT
    )

    #----------------------------------
    # Read command line args
    for arg in sys.argv:
        if 'dir' in arg or 'directory' in arg:
            print(arg)
            gamedir = arg.split('=')[1]
        elif '-d' in sys.argv or '--debug' in sys.argv:
            logging.basicConfig(
                level=logging.DEBUG,
            )

    #-----------------------------------
    # Load game files we have a directory
    if gamedir:
        mygame = game.Game(gamedir)
    else:
        logging.error("MAIN: missing game directory")
        print("Missing game directory.")

    #-----------------------------------
    # Start UI
    root = tk.Tk()
    ui = display.Display(root, mygame)
    ui.Run()

    #-----------------------------------
    # Tests of bringing things together
    # unit = GAME.units[28856]
    # unit_oob = GAME.oob.GetElement(28856)
    # uhist = unit.GetData('history')
    # for k,v in uhist.items():
    #     print(k, v.toe/unit_oob.GetData('toe'))

if __name__ == "__main__":
    main()