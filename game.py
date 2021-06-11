import os
import logging as lg
import math

import oob
import defs

class UnitHistory:
    def __init__(self):
        self.name = None
        self.x = None
        self.y = None
        self.toe = None
        self.fatigue = None
        self.combined_units = []

class Unit:
    def __init__( self, data=None):
        self.data = data
    def GetData(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None
    def SetData(self, k, v):
        try:
            self.data[k] = v
            return True
        except KeyError:
            return False
    def AddHistory(self, uh):
        self.data['history'].append(uh)

class ScenData:
    def __init__( self, _data={}):
        self.data = _data
    def GetData(self, key):
        try:
            return self.data[key]
        except KeyError:
            return None
    def SetData(self, k, v):
        try:
            self.data[k] = v
            return True
        except KeyError:
            return False


class Game:
    def __init__(self, directory):
        self.directory = directory
        self.scenario_name = None
        self.map_filename = None
        self.oob_filename = None
        self.pdt_filename = None
        self.victory_levels = None
        self.oob = None
        self.units = {}
        self.scen_data = {}

        self.ReadGameFiles()

    def ReadGameFiles(self):
        lg.debug("GAME: Loading game files")

        abspath = os.path.abspath(self.directory)
        #print(abspath)

        save_files = []

        with os.scandir(abspath) as it:
            for entry in it:
                if entry.is_file():
                    file_extension = entry.name[-4:]
                    if file_extension=='.oob':
                        self.oob = oob.OOB(entry.path)
                    elif file_extension=='.btl':
                        save_files.append(
                            (entry.name[:-4],entry.path)
                        )

        save_files = sorted(save_files,key=lambda x: x[0])
        
        for f in save_files:
            fileh = open(f[1], 'r')
            sdata = self.ReadBtlFile(f[0], fileh)
            fileh.close()
                    
    def ReadBtlFile(self, fname, fileh):
        sdata = {}

        self.ReadBtlFileHeader(fname, fileh, sdata)

        self.ReadBtlFileBody(fname, fileh)
    
        return sdata

    def ReadBtlFileHeader(self, fname, fileh, sdata):
        header_lines = []
        for i in range(15):
            header_lines.append(fileh.readline().strip())
        
        # LINE 1
        # I do not know what the first line is. Just an int.
        # Left as a string
        sdata['unknown_1_0'] = header_lines[0]

        # LINE 2
        # If we haven't stored the scenario name yet.
        if not self.scenario_name:
            self.scenario_name = header_lines[1]

        # LINE 3
        # Time/turn data
        splt = header_lines[2].split()
        sdata['year'] = int(splt[0])
        sdata['month'] = int(splt[1])
        sdata['day'] = int(splt[2])
        sdata['hour'] = int(splt[3])
        sdata['player_active'] = int(splt[4])
        sdata['unknown_2_0'] = int(splt[5])
        sdata['cur_turn'] = int(splt[6])
        sdata['max_turn'] = int(splt[7])

        # LINE 4
        # Victory point data
        if not self.victory_levels:
            splt = header_lines[3].split()
            self.victory_levels = []
            for s in splt:
                self.victory_levels.append(int(s))

        # LINE 5
        # Player Order by Side and supply
        splt = header_lines[4].split()
        sdata['player_order'] = [int(splt[0]), int(splt[1])]
        sdata['supply0'] = int(splt[2])
        sdata['supply1'] = int(splt[3])

        # LINE 6 - 12
        # I haven't figured out what these are. Will
        # separate them out as I do.
        sdata['unknown_6_0'] = header_lines[5]
        sdata['unknown_7_0'] = header_lines[6]
        sdata['unknown_8_0'] = header_lines[7]
        sdata['unknown_9_0'] = header_lines[8]
        sdata['unknown_10_0'] = header_lines[9]
        sdata['unknown_11_0'] = header_lines[10]
        sdata['unknown_12_0'] = header_lines[11]

        # LINE 13
        # Map file name
        if not self.map_filename:
            self.map_filename = header_lines[12]

        # LINE 14
        # OOB file name
        if not self.oob_filename:
            self.oob_filename = header_lines[13]

        # LINE 15
        if not self.pdt_filename:
            self.pdt_filename = header_lines[14]

    def ReadBtlFileBody(self, fname, fileh):
        while True:
            
            # Read a line and get the line code
            line = fileh.readline().strip().split()
            line_code = int(line[0])

            # I think the single 0 indicates that
            # that the body section is done.
            # Or at least that the section which uses
            # these line codes is finished.
            if line_code==0:
                break
            elif line_code==1:
                self.ReadBTL_1(fname, line)
            elif line_code==2:
                pass
            elif line_code==3:
                pass
            elif line_code==4:
                pass
            elif line_code==5:
                pass

    def ReadBTL_1(self, fname, line):
        UNIT_ID = int(line[3])

        if UNIT_ID not in self.units:
            data = {
                'ID':UNIT_ID,
                'history':[]
            }
            self.units[UNIT_ID] = Unit(data)

        uh = UnitHistory()
        uh.name = fname
        uh.x = int(line[1])
        uh.y = int(line[2])
        uh.toe = int(line[6])
        uh.fatigue = int(line[7])

        # Need to check if this unit is combined with
        # other units.
        if len(line) > 11:
            index = 11
            while index < len(line):
                if line[index] != '-1':
                    uh.combined_units.append(int(line[index]))
                index+=1

        self.units[UNIT_ID].AddHistory(uh)

    def GetFormationDataByTurnRecursive(self, turn, ID):

        open_list = [ID]
        data = {
            "strength":0,
            "fatigue":0
        }
        strength=[]
        fatigue=[]

        while len(open_list) > 0:
            nextID = open_list[0]
            open_list = open_list[1:]

            oobele = self.oob.GetElement(nextID)
                
            if oobele.GetData('etype')==oob.EType.FORMATION:
                if len(oobele.GetData('CIDS')) > 0:
                    open_list = open_list + oobele.GetData('CIDS')
                
            elif oobele.GetData('etype')==oob.EType.UNIT:
                if nextID in self.units:
                    max_strength = oobele.GetData('toe')

                    unit_hist = self.units[nextID].GetData('history')
                    cur_strength = 0
                    cur_fatigue = 0
                    if len(unit_hist) > 0:
                        cur_strength = unit_hist[turn].toe
                        cur_fatigue = unit_hist[turn].fatigue

                        if len(unit_hist[turn].combined_units) > 0:
                            for u in unit_hist[turn].combined_units:
                                comb_oobele = self.oob.GetElement(u)
                                if not comb_oobele:
                                    print(u)
                                max_strength += comb_oobele.GetData('toe')

                    strength.append(cur_strength/max_strength)
                    fatigue.append(cur_fatigue/defs.MAXIMUM_FATIGUE)
        if len(strength) > 0:
            data['strength']=sum(strength) / len(strength)
        if len(fatigue) > 0:
            data['fatigue']=sum(fatigue) / len(fatigue)

        return data