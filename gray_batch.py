#!/usr/bin/env python3
from pathlib import Path
import cv2

# === 설정 ===
SRC_DIR = Path("/home/robit/colcon_ws/src/gray_scale/images")      # 원본 폴더
DST_DIR = Path("/home/robit/colcon_ws/src/gray_scale/images_gray") # 저장 폴더(새로 생성됨)
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def main():
    if not SRC_DIR.exists():
        raise FileNotFoundError(f"SRC_DIR not found: {SRC_DIR}")

    files = [p for p in SRC_DIR.rglob("*") if p.is_file() and p.suffix.lower() in EXTS]
    print(f"Found {len(files)} images under {SRC_DIR}")

    converted = 0
    skipped = 0

    for src_path in files:
        rel = src_path.relative_to(SRC_DIR)
        dst_path = (DST_DIR / rel).with_suffix(".png")  # ✅ 그레이는 PNG로 저장(손실 적음)
        dst_path.parent.mkdir(parents=True, exist_ok=True)

        img = cv2.imread(str(src_path), cv2.IMREAD_UNCHANGED)
        if img is None:
            print(f"[SKIP] Failed to read: {src_path}")
            skipped += 1
            continue

        # 1) 이미 그레이(2D)면 그대로
        if len(img.shape) == 2:
            gray = img
        else:
            # 2) 알파 채널 있으면(BGRA) 먼저 BGR로
            if img.shape[2] == 4:
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ok = cv2.imwrite(str(dst_path), gray)
        if not ok:
            print(f"[SKIP] Failed to write: {dst_path}")
            skipped += 1
            continue

        converted += 1

    print(f"Done. converted={converted}, skipped={skipped}")
    print(f"Output dir: {DST_DIR}")

if __name__ == "__main__":
    main()
