import os

def system_sync():
    rebuilddb = 'rpm --rebuilddb;dnf clean all'
    os.system(rebuilddb)
    cmd = 'dnf -y distro-sync --allowerasing --skip-broken'
    os.system(cmd)

def main():
    system_cross_sync()

if __name__ == '__main__':
    main()
