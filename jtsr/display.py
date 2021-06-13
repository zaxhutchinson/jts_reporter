import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk

from jtsr import defs

class Display(tk.Frame):
    def __init__(self, master, game, config):
        super().__init__(master)

        self.game = game
        self.config = config

        self.pack()
        version = self.config.GetCfg('general','version')
        self.master.title('JTS Reporter v' + version)

        self.BuildUI()



    def BuildUI(self):
        self.notebook = ttk.Notebook(self)

        fwidth = 500
        fheight = 500
        self.frame_sceninfo = tk.Frame(self.notebook, width=fwidth, height=fheight)
        self.frame_unitinfo = tk.Frame(self.notebook, width=fwidth, height=fheight)
        self.frame_map = tk.Frame(self.notebook, width=fheight, height=fheight)

        self.frame_sceninfo.pack(side=tk.LEFT, fill=tk.BOTH)
        self.frame_unitinfo.pack(side=tk.LEFT,fill=tk.BOTH)
        self.frame_map.pack(side=tk.LEFT,fill=tk.BOTH)

        self.notebook.add(self.frame_sceninfo, text="Scen Info")
        self.notebook.add(self.frame_unitinfo, text="Unit Info")
        self.notebook.add(self.frame_map, text="Map")

        self.notebook.pack(side=tk.RIGHT,fill=tk.BOTH)

        self.BuildNotebookScenInfoTab()
        self.BuildNotebookUnitInfoTab()
        
        self.DisplayScenInfo()
        self.BuildFormationTree()

    def BuildNotebookScenInfoTab(self):
        px=5
        py=5

        self.lScenName = tk.Label(self.frame_sceninfo, text='Scenario Name:')

        self.eScenName = tk.Entry(self.frame_sceninfo, width=60)

        self.lScenName.grid(row=0, column=0, sticky=tk.W, padx=px, pady=py)

        self.eScenName.grid(row=0, column=1, sticky=tk.W, padx=px, pady=py)

        self.tvLosses = ttk.Treeview(self.frame_sceninfo)
        self.tvLosses['columns'] = ('file', 'turn', 'men', 'guns', 'vehicles', 'air', 'naval')
        self.tvLosses['height'] = 20
        self.tvLosses['selectmode'] = 'browse'
        self.tvLosses.column('#0',width=5)
        self.tvLosses.column('file', width=100, anchor=tk.CENTER)
        self.tvLosses.heading('file', text='FILE')
        self.tvLosses.column('turn', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('turn', text='TURN')
        self.tvLosses.column('men', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('men', text='MEN')
        self.tvLosses.column('guns', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('guns', text='GUNS')
        self.tvLosses.column('vehicles', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('vehicles', text='VEHICLES')
        self.tvLosses.column('air', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('air', text='AIR')
        self.tvLosses.column('naval', width=70, anchor=tk.CENTER)
        self.tvLosses.heading('naval', text='NAVAL')
        self.tvLosses.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=px, pady=py)

    def BuildNotebookUnitInfoTab(self):
        px=5
        py=5

        self.lName = tk.Label(self.frame_unitinfo, text='Name: ')
        self.lID = tk.Label(self.frame_unitinfo, text='ID: ')
        self.lNation = tk.Label(self.frame_unitinfo, text='Nation: ')

        self.eName = tk.Entry(self.frame_unitinfo)
        self.eID = tk.Entry(self.frame_unitinfo)
        self.eNation = tk.Entry(self.frame_unitinfo)

        self.lName.grid(row=0, column=1, sticky=tk.W, padx=px, pady=py)
        self.lID.grid(row=1, column=1, sticky=tk.W, padx=px, pady=py)
        self.lNation.grid(row=2, column=1, sticky=tk.W, padx=px, pady=py)

        self.eName.grid(row=0, column=2, sticky=tk.W, padx=px, pady=py)
        self.eID.grid(row=1, column=2, sticky=tk.W, padx=px, pady=py)
        self.eNation.grid(row=2, column=2, sticky=tk.W, padx=px, pady=py)

        style = ttk.Style(self)
        style.configure('Treeview',indent=10)

        self.form_tree = ttk.Treeview(self.frame_unitinfo)
        self.form_tree['columns'] = ('id', 'name')
        self.form_tree['height'] = 30
        self.form_tree['selectmode']='browse'
        self.form_tree.column('#0',width=100)
        self.form_tree.column('id',width=100)
        self.form_tree.heading('id', text='ID')
        self.form_tree.column('name',width=200)
        self.form_tree.heading('name', text='NAME')

        oob = self.game.oob
        nodelist = oob.tree

        self.AddToTree(nodelist)

        self.form_tree.bind('<<TreeviewSelect>>', self.DisplayOOBElementInfo)
        self.form_tree.grid(row=0,column=0,rowspan=20,padx=px,pady=py)

        self.tvHistory = ttk.Treeview(self.frame_unitinfo)
        self.tvHistory['columns'] = ('file', 'turn', 'strength', 'fatigue')
        self.tvHistory['height'] = 15
        self.tvHistory['selectmode'] = 'browse'
        self.tvHistory.column('#0',width=10)
        self.tvHistory.column('file',width=200,anchor=tk.CENTER)
        self.tvHistory.heading('file', text='FILE')
        self.tvHistory.column('turn',width=100,anchor=tk.CENTER)
        self.tvHistory.heading('turn', text='TURN')
        self.tvHistory.column('strength',width=100,anchor=tk.CENTER)
        self.tvHistory.heading('strength', text='STRENGTH')
        self.tvHistory.column('fatigue',width=100,anchor=tk.CENTER)
        self.tvHistory.heading('fatigue', text='FATIGUE')
        self.tvHistory.grid(row=3, column=1, columnspan=4, sticky=tk.W, padx=px, pady=py)

    def DisplayScenInfo(self):
        
        self.SetText(self.eScenName, self.game.scenario_name)

        scen_data = self.game.GetLossData()
        
        for name in scen_data['fnames']:

            file = name
            turn = f"{scen_data['turns'][name]}"
            men = f"{scen_data['men'][name]}"
            guns = f"{scen_data['guns'][name]}"
            vehicles = f"{scen_data['vehicles'][name]}"
            air = f"{scen_data['air'][name]}"
            naval = f"{scen_data['naval'][name]}"

            self.tvLosses.insert('','end',values=(file, turn, men, guns, vehicles, air, naval))

            
    def BuildFormationTree(self):
        px=5
        py=5

        

    # Recursive function that adds all the formations/units
    # To the tree.
    def AddToTree(self, nodelist):
        for node in nodelist:

            unit = self.game.oob.elements[node.GetID()]

            if unit.GetData('side') != self.game.side:
                continue

            pid = ''
            if node.parent:
                pid = node.parent.GetID()


            unitname = unit.GetData('name')

            self.form_tree.insert(pid,'end',node.GetID(),values=(node.GetID(),unitname))

            self.AddToTree(node.GetChildren())
            

    def DisplayOOBElementInfo(self, NOTUSEDPARAM):
        s = self.form_tree.selection()
        item = self.form_tree.item(s)
        record = item['values']
        oobele = self.game.oob.GetElement(int(record[0]))

        self.SetText(self.eName, oobele.GetData('name'))
        self.SetText(self.eID, str(oobele.GetData('ID')))
        self.SetText(self.eNation, oobele.GetData('nation'))

        formation_data = self.game.GetFormationData(oobele.GetData('ID'))

        for i in self.tvHistory.get_children():
            self.tvHistory.delete(i)

        for d in formation_data['fnames']:
            strength = f"{formation_data['strength'][d]*100:.1f}%"
            fatigue = f"{formation_data['fatigue'][d]*100:.1f}%"
            turn = f"{formation_data['turn'][d]}"
            self.tvHistory.insert('','end',None, values=(d, turn, strength, fatigue))


        # self.SetText(self.eStrength, f"{formation_data['strength']*100.0:.1f}%")
        # self.SetText(self.eFatigue, f"{formation_data['fatigue']*100.0:.1f}%")

    def SetText(self, entry, text):
        entry.delete(0,tk.END)
        entry.insert(0, text)




    def Run(self):
        self.mainloop()



#------------------------------------------------------------------------------
# 