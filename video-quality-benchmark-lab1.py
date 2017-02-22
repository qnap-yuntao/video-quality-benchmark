# -*- coding: utf-8 *-*
import os
import time
import datetime


if __name__=="__main__":

    # 參數實驗組
    # g_arr = [3, 5, 10, 20]
    # bf_arr = [1, 3, 5, 10]
    # i_qfactor_arr = [-0.8, 0, 0.1, 0.5]
    # i_qoffset_arr = [-5, 0, 5]
    # b_qfactor_arr = [-0.8, 0, 0.1, 0.5]
    # b_qoffset_arr = [-5, 0, 5]
    # qmin_arr = [1, 5, 10]
    # qmax_arr = [30, 60, 120]
    # preset_arr = ["ultrafast", "medium", "placebo"]

    g_arr = [5, 10]
    bf_arr = [5]
    i_qfactor_arr = [-0.8]
    i_qoffset_arr = [-5]
    b_qfactor_arr = [-0.8]
    b_qoffset_arr = [-5]
    qmin_arr = [1]
    qmax_arr = [30]
    preset_arr = ["ultrafast", "medium", "placebo"]

    # 用來儲存參數組合的 array
    # 會長這樣： [[參數組合1],[參數組合2], ... ,[參數組合n]]
    vaapi_param_arr = []

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
    
    # 查看有幾種參數組合，目前共有 62208 種
    print len(vaapi_param_arr)
    # for i in range(vaapi_param_arr.size)

    # 查看第一組參數組合是否正確
    # print vaapi_param_arr[0]

    # 我們要把結果存到 實驗日期-實驗時間-report.csv 檔案裡面
    # 取得現在的時間
    now = datetime.datetime.now()
    filename = str(now.year) + str(now.month) + str(now.day) + "-" + str(now.hour) + str(now.minute) + str(now.second) + "-report.csv"
    print filename # 印出檔案名稱來查看

    # 我們利用 output.csv 當作暫存檔，來存放這筆實驗的結果
    # 這個 csv 檔前 9 個欄位存放實驗用的參數種類，接著是轉檔品質的 --- 四種 SSIM 值 Y,U,V,All; 四種 PSNR 值 y, u, v, average; 以及執行時間(秒) 與檔案大小(MB)
    os.system("""echo 'g, bf, i_qfactor, i_qoffset, b_qfactor, b_qoffset, qmin, qmax, preset,\
SSIM_Y, SSIM_U, SSIM_V, SSIM_All, PSNR_y, PSNR_u, PSNR_v, PSNR_average, Elapsed_Time, File_Size' > output.csv""")


    for i in xrange(len(vaapi_param_arr)):
        # 做轉檔的指令
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
-c:a copy -f mp4 /data/xxx/xxx_1080p_10M_dj2_result_tmp.mp4'""".format(vaapi_param_arr[i][0], vaapi_param_arr[i][1], vaapi_param_arr[i][2], vaapi_param_arr[i][3], vaapi_param_arr[i][4], vaapi_param_arr[i][5], vaapi_param_arr[i][6], vaapi_param_arr[i][7], vaapi_param_arr[i][8])
        print transcode_command # 印出轉檔指令

        # 將這次轉檔所使用的參數印到 output.csv
        os.system("echo -n \"{}, {}, {}, {}, {}, {}, {}, {}, {},\" >> output.csv".format(vaapi_param_arr[i][0], vaapi_param_arr[i][1], vaapi_param_arr[i][2], vaapi_param_arr[i][3], vaapi_param_arr[i][4], vaapi_param_arr[i][5], vaapi_param_arr[i][6], vaapi_param_arr[i][7], vaapi_param_arr[i][8]))

        # 轉檔開始的時間
        start_time = time.time()
        # 執行轉檔
        os.system(transcode_command)
        # 轉檔所需時間 = 轉檔結束的時間 - 轉檔開始的時間
        elapsed_time = time.time() - start_time

        # 做 ssim 與 psnr 的指令，會將結果數值 append 存到 csv 檔案當中
        ssim_psnr_command = """ffmpeg -i xxx/xxx_1080p_10M_15sec.mp4 -i xxx/xxx_1080p_10M_dj2_result_tmp.mp4 -lavfi \"ssim;[0:v][1:v]psnr\" -f null - 2>&1 | \
grep 'Parsed_psnr\|Parsed_ssim' | \
awk 'NR==1{print $5","$6","$7","$8","} NR==2{print $5","$6","$7","$8","}' | sed 's/[A-Za-z]*:/\ /g' | sed ':a;N;$!ba;s/\\n//g' | tr -d '\\n' >> output.csv"""

        print ssim_psnr_command

        # 執行 ssim 與 psnr 分析
        os.system(ssim_psnr_command)

        # 加入執行時間數據的指令
        add_elapsed_time_command = """ echo -n " {}, " >> output.csv """.format(elapsed_time)
        # 加入執行時間數據
        os.system(add_elapsed_time_command)
        # 加入檔案大小數值的指令
        add_file_size_command = """ls xxx -l | grep "xxx_1080p_10M_dj2_result_tmp.mp4" | awk '{print $5/1024/1024}' >>  output.csv"""
        # 加入檔案大小數值
        os.system(add_file_size_command)

        # 將轉檔完的影片暫存檔案刪除
        os.system("sudo rm xxx/xxx_1080p_10M_dj2_result_tmp.mp4")

    # end for loop

    # 將實驗結果複製到 report 資料夾存檔！
    os.system("cp output.csv report/{}".format(filename))


