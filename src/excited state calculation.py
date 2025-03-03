import functions
import excitations
import circuit_d
import circuit_od

def ee_exact(symbols, geometry, electrons, charge,params,shots=0):
    # Build the electronic Hamiltonian
    H, qubits = qml.qchem.molecular_hamiltonian(symbols, geometry, charge=charge)
    hf_state = qml.qchem.hf_state(electrons, qubits)
    singles, doubles = qml.qchem.excitations(electrons, qubits)

    # Map excitations to the wires the UCCSD circuit will act on
    s_wires, d_wires = qml.qchem.excitations_to_wires(singles, doubles)
    wires=range(qubits)
    null_state = np.zeros(qubits,int)
    list1 = inite(electrons,qubits)
    eigenvalues =[]

    if shots==0:
        dev = qml.device("default.qubit", wires=qubits)
    else:
        dev = qml.device("default.qubit", wires=qubits,shots=shots)

    
    #M matrix
    M = np.zeros((len(list1),len(list1)))
    for i in range(len(list1)):
        for j in range(len(list1)):
            if i == j:
                M[i,i] = circuit_d(params, list1[i], wires, s_wires, d_wires, null_state)
    print("diagonal parts done")
    for i in range(len(list1)):
        for j in range(len(list1)):
            if i!=j:
                Mtmp = circuit_od(params, list1[i],list1[j],wires, s_wires, d_wires, null_state)
                M[i,j]=Mtmp-M[i,i]/2.0-M[j,j]/2.0
    print("off diagonal terms done")
    eig,evec=np.linalg.eig(M)
    eigenvalues.append(np.sort(eig))
    return eigenvalues
