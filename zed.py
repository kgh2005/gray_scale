import os
from pathlib import Path
import cv2
import pyzed.sl as sl

SVO_PATH = "/home/robit/Documents/ZED/HD720_SN19078631_17-35-49.svo2"   # 녹화한 SVO(.svo 또는 .svo2)
OUT_DIR  = "/home/robit/colcon_ws/src/gray_scale/images"      # 저장 폴더
SAVE_EVERY_N = 20                    # 프레임 간격(1이면 전부 저장, 3이면 3프레임마다 저장)

def main():
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)

    zed = sl.Camera()
    init = sl.InitParameters()
    init.set_from_svo_file(SVO_PATH)
    init.svo_real_time_mode = False  # 오프라인 처리(빠르게 가능)
    init.depth_mode = sl.DEPTH_MODE.NONE  # 학습용 RGB만이면 끄는게 가벼움

    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS:
        raise RuntimeError(f"ZED open failed: {err}")

    runtime = sl.RuntimeParameters()
    mat_left = sl.Mat()

    idx = 0
    saved = 0
    while True:
        if zed.grab(runtime) != sl.ERROR_CODE.SUCCESS:
            break

        if idx % SAVE_EVERY_N == 0:
            zed.retrieve_image(mat_left, sl.VIEW.LEFT)  # ✅ 왼쪽만
            left = mat_left.get_data()                  # RGBA (H,W,4)
            bgr = cv2.cvtColor(left, cv2.COLOR_RGBA2BGR)

            out_path = os.path.join(OUT_DIR, f"{idx:06d}.png")
            cv2.imwrite(out_path, bgr)
            saved += 1

        idx += 1

    zed.close()
    print(f"Done. total_frames={idx}, saved={saved}, out={OUT_DIR}")

if __name__ == "__main__":
    main()
