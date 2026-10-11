#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest.py —— quality_scan.py 一键自测

自动完成: 建 tests_fixture/ 种入已知问题样本 → 运行 quality_scan.py 扫描
→ 断言全部种入问题均被抓到（含 .py ast 精确行号）→ 校验 --help 与用法错误
（退出码 2）→ 6000 行大文件性能冒烟（不卡死）→ 清理临时目录 → 全部通过
打印 OK。

种入的样本与期望：
  long_deep.py  超长函数（def 在第 3 行，共 58 行）+ 深嵌套（第 9 行，深度 5）
                + 裸 print（第 59 行）+ 空 except（第 64 行）+ 超长行（第 67 行）
  debug.js      console.log（第 2 行，heuristic）+ 空 catch（第 5 行，heuristic）
                + TODO 标记（第 9 行）
  longfn.js     61 行函数（第 1 行，heuristic 近似）
  dup_a.py      6 行重复块出现两处（第 2、12 行）
  dup_b.py      同一重复块第三处（第 2 行，跨文件）
  note.txt      其他扩展名：FIXME 标记（第 2 行）
"""

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = Path(__file__).resolve().parent
SCAN = HERE / "quality_scan.py"
FIX = HERE / "tests_fixture"
PERF = HERE / "tests_fixture_perf"
OUT = HERE / "selftest_out.json"
OUT2 = HERE / "selftest_out2.json"

passed = 0
failed = []


def check(name, cond, extra=""):
    global passed
    if cond:
        passed += 1
        print("  PASS  %s" % name)
    else:
        failed.append(name)
        print("  FAIL  %s  %s" % (name, extra))


def run(*args):
    return subprocess.run(
        [sys.executable, str(SCAN)] + [str(a) for a in args],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        cwd=str(HERE))


def seed_fixture():
    FIX.mkdir(parents=True, exist_ok=True)
    PERF.mkdir(parents=True, exist_ok=True)

    # --- long_deep.py: 行号必须与 docstring 中的期望一致 ---
    lines = []
    lines.append("import os")                            # 1
    lines.append("")                                     # 2
    lines.append("def long_and_deep(items, flag):")      # 3  <- 函数起始
    lines.append("    acc = 0")                          # 4
    lines.append("    for i in items:")                  # 5  depth 1
    lines.append("        if i % 2 == 0:")               # 6  depth 2
    lines.append("            for j in range(3):")       # 7  depth 3
    lines.append("                if flag:")             # 8  depth 4
    lines.append("                    while j < 2:")     # 9  depth 5 <- 最深
    lines.append("                        acc += i * j") # 10
    lines.append("                        j += 1")       # 11
    for k in range(12, 59):                              # 12..58 填充行
        lines.append("    acc = acc + %d" % k)
    lines.append('    print("debug sample", acc)')       # 59 <- 裸 print
    lines.append("    return acc")                       # 60 <- 函数共 58 行
    lines.append("")                                     # 61
    lines.append("try:")                                 # 62
    lines.append("    os.getcwd()")                      # 63
    lines.append("except OSError:")                      # 64 <- 空 except
    lines.append("    pass")                             # 65
    lines.append("")                                     # 66
    long_line = 'LONG_SEED = "' + "a" * 112 + '"'
    assert len(long_line) > 120
    lines.append(long_line)                              # 67 <- 超长行
    (FIX / "long_deep.py").write_text("\n".join(lines) + "\n", encoding="utf-8")

    # --- debug.js ---
    js = (
        'function greet(name) {\n'
        '  console.log("hello", name);\n'
        '  try {\n'
        '    risky(name);\n'
        '  } catch (err) {}\n'
        '  return name;\n'
        '}\n'
        '\n'
        '// TODO: 上线前移除调试逻辑\n'
    )
    (FIX / "debug.js").write_text(js, encoding="utf-8")

    # --- longfn.js: 61 行函数（启发式近似） ---
    jl = [
        "function long_pad(items) {",
        "  let out = 0;",
        "  for (let i = 0; i < items.length; i++) {",
        "    out += items[i];",
        "  }",
    ]
    jl += ["  out = out + 1;"] * 54
    jl += ["  return out;", "}"]
    assert len(jl) == 61
    (FIX / "longfn.js").write_text("\n".join(jl) + "\n", encoding="utf-8")

    # --- 重复块（6 行核心内容，去掉首尾正好留 >=5 行窗口） ---
    dup_body = [
        "    total = 0",
        "    for item in data:",
        "        step = item * 2 + 1",
        "        total += step",
        "    if total > 100:",
        "        return total - 100",
        "    return total",
    ]
    dup_a = (
        "def part_one(data):\n"
        + "\n".join(dup_body) + "\n"
        + "\n\n"
        + "def part_two(data):\n"
        + "\n".join(dup_body) + "\n"
    )
    (FIX / "dup_a.py").write_text(dup_a, encoding="utf-8")
    dup_b = "def part_one_b(data):\n" + "\n".join(dup_body) + "\n"
    (FIX / "dup_b.py").write_text(dup_b, encoding="utf-8")

    # --- note.txt: 其他扩展名只查行数与残留标记 ---
    (FIX / "note.txt").write_text("说明文件\nFIXME: 待处理事项\n", encoding="utf-8")

    # --- 性能冒烟: 6000 行大文件（O(n) 重复块检测不应卡死） ---
    big = ["v%d = %d" % (i, i) for i in range(3000)]
    big += ["counter = counter + 1"] * 3000
    (PERF / "big.py").write_text("\n".join(big) + "\n", encoding="utf-8")


def cleanup():
    shutil.rmtree(FIX, ignore_errors=True)
    shutil.rmtree(PERF, ignore_errors=True)
    for p in (OUT, OUT2):
        try:
            p.unlink()
        except OSError:
            pass


def has(finds, ftype, file_end=None, line=None, heur=None, contains=None):
    for f in finds:
        if f["type"] != ftype:
            continue
        if file_end and not f["file"].endswith(file_end):
            continue
        if line is not None and f["line"] != line:
            continue
        if heur is not None and f["heuristic"] != heur:
            continue
        if contains and contains not in f["detail"]:
            continue
        return True
    return False


def count(finds, ftype):
    return sum(1 for f in finds if f["type"] == ftype)


def main():
    seed_fixture()
    try:
        # ---- 1) 主扫描（JSON 输出） ----
        r = run(FIX, "--json", OUT)
        check("主扫描退出码 0（有 findings 不是错误）", r.returncode == 0,
              r.stderr[-300:])
        data = json.loads(OUT.read_text(encoding="utf-8"))
        finds = data["findings"]

        check("scanned_files == 6", data["scanned_files"] == 6,
              str(data["scanned_files"]))
        check("skipped 为空", data["skipped"] == [])
        keys = {f["type"] for f in finds}
        check("findings 字段结构完整",
              all(set(f) == {"type", "file", "line", "detail", "heuristic"}
                  for f in finds))
        types = [f["type"] for f in finds]
        check("findings 按类型稳定排序", types == sorted(types))

        # .py ast 精确性
        check("long_function .py 精确起始行=3 (58 行)",
              has(finds, "long_function", "long_deep.py", line=3, heur=False,
                  contains="58 行"))
        check("deep_nesting .py 精确行=9 (深度 5)",
              has(finds, "deep_nesting", "long_deep.py", line=9, heur=False,
                  contains="深度 5"))
        check("deep_nesting 全部仅 1 条",
              count(finds, "deep_nesting") == 1,
              str([f for f in finds if f["type"] == "deep_nesting"]))
        check("debug_residue 裸 print 行=59 (ast)",
              has(finds, "debug_residue", "long_deep.py", line=59, heur=False))
        check("empty_catch .py 行=64 (ast, except: pass)",
              has(finds, "empty_catch", "long_deep.py", line=64, heur=False))
        check("long_line 行=67",
              has(finds, "long_line", "long_deep.py", line=67, heur=False)
              and count(finds, "long_line") == 1)

        # .js 启发式
        check("long_function .js 启发式 行=1",
              has(finds, "long_function", "longfn.js", line=1, heur=True))
        check("debug_residue console.log 行=2 (heuristic)",
              has(finds, "debug_residue", "debug.js", line=2, heur=True))
        check("empty_catch .js 行=5 (heuristic)",
              has(finds, "empty_catch", "debug.js", line=5, heur=True))

        # 重复块（同文件两处 + 跨文件一处 = 共 3 处）
        check("duplicate_block 共 3 处（含跨文件）",
              count(finds, "duplicate_block") == 1
              and has(finds, "duplicate_block", "dup_a.py", line=2,
                      contains="共 3 处")
              and has(finds, "duplicate_block", contains="dup_b.py:2-8"),
              str([f["detail"] for f in finds
                   if f["type"] == "duplicate_block"]))

        # 残留标记（TODO 在 .js，FIXME 在 .txt）
        check("residual_marker TODO 行=9 (.js)",
              has(finds, "residual_marker", "debug.js", line=9,
                  contains="TODO"))
        check("residual_marker FIXME 行=2 (.txt)",
              has(finds, "residual_marker", "note.txt", line=2,
                  contains="FIXME"))
        check("residual_marker 恰好 2 条", count(finds, "residual_marker") == 2)

        check("无 parse_error / long_file",
              count(finds, "parse_error") == 0 and count(finds, "long_file") == 0)

        # summary 与 findings 一致
        check("summary 计数与 findings 一致",
              data["summary"]["long_function"] == count(finds, "long_function") == 2
              and data["summary"]["duplicate_block"] == 1
              and data["summary"]["total"] == len(finds),
              str(data["summary"]))

        # ---- 2) 默认人类可读摘要 ----
        r2 = run(FIX)
        check("默认输出人类可读摘要（退出码 0）",
              r2.returncode == 0 and "证据收集器" in r2.stdout, r2.stderr[-200:])

        # ---- 3) 阈值参数生效（--max-file-lines 触发 long_file） ----
        r3 = run(FIX / "debug.js", "--max-file-lines", "3", "--json", OUT2)
        d3 = json.loads(OUT2.read_text(encoding="utf-8"))
        check("--max-file-lines 生效（long_file, line 为空）",
              r3.returncode == 0 and d3["scanned_files"] == 1
              and has(d3["findings"], "long_file", "debug.js", line=None))

        # ---- 4) CLI 行为 ----
        rh = run("--help")
        check("--help 退出码 0", rh.returncode == 0
              and ("用法" in rh.stdout or "usage" in rh.stdout
                   or "证据收集器" in rh.stdout))
        rn = run()
        check("缺少目标参数 → 退出码 2", rn.returncode == 2)
        rx = run(HERE / "no_such_dir_xyz")
        check("目标不存在 → 退出码 2", rx.returncode == 2)

        # ---- 5) 性能冒烟: 6000 行文件不卡死 ----
        t0 = time.time()
        rp = run(PERF, "--json", OUT2)
        elapsed = time.time() - t0
        dp = json.loads(OUT2.read_text(encoding="utf-8"))
        check("6000 行文件 15 秒内完成（实际 %.2fs）" % elapsed,
              rp.returncode == 0 and elapsed < 15, rp.stderr[-200:])
        check("6000 行文件仅报 long_file（重复行不误报 dup）",
              count(dp["findings"], "long_file") == 1
              and len(dp["findings"]) == 1,
              str(dp["summary"]))

    finally:
        cleanup()

    print("-" * 64)
    print("自测结果: %d 项通过, %d 项失败" % (passed, len(failed)))
    if failed:
        for name in failed:
            print("  失败: %s" % name)
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
