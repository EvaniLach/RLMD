# This file runs the nvcc commands to produce the desired output file along with
# the dependency file needed by CMake to compute dependencies.  In addition the
# file checks the output of each command and if the command fails it deletes the
# output files.

# Input variables
#
# verbose:BOOL=<>          OFF: Be as quiet as possible (default)
#                          ON : Describe each step
#

# Set these up as variables to make reading the generated file easier
set(CMAKE_COMMAND "/usr/bin/cmake")
set(source_file "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/./electrostatics/cuda_internal/StandardKernels.cu")
set(generated_file "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/src/cuda/fastgrid4_generated_StandardKernels.cu.cpp")
set(NVCC_generated_dependency_file "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/src/cuda/fastgrid4_generated_StandardKernels.cu.cpp.NVCC-depend")
set(cmake_dependency_file "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/src/cuda/fastgrid4_generated_StandardKernels.cu.cpp.depend")
set(CUDA_make2cmake "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/CMake/cuda/make2cmake.cmake")
set(generated_cubin_file "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/src/cuda/fastgrid4_generated_StandardKernels.cu.cpp.cubin.txt")
set(CUDA_parse_cubin "/mnt/c/Users/evani/OneDrive/Documenten/Phd/RLMD/fastgrid/fastgrid/CMake/cuda/parse_cubin.cmake")
set(build_cubin ON)

set(CUDA_NVCC "/usr/bin/nvcc")
set(CUDA_NVCC_FLAGS "--ptxas-options=-v")
set(nvcc_flags "-m64")
set(CUDA_NVCC_INCLUDE_ARGS "-I/usr/include;-I/usr/include")
set(format_flag "-cuda")

if(DEFINED CCBIN)
  set(CCBIN -ccbin "${CCBIN}")
endif()

if(debug)
  set(CMAKE_COMMAND "C:/code/CMake-cuda-staging/build-32/src/debug/args.exe")
  set(CUDA_NVCC "C:/code/CMake-cuda-staging/build-32/src/debug/args.exe")
endif()

# cuda_execute_process - Executes a command with optional command echo and status message.
#
#   status  - Status message to print if verbose is true
#   command - COMMAND argument from the usual execute_process argument structure
#   ARGN    - Remaining arguments are the command with arguments
#
#   CUDA_result - return value from running the command
#
# Make this a macro instead of a function, so that things like RESULT_VARIABLE
# and other return variables are present after executing the process.
macro(cuda_execute_process status command)
  set(_command ${command})
  if(NOT _command STREQUAL "COMMAND")
    message(FATAL_ERROR "Malformed call to cuda_execute_process.  Missing COMMAND as second argument. (command = ${command})")
  endif()
  if(verbose)
    execute_process(COMMAND "${CMAKE_COMMAND}" -E echo -- ${status})
    # Now we need to build up our command string.  We are accounting for quotes
    # and spaces, anything else is left up to the user to fix if they want to
    # copy and paste a runnable command line.
    set(cuda_execute_process_string)
    foreach(arg ${ARGN})
      # If there are quotes, excape them, so they come through.
      string(REPLACE "\"" "\\\"" arg ${arg})
      # Args with spaces need quotes around them to get them to be parsed as a single argument.
      if(arg MATCHES " ")
        list(APPEND cuda_execute_process_string "\"${arg}\"")
      else()
        list(APPEND cuda_execute_process_string ${arg})
      endif()
    endforeach()
    # Echo the command
    execute_process(COMMAND ${CMAKE_COMMAND} -E echo ${cuda_execute_process_string})
  endif(verbose)
  # Run the command
  execute_process(COMMAND ${ARGN} RESULT_VARIABLE CUDA_result )
endmacro()

# Delete the target file
cuda_execute_process(
  "Removing ${generated_file}"
  COMMAND "${CMAKE_COMMAND}" -E remove "${generated_file}"
  )

# Generate the dependency file
cuda_execute_process(
  "Generating dependency file: ${NVCC_generated_dependency_file}"
  COMMAND "${CUDA_NVCC}"
  "${source_file}"
  ${CUDA_NVCC_FLAGS}
  ${nvcc_flags}
  ${CCBIN}
  -DNVCC
  -M
  -o "${NVCC_generated_dependency_file}"
  ${CUDA_NVCC_INCLUDE_ARGS}
  )

if(CUDA_result)
  message(FATAL_ERROR "Error generating ${generated_file}")
endif()

# Generate the cmake readable dependency file to a temp file.  Don't put the
# quotes just around the filenames for the input_file and output_file variables.
# CMake will pass the quotes through and not be able to find the file.
cuda_execute_process(
  "Generating temporary cmake readable file: ${cmake_dependency_file}.tmp"
  COMMAND "${CMAKE_COMMAND}"
  -D "input_file:FILEPATH=${NVCC_generated_dependency_file}"
  -D "output_file:FILEPATH=${cmake_dependency_file}.tmp"
  -P "${CUDA_make2cmake}"
  )

if(CUDA_result)
  message(FATAL_ERROR "Error generating ${generated_file}")
endif()

# Copy the file if it is different
cuda_execute_process(
  "Copy if different ${cmake_dependency_file}.tmp to ${cmake_dependency_file}"
  COMMAND "${CMAKE_COMMAND}" -E copy_if_different "${cmake_dependency_file}.tmp" "${cmake_dependency_file}"
  )

if(CUDA_result)
  message(FATAL_ERROR "Error generating ${generated_file}")
endif()

# Delete the temporary file
cuda_execute_process(
  "Removing ${cmake_dependency_file}.tmp and ${NVCC_generated_dependency_file}"
  COMMAND "${CMAKE_COMMAND}" -E remove "${cmake_dependency_file}.tmp" "${NVCC_generated_dependency_file}"
  )

if(CUDA_result)
  message(FATAL_ERROR "Error generating ${generated_file}")
endif()

# Generate the code
cuda_execute_process(
  "Generating ${generated_file}"
  COMMAND "${CUDA_NVCC}"
  "${source_file}"
  ${CUDA_NVCC_FLAGS}
  ${nvcc_flags}
  ${CCBIN}
  -DNVCC
  ${format_flag} -o "${generated_file}"
  ${CUDA_NVCC_INCLUDE_ARGS}
  )

if(CUDA_result)
  # Since nvcc can sometimes leave half done files make sure that we delete the output file.
  cuda_execute_process(
    "Removing ${generated_file}"
    COMMAND "${CMAKE_COMMAND}" -E remove "${generated_file}"
    )
  message(FATAL_ERROR "Error generating file ${generated_file}")
else()
  message("Generated ${generated_file} successfully.")
endif()

# Cubin resource report commands.
if( build_cubin )
  # Run with -cubin to produce resource usage report.
  cuda_execute_process(
    "Generating ${generated_cubin_file}"
    COMMAND "${CUDA_NVCC}"
    "${source_file}"
    ${CUDA_NVCC_FLAGS}
    ${nvcc_flags}
    ${CCBIN}
    -DNVCC
    -cubin
    -o "${generated_cubin_file}"
    ${CUDA_NVCC_INCLUDE_ARGS}
    )

  # Execute the parser script.
  cuda_execute_process(
    "Executing the parser script"
    COMMAND  "${CMAKE_COMMAND}"
    -D "input_file:STRING=${generated_cubin_file}"
    -P "${CUDA_parse_cubin}"
    )

endif( build_cubin )
