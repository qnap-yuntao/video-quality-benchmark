# -*- coding: utf-8 *-*
import os
import time

if __name__=="__main__":

    psnr_command = """ffmpeg -i xxx/xxx_1080p_10M_15sec.mp4 -i xxx/xxx_1080p_10M_dj2_result_tmp.mp4 -lavfi \"ssim;[0:v][1:v]psnr\" -f null - 2>&1 | \
grep 'Parsed_psnr\|Parsed_ssim' | \
awk 'NR==1{print $5","$6","$7","$8","} NR==2{print $5","$6","$7","$8","}' | sed 's/[A-Za-z]*:/\ /g' | sed ':a;N;$!ba;s/\\n//g' | tr -d '\\n' | \
tee -a output.csv"""

    print psnr_command

    os.system(psnr_command)