import csv
import subprocess
import os
import sys

#mudar

# REPO_FOLDER = "/home/infra/agglomerations/repos/%s"
# OUT_FOLDER = "/home/infra/agglomerations/output-lcom"
# EQUINOX = "/home/infra/apps/eclipse_mars/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"

REPO_FOLDER = "/Users/diego/Downloads/%s"
OUT_FOLDER = "/Users/diego/PycharmProjects/scripts_cedrim/organic_support/meyer_control_results"
EQUINOX = "/Applications/Eclipse.app/Contents/Eclipse/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"


ORGANIC = "organic.Organic"
MAIN = "org.eclipse.core.launcher.Main"


def collect_agglomerations(input_folder, prefix):
    smell_file = "%s/%s_smells.json" % (OUT_FOLDER, prefix)
    agg_file = "%s/%s_agglomeration.json" % (OUT_FOLDER, prefix)

    cmd = 'java -jar -XX:MaxPermSize=6000m -Xms40m -Xmx6000m "%s" %s -application %s -sf "%s" -af "%s" -src "%s"'
    cmd %= (EQUINOX, MAIN, ORGANIC, smell_file, agg_file, input_folder)
    subprocess.call(cmd, shell=True)


def run_cmd(cmd):
    code = subprocess.call(cmd, shell=True)
    if code != 0:
        print "Erro ao rodar", cmd
        exit()


collect_agglomerations("/Users/diego/Downloads/meyer-control", "meyer_control")