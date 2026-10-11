#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quality_scan.py —— 代码质量「证据收集器」（不是裁判）

用途
----
扫描目标目录或文件，收集可机械核实的质量相关「事实证据」：

  1. long_file        超长文件（行数 > --max-file-lines，适用于所有文本文件）
  2. long_function    超长函数（行数 > --max-func-lines）
  3. deep_nesting     深嵌套（最大嵌套深度 > --max-depth 的位置）
  4. duplicate_block  重复代码块（去空白后 >=5 连续行，在文件内或跨文件
                      出现 >=2 次；行块哈希，O(n)）
  5. residual_marker  残留标记（TODO / FIXME / XXX / HACK 的计数与位置）
  6. debug_residue    调试残留（Python 裸 print( 调用、JS console.log 调用；
                      仅报告事实，type=debug_residue 体现「证据非结论」——
                      是否应删由人判断）
  7. empty_catch      空 except/catch（如 Python ``except ...: pass``、
                      JS ``catch (e) {}``）
  8. long_line        超长行（>120 字符）计数
  9. parse_error      Python 源码无法通过 ast 解析（本身即证据）

分析方式
--------
- .py / .pyw / .pyi : 用 ast 模块精确分析（函数起止行、嵌套深度、
  print 调用、空 except），heuristic=false。
- .js/.mjs/.cjs/.ts/.jsx/.tsx/.java/.go/.c/.h/.cpp/.cc/.cxx/.hpp/.rs/
  .kt/.swift/.cs/.php/.scala 等 : 用文本启发式近似（大括号块近似函数、
  缩进层级近似嵌套、正则近似空 catch / console.log），一律标注
  heuristic=true。
- 其他扩展名 : 只做行数（超长文件、超长行）与残留标记检查。
- 重复块检测对所有文本文件启用（去空白后整行比对，纯事实）。

边界（务必阅读）
----------------
- 本脚本是「证据收集器，不是裁判」：只输出可机械核实的事实，不做好坏
  判断、不打分、不给修改建议；「有 findings」不是错误，退出码仍为 0。
- heuristic=true 的结果来自文本启发式，可能有误报/漏报，仅供人工复核；
  heuristic=false 表示证据来自精确分析（ast）或纯文本事实
  （行数、标记、重复块）。
- 仅依赖 Python 标准库（>= 3.8），跨平台（Windows / Linux / macOS）。
- 跳过：二进制文件（含 NUL 字节）与 node_modules/.git/venv/.venv/
  dist/build/__pycache__ 目录；目录访问失败记入 skipped 并继续。
- 非 UTF-8 文本按 latin-1 兜底解码并记入 skipped 注记（避免坏字节被
  替换成 U+FFFD 后产生假 parse_error；非 ASCII 内容可能显示为乱码，
  行号不受影响）。
- 行切分与 ast 同口径：仅 \r\n、\r、\n 计为换行（\x0c/\x0b/\u2028 等
  不算），保证文本行号与 ast 行号一致。

用法
----
    python quality_scan.py <目标目录或文件> [--json out.json]
                           [--max-func-lines 50] [--max-depth 4]
                           [--max-file-lines 800]

默认打印人类可读摘要；--json 将结构化结果写入指定文件。
JSON 结构：
    {"target": ..., "scanned_files": N, "skipped": [...],
     "summary": {各类型计数}, "findings": [{"type", "file", "line"(可空),
     "detail", "heuristic"}]}
findings 按类型分组稳定排序（type -> file -> line）。

退出码：0 正常完成（即使有 findings）；2 用法错误（含目标不存在、
阈值非正）；1 运行期 I/O 错误。
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

TOOL_NAME = "quality_scan"
TOOL_VERSION = "1.0.0"

# ---------------------------------------------------------------------------
# 常量与正则
# ---------------------------------------------------------------------------

SKIP_DIRS = {"node_modules", ".git", "venv", ".venv", "dist", "build", "__pycache__"}

PY_EXTS = {".py", ".pyw", ".pyi"}

HEURISTIC_EXTS = {
    ".js", ".mjs", ".cjs", ".ts", ".jsx", ".tsx",
    ".java", ".go", ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh",
    ".rs", ".kt", ".kts", ".swift", ".cs", ".php", ".scala",
}

FINDING_TYPES = (
    "long_file",        # 超长文件
    "long_function",    # 超长函数
    "deep_nesting",     # 深嵌套
    "duplicate_block",  # 重复代码块
    "residual_marker",  # TODO/FIXME/XXX/HACK
    "debug_residue",    # print( / console.log（证据非结论）
    "empty_catch",      # 空 except/catch
    "long_line",        # 超长行(>120)
    "parse_error",      # Python 源码解析失败
)

LONG_LINE_LIMIT = 120   # 超长行阈值（字符数）
DUP_WINDOW = 5          # 重复块窗口：连续行数

# 行切分口径：与 ast / Python 源码一致，仅 \r\n、\r、\n 计为换行。
# （str.splitlines 还会把 \x0c/\x0b/\u2028/\u2029/\x85 等当换行，
#   导致文本行号与 ast 行号错位）
LINE_SEP_RE = re.compile(r"\r\n|\r|\n")

# 残留标记：TODO/FIXME/XXX/HACK，前后紧邻字母/数字则不算（避免匹配 xxxxx）
MARKER_RE = re.compile(r"(?<![A-Za-z0-9])(TODO|FIXME|XXX|HACK)(?![A-Za-z0-9])")

# JS 系调试残留
CONSOLE_LOG_RE = re.compile(r"console\.log\s*\(")

# 空 catch 启发式：catch (e) {} / catch {} / catch (...) {}（C++）
EMPTY_CATCH_RE = re.compile(
    r"catch\s*(?:\(\s*(?:\.\.\.|[A-Za-z_$][\w$]*)\s*\))?\s*\{\s*\}"
)

# 函数头启发式（自上一处语句边界 ; { } 以来累积的代码文本）
FUNC_HEAD_RE = re.compile(
    r"""(?:
        \bfunction\b |
        \bfunc\s+(?:\([^{}]*\)\s*)?[A-Za-z_$][\w$]* |
        \bfn\s+[A-Za-z_$][\w$]* |
        \bfun\s+[A-Za-z_$][\w$]* |
        \bdef\s+[A-Za-z_$][\w$]* |
        \b(?:public|private|protected)\b |
        [A-Za-z_$][\w$]*\s*\([^()]*\)\s*(?:(?:const|noexcept|final|override)\s*)*$ |
        [A-Za-z_$\)\]]\s*=>\s*$
    )""",
    re.VERBOSE,
)

# 明确不是函数头的控制结构 / 类型定义（可带修饰符前缀）
NON_FUNC_HEAD_RE = re.compile(
    r"^\s*(?:(?:public|private|protected|static|final|abstract|sealed|override|"
    r"virtual|inline|extern|const|let|var|export|default|async)\s+)*"
    r"(?:if|elif|else|for|while|switch|catch|try|finally|do|return|throw|case|"
    r"default|break|continue|class|interface|enum|struct|union|record|module|mod|"
    r"impl|trait|object|namespace|package|import|using|go|defer|select|"
    r"synchronized|lock|with|match|new|delete|sizeof|typeof)\b"
)

# ---------------------------------------------------------------------------
# 通用工具
# ---------------------------------------------------------------------------


def _add(findings, ftype, disp, line, detail, heuristic):
    """追加一条 finding（证据条目）。"""
    findings.append({
        "type": ftype,
        "file": disp,
        "line": line,
        "detail": detail,
        "heuristic": heuristic,
    })


def display(path: Path, target: Path) -> str:
    """输出用的展示路径：目录目标下的文件给出相对路径，其余给原样路径。"""
    if path == target:
        return path.name
    try:
        return path.resolve().relative_to(target.resolve()).as_posix()
    except (ValueError, OSError):
        return path.as_posix()


def split_lines(text: str) -> list:
    """按 Python 源码行规则切分文本（仅 \\r\\n、\\r、\\n 计为换行）。

    与 ast 的行号口径一致（str.splitlines 会把 \x0c 等也当换行导致偏移）；
    末尾换行不产生多余空行，与 splitlines 的行为保持一致。
    """
    parts = LINE_SEP_RE.split(text)
    if parts and parts[-1] == "":
        parts.pop()
    return parts


def collect_files(target: Path, skipped):
    """收集待扫描文件；目录按名称排序保证稳定；跳过指定目录与二进制。"""
    if target.is_file():
        return [target]

    def _on_walk_error(err):
        # 目录访问失败（权限不足等）：记入 skipped 并继续，保证结果不静默缺失
        where = getattr(err, "filename", None) or target.as_posix()
        skipped.append("目录访问失败: %s (%s)"
                       % (where, getattr(err, "strerror", None) or err))

    out = []
    for root, dirs, names in os.walk(target, onerror=_on_walk_error):
        for d in sorted(dirs):
            if d in SKIP_DIRS:
                skipped.append("目录: " + (Path(root) / d).as_posix())
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(names):
            out.append(Path(root) / name)
    return out


# ---------------------------------------------------------------------------
# Python（ast 精确分析）
# ---------------------------------------------------------------------------

_FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
_TRY_TYPES = (ast.Try, ast.TryStar) if hasattr(ast, "TryStar") else (ast.Try,)
_MATCH_TYPES = (ast.Match,) if hasattr(ast, "Match") else ()
_BLOCK_STEP_TYPES = (ast.If, ast.For, ast.AsyncFor, ast.While,
                     ast.With, ast.AsyncWith) + _TRY_TYPES + _MATCH_TYPES


def _touch_depth(best, depth, lineno):
    """记录更深一层控制流块（同深保留首次出现位置）。"""
    if depth > best[0]:
        best[0] = depth
        best[1] = lineno


def _scan_block_depth(stmts, depth, best):
    """递归计算控制流块嵌套深度（不进入嵌套函数/类——它们各自单独分析）。

    深度语义：函数体/模块体基准为 0，每个 if/for/while/try/with/match
    块使深度 +1；elif 链视为同级；else/finally/except 体与其宿主块同级。
    """
    for s in stmts:
        if isinstance(s, _FUNC_TYPES + (ast.ClassDef,)):
            continue  # 嵌套函数/类单独作为分析单元
        if isinstance(s, ast.If):
            d = depth + 1
            _touch_depth(best, d, s.lineno)
            _scan_block_depth(s.body, d, best)
            if len(s.orelse) == 1 and isinstance(s.orelse[0], ast.If):
                _scan_block_depth(s.orelse, depth, best)  # elif 链同级
            else:
                _scan_block_depth(s.orelse, d, best)      # else 同级
        elif isinstance(s, (ast.For, ast.AsyncFor, ast.While)):
            d = depth + 1
            _touch_depth(best, d, s.lineno)
            _scan_block_depth(s.body, d, best)
            _scan_block_depth(s.orelse, d, best)
        elif isinstance(s, _TRY_TYPES):
            d = depth + 1
            _touch_depth(best, d, s.lineno)
            _scan_block_depth(s.body, d, best)
            for h in s.handlers:
                _touch_depth(best, d, h.lineno)
                _scan_block_depth(h.body, d, best)
            _scan_block_depth(s.orelse, d, best)
            _scan_block_depth(s.finalbody, d, best)
        elif isinstance(s, (ast.With, ast.AsyncWith)):
            d = depth + 1
            _touch_depth(best, d, s.lineno)
            _scan_block_depth(s.body, d, best)
        elif _MATCH_TYPES and isinstance(s, _MATCH_TYPES):
            d = depth + 1
            _touch_depth(best, d, s.lineno)
            for case in s.cases:
                _scan_block_depth(case.body, d, best)


def analyze_python(disp, text, args, findings):
    """对 Python 源码做 ast 精确分析（heuristic=false）。"""
    try:
        tree = ast.parse(text)
    except SyntaxError as e:
        _add(findings, "parse_error", disp, getattr(e, "lineno", None) or 1,
             "Python 语法错误: %s" % e.msg, False)
        return
    except (ValueError, RecursionError) as e:
        _add(findings, "parse_error", disp, None,
             "Python 解析失败: %s" % e, False)
        return

    for node in ast.walk(tree):
        if isinstance(node, _FUNC_TYPES):
            name = node.name
            end = getattr(node, "end_lineno", None)
            if end is not None:
                length = end - node.lineno + 1
                if length > args.max_func_lines:
                    _add(findings, "long_function", disp, node.lineno,
                         "函数 %s() 共 %d 行（阈值 %d）"
                         % (name, length, args.max_func_lines), False)
            best = [0, None]
            _scan_block_depth(node.body, 0, best)
            if best[0] > args.max_depth:
                _add(findings, "deep_nesting", disp, best[1],
                     "函数 %s() 内最大控制流嵌套深度 %d（阈值 %d）"
                     % (name, best[0], args.max_depth), False)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "print":
            _add(findings, "debug_residue", disp, node.lineno,
                 "裸 print(...) 调用（证据非结论）", False)
        elif isinstance(node, ast.ExceptHandler):
            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                var = "，变量 %s" % node.name if node.name else ""
                _add(findings, "empty_catch", disp, node.lineno,
                     "空 except（子句体仅为 pass%s）" % var, False)

    # 模块级（函数之外）的深嵌套
    best = [0, None]
    _scan_block_depth(tree.body, 0, best)
    if best[0] > args.max_depth:
        _add(findings, "deep_nesting", disp, best[1],
             "模块级最大控制流嵌套深度 %d（阈值 %d）"
             % (best[0], args.max_depth), False)


# ---------------------------------------------------------------------------
# 启发式语言（JS/TS/Java/Go/C/C++/Rust 等，文本近似，heuristic=true）
# ---------------------------------------------------------------------------


def _clean_code(text):
    """把注释与字符串字面量内容替换为空白（逐字符 1:1，保留换行与行列号）。

    返回“纯代码骨架”，供大括号/正则分析使用，避免被字符串与注释误导。
    这是启发式的一部分：模板字符串插值 ${...} 内的代码也会被清空。
    """
    out = []
    i, n = 0, len(text)
    NORMAL, LINE_C, BLOCK_C, IN_STR = range(4)
    state = NORMAL
    quote = ""
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state == NORMAL:
            if c == "/" and nxt == "/":
                state = LINE_C
                out.append("  ")
                i += 2
                continue
            if c == "/" and nxt == "*":
                state = BLOCK_C
                out.append("  ")
                i += 2
                continue
            if c in ('"', "'", "`"):
                state = IN_STR
                quote = c
                out.append(" ")
                i += 1
                continue
            out.append(c)
            i += 1
        elif state == LINE_C:
            if c == "\n":
                state = NORMAL
                out.append("\n")
            else:
                out.append(" ")
            i += 1
        elif state == BLOCK_C:
            if c == "*" and nxt == "/":
                state = NORMAL
                out.append("  ")
                i += 2
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
        else:  # IN_STR
            if c == "\\" and nxt:
                if nxt == "\n":
                    out.append(" \n")
                else:
                    out.append("  ")
                i += 2
                continue
            if c == quote:
                state = NORMAL
                out.append(" ")
                i += 1
                continue
            out.append("\n" if c == "\n" else " ")
            i += 1
    return "".join(out)


def _guess_func_name(header):
    m = re.search(
        r"(?:function|func|fn|fun|def)\s+(?:\([^{}]*\)\s*)?([A-Za-z_$][\w$]*)",
        header)
    if m:
        return m.group(1)
    m = re.search(r"([A-Za-z_$][\w$]*)\s*\([^()]*\)\s*$", header)
    if m:
        return m.group(1)
    return None


def analyze_heuristic(disp, text, args, findings):
    """对大括号类语言做文本启发式分析，结果一律 heuristic=true。"""
    cleaned = _clean_code(text)

    # --- 1) 超长函数：大括号块近似 ---
    stack = []          # [(is_func, start_line, header)]
    buf = []            # 自上一处语句边界以来的代码文本
    paren = 0           # 括号深度（for 头内的 “;” 不重置缓冲）
    line_no = 1
    for ch in cleaned:
        if ch == "\n":
            line_no += 1
            buf.append(" ")
            continue
        if ch == "(":
            paren += 1
            buf.append(ch)
        elif ch == ")":
            paren = max(0, paren - 1)
            buf.append(ch)
        elif ch == "{":
            header = "".join(buf)[-400:].strip()
            is_func = bool(FUNC_HEAD_RE.search(header)) and \
                not NON_FUNC_HEAD_RE.search(header)
            stack.append((is_func, line_no, header))
            buf = []
        elif ch == "}":
            if stack:
                is_func, start, header = stack.pop()
                if is_func:
                    length = line_no - start + 1
                    if length > args.max_func_lines:
                        name = _guess_func_name(header)
                        label = "函数 %s()" % name if name else "函数(名称未识别)"
                        _add(findings, "long_function", disp, start,
                             "%s 约 %d 行（阈值 %d；大括号块近似）"
                             % (label, length, args.max_func_lines), True)
            buf = []
        elif ch == ";" and paren == 0:
            buf = []
        else:
            buf.append(ch)

    # --- 2) 深嵌套：缩进层级近似 ---
    lines = cleaned.split("\n")
    logical = []
    for idx, raw in enumerate(lines, 1):
        if not raw.strip():
            continue
        leading = raw[: len(raw) - len(raw.lstrip())].expandtabs(4)
        logical.append((len(leading), idx))
    if logical:
        distinct = sorted({d for d, _ in logical})
        diffs = [b - a for a, b in zip(distinct, distinct[1:]) if b > a]
        unit = Counter(diffs).most_common(1)[0][0] if diffs else 4
        unit = max(2, min(unit, 8))
        max_level, max_line, first_over = 0, None, None
        for indent, idx in logical:
            level = indent // unit
            if level > max_level:
                max_level, max_line = level, idx
            if first_over is None and level > args.max_depth:
                first_over = idx
        if max_level > args.max_depth:
            _add(findings, "deep_nesting", disp, first_over or max_line,
                 "按缩进近似最大嵌套层级约 %d（阈值 %d；缩进启发式）"
                 % (max_level, args.max_depth), True)

    # --- 3) 调试残留：console.log（代码骨架上匹配，字符串/注释不计） ---
    for idx, raw in enumerate(lines, 1):
        if CONSOLE_LOG_RE.search(raw):
            _add(findings, "debug_residue", disp, idx,
                 "console.log(...) 调用（证据非结论；正则近似）", True)

    # --- 4) 空 catch：正则近似 ---
    for m in EMPTY_CATCH_RE.finditer(cleaned):
        line = cleaned.count("\n", 0, m.start()) + 1
        _add(findings, "empty_catch", disp, line,
             "空 catch 块（正则近似）", True)


# ---------------------------------------------------------------------------
# 所有文本文件的公共检查 + 重复块
# ---------------------------------------------------------------------------


def analyze_common(disp, lines, args, findings, dup_map, stripped_store):
    """行数 / 残留标记 / 超长行 / 重复块窗口（纯文本事实，heuristic=false）。"""
    n = len(lines)
    if n > args.max_file_lines:
        _add(findings, "long_file", disp, None,
             "文件共 %d 行（阈值 %d）" % (n, args.max_file_lines), False)

    for idx, raw in enumerate(lines, 1):
        for m in MARKER_RE.finditer(raw):
            _add(findings, "residual_marker", disp, idx,
                 "%s 标记: %s" % (m.group(1), raw.strip()[:60]), False)

    longs = [(idx, len(raw)) for idx, raw in enumerate(lines, 1)
             if len(raw) > LONG_LINE_LIMIT]
    if longs:
        _add(findings, "long_line", disp, longs[0][0],
             ">120 字符的行共 %d 处，最长 %d 字符"
             % (len(longs), max(ln for _, ln in longs)), False)

    stripped = [ln.strip() for ln in lines]
    stripped_store[disp] = stripped
    for i in range(n - DUP_WINDOW + 1):
        win = stripped[i: i + DUP_WINDOW]
        if any(not s for s in win):
            continue  # 空行打断连续性
        if sum(1 for s in win if len(s) >= 3) < 3:
            continue  # 整窗几乎都是 { } ; 等碎片，视为噪音
        dup_map.setdefault(tuple(win), []).append((disp, i + 1))


def _window_key(stripped_store, disp, start):
    """取 disp 文件第 start 行（1-based）起的窗口键；无效返回 None。"""
    stripped = stripped_store.get(disp)
    if stripped is None or start < 1 or start + DUP_WINDOW - 1 > len(stripped):
        return None
    win = stripped[start - 1: start - 1 + DUP_WINDOW]
    if any(not s for s in win):
        return None
    if sum(1 for s in win if len(s) >= 3) < 3:
        return None
    return tuple(win)


def _extend_dup_end(stripped_store, dup_map, disp, start):
    """向右扩展重复块终点：后续窗口仍出现 >=2 次即延伸（与左极大对称），
    使相邻/重叠的等值行窗口合并为完整范围（10 行块报 2-11 而非 2-6）。"""
    stripped = stripped_store.get(disp)
    if stripped is None:
        return start + DUP_WINDOW - 1
    end = start + DUP_WINDOW - 1
    while end < len(stripped):
        # 覆盖到 end+1 行的唯一窗口起点：
        nxt = _window_key(stripped_store, disp, end - DUP_WINDOW + 2)
        if nxt is None or len(dup_map.get(nxt, ())) < 2:
            break
        end += 1
    return end


def finalize_duplicates(dup_map, stripped_store, findings):
    """汇总重复块：仅报告“左极大”块起点，并向右扩展/合并相邻重叠窗口，
    给出每处的完整行范围。"""
    for occs in dup_map.values():
        if len(occs) < 2:
            continue
        kept = []
        for disp, start in occs:
            prev = _window_key(stripped_store, disp, start - 1)
            if prev is not None and len(dup_map.get(prev, ())) >= 2:
                continue  # 前一行窗口也能匹配 → 本窗口不是块起点
            kept.append((disp, start))
        if len(kept) < 2:
            continue
        kept.sort()
        clusters = []  # [file, start, end]
        for disp, start in kept:
            end = _extend_dup_end(stripped_store, dup_map, disp, start)
            if clusters and clusters[-1][0] == disp and start <= clusters[-1][2]:
                clusters[-1][2] = max(clusters[-1][2], end)
            else:
                clusters.append([disp, start, end])
        if len(clusters) < 2:
            continue
        locs = "、".join("%s:%d-%d" % (d, a, b) for d, a, b in clusters)
        _add(findings, "duplicate_block", clusters[0][0], clusters[0][1],
             "重复代码块（去空白后 %d 行）共 %d 处：%s"
             % (clusters[0][2] - clusters[0][1] + 1, len(clusters), locs), False)


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------


def scan_target(args):
    """执行扫描并返回结果字典（即 JSON 输出结构）。"""
    target = Path(args.target)
    skipped = []
    findings = []
    dup_map = {}
    stripped_store = {}
    scanned = 0

    for path in collect_files(target, skipped):
        disp = display(path, target)
        try:
            raw = path.read_bytes()
        except OSError as e:
            skipped.append("读取失败: %s (%s)" % (disp, e))
            continue
        if b"\x00" in raw:
            skipped.append("二进制文件: %s" % disp)
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            # 非 UTF-8 文本：latin-1 对任意字节均可解码，避免坏字节被
            # errors="replace" 换成 U+FFFD（GBK 双字节第二字节撞上引号/
            # 反斜杠时会假报 parse_error）；记一条注记供人工复核编码
            text = raw.decode("latin-1")
            skipped.append("非 UTF-8 编码，已按 latin-1 兜底解码: %s" % disp)
        lines = split_lines(text)
        scanned += 1

        analyze_common(disp, lines, args, findings, dup_map, stripped_store)
        ext = path.suffix.lower()
        if ext in PY_EXTS:
            analyze_python(disp, text, args, findings)
        elif ext in HEURISTIC_EXTS:
            analyze_heuristic(disp, text, args, findings)

    finalize_duplicates(dup_map, stripped_store, findings)

    # 按类型分组稳定排序（type -> file -> line -> detail）
    findings.sort(key=lambda f: (f["type"], f["file"], f["line"] or 0, f["detail"]))
    counts = Counter(f["type"] for f in findings)
    summary = {t: counts.get(t, 0) for t in FINDING_TYPES}
    summary["total"] = len(findings)

    return {
        "target": target.as_posix(),
        "scanned_files": scanned,
        "skipped": skipped,
        "summary": summary,
        "findings": findings,
    }


def print_human(payload):
    """打印人类可读摘要（默认输出）。"""
    out = []
    out.append("=" * 64)
    out.append("质量证据扫描报告 —— 证据收集器，不是裁判")
    out.append("目标: %s" % payload["target"])
    out.append("已扫描文件: %d；跳过: %d 项"
               % (payload["scanned_files"], len(payload["skipped"])))
    out.append("-" * 64)
    out.append("发现统计（按类型）:")
    summary = payload["summary"]
    for t in FINDING_TYPES:
        if summary.get(t):
            out.append("  %-16s %5d" % (t, summary[t]))
    out.append("  %-16s %5d" % ("total", summary.get("total", 0)))
    if payload["skipped"]:
        out.append("跳过明细（前 10 项）:")
        for s in payload["skipped"][:10]:
            out.append("  - %s" % s)
        if len(payload["skipped"]) > 10:
            out.append("  ... 等共 %d 项" % len(payload["skipped"]))
    if payload["findings"]:
        out.append("证据明细（按类型分组，最多显示 100 条）:")
        shown = 0
        for f in payload["findings"]:
            if shown >= 100:
                out.append("  ... 其余 %d 条从略（--json 可查看全部）"
                           % (summary.get("total", 0) - 100))
                break
            loc = "%s:%s" % (f["file"], f["line"]) if f.get("line") else f["file"]
            tag = " [heuristic]" if f["heuristic"] else ""
            out.append("  [%s]%s %s — %s" % (f["type"], tag, loc, f["detail"]))
            shown += 1
    else:
        out.append("未收集到任何证据（不代表没有问题，只是没有可机械核实的发现）。")
    out.append("=" * 64)
    out.append("说明: 以上均为事实证据而非质量结论；[heuristic] 项来自文本近似，"
               "仅供人工复核。")
    print("\n".join(out))


def build_parser():
    p = argparse.ArgumentParser(
        prog="quality_scan.py",
        description="代码质量证据收集器（不是裁判）：只收集可机械核实的事实证据，"
                    "不做好坏判断；.py 用 ast 精确分析，其他大括号类语言用文本"
                    "启发式（heuristic=true）。",
        epilog="示例: python quality_scan.py src/ --json report.json\n"
               "退出码: 0 正常完成（即使有 findings）；2 用法错误。",
    )
    p.add_argument("target", help="要扫描的目录或文件")
    p.add_argument("--json", metavar="OUT",
                   help="将结构化结果写入 OUT 文件（默认打印人类可读摘要）")
    p.add_argument("--max-func-lines", type=int, default=50,
                   help="超长函数阈值，行数（默认 50）")
    p.add_argument("--max-depth", type=int, default=4,
                   help="深嵌套阈值，层数（默认 4）")
    p.add_argument("--max-file-lines", type=int, default=800,
                   help="超长文件阈值，行数（默认 800）")
    return p


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = build_parser()
    args = parser.parse_args(argv)  # 用法错误时 argparse 自动以退出码 2 结束

    if min(args.max_func_lines, args.max_depth, args.max_file_lines) < 1:
        parser.error("阈值参数必须为正整数")  # 退出码 2

    target = Path(args.target)
    if not target.exists():
        print("[用法错误] 目标不存在: %s" % target, file=sys.stderr)
        return 2

    payload = scan_target(args)

    if args.json:
        try:
            out_path = Path(args.json)
            out_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8")
        except OSError as e:
            print("[错误] 写入 JSON 失败: %s" % e, file=sys.stderr)
            return 1
        print("JSON 已写入 %s（scanned_files=%d, findings=%d）"
              % (out_path, payload["scanned_files"],
                 payload["summary"]["total"]))
    else:
        print_human(payload)

    return 0  # 有 findings 不是错误


if __name__ == "__main__":
    sys.exit(main())

# ---------------------------------------------------------------------------
# 自测（一键）:  python selftest.py
#   selftest.py 会自动: 在 tests_fixture/ 种入已知问题样本（超长函数+深嵌套
#   的 .py、console.log+空 catch 的 .js、跨文件 6 行重复块、TODO 标记等）
#   → 调用本脚本扫描 → 断言全部种入问题均被抓到（含 .py ast 精确行号）
#   → 校验 --help 与用法错误退出码 → 清理临时目录 → 全部通过打印 OK。
# ---------------------------------------------------------------------------
