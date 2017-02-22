# -*- coding: utf-8 *-*
import os
import time

if __name__=="__main__":

    g_arr = [3, 5, 10, 20]
    bf_arr = [1, 3, 5, 10]
    i_qfactor_arr = [-0.8, 0, 0.1, 0.5]
    i_qoffset_arr = [-5, 0, 5]
    b_qfactor_arr = [-0.8, 0, 0.1, 0.5]
    b_qoffset_arr = [-5, 0, 5]
    qmin_arr = [1, 5, 10]
    qmax_arr = [30, 60, 120]
    preset_arr = ["ultrafast", "medium", "placebo"]

    vaapi_param_arr = []

    # for preset in preset:
    #     print "{}".format(preset)
    # for qmin in qmin:
    #     print "{}".format(qmin)

    for g in g_arr:
        for bf in bf_arr:
            for i_qfactor in i_qfactor_arr:
                for i_qoffset in i_qoffset_arr:
                    for b_qfactor in b_qfactor_arr:
                        for b_qoffset in b_qoffset_arr:
                            for qmin in qmin_arr:
                                for qmax in qmax_arr:
                                    for preset in preset_arr:
                                        # print "{}, {}, {}, {}, {}, {}, {}, {}, {}".format(g, bf, i_qfactor, i_qoffset, b_qfactor, b_qoffset, qmin, qmax, preset)
                                        vaapi_param_arr.append([g, bf, i_qfactor, i_qoffset, b_qfactor, b_qoffset, qmin, qmax, preset])
    
    #print len(vaapi_param_arr)
    # for i in range(vaapi_param_arr.size)

    # -g: [3, 5, 10, 20]
    # -bf: [1, 3, 5, 10]
    # -i_qfactor: [-0.8, 0, 0.1, 0.5]
    # -i_qoffset: [-5, 0, 5]
    # -b_qfactor: [-0.8, 0, 0.1, 0.5]
    # -b_qoffset: [-5, 0, 5]
    # -qmin: [1, 5, 10]
    # -qmax: [30, 60, 120]
    # -preset: ["ultrafast", "medium", "placebo"]

    print vaapi_param_arr[0]

    os.system("""echo 'g, bf, i_qfactor, i_qoffset, b_qfactor, b_qoffset, qmin, qmax, preset,\
SSIM_Y, SSIM_U, SSIM_V, SSIM_All, PSNR_y, PSNR_u, PSNR_v, PSNR_average, Elapsed_Time, File_Size' > output.csv""")


    transcode_command = """docker exec dj2transcode2 bash -c 'dj2-transcode -hwaccel vaapi -hwaccel_output_format vaapi -vaapi_device /dev/dri/renderD128 \
-i /data/xxx/xxx_1440p_10M_15sec.mp4 -vf \"format=vaapi|nv12,hwupload,scale_vaapi=w=1920:h=1080\" -c:v h264_vaapi \
-g {} \
-bf {} \
-i_qfactor {} -i_qoffset {} \
-b_qfactor {} -b_qoffset {} \
-r 30 \
-qmin {} \
-qmax {} \
-preset {} \
-8x8dct 1 \
-dct 5 \
-b:v 6000k \
-maxrate 12000k -bufsize 2000k \
-minrate 5500k \
-me_method full \
-c:a copy -f mp4 /data/xxx/xxx_1080p_10M_dj2_result_tmp.mp4'""".format(vaapi_param_arr[0][0], vaapi_param_arr[0][1], vaapi_param_arr[0][2], vaapi_param_arr[0][3], vaapi_param_arr[0][4], vaapi_param_arr[0][5], vaapi_param_arr[0][6], vaapi_param_arr[0][7], vaapi_param_arr[0][8])
    print transcode_command

    os.system("echo -n \"{}, {}, {}, {}, {}, {}, {}, {}, {},\" >> output.csv".format(vaapi_param_arr[0][0], vaapi_param_arr[0][1], vaapi_param_arr[0][2], vaapi_param_arr[0][3], vaapi_param_arr[0][4], vaapi_param_arr[0][5], vaapi_param_arr[0][6], vaapi_param_arr[0][7], vaapi_param_arr[0][8]))

    start_time = time.time()
    os.system(transcode_command)
    elapsed_time = time.time() - start_time

    psnr_command = """ffmpeg -i xxx/xxx_1080p_10M_15sec.mp4 -i xxx/xxx_1080p_10M_dj2_result_tmp.mp4 -lavfi  \"ssim;[0:v][1:v]psnr\" -f null - 2>&1 \
grep 'Parsed_psnr\|Parsed_ssim' | \
awk 'NR==1{print $5", "$6", "$7", "$8", "} NR==2{print $5", "$6", "$7", "$8", "}' | sed 's/[A-Za-z]*:/\ /g' | \
tee -a output.csv"""

    print psnr_command

    os.system(psnr_command)

    add_elapsed_time_command = """ echo -n " {}," >> output.csv """.format(elapsed_time)

    os.system(add_elapsed_time_command)

    add_file_size_command = """ls xxx -l | grep "xxx_1080p_10M_dj2_result_tmp.mp4" | awk '{print $5/1024/1024}' >>  output.csv"""
    
    os.system(add_file_size_command)

    os.system("echo '\n' >> output.csv")



