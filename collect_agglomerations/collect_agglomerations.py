import csv
import subprocess
import os
import sys

#mudar

REPO_FOLDER = "/home/infra/agglomerations/repos/%s"
OUT_FOLDER = "/home/infra/agglomerations/output"
EQUINOX = "/home/infra/apps/eclipse_mars/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"

# REPO_FOLDER = "/Users/diego/Downloads/%s"
# OUT_FOLDER = "/Users/diego/Downloads/out"
# EQUINOX = "/Applications/Eclipse.app/Contents/Eclipse/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"


ORGANIC = "organic.Organic"
MAIN = "org.eclipse.core.launcher.Main"


def can_proj_name(version):
    return version["name"].replace("/", "_")

def repository_folder(version):
    return REPO_FOLDER % (can_proj_name(version))

def already_downloaded(version):
    return os.path.exists(repository_folder(version))


def download_repository(version):
    if already_downloaded(version):
        return
    cmd = "git clone %s %s" % (version["sshUrl"], repository_folder(version))
    subprocess.call(cmd, shell=True)


def collect_agglomerations(version):
    smell_file = "%s/%s_%s_smells.json" % (OUT_FOLDER, can_proj_name(version), version["hash"])
    agg_file = "%s/%s_%s_agglomeration.json" % (OUT_FOLDER, can_proj_name(version), version["hash"])

    if os.path.exists(smell_file) and os.path.exists(agg_file):
        print "Versao %s ja coletada" % version["hash"]
        return

    cmd = 'java -jar -XX:MaxPermSize=6000m -Xms40m -Xmx6000m "%s" %s -application %s -sf "%s" -af "%s" -src "%s"'
    cmd = cmd % (EQUINOX, MAIN, ORGANIC, smell_file, agg_file, repository_folder(version))
    subprocess.call(cmd, shell=True)

def run_cmd(cmd):
    code = subprocess.call(cmd, shell=True)
    if code != 0:
        print "Erro ao rodar", cmd
        exit()

def revert_to_correct_version(version):
    codes = []
    repo = repository_folder(version)
    commit = version["hash"]

    stash = "git -C %s stash" % repo
    print stash
    run_cmd(stash)

    reset = "git -C %s reset HEAD --hard" % repo
    print reset
    run_cmd(reset)

    checkout = "git -C %s checkout %s" % (repo, commit)
    print checkout
    run_cmd(checkout)

def load_all():
    versions = []
    with open('versions_with_refactorings.csv') as input:
        reader = csv.DictReader(input, delimiter=',', quotechar='"')
        for version in reader:
            versions.append(version)
    return versions

# project_names = ["orhanobut/logger"]
project_names = set(sys.argv)
versions = load_all()
for version in versions:
    if version["name"] not in project_names:
        continue
    download_repository(version)
    revert_to_correct_version(version)
    collect_agglomerations(version)