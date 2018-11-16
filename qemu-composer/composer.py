import qemuComposer

def main(**kwargs):
    q = qemuComposer.QemuComposer(**kwargs)
    q.build()
    q.make()
    return q
