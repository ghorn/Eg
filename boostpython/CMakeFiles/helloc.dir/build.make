# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canoncical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/jg/eg/boostpython

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/jg/eg/boostpython

# Include any dependencies generated for this target.
include CMakeFiles/helloc.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/helloc.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/helloc.dir/flags.make

CMakeFiles/helloc.dir/hello.o: CMakeFiles/helloc.dir/flags.make
CMakeFiles/helloc.dir/hello.o: hello.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/jg/eg/boostpython/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/helloc.dir/hello.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/helloc.dir/hello.o -c /home/jg/eg/boostpython/hello.cpp

CMakeFiles/helloc.dir/hello.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/helloc.dir/hello.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/jg/eg/boostpython/hello.cpp > CMakeFiles/helloc.dir/hello.i

CMakeFiles/helloc.dir/hello.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/helloc.dir/hello.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/jg/eg/boostpython/hello.cpp -o CMakeFiles/helloc.dir/hello.s

CMakeFiles/helloc.dir/hello.o.requires:
.PHONY : CMakeFiles/helloc.dir/hello.o.requires

CMakeFiles/helloc.dir/hello.o.provides: CMakeFiles/helloc.dir/hello.o.requires
	$(MAKE) -f CMakeFiles/helloc.dir/build.make CMakeFiles/helloc.dir/hello.o.provides.build
.PHONY : CMakeFiles/helloc.dir/hello.o.provides

CMakeFiles/helloc.dir/hello.o.provides.build: CMakeFiles/helloc.dir/hello.o
.PHONY : CMakeFiles/helloc.dir/hello.o.provides.build

# Object files for target helloc
helloc_OBJECTS = \
"CMakeFiles/helloc.dir/hello.o"

# External object files for target helloc
helloc_EXTERNAL_OBJECTS =

helloc.so: CMakeFiles/helloc.dir/hello.o
helloc.so: CMakeFiles/helloc.dir/build.make
helloc.so: CMakeFiles/helloc.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library helloc.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/helloc.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/helloc.dir/build: helloc.so
.PHONY : CMakeFiles/helloc.dir/build

CMakeFiles/helloc.dir/requires: CMakeFiles/helloc.dir/hello.o.requires
.PHONY : CMakeFiles/helloc.dir/requires

CMakeFiles/helloc.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/helloc.dir/cmake_clean.cmake
.PHONY : CMakeFiles/helloc.dir/clean

CMakeFiles/helloc.dir/depend:
	cd /home/jg/eg/boostpython && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/jg/eg/boostpython /home/jg/eg/boostpython /home/jg/eg/boostpython /home/jg/eg/boostpython /home/jg/eg/boostpython/CMakeFiles/helloc.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/helloc.dir/depend

