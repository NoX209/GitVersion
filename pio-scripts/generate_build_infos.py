Import("env", "projenv")
import datetime
import os


# collect version time, hash and version
buildtimestring = datetime.datetime.now().strftime("%Y-%b-%d %X")
githash = os.environ.get('GITHUB_SHA') or "0"*40
gitversion = os.environ.get('GITHUB_REF_NAME') or "selfbuild"

# define content of build_infos.h
build_infos_h = f"""
#ifndef __build_infos__
#define __build_infos__

// !!! THIS FILE IS GENERATED - DO NOT MODIFY !!!

class BuildInfos {{
  public:
    const char* getBuildTime(){{
      return "{buildtimestring}";
    }}
    const char* getGitHash(){{
      return "{githash}";
    }}
    const char* getGitVersion(){{
      return "{gitversion}";
    }}
}};

BuildInfos Build;

#endif
"""

# define content of build_infos.cpp
build_infos_cpp = f"""
#include <build_infos.h>

// !!! THIS FILE IS GENERATED - DO NOT MODIFY !!!

BuildInfos Build;

const char* BuildInfos::getBuildTime(){{
  return "{buildtimestring}";
}}

const char* BuildInfos::getGitHash(){{
  return "{githash}";
}}

const char* BuildInfos::getGitVersion(){{
  return "{gitversion}";
}}
"""

# write files
with open('src/build_infos.h', 'w') as f:
  f.write(build_infos_h)
#with open('src/build_infos.cpp', 'w') as f:
#  f.write(build_infos_cpp)

# output info on build console
print("/-----------------------")
print("| generated build infos")
print(f"| {buildtimestring}")
print(f"| {githash}")
print(f"| {gitversion}")
print("\\-----------------------")
