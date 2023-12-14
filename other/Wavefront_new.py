import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox, Toplevel
import datetime

# Main application
class PortApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Port Ops')
        self.geometry('800x460')

        # Login Button.
        self.btnLogin = tk.Button(self, text="LOGIN", command=self.askName)
        self.btnLogin.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # Setup other elements, but don't show them
        self.setupOther()

        # Variables for user and file
        self.currUser = None
        self.manifestFile = None
        self.contMap = {}  # Container mapping

    def setupOther(self):
        # Setup second window, but keep it hidden
        self.winOps = Toplevel(self)
        self.winOps.title("Operations")
        self.winOps.geometry("800x460")
        self.winOps.withdraw()

        # Button for file upload
        self.btnUpload = tk.Button(self.winOps, text="UPLOAD FILE", command=self.uploadFile)
        self.btnUpload.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Button for balance check
        self.btnCheck = tk.Button(self.winOps, text="CHECK BALANCE")
        self.btnCheck.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def askName(self):
        # Ask for user name
        self.currUser = simpledialog.askstring("Name", "Enter your name:")
        if self.currUser:
            self.logUser(self.currUser)
            self.winOps.deiconify()
            self.withdraw()

    def logUser(self, name):
        # Log user name and time
        timeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logText = f"{timeNow}: '{name}' logged in.\n"
        messagebox.showinfo("Login Info", logText)
        with open("Log2023.txt", "a") as logFile:
            logFile.write(logText)

    def uploadFile(self):
        # Choose a file to upload
        self.manifestFile = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.manifestFile:
            messagebox.showinfo("File Uploaded", f"File '{self.manifestFile}' uploaded.")
            self.showLoadOffload()
    def showLoadOffload(self):
        # Show the load/offload window
        self.winLoadOffload = Toplevel(self)
        self.winLoadOffload.title("Load/Offload")
        self.winLoadOffload.geometry("600x400")

        # Button for loading or offloading
        self.btnLoadOffload = tk.Button(self.winLoadOffload, text="LOAD/OFFLOAD", command=self.showManifest)
        self.btnLoadOffload.pack(pady=20)

    def showManifest(self):
        # Show manifest details
        self.winManifest = Toplevel(self)
        self.winManifest.title("Manifest Details")
        self.winManifest.geometry("600x400")
        self.canvas = tk.Canvas(self.winManifest, bg='white', width=800, height=500)
        self.canvas.pack(pady=20)
        self.setupBindings()
        tk.Label(self.winManifest, text=f"Current manifest: {self.manifestFile}").pack()
        tk.Button(self.winManifest, text="CHANGE", command=self.uploadFile).pack()
        tk.Label(self.winManifest, text="Check the manifest matches the ship.").pack()
        self.lblShipWeight = tk.Label(self.winManifest, text="Ship Weight: 0", bg="yellow")
        self.lblShipWeight.pack()
        self.lblDockWeight = tk.Label(self.winManifest, text="Dock Weight: 0", bg="yellow")
        self.lblDockWeight.pack()

        # Read and display containers
        self.containers = self.readManifest(self.manifestFile)
        ship_conts = [c for c in self.containers if c['position'][1] < 50]
        self.showContainers(ship_conts, self.canvas)

        # Buttons for steps
        self.btnPrev = tk.Button(self.winManifest, text="PREV", command=self.prevStep)
        self.btnPrev.pack(side=tk.LEFT, padx=10)
        self.btnNext = tk.Button(self.winManifest, text="NEXT", command=self.nextStep)
        self.btnNext.pack(side=tk.RIGHT, padx=10)
        self.lblStep = tk.Label(self.winManifest, text="Step 1 of 9")
        self.lblStep.pack()

    def readManifest(self, file_name):
        # Read manifest file
        conts = []
        with open(file_name, 'r') as file:
            for line in file:
                parts = line.strip().split(', ')
                loc = parts[0].strip('[]')
                x, y = map(int, loc.split(','))
                weight = int(parts[1].strip('{}'))
                desc = parts[2].strip('"')
                conts.append({"position": (x, y), "weight": weight, "description": desc})
        return conts

    def showContainers(self, ship_conts, canvas):
        # Display containers
        shipX, shipY = 50, 50
        dockX, dockY = 350, 50
        size = 20
        canvasHeight = 400
        canvas.create_text(shipX + 100, shipY - 20, text="SHIP", font="Arial 20", fill="black")
        canvas.create_text(dockX + 100, dockY - 20, text="DOCK", font="Arial 20", fill="black")
        canvas.delete("container")

        # Display containers on ship
        for cont in ship_conts:
            x, y = cont['position']
            rectY = canvasHeight - (shipY + y*size)
            cont_id = canvas.create_rectangle(shipX + x*size, rectY, shipX + (x+1)*size, rectY + size, fill="blue", outline="white", tags=("container", "ship"))
            self.contMap[cont_id] = cont

        # Define and display dock containers
        dock_conts = [
            {"position": (8, 2), "weight": 72573, "description": "Raw sugar Hawaii farms2"},
        {"position": (9, 2), "weight": 72697, "description": "Raw sugar Hawaii farms3"},
        {"position": (10, 2), "weight": 72773, "description": "Raw sugar Hawaii farms4"},
        {"position": (11, 2), "weight": 72773, "description": "Raw sugar Hawaii farms4"}, {"position": (7, 2), "weight": 72773, "description": "Raw sugar Hawaii farms4"},
         {"position": (7, 3), "weight": 72773, "description": "Raw sugar Hawaii farms4"},
         {"position": (7, 4), "weight": 72773, "description": "Raw sugar Hawaii farms4"},
        ]
        # Display dock containers.
        for cont in dock_conts:
            x, y = cont['position']
            rectY = canvasHeight - (dockY + (y - 1) * size)  # Calculate Y coordinate for canvas
            cont_id = self.canvas.create_rectangle(dockX + (x - 1) * size, rectY, 
                                           dockX + x * size, rectY + size, 
                                           fill="black", outline="white", 
                                           tags=("container", "dock"))
            self.contMap[cont_id] = cont  # Map container ID to its data

    # Code for defining and displaying dock containers
        for cont in dock_conts:
            x, y = cont['position']
            rectY = canvasHeight - (dockY + (y - 1) * size)
            cont_id = canvas.create_rectangle(dockX + (x - 1) * size, rectY, dockX + x * size, rectY + size, fill="black", outline="white", tags=("container", "dock"))
            self.contMap[cont_id] = cont

        # Bind events to containers
        for cont_id in self.contMap.keys():
            canvas.tag_bind(cont_id, "<Button-1>", 
                            lambda event, c=canvas, id=cont_id: self.selectCont(event, c, id))

        canvas.bind("<Button-1>", self.moveCont)

    def getContData(self, cont_id):
        # Get data for a container
        return self.contMap.get(cont_id)
    def selectCont(self, event, canvas, cont_id):
        # Select a container
        print("Selected container:", cont_id)
        self.selectedCont = cont_id
        self.origPos = canvas.coords(cont_id)
        canvas.itemconfig(cont_id, fill="green")
        self.startX = event.x
        self.startY = event.y

    def moveCont(self, event):
        # Move selected container
        if self.canvas.find_withtag("current"):
            return
        if not hasattr(self, 'selectedCont') or self.selectedCont is None:
            print("No container selected")
            return

        print("Moving container:", self.selectedCont)
        canvas = self.canvas

        # Get original container position and size
        x1, y1, x2, y2 = self.origPos
        width = x2 - x1
        height = y2 - y1

        # Calculate new position
        newX1 = event.x - width / 2
        newY1 = event.y - height / 2
        newX2 = event.x + width / 2
        newY2 = event.y + height / 2

        # Create a new container at the new position
        newContId = canvas.create_rectangle(newX1, newY1, newX2, newY2, fill="red", outline="white")
        canvas.tag_raise(newContId)

        # Delete the original container
        canvas.delete(self.selectedCont)

        # Clear selection
        self.selectedCont = None
        self.origPos = None

    def setupBindings(self):
        # Bind events for moving containers
        self.canvas.bind("<Button-1>", self.moveCont)
    def moveContainer(self, event):
        # Move container with mouse movement
        dx = event.x - self.prevX
        dy = event.y - self.prevY
        canvas = event.widget
        canvas.move(self.selectedContainer, dx, dy)
        # Update mouse position
        self.prevX = event.x
        self.prevY = event.y

    def isShipArea(self, position):
        # Check if position is in the ship area
        thresholdX = 600
        return position[0] < thresholdX  # If x-coordinate is less than threshold

    def updateContPosition(self, cont_id, newX, newY):
        # Update container position
        cont = self.getContData(cont_id)
        if cont:
            # Calculate new position
            contSize = 30  # Container size
            cont['position'] = (newX // contSize, newY // contSize)

    def updateTotalWeights(self):
        # Recalculate total weights for ship and dock
        totalShipWeight = sum(cont['weight'] for cont in self.containers if self.isShipArea(cont['position']))
        totalDockWeight = sum(cont['weight'] for cont in self.containers if not self.isShipArea(cont['position']))
    
        # Update weight labels.
        self.lblShipWeight.config(text=f"Ship Weight: {totalShipWeight}")
        self.lblDockWeight.config(text=f"Dock Weight: {totalDockWeight}")

    def printTotalWeights(self):
        # Print total weights for ship and dock to console
        totalShipWeight = sum(cont['weight'] for cont in self.containers if self.isShipArea(cont['position']))
        totalDockWeight = sum(cont['weight'] for cont in self.containers if not self.isShipArea(cont['position']))
        print(f"Ship Weight: {totalShipWeight}")
        print(f"Dock Weight: {totalDockWeight}")

    def dropContainer(self, event):
        # Drop container and update position and weight
        canvas = event.widget
        cont_id = self.selectedContainer
        self.selectedContainer = None
        canvas.unbind("<Motion>")
        canvas.unbind("<ButtonRelease-1>")
    
        # Update container position
        contSize = 30  # Container size
        newX = canvas.canvasx(event.x) - (contSize / 2)
        newY = canvas.canvasy(event.y) - (contSize / 2)
        self.updateContPosition(cont_id, newX, newY)
        self.updateTotalWeights()
        self.printTotalWeights()

# Main program
if __name__ == "__main__":
    app = PortApp()
    app.mainloop()

