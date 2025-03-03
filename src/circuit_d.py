#circuit for diagonal part
@qml.qnode(dev)
def circuit_d(params, occ,wires, s_wires, d_wires, hf_state):
    for w in occ:
        qml.X(wires=w)
    qml.UCCSD(params, wires, s_wires, d_wires, hf_state)
    return qml.expval(H)