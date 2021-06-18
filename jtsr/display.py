import tkinter as tk
from tkinter.constants import ANCHOR
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
import matplotlib.figure as figure
import matplotlib.backends.backend_tkagg as tkagg

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

    def BuildNotebookScenInfoTab(self):
        px=5
        py=5

        self.lScenName = tk.Label(self.frame_sceninfo, text='Scenario Name:')

        self.eScenName = tk.Entry(self.frame_sceninfo, width=60)

        self.lScenName.grid(row=0, column=0, sticky=tk.W, padx=px, pady=py)

        self.eScenName.grid(row=0, column=1, sticky=tk.W, padx=px, pady=py)

        self.tvLosses = ttk.Treeview(self.frame_sceninfo)
        self.tvLosses['columns'] = ('file', 'turn', 'men', 'guns', 'vehicles', 'air', 'naval')
        self.tvLosses['height'] = 25
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
        self.tvLosses.grid(row=1, column=0, columnspan=2, sticky=tk.W, padx=px, pady=py)


        #==================================================
        # LOSS FRAME
        self.frame_scen_graph = ttk.LabelFrame(self.frame_sceninfo, text="GRAPH",width=650,height=600)
        self.frame_scen_graph.grid_propagate(False)
        self.frame_scen_graph.grid(row=0, column=2, rowspan=2,columnspan=2, sticky=tk.W, padx=px, pady=py)

        # Holder for the pyplot figures. Allowing us to close them.
        self.loss_fig = None

        #==================================================
        #BUTTONS and other functionality

        self.frame_scen_btns = ttk.LabelFrame(self.frame_sceninfo, text="Loss",width=1000,height=200)
        self.frame_scen_btns.grid(row=2, column=0, columnspan=4, sticky=tk.W, padx=px, pady=py)

        self.radbtnLossVar = tk.StringVar()
        self.radbtnLossMen = tk.Radiobutton(self.frame_scen_btns, text="Men", variable=self.radbtnLossVar, value="men")
        self.radbtnLossGuns = tk.Radiobutton(self.frame_scen_btns, text="Guns", variable=self.radbtnLossVar, value="guns")
        self.radbtnLossVehicles = tk.Radiobutton(self.frame_scen_btns, text="Vehicles", variable=self.radbtnLossVar, value="vehicles")
        self.radbtnLossAir = tk.Radiobutton(self.frame_scen_btns, text="Air", variable=self.radbtnLossVar, value="air")
        self.radbtnLossNaval = tk.Radiobutton(self.frame_scen_btns, text="Naval", variable=self.radbtnLossVar, value="naval")
        self.radbtnLossMen.grid(row=0,column=0, sticky=tk.W, padx=px, pady=py)
        self.radbtnLossGuns.grid(row=1, column=0, sticky=tk.W, padx=px, pady=py)
        self.radbtnLossVehicles.grid(row=2, column=0, sticky=tk.W, padx=px, pady=py)
        self.radbtnLossAir.grid(row=3, column=0, sticky=tk.W, padx=px, pady=py)
        self.radbtnLossNaval.grid(row=4, column=0, sticky=tk.W, padx=px, pady=py)
        self.radbtnLossMen.select()
        
        self.btnLosses = tk.Button(self.frame_scen_btns, text="Graph", command=self.GraphLosses)
        self.btnLosses.grid(row=5, column=0, sticky=tk.W, padx=px, pady=py)



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

            
    def GraphLosses(self):

        # If a figure is already displayed, close it.
        if(self.loss_fig):
            plt.close(self.loss_fig)
        
        scen_data = self.game.GetLossData()

        loss_selection = self.radbtnLossVar.get()
        
        yaxis = []
        xaxis = []
        delta = []

        prev = 0
        for name in sorted(scen_data['fnames']):
            xaxis.append(scen_data['turns'][name])
            yaxis.append(scen_data[loss_selection][name])
            delta.append(scen_data[loss_selection][name] - prev)
            prev=scen_data[loss_selection][name]

        self.loss_fig = figure.Figure(figsize=(6,5))
        ax = self.loss_fig.add_subplot()
        ax.set_xlabel("TURNS")
        ax.set_ylabel(loss_selection.upper())
        ax.plot(xaxis, yaxis, linewidth=1, color='#33bb33')
        ax.plot(xaxis, delta, linewidth=1, linestyle='--', color='#555555')
        ax.legend(['Loss','Change'])
        ax.set_title(f"Losses {loss_selection}")

        self.loss_canvas = tkagg.FigureCanvasTkAgg(self.loss_fig, master=self.frame_scen_graph)
        self.loss_canvas.draw()
        self.loss_canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.W)



        

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