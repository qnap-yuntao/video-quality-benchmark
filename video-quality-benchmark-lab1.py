# -*- coding: utf-8 *-*
import os


if __name__=="__main__":

    g_arr = ["3", "5", "10", "20"]
    bf_arr = ["1", "3", "5", "10"]
    i_qfactor_arr = ["-0.8", "0", "0.1", "0.5"]
    i_qoffset_arr = ["-5", "0", "5"]
    b_qfactor_arr = ["-0.8", "0", "0.1", "0.5"]
    b_qoffset_arr = ["-5", "0", "5"]
    qmin_arr = ["1", "5", "10"]
    qmax_arr = ["30", "60", "120"]
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
    
    print len(vaapi_param_arr)
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

    command = """sudo docker exec dj2transcode2 bash -c \'dj2-transcode -hwaccel vaapi -hwaccel_output_format vaapi -vaapi_device /dev/dri/renderD128 \\ 
-i /data/xxx/xxx_1440p_10M.mp4 -vf \"format=vaapi|nv12,hwupload,scale_vaapi=w=1920:h=1080\" -c:v h264_vaapi \\
-g {} \\
-bf {} \\
-i_qfactor {} -i_qoffset {} \\
-b_qfactor {} -b_qoffset {} \\
-r 30 \\
-qmin {} \\
-qmax {} \\
-preset {} \\
-8x8dct 1 \\
-dct 5 \\
-b:v 6000k \\
-maxrate 12000k -bufsize 2000k \\
-minrate 5500k \\
-me_method full \\
-c:a copy -f mp4 /data/xxx/xxx_1440p_10M_dj2_leo_test.mp4\' """.format(g[0], bf[0], i_qfactor[0], i_qoffset[0], b_qfactor[0], b_qoffset[0], qmin[0], qmax[0], preset[0])


    print command

    # os.system(command)
 



