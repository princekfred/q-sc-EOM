
import functions

def gs_exact(symbols, geometry, electrons, charge, shots=None, max_iter=100):
    # Build the electronic Hamiltonian
    H, qubits = qml.qchem.molecular_hamiltonian(symbols, geometry, charge=charge)
    hf_state = qml.qchem.hf_state(electrons, qubits)
    singles, doubles = qml.qchem.excitations(electrons, qubits)
   
   # Map excitations to the wires the UCCSD circuit will act on
    s_wires, d_wires = qml.qchem.excitations_to_wires(singles, doubles)
    wires=range(qubits)
    params = np.zeros(len(singles) + len(doubles))
    # Define the device
    dev = qml.device("default.qubit", wires=qubits, shots=shots)
    
    # Define the qnode
    if shots==None:
        @qml.qnode(dev, interface="autograd", diff_method="adjoint")
        def circuit(params, wires, s_wires, d_wires, hf_state):
            qml.UCCSD(params, wires, s_wires, d_wires, hf_state)
            return qml.expval(H)
    else:
        @qml.qnode(dev, interface="autograd")
        def circuit(params, wires, s_wires, d_wires, hf_state):
            qml.UCCSD(params, wires, s_wires, d_wires, hf_state)
            return qml.expval(H)

    optimizer = qml.GradientDescentOptimizer(stepsize=2.0)
    for n in range(max_iter):
        params, energy = optimizer.step_and_cost(circuit, params, wires=range(qubits),
                                                 s_wires=s_wires, d_wires=d_wires,
                                                 hf_state=hf_state)
    print(circuit(params, wires, s_wires, d_wires, hf_state))
    return params