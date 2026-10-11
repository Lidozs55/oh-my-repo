#!/usr/bin/env node
"use strict";

/*
 * vibe-quality 安装器：把本包内的技能文件复制到 agent skills 目录。
 * 零依赖，仅用 Node 标准库；Node >= 18。
 */

const fs = require("fs");
const os = require("os");
const path = require("path");

const SKILL_NAME = "vibe-quality";
const PKG_ROOT = path.join(__dirname, "..");
const ENTRIES = ["SKILL.md", "references", "scripts"];

function usage(code) {
  const lines = [
    `用法：npx ${SKILL_NAME} [选项]`,
    "",
    "把 vibe-quality 技能安装到 agent skills 目录（默认当前项目的 .agents/skills/）。",
    "",
    "选项：",
    "  -g, --global      安装到用户级目录（~/.agents/skills/）",
    "  -d, --dir <路径>  安装到指定目录（在其下创建 vibe-quality/）",
    "  -f, --force       目标已存在时覆盖",
    "  -h, --help        显示本说明",
  ];
  console.log(lines.join("\n"));
  process.exit(code);
}

function parseArgs(argv) {
  const opts = { global: false, dir: null, force: false };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === "-g" || arg === "--global") opts.global = true;
    else if (arg === "-f" || arg === "--force") opts.force = true;
    else if (arg === "-h" || arg === "--help") usage(0);
    else if (arg === "-d" || arg === "--dir") {
      const value = argv[++i];
      if (!value || value.startsWith("-")) usage(2);
      opts.dir = value;
    } else {
      usage(2);
    }
  }
  return opts;
}

function main() {
  const opts = parseArgs(process.argv.slice(2));
  const root = opts.dir
    ? path.resolve(opts.dir)
    : opts.global
      ? path.join(os.homedir(), ".agents", "skills")
      : path.join(process.cwd(), ".agents", "skills");
  const target = path.join(root, SKILL_NAME);

  if (fs.existsSync(target)) {
    if (!opts.force) {
      console.error(`目标已存在：${target}`);
      console.error("如需覆盖请加 --force。");
      process.exit(1);
    }
    fs.rmSync(target, { recursive: true, force: true });
  }
  fs.mkdirSync(root, { recursive: true });
  for (const entry of ENTRIES) {
    const source = path.join(PKG_ROOT, entry);
    if (!fs.existsSync(source)) {
      console.error(`包内缺少 ${entry}，安装中止（包可能已损坏）。`);
      process.exit(1);
    }
    fs.cpSync(source, path.join(target, entry), { recursive: true });
  }

  const scope = opts.dir ? "指定目录" : opts.global ? "用户级" : "项目级";
  console.log(`已安装（${scope}）：${target}`);
  console.log("重启 agent 会话后即可被识别，试试说：");
  console.log("  「帮我体检一下这坨 AI 生成的代码」");
  console.log("  「这段代码太膨胀了，重构清理一下，但别改行为」");
}

main();
