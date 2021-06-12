import tkinter as tk
import tkinter.ttk as ttk

import defs

class Display(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master)

        self.game = game

        self.pack()
        self.master.title('JTS Reporter v' + str(defs.VERSION))

        self.BuildUI()

    def BuildUI(self):

        self.BuildFormationTree()
        self.BuildDataNotebook()

    def BuildFormationTree(self):
        style = ttk.Style(self)
        style.configure('Treeview',indent=10)

        self.form_tree = ttk.Treeview(self)
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
        self.form_tree.pack(side=tk.LEFT, fill=tk.BOTH)

    # Recursive function that adds all the formations/units
    # To the tree.
    def AddToTree(self, nodelist):
        for node in nodelist:
            pid = ''
            if node.parent:
                pid = node.parent.GetID()

            unit = self.game.oob.elements[node.GetID()]
            unitname = unit.GetData('name')

            self.form_tree.insert(pid,'end',node.GetID(),values=(node.GetID(),unitname))

            self.AddToTree(node.GetChildren())

    def BuildDataNotebook(self):
        self.notebook = ttk.Notebook(self)

        fwidth = 500
        fheight = 500
        self.frame_info = tk.Frame(self.notebook, width=fwidth, height=fheight)
        self.frame_map = tk.Frame(self.notebook, width=fheight, height=fheight)

        self.frame_info.pack(side=tk.LEFT,fill=tk.BOTH)
        self.frame_map.pack(side=tk.LEFT,fill=tk.BOTH)

        self.notebook.add(self.frame_info, text="Info")
        self.notebook.add(self.frame_map, text="Map")

        self.notebook.pack(side=tk.RIGHT,fill=tk.BOTH)

        self.BuildNotebookInfoTab()

    def BuildNotebookInfoTab(self):
        px=5
        py=5

        self.lName = tk.Label(self.frame_info, text='Name: ')
        self.lID = tk.Label(self.frame_info, text='ID: ')
        self.lNation = tk.Label(self.frame_info, text='Nation: ')
        # self.lStrength = tk.Label(self.frame_info, text='Strength: ')
        # self.lFatigue = tk.Label(self.frame_info, text='Fatigue: ')

        self.eName = tk.Entry(self.frame_info)
        self.eID = tk.Entry(self.frame_info)
        self.eNation = tk.Entry(self.frame_info)
        # self.eStrength = tk.Entry(self.frame_info)
        # self.eFatigue = tk.Entry(self.frame_info)

        self.lName.grid(row=0, column=0, sticky=tk.W, padx=px, pady=py)
        self.lID.grid(row=1, column=0, sticky=tk.W, padx=px, pady=py)
        self.lNation.grid(row=2, column=0, sticky=tk.W, padx=px, pady=py)
        # self.lStrength.grid(row=0, column=3, sticky=tk.W)
        # self.lFatigue.grid(row=1, column=3, sticky=tk.W)

        self.eName.grid(row=0, column=1, sticky=tk.W, padx=px, pady=py)
        self.eID.grid(row=1, column=1, sticky=tk.W, padx=px, pady=py)
        self.eNation.grid(row=2, column=1, sticky=tk.W, padx=px, pady=py)
        # self.eStrength.grid(row=0, column=4, sticky=tk.W)
        # self.eFatigue.grid(row=1, column=4, sticky=tk.W)

        self.tvHistory = ttk.Treeview(self.frame_info)
        self.tvHistory['columns'] = ('file', 'turn', 'strength', 'fatigue')
        self.tvHistory['height'] = 10
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
        self.tvHistory.grid(row=3, column=0, columnspan=4, sticky=tk.W, padx=px, pady=py)

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