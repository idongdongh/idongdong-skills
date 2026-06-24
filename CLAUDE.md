# idongdong-skills

我的 Claude Code 开源 Skill 合集。每个 skill 是一个独立目录，有自己的 `SKILL.md` 定义文件。

## 当前 Skill

| Skill | 用途 | 状态 |
|-------|------|------|
| cc-switcher | 在 Claude Code 中快速切换 AI 提供商 | 已发布，可用 |
| image-crop-tool | 图像分析时裁剪并放大局部细节 | 已发布，可用 |

## 目录结构

```
idongdong-skills/
├── CLAUDE.md            # 项目说明（本文件）
├── README.md            # 面向用户的文档
├── .gitignore
├── plan/                # 开发计划（已 gitignore）
├── cc-switcher/         # 提供商切换 skill
│   ├── SKILL.md
│   └── scripts/
│       ├── launch.sh    # macOS / Linux
│       └── launch.ps1   # Windows
├── image-crop-tool/     # 图像局部裁剪 skill
│   ├── SKILL.md
│   └── scripts/
│       └── crop_image.py
└── <future-skill>/      # 未来新增的 skill
    └── SKILL.md
```

## 开发约定

- 每个 skill 必须有 `SKILL.md`（Claude Code 加载入口）
- 需要脚本的 skill 放在 `scripts/` 子目录
- `README.md` 面向用户，只写使用说明，不写技术细节
- `plan/` 放开发计划和设计文档，不进 git
- 新增 skill 时更新本文件和 `README.md` 的更新日志
- skill 更新完成后，询问用户是否需要同步到 Claude Code 技能目录，需要则执行：`cp -r <skill-dir> ~/.claude/skills/`
