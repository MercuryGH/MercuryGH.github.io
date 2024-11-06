---
title: Slang 构建指南
date: 2024-01-31 18:37:33
tags: 
- 着色语言
- 编译
---

> https://github.com/shader-slang/slang/

Slang 是一个“高级”着色语言，在 HLSL 的基础上提供了许多便捷的特性，同时支持自动微分功能。本文简要介绍如何在本地用 CMake 工具链构建 Slang。

<!--more-->

## git submodule 更新方式替换为 SSH clone

首先 clone git 仓库。网络原因可能导致 submodule clone 缓慢。为此，我们需要将 https clone 改为 ssh clone。找到 `.gitmodules`，替换文本

```
https://
```

为

```
ssh://git@
```

然后，完整执行以下命令：

```
git submodule init
git submodule sync
git submodule update
```

即可完成有一定速度保障的 ssh clone。

## CMake Presets 构建

参考官方构建教程，按需执行如下命令即可：

```
cmake --workflow --preset release
cmake --workflow --preset debug
```

需要 C++ 编译系统（gcc or clang），以及 ninja 构建工具。
如果 CMake 找不到 `--workflow` 选项，需要升级之。

## CMake 构建 examples

默认 `CMakePresets.json` 不提供 examples 的构建，但 `CMakeLists.txt` 中存在构建命令。我们需要在  `"buildPresets":` 下加入如下内容

```json
{
    "name": "examples",
    "inherits": "debug",
    "configurePreset": "single-component",
    "targets": [
        "all-examples"
    ]
},
```

随后运行

```
cmake --build --preset examples
```

即可在 `/build/Debug/bin/` 下找到构建出来的 examples 可执行文件。我们需要将 `examples` 下的若干 `.slang` 文件拷贝到这一目录下，才能正常运行这些可执行文件，否则会提示找不到相应的 shader。

最后，进入 `/build/Debug/bin/` 目录，运行样例程序 `./hello-world`。如果程序正常运行，会正常调用 Vulkan compute shader，最后终端会输出若干行数字。

## VSCode Debug 配置

如果你使用 VSCode 作为 IDE，可以编辑 `.vscode/launch.json` 进行 Debug:

```json
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "(gdb) Launch",
            "type": "cppdbg",
            "request": "launch",
            "program": "${workspaceFolder}/build/Debug/bin/hello-world",
            "args": [],
            "stopAtEntry": false,
            "cwd": "${fileDirname}",
            "environment": [],
            "externalConsole": false,
            "MIMode": "gdb",
            "setupCommands": [
                {
                    "description": "Enable pretty-printing for gdb",
                    "text": "-enable-pretty-printing",
                    "ignoreFailures": true
                },
                {
                    "description": "Set Disassembly Flavor to Intel",
                    "text": "-gdb-set disassembly-flavor intel",
                    "ignoreFailures": true
                }
            ]
        }
    ]
}
```

* `gdb` 可换为其他 Debugger，如 Windows 系统下的 `cppvsdbg`。在 `launch.json` 的右下角找到 `Add Configuration` 获取 Debugger 配置模板。
* `program` 可改为其他可执行文件目录。

