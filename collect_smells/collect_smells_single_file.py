import csv
import subprocess
import os
import sys
import glob

#mudar

# REPO_FOLDER = "/home/infra/smells/repos/%s"
# OUT_FOLDER = "/home/infra/smells/output_ultimos"
# EQUINOX = "/home/infra/apps/eclipse_mars/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"

REPO_FOLDER = "/Users/diego/repos/%s"
OUT_FOLDER = "/Users/diego/Downloads/output_ultimos"
EQUINOX = "/Applications/Eclipse.app/Contents/Eclipse/plugins/org.eclipse.equinox.launcher_1.3.100.v20150511-1540.jar"


ORGANIC = "organic.Organic"
MAIN = "org.eclipse.core.launcher.Main"


def can_proj_name(version):
    return version["project_name"].replace("/", "_")


def repository_folder(version):
    return REPO_FOLDER % (can_proj_name(version))


def already_downloaded(version):
    return os.path.exists(repository_folder(version))


def download_repository(version):
    if already_downloaded(version):
        return
    cmd = "git clone %s %s" % (version["url"], repository_folder(version))
    subprocess.call(cmd, shell=True)


def collect_smells(version):
    smell_file = "%s/%s_%s_smells.json" % (OUT_FOLDER, can_proj_name(version), version["commit"])

    if os.path.exists(smell_file):
        print "Versao %s ja coletada" % version["commit"]
        return

    cmd = 'java -jar -XX:MaxPermSize=6000m -Xms40m -Xmx6000m "%s" %s -application %s -sf "%s" -os -src "%s"'
    cmd = cmd % (EQUINOX, MAIN, ORGANIC, smell_file, repository_folder(version))
    subprocess.call(cmd, shell=True)


def run_cmd(cmd):
    code = subprocess.call(cmd, shell=True)
    if code != 0:
        print "Erro ao rodar", cmd
        exit()


def revert_to_correct_version(version):
    codes = []
    repo = repository_folder(version)
    commit = version["commit"]

    stash = "git -C %s stash" % repo
    print stash
    run_cmd(stash)

    reset = "git -C %s reset HEAD --hard" % repo
    print reset
    run_cmd(reset)

    checkout = "git -C %s checkout %s" % (repo, commit)
    print checkout
    run_cmd(checkout)


def load_all(file_name):
    versions = []
    with open(file_name) as input:
        reader = csv.DictReader(input, delimiter=',', quotechar='"')
        for version in reader:
            versions.append(version)
    return versions


for commits_file in ["last_commits/commits.csv"]:
    versions = load_all(commits_file)
    print "Processing %s (%s commits)" % (commits_file, len(versions))
    for version in versions:
        download_repository(version)
        smell_file = "%s/%s_%s_smells.json" % (OUT_FOLDER, can_proj_name(version), version["commit"])
        if os.path.exists(smell_file):
            print "%s: Versao %s ja coletada" % (version["project_name"], version["commit"])
            continue
        revert_to_correct_version(version)
        collect_smells(version)
