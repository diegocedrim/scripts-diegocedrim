import csv
import subprocess
import os
import sys

mapping = {
    "Netflix-Hystrix":"git@github.com:Netflix/Hystrix.git",
    "Netflix-SimianArmy":"git@github.com:Netflix/SimianArmy.git",
    "PhilJay-MPAndroidChart":"git@github.com:PhilJay/MPAndroidChart.git",
    "alibaba-dubbo":"git@github.com:alibaba/dubbo.git",
    "elastic-elasticsearch":"git@github.com:elastic/elasticsearch.git",
    "facebook-facebook-android-sdk":"git@github.com:facebook/facebook-android-sdk.git",
    "google-iosched":"git@github.com:google/iosched.git",
    "google-j2objc":"git@github.com:google/j2objc.git",
    "junit-team-junit4":"git@github.com:junit-team/junit4.git",
    "orhanobut-logger":"git@github.com:orhanobut/logger.git",
    "prestodb-presto":"git@github.com:prestodb/presto.git",
    "realm-realm-java":"git@github.com:realm/realm-java.git",
    "spring-projects-spring-boot":"git@github.com:spring-projects/spring-boot.git",
    "spring-projects-spring-framework":"git@github.com:spring-projects/spring-framework.git",
    "square-dagger":"git@github.com:square/dagger.git",
    "square-leakcanary":"git@github.com:square/leakcanary.git",
    "square-okhttp":"git@github.com:square/okhttp.git",
    "square-retrofit":"git@github.com:square/retrofit.git"
}


class Understand:
    def __init__(self, version):
        self.version = version

    def settings(self):
        cmd = "und settings -MetricOutputFile \"%s\" %s" % (self.metrics_file(), self.udb_file())
        run_cmd(cmd)
        cmd = "und settings -MetricMetrics all  %s" % self.udb_file()
        run_cmd(cmd)
        cmd = "und settings -MetricFileNameDisplayMode RelativePath %s" % self.udb_file()
        run_cmd(cmd)
        cmd = "und settings -MetricDeclaredInFileDisplayMode RelativePath %s" % self.udb_file()
        run_cmd(cmd)
        cmd = "und settings -MetricShowDeclaredInFile on %s" % self.udb_file()
        run_cmd(cmd)

    def udb_file(self):
        return OUT_FOLDER + "/%s-%s-project.udb" % (self.version["project_key"], self.version["hash"])

    def metrics_file(self):
        return OUT_FOLDER + "/%s-%s-metrics.csv" % (self.version["project_key"], self.version["hash"])

    def create_udb(self):
        cmd = "und create -db %s -languages java" % self.udb_file()
        run_cmd(cmd)

    def add_files(self):
        files = repository_folder(version) + "/files"
        cmd = "find %s -name \"*.java\"  > %s" % (repository_folder(version), files)
        run_cmd(cmd)
        cmd = "und -quiet -db %s add @%s" % (self.udb_file(), files)
        run_cmd(cmd)

    def analyze(self):
        cmd = "und -quiet analyze %s" % self.udb_file()
        run_cmd(cmd)

    def collect(self):
        print "Collecting", self.metrics_file()
        self.create_udb()
        self.add_files()
        self.analyze()
        self.settings()
        cmd = "und metrics -db %s" % self.udb_file()
        run_cmd(cmd)
        cmd = "rm -f %s" % self.udb_file()
        run_cmd(cmd)


REPO_FOLDER = "/home/infra/agglomerations/repos/%s"
OUT_FOLDER = "/home/infra/agglomerations/metrics-output"

# REPO_FOLDER = "/Users/diego/Downloads/%s"
# OUT_FOLDER = "/Users/diego/Downloads/metrics-out"


def can_proj_name(version):
    return version["project_key"].replace("/", "_")


def repository_folder(version):
    return REPO_FOLDER % (can_proj_name(version))


def already_downloaded(version):
    return os.path.exists(repository_folder(version))


def download_repository(version):
    if already_downloaded(version):
        return
    cmd = "git clone %s %s" % (version["sshUrl"], repository_folder(version))
    subprocess.call(cmd, shell=True)


def exists_metrics_file(version):
    und = Understand(version)
    filename = und.metrics_file()
    return os.path.exists(filename)


def collect_metrics(version):
    und = Understand(version)
    und.collect()


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


def load_all(starting=None, ending=None):
    versions = []
    with open('metrics_to_collect.csv') as input:
        reader = csv.DictReader(input, delimiter=';', quotechar='"')
        if starting is None and ending is None:
            for version in reader:
                version["sshUrl"] = mapping[version["project_key"]]
                versions.append(version)
        else:
            line_cursor = 0
            for version in reader:
                line_cursor += 1
                if starting <= line_cursor <= ending:
                    version["sshUrl"] = mapping[version["project_key"]]
                    versions.append(version)
    return versions

starting = int(sys.argv[1])
ending = int(sys.argv[2])
run_cmd("mkdir -p %s" % OUT_FOLDER)
# starting = 1
# ending = 2
versions = load_all(starting, ending)
# print versions
counter = 0
for version in versions:
    counter += 1
    print "Processing %s/%s (%s)" % (counter, len(versions), str(version))
    if not exists_metrics_file(version):
        # print version
        download_repository(version)
        revert_to_correct_version(version)
        collect_metrics(version)
