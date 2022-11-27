Import('env')
import os
import shutil
import gzip

OUTPUT_DIR = "build_output{}".format(os.path.sep)

def _get_cpp_define_value(env, define):
    define_list = [item[-1] for item in env["CPPDEFINES"] if item[0] == define]

    if define_list:
        return define_list[0]

    return None

def _create_dirs(dirs=["firmware"]):
    # check if output directories exist and create if necessary
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
        print(f"mkdir {OUTPUT_DIR}")

    for d in dirs:
        if not os.path.isdir("{}{}".format(OUTPUT_DIR, d)):
            os.mkdir("{}{}".format(OUTPUT_DIR, d))
            print(f"mkdir {OUTPUT_DIR}{d}")

def bin_rename_copy(source, target, env):
    print("/------")
    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
        print("mk out dir")
    if not os.path.isdir("{}{}".format(OUTPUT_DIR, "firmware")):
        os.mkdir("{}{}".format(OUTPUT_DIR, "firmware"))
        print("mk firmware dir")

    variant = env["PIOENV"]

    # create string with location and file names based on variant
    bin_file = "{}firmware{}{}.bin".format(OUTPUT_DIR, os.path.sep, variant)
    print(f"bin:{bin_file}")

    release_name = _get_cpp_define_value(env, "RELEASE_NAME")
    print(f"rel:{release_name}")

    if release_name:
        _create_dirs(["release"])
        release_file = "{}release{}GitVersion_{}_{}.bin".format(OUTPUT_DIR, os.path.sep, variant, release_name)
        shutil.copy(str(target[0]), release_file)
        print(f"copy rel: to'{str(target[0])}' from'{release_file}'")

    # check if new target files exist and remove if necessary
    for f in [bin_file]:
        if os.path.isfile(f):
            print(f"rm:{f}")
            os.remove(f)

    # copy firmware.bin to firmware/<variant>.bin
    shutil.copy(str(target[0]), bin_file)
    print(f"copy: to'{str(target[0])}' from'{bin_file}'")

    # # copy firmware.map to map/<variant>.map
    # if os.path.isfile("firmware.map"):
    #     shutil.move("firmware.map", map_file)
    print("\\------")

def bin_gzip(source, target, env):
    # _create_dirs()
    variant = env["PIOENV"]

    # create string with location and file names based on variant
    bin_file = "{}firmware{}GitVersion_{}.bin".format(OUTPUT_DIR, os.path.sep, variant)
    gzip_file = "{}firmware{}{}.bin.gz".format(OUTPUT_DIR, os.path.sep, variant)

    # check if new target files exist and remove if necessary
    if os.path.isfile(gzip_file): os.remove(gzip_file)

    # # write gzip firmware file
    # with open(bin_file,"rb") as fp:
    #     with gzip.open(gzip_file, "wb", compresslevel = 9) as f:
    #         shutil.copyfileobj(fp, f)

env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", [bin_rename_copy, bin_gzip])