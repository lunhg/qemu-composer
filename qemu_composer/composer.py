import qemuComposer

def main(**kwargs):
    q = qemuComposer.QemuComposer(**kwargs)
    q.make()
    return q
