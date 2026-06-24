# idongdong-skills

我的 Claude Code / Codex Skill 合集。每个 skill 是一个独立目录，包含自己的 `SKILL.md`。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgray.svg)

## Skills

| Skill | 用途 | 状态 |
|-------|------|------|
| `cc-switcher` | 在 Claude Code 中快速切换 AI 提供商 | 已发布，可用 |
| `image-crop-tool` | 图像分析时裁剪并放大局部细节 | 已发布，可用 |

## 安装

```bash
git clone https://github.com/idongdongh/idongdong-skills.git
mkdir -p ~/.claude/skills
cp -r idongdong-skills/<skill-name> ~/.claude/skills/
```

示例：

```bash
cp -r idongdong-skills/cc-switcher ~/.claude/skills/
cp -r idongdong-skills/image-crop-tool ~/.claude/skills/
```

## cc-switcher

在 Claude Code 中快速切换 AI 提供商，支持 Anthropic、DeepSeek、Qwen、OpenRouter、Gemini 等任意 Anthropic 兼容 API。

macOS / Linux 使用 `cc-switcher` 需要 `fzf` 和 `jq`：

```bash
brew install fzf jq
```

Windows 无强制依赖，`fzf` 可选。

### 使用

在 Claude Code 中说：

- **首次配置**：「帮我配置 Claude Code 提供商」或「我想用 DeepSeek」
- **添加提供商**：「帮我添加 OpenRouter」
- **删除提供商**：「删除 OpenRouter」
- **更新模型**：「帮我更新 DeepSeek 的模型」

配置完成后，终端运行 `cc` 即可通过交互菜单选择提供商启动 Claude Code。

```bash
cc
cc --yolo
```

`cc --yolo` 等价于 `cc --dangerously-skip-permissions`。

### 配置文件格式

`~/.claude/providers/<公司名>.json`：

```json
{
  "docs_url": "<提供商模型文档页 URL>",
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "<API Key>",
    "ANTHROPIC_BASE_URL": "<Anthropic 兼容端点>",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "<轻量模型 ID>",
    "ANTHROPIC_SMALL_FAST_MODEL": "<轻量模型 ID>",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "<旗舰模型 ID>",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "<主力模型 ID>",
    "ANTHROPIC_MODEL": "<主力模型 ID>",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

## image-crop-tool

用于图像分析中需要裁剪关键区域、放大局部细节的场景，例如小字看不清、图表刻度或数值难读、技术图标签太小、密集截图局部 UI 状态、报错文本、商品瑕疵等。

### 依赖

脚本依赖 `Pillow`：

```bash
python3 -c "import PIL; print(PIL.__version__)"
uv add pillow 2>/dev/null || (uv venv && uv pip install pillow)
```

### 使用

在 Claude Code / Codex 中说：

- 「这张截图里的报错信息太小了，帮我放大局部读出来」
- 「放大图表底部坐标轴，比较这两个数值」
- 「检查这个 UI 截图右下角按钮是 disabled 还是 loading」

也可以直接运行脚本：

```bash
python3 ~/.claude/skills/image-crop-tool/scripts/crop_image.py \
  /path/to/input.png \
  --box 0.65 0.65 1.00 1.00 \
  --output /path/to/output-crop.png \
  --metadata-output /path/to/output-crop.json
```

坐标使用 `0-1` 归一化坐标，顺序是 `x1 y1 x2 y2`。

## 更新日志

### 2026-06-24

**新增 image-crop-tool**

新增图像局部裁剪 skill，用 `0-1` 归一化坐标裁剪图片关键区域，辅助读取小字、图表刻度、UI 状态和局部瑕疵。

### 2026-06-09

**多终端独立模型切换**

之前所有终端共享同一个提供商配置，后启动的终端会覆盖前面的。现在每个终端通过 `--settings` 独立注入提供商配置，互不干扰。

```
终端 A: cc → 选 DeepSeek → 用 DeepSeek
终端 B: cc → 选 智谱    → 用 智谱
终端 C: cc → 选 MiniMax → 用 MiniMax
```

## 许可证

MIT License
