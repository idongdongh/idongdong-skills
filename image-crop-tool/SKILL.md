---
name: image-crop-tool
description: "用于图像分析中需要裁剪关键区域、放大局部细节时使用；触发于小字看不清、图表刻度或数值难读、技术图标签太小、密集截图局部 UI 状态、报错文本、商品瑕疵等需要 crop image、zoom in、magnify details 的场景；不用于普通图片描述或整体内容概括。"
---

# Image Crop Tool

## 使用边界

触发后先确认任务是否真的需要局部放大或裁剪。普通“看图”“描述图片”“分析截图”如果只需要整体理解，不要使用裁剪脚本；只有答案依赖小字、密集 UI、图表刻度、技术图标签、局部瑕疵、按钮状态、报错文本等细节时才裁剪。

典型细节需求包括：`crop image`、`zoom in`、`magnify details`、`small text`、`inspect screenshot detail`、`chart value is hard to read`。

## 依赖

脚本依赖 `Pillow`，它不是 Python 标准库。运行前先检查：

```bash
python3 -c "import PIL; print(PIL.__version__)"
```

如果缺失，优先加入当前 uv 项目；若当前目录不是 uv 项目，则创建本地虚拟环境后安装：

```bash
uv add pillow 2>/dev/null || (uv venv && uv pip install pillow)
```

## 工作流

先读取或查看原图，建立全图上下文。若答案依赖局部细节，自动调用脚本裁剪关键区域，不要让用户判断是否需要裁剪。

```bash
python3 /absolute/path/to/image-crop-tool/scripts/crop_image.py INPUT --box X1 Y1 X2 Y2 --output OUTPUT
```

脚本路径必须用 skill 根目录拼接：`skill_dir = dirname(SKILL.md)`，脚本为 `skill_dir/scripts/crop_image.py`。不要依赖用户当前工作目录，也不要要求用户先 `cd` 到 skill 目录。若本 skill 位于 `/path/to/image-crop-tool/SKILL.md`，则脚本路径是 `/path/to/image-crop-tool/scripts/crop_image.py`。

坐标使用 `0-1` 归一化坐标：`(0, 0)` 是左上角，`(1, 1)` 是右下角。脚本会拒绝超出 `[0, 1]` 或 `x1 >= x2`、`y1 >= y2` 的裁剪框。

裁剪后查看 `OUTPUT`；如果仍看不清，继续裁剪或说明不确定性。多图任务逐张处理，并在最终回答中按图片列出裁剪证据。最终回答基于全图上下文和裁剪证据。

## 坐标估算

坐标顺序是 `x1 y1 x2 y2`。不确定时先裁大框，保留上下文，再根据裁剪结果二次缩小。常用起点：

- 中央区域：`0.25 0.25 0.75 0.75`
- 右下角细节：`0.65 0.65 1.00 1.00`
- 底部文字或坐标轴：`0.00 0.75 1.00 1.00`
- 左侧刻度或标签：`0.00 0.00 0.30 1.00`

如果目标仍太小，基于第一张 crop 的相对位置继续裁第二次。

## 使用示例

```bash
python3 /absolute/path/to/image-crop-tool/scripts/crop_image.py \
  /path/to/input.png \
  --box 0.82 0.17 0.97 0.44 \
  --output /path/to/output-crop.png \
  --metadata-output /path/to/output-crop.json
```

输出 JSON 会包含原图尺寸、像素裁剪框、归一化裁剪框和裁剪图尺寸。JSON 只作为元数据和证据索引用；真正用于视觉检查的是 `--output` 生成的裁剪图片文件。裁剪后读取或查看该输出图片。

## 失败处理

- 缺少 `Pillow`：按依赖段落安装后重试。
- 输入图片不存在：检查 `INPUT` 路径是否相对于当前工作目录正确。
- 图片格式不支持或文件损坏：换用 Pillow 可读取的图片格式，例如 PNG/JPEG。
- 裁剪区域无效：重新估计 `0-1` 坐标，确保 `x1 < x2` 且 `y1 < y2`。
