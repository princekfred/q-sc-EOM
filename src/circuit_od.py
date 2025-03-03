#circuit for off-diagonal part
@qml.qnode(dev)
def circuit_od(params, occ1, occ2,wires, s_wires, d_wires, hf_state):
    for w in occ1:
        qml.X(wires=w)
    first=-1
    for v in occ2:
        if v not in occ1:
            if first==-1:
                first=v
                qml.Hadamard(wires=v)
            else:
                qml.CNOT(wires=[first,v])
    for v in occ1:
        if v not in occ2:
            if first==-1:
                first=v
                qml.Hadamard(wires=v)
            else:
                qml.CNOT(wires=[first,v])
    qml.UCCSD(params, wires, s_wires, d_wires, hf_state)
    return qml.expval(H)