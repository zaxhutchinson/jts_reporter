import enum
import string

import defs

class EType(enum.Enum):
    FORMATION=0,
    UNIT=1

class Side(enum.Enum):
    ALLIES=0,
    AXIS=1

class OOBElement:
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

class OOBTreeNode:
    def __init__(self, ID, parent, nation):
        self.ID = ID
        self.parent = parent
        self.children = []
        self.nation = nation
    def AddChildren(self, child):
        self.children.append(child)
    def GetID(self):
        return self.ID
    def GetParent(self):
        return self.parent
    def GetChildren(self):
        return self.children

class OOB:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}
        self.elements = {}
        self.tree = []
        # Parse the oob file.
        self.ReadOOBFile()

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

    def AddElement(self, element):
        key = element.GetData('ID')
        if key:
            self.elements[key]=element
    def GetElement(self, key):
        if key in self.elements:
            return self.elements[key]
        else:
            return None
    def GetEtypes(self, etype):
        etype_dict = {}
        for k,v in self.data.items():
            if v.GetData('etype')==etype:
                etype_dict[k]=v


    def ReadOOBFile(self):

        with open(self.filename, 'r') as f:

            # Read the unknown lines at the top of the oob file.
            unknown0 = int(f.readline().strip())
            unknown1 = int(f.readline().strip())
            self.SetData('unknown0',unknown0)
            self.SetData('unknown1',unknown1)

            parent_ids = []
            treenode = None
            nation = []
            line_counter=3
            for line in f:


                # If empty line
                if len(line)==0:
                    line_counter +=1
                    continue
                # if BEGIN
                elif line.strip().lower()=='begin':
                    pass
                # elif END
                elif line.strip().lower()=='end':
                    parent_ids.pop()
                    nation.pop()
                    # If we've popped off all pids, then we've
                    # finished processing a nation. Store the
                    # nation in the tree and reset.
                    if treenode.GetParent()==None:
                        self.tree.append(treenode)
                    treenode = treenode.GetParent()

                    
                # elif unit
                else:
                    # Find the start of the ID.
                    # Necessary because the ftype can contain spaces.
                    id_start_index = 0
                    for i in range(len(line)):
                        if line[i] in string.digits:
                            id_start_index=i
                            break

                    ftype = line[:id_start_index].strip()
                    line = line[id_start_index:].strip()
                    splt_line = line.split()

                    

                    data = {}

                    if ftype[-1]=='.':

                        ftype = ftype[:-1]

                        data['etype'] = EType.UNIT
                        data['ftype'] = ftype
                        data['nation'] = nation[-1]

                        if data['nation'] in defs.ALLIES:
                            data['side'] = Side.ALLIES
                        elif data['nation'] in defs.AXIS:
                            data['side'] = Side.AXIS

                        data['ID'] = int(splt_line[0])
                        data['unit_type'] = splt_line[1]
                        data['move_type'] = splt_line[2]
                        data['toe'] = int(splt_line[3])
                        data['morale_code'] = int(splt_line[4])
                        data['hard_attack'] = int(splt_line[5])
                        data['hard_dist'] = int(splt_line[6])
                        data['unknown0'] = int(splt_line[7])
                        data['soft_attack'] = int(splt_line[8])
                        data['soft_dist'] = int(splt_line[9])
                        data['unknown1'] = int(splt_line[10])
                        data['aa_attack'] = int(splt_line[11])
                        data['aa_dist'] = int(splt_line[12])
                        data['unknown2'] = int(splt_line[13])
                        data['unknown3'] = int(splt_line[14])
                        data['assault'] = int(splt_line[15])
                        data['speed'] = int(splt_line[16])
                        data['unknown4'] = int(splt_line[17])
                        names = line.split(maxsplit=18)[-1]
                        splt_names = names.split(',')
                        data['name'] = splt_names[0].strip()
                        data['equip_name'] = splt_names[1].split()
                        data['PID'] = parent_ids[-1]
                        self.GetElement(data['PID']).GetData('CIDS').append(data['ID'])

                        unit_treenode = OOBTreeNode(data['ID'], treenode, nation[-1])
                        treenode.AddChildren(unit_treenode)
                    # else formation
                    else:
                        
                        data['etype'] = EType.FORMATION

                        if treenode==None or len(ftype.split())>1:
                            data['ftype'] = ftype.split()[1]
                            nation.append(ftype.split()[0])
                        else:
                            data['ftype'] = ftype
                            nation.append(nation[-1])

                        data['nation'] = nation[-1]
                        data['ID'] = int(splt_line[0])
                        try:
                            data['unknown0'] = int(splt_line[1])
                        except Exception as e:
                            print(line_counter, splt_line, e)
                            return
                        data['name'] = line.split(maxsplit=2)[-1]

                        if len(parent_ids) > 0:
                            data['PID'] = parent_ids[-1]
                        else:
                            data['PID'] = None

                        parent_ids.append(data['ID'])
                        data['CIDS'] = []

                        # Add this id to the parent's list of child ids.
                        if data['PID'] != None:
                            self.GetElement(data['PID']).GetData('CIDS').append(data['ID'])

                        # New formation: update tree node.
                        form_treenode = OOBTreeNode(data['ID'], treenode, nation)
                        if treenode:
                            treenode.AddChildren(form_treenode)
                        treenode = form_treenode
                            



                    


                element = OOBElement(data)
                self.AddElement(element)
                line_counter+=1

