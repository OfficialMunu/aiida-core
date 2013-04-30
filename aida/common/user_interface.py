'''
This file contains specifications on the user interface of Aiida.
The goal is to keep the UI as simple as possible without sacrificing the querying and inheritance power.
'''

#Workflow use cases
def SimpleWorkflow():
    
    #select code
    mycode = Code.query(name='Espresso-4.2')   #gets code object
    mycomputer = Computer.query(name='titan')
    
    #select structure - this is a structured object
    mystruc = Struc.find(natoms__gte = 6.0, atoms__contains = 'Li') #gets struc object based on attributes, probably will be hard to map using ORM   
    mystruc = Struc.query(attr__key = 'natoms', attr__key__gte = 6.0) # with current node library
    
    print mystruc.atoms
    mystruc.set_cell([[1,0,0],[0,1,0],[0,0,1]])  #should be able to inherit from multiple classes like ase
    struclist = Struc.filter(child__type__startswith = 'calculation', child__attr__key = 'energy', child__attr__fval__lte = 10.4)
    mystruc = struclist[0].copy()  # create a copy to be modified - this should set up a link with label 'copy'
    mystruc.junk = 55   # should be able to use attributes only for coding, not to be saved
    mystruc.attr.tag = 'something'  # set meta using attributes - to be saved
    mystruc.store()
    
    #create input file data object, without having to write plugins. This reduces user barrier and allows scripting using parameters.
    myinput = Inputfile.create() # a subclass of Data with certain methods like 'template'
    myinput.input_template = '''
        &control
    calculation = {{ CALCTYPE }},
    restart_mode = from_scratch
    nstep = NSTEP
    dt = 100.0
    tstress = .true.
    wf_collect = .true.
    forc_conv_thr = 5.0d-3,
    '''
    myinput.CALCTYPE = 'relax'
    myinput.attr.NSTEP = 5
    #both temporary and persistant attributes should be substituted using templates
    
    myjobparams = Jobparams.create() # a subclass of Data with a preset schema
    
    mycalc = Relaxation.create() # creates an 'abstract' object
    # Sublcass of calculation which expects input {'input_file': Input(), 'struc': Struc(), ...} and produces {
    mycalc.attrs.add({'NPROC' : 32, 'NPOOL' : 1, 'CALCTYPE' : 'md', 'RUNTIME' : '1:00:00'})  # add or modify job attributes
    
    mycalc.NODES = 4   # only a temporary object property
    mycalc.attr.NPROC = 8 * mycalc.NODES  #example way of defining the attribute
    mycalc.store()  #State = initiated
    # params are validated based on expected schema at the store time
    
    #connect concrete objects to calculation
    mycalc.set_input({'input_file':myinput, 'struc':mystruc,...})
    
    mycalc.submit()
    # execution manager loads plugins and does its thing
    # when finished code plugin will serialize and store output data


def AbstractWorkflow():
    '''
    In case of a predefined workflow we have the full graph.
    This is an example of constructing it.
    The end result should look like a single calculation.
    For now assume the outputs are well defined for each calculation.
    Later we will deal with unpredictable number of outputs.
    USE ACTUAL NODES BUT WITH ABSTRACT TYPES
    '''
    struc0 = Struc.find(...) 
    param_rel = Parameter.create(...)
        
    struc1 = Struc.create(type='abstract')
    struc2 = Struc.create(type='abstract')
    calc1 = Relaxation(inputs={'input.struc':struc0, 'input.param':param_rel}, 
                       outputs={'output.first_struc':struc1, 'output.last_struc':struc2})
    calc1.execute(callbak=newfunc("calc1")))
    # struc1 and struc2 are now concrete
    
   
    ############ INDPENDENT PARALLEL PART ###########

    struc3 = Struc.create(type='abstract')
    struc4 = Struc.create(type='abstract')
    param_rel2 = Parameter.create(...)
    calc3 = Relaxation(inputs={'input.struc':struc0, 'input.param':param_rel2}, 
                       outputs={'output.first_struc':struc3, 'output.last_struc':struc4})
    calc3.execute()

    param_ph = Parameter.create(...)
    calc4 = Phonon(inputs={'input.struc':struc4, 'input.param':param_ph}, outputs={...})
    calc4.waitfor(calc3) # this will hold cacl2 until calc1 is done
    # calc4.execute()


def newfunct(arg):

    if (arg=="calc1"):    
      param_ph = Parameter.create(...)
      calc2 = Phonon(inputs={'input.struc':struc2, 'input.param':param_ph}, outputs={...})
      calc2.waitfor(calc1) # this will hold cacl2 until calc1 is done
      #calc2.execute()


def LabelWorkflow():
    '''
    SAME BUT USING LABELS OF PORTS
    '''
    
    struc0 = Struc.find(...) 
    
    param_rel = Parameter.create_or_retrieve(...)
        
    calc1 = Calculation(type='qe.relax', inputs={'input.struc':struc0, 'input.param':param_rel})
    # Code plugin creates data objects and assign labels 'output.first_struc' and 'output.last_struc' to the right output objects
    calc1.execute(label='calc1')
    # struc1 and struc2 are only created in the end of calc1
    
    param_ph = Parameter.create(...)
    
    if calc1.output.first_struc.energy < calc1.output.first_struc.energy
        calc2 = Calculation(type='qe.ph', inputs={'input.struc':calc1.get_output_labels('output.last_struc'), 'input.param':param_ph}, outputs={...})
        # Plugin will check if all objects pointed to by the label exists
        # If not, DB object is not created and execution is skipped.
    # If calc1 does not even exist yet, then
    calc2.execute()
    
    ############ INDPENDENT PARALLEL PART ###########


def DynamicWorkflow():
    '''
    In case of dynamic workflows, nodes are created on the fly.
    Each data object will have a unique label, derived from its variable name. ???
    '''
    
    struc0 = Struc(...)
    calc1 = Relaxation(...)
    
    struc1.energy = 
    struc2 = 
    if 
    
    calc2 = Phonon(...)
    calc2.set_input({
    for data2 in output_set:
        


def Observing():
    
    

def RestartWorkflow():



def QueryWorkflow():
    struclist = Struc.filter(child__type__startswith = 'calculation', child__attr__key = 'energy', child__attr__fval__lte = 10.4)

    

def Queries():
    '''Enumerate the most important user queries.'''
    
    # find a structure 
    mystruc = Struc.filter(attr__key = 'group', attr__ival = 230).filter(attr__key)
    mystruc = Struc.filterattr({'group': 230, })
    #filter charge density data that comes from calculations that use Li.UPF and LiCl
    #This should only look for objects of type 'node.data.charge'
    
    results = Charge_density.filter().filter
    
    #would be better to do
    results = Data.
    
