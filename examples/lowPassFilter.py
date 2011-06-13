class LowPassFilterElement(element):
	'''
	LowPassFilterElement is an element consisting of a resistor and a capacitor in parallel.
	'''
	
	def __init__(self, id, nodeIds, elementParameters, side=None, name=None):
		'''
		Constructor
		'''
		Element.__init__(self) #Calling Element superclass
		self.Type = "Low-Pass Filter" #element type
		self.Side = side #arterial or venous side
		self.Id = id #element id
		self.Name = name #element name
		self.NodeIds = [] #element nodes
		self.NodeIds[:] = nodeIds[:]
		
		#elementParameters. (Resistance and Capacitor)
		try:
			self.Resistance = elementParameters["resistance"]
		except KeyError:
            self.Resistance = None
        for name in elementParameters:
            if type(elementParameters[name]) is str:
                self.nonLinear = True
        try:
			self.Compliance = elementParameters["compliance"]
		except KeyError:
            self.Compliance = None
        for name in elementParameters:
            if type(elementParameters[name]) is str:
                self.nonLinear = True
        
        self.R = None  #Resistance value
        self.C = None  #Compliance value
        self.dof = [0,1,2] #Local degrees of freedom
        self.Initialized = False  #Boolean variable for element initialization
        
    def SetResistance(self, resistance):
        '''
        This method sets Resistance.
        '''
        self.R = resistance
    
    def SetCompliance(self, compliance):
        '''
        This method sets Compliance.
        '''
        self.C = compliance
        
    def InputParameters(self,evaluator=None):
    	'''
    	This method calculates R and C from element's parameters:
        If resistance and/or compliance is expressed with non-linear equations,
        non linear value will overwrite the linear one.
    	'''
    	Element.InputParameters(self)  #calling InputParameters method from superclass
        if type(self.Resistance) is  str:
            evaluator.Evaluate(self.Resistance)
        else:    
            self.R = self.Resistance
        if type(self.Compliance) is  str:
            evaluator.Evaluate(self.Compliance)
        else:    
            self.C = self.Compliance
        self.Initialized = True
    
    def GetPoiseuilleDofs(self):
        '''
        This method return Poiseuille's resistance local dofs
        '''
        return [self.dof[0], self.dof[1]]
    
    def GetCircuitMatrix(self):
        '''
        This method builds element's circuit matrix
        Each Row is an edge, Node1 - Node2 - C - R - L
        '''        
        circuitMatrix = array ([[self.dof[0], self.dof[1], 0, self.R, 0],
                                [self.dof[1], self.dof[2], self.C, 0, 0]])
        return CircuitMatrix  
        
    def GetExternalPressureLocalDofs(self):
        '''
        Setting Transmural pressure in the correct local dofs.
        '''
        return [self.dof[2]]
    
    def GetLocalDof (self, NodeId):
        '''
        This method returns Local dof number corresponding to specific NodeId 
        '''
        if NodeId == self.NodeIds[0]:
            LocalDof = 0
        if NodeId == self.NodeIds[1]:
            LocalDof = 1   
        return LocalDof
    
    def GetNodeLocalDofs(self):
        '''
        This method returns local dof number corresponding to its NodeId (if exist)
        '''
        for dofs in self.NodeIds:
            if dofs == self.NodeIds[0]:
                NodeDof1 = 0
            if dofs == self.NodeIds[1]:
                NodeDof2 = 1
        NodeDofs = [NodeDof1, NodeDof2]
        return NodeDofs
    
    def GetDofNodes(self):
        '''
        This method returns NodeId corresponding to local dof number (if exist)
        '''
        for dofs in self.dof:
            if dofs == 0:
                DofNodeId1 = self.NodeIds[0]
            if dofs == 1:
                DofNodeId2 = self.NodeIds[1]
        DofNodes = [DofNodeId1,DofNodeId2]
        return DofNodes
                