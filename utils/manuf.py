from os.path import isfile
from subprocess import check_output


def get_oui_vendor_name(oui, oui_file):
    """
    Returns the vendor name of the given OUI by parsing the given OUI file.
    Returns False if OUI is not found.
    """

    if oui is '':
        return False

    if not isfile(oui_file):
        return False

    cmd = ["""cat {0} |grep "^{1}" |awk '{{print $2}}'""".format(oui_file, oui.upper())]
    res = check_output(cmd, shell=True)
    res = res.rstrip().decode('utf-8')

    if res is not '':
        return res
    else:
        return False
