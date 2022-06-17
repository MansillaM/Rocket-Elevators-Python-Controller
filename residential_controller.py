from math import floor

#Global Variables
elevatorID = 1
floorRequestButtonID = 1
callButtonID = 1


#Create Column CLASS
class Column:
    def __init__(self, _id, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = 'active'
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorList = []
        self.callButtonList = []

        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)
    
    #Create callButtons for elevator
    def createCallButtons(self, _amountOfFloors):
        buttonFloor = 1
        for i in range(1, _amountOfFloors):
            #If it's not the last floor
            if i < _amountOfFloors:
                callButton = CallButton(i + 1, buttonFloor, 1)
                self.callButtonList.append(callButton)
            #If it's not the first floor
            if i >= 1:
                callButton = CallButton(i + 1, buttonFloor, 1)
                self.callButtonList.append(callButton)
            buttonFloor =+ 1
        
    
    #create elevators
    def createElevators(self, _amountOfFloors, _amountOfElevators):
        global elevatorID
        for i in range(_amountOfElevators):
            elevator = Elevator(elevatorID, _amountOfFloors)
            self.elevatorList.append(elevator)
            elevatorID += 1

    #Simulate when a user press a button outside the elevator
    def requestElevator(self, requestedFloor, direction):
        elevator = self.findElevator(requestedFloor, direction)
        elevator.floorRequestList.append(requestedFloor)
        elevator.move()
        elevator.operateDoors()
        return elevator

    #We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are 
    #higher values than what could be possibly calculated, the first elevator will always become the default bestElevator, 
    #before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.
    def findElevator(self, requestedFloor, requestedDirection):
        bestElevatorInformations = None
        bestElevator = None
        bestScore = 5
        referenceGap = 10000000
        for elevator in self.elevatorList:
            #The elevator is at my floor and going in the direction I want
            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(1, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                #The elevator is lower than me, is coming up and I want to go up
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                #The elevator is higher than me, is coming down and I want to go down
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(2, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                #The elevator is idle
            elif elevator.status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(3, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
                #The elevator is not available, but still could take the call if nothing better is found
            else :
                bestElevatorInformations = self.checkIfElevatorIsBetter(4, elevator, bestScore, referenceGap, bestElevator, requestedFloor)
            bestElevator = bestElevatorInformations["bestElevator"]
            bestScore = bestElevatorInformations["bestScore"]
            referenceGap = bestElevatorInformations["referenceGap"]
        return bestElevator
    
    #With all the info we get choose the best elevator
    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestScore, referenceGap, bestElevator, floor):
        if scoreToCheck < bestScore:
            bestScore = scoreToCheck
            bestElevator = newElevator
            referenceGap = abs(newElevator.currentFloor - floor)
        elif bestScore == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if referenceGap > gap:
                bestElevator = newElevator
                referenceGap = gap
        return {
            "bestScore": bestScore,
            "referenceGap": referenceGap,
            "bestElevator": bestElevator,
        }
#END of Column

#Create Elevator CLASS
class Elevator:
    def __init__(self, _id, _amountOfFloors):
        self.ID = _id
        self.status = 'idle'
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = 1
        self.direction = None
        self.door = Door(_id)
        self.floorRequestButtonList = []
        self.floorRequestList = []

        self.createFloorRequestButtons(_amountOfFloors)
    
    #floor request buttons needed
    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        for i in range(0, _amountOfFloors):
            floorRequestButton = FloorRequestButton(i, buttonFloor)
            self.floorRequestButtonList.append(floorRequestButton)
            buttonFloor += 1
            i += 1

    #Simulate when a user press a button inside the elevator
    def requestFloor(self, requestedFloor):
        self.floorRequestList.append(requestedFloor)
        self.sortFloorList()
        self.move()
        self.operateDoors()

    #Move elevator with destination and requestfloor elements
    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up';
                while self.currentFloor < destination:
                    self.currentFloor += 1
            elif self.currentFloor > destination:
                self.direction = 'down'
                while self.currentFloor > destination:
                    self.currentFloor -= 1
            self.status = 'opened';
            self.floorRequestList.pop(0)
            self.status = 'idle';

    #Sort floor list in numerical order or reverse
    def sortFloorList(self):
        if self.direction == 'up':
            self.floorRequestList.sort()
        else:
            self.floorRequestList.sort(reverse=True)

    #Change status of door
    def operateDoors(self):
        if self.door.status == 'opened':
            self.door.status = 'closed'
        elif self.door.status == 'closed':
            self.door.status = 'opened'
#END OF ELEVATOR  

#Create CallButton CLASS
class CallButton:
    def __init__(self, _id, _floor, _direction):
        self.ID = _id
        self.status = 'active'
        self.floor = _floor
        self.direction = _direction

#Create FloorRequestButton CLASS
class FloorRequestButton:
    def __init__(self, _id, _floor): 
        self.ID = _id
        self.status = 'active'
        self.floor = _floor
    
#Crete Door CLASS
class Door:
    def __init__(self, _id):
        self.ID = _id
        self.status = 'active'
    





