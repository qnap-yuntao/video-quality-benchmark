# input : xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4
# input : xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4
# reference : xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4
# reference : xxx_1440p_10M_skylake-1080-4500k-vaapi-sdhe.mp4
# reference : xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-vbr.mp4
# reference : xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-cbr.mp4
# reference : xxx_1440p_10M_kabylake-1080-4500k-vaapi-hdhe.mp4 
# reference : xxx_1440p_10M_kabylake-1080-4500k-vaapi-sdhe.mp4
# reference : xxx_1440p_10M_gst_4.5M-cbr.mp4
# reference : xxx_1440p_10M_gst_4.5M-cbr-bf2.mp4
# reference : xxx_1440p_10M_gst_4.5M-cbr-bf2-tune1.mp4

datetime=$(date +%Y%m%d_%H%M%S)
result=$datetime"_result.txt"

# test data 20170123
# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4 xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4 xxx_1440p_10M_skylake-1080-4500k-vaapi-sdhe.mp4 xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-vbr.mp4 xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-cbr.mp4)

# test one raw data
#input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4)
#reference_arr=(xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4)

# test new data 20170124
# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4 xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_kabylake-1080-4500k-vaapi-hdhe.mp4 xxx_1440p_10M_kabylake-1080-4500k-vaapi-sdhe.mp4)

# test gstreamer data 20170125
# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4 xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_gst_4.5M-cbr.mp4 xxx_1440p_10M_gst_4.5M-cbr-bf2.mp4 xxx_1440p_10M_gst_4.5M-cbr-bf2-tune1.mp4)

# test all data

fileExtension='mp4'
sourceIdf='x264'
sourceFile='xxx_1440p_10M.mp4'

inputArray=($(ls | grep -i $sourceIdf | grep -i $fileExtension))
referenceArray=($(ls | grep -v $sourceIdf | grep -v $sourceFile | grep -i $fileExtension))

for input in ${inputArray[@]}
do
    for reference in ${referenceArray[@]}
    do
        echo $datetime
        echo $'\ninput : \t'$input
        echo $'reference : \t'$reference
        echo $'\n====================================================================\n'
        echo $'\n====================================================================\n' >> $result.txt
        echo "ffmpeg start"
        ffmpeg -i $input -i $reference -filter_complex psnr -f null - 2>> temp.txt
        echo "ffmpeg end"
        grep 'Input\|Parsed_psnr' temp.txt | awk 'NR==1{print "input: \t\t"  $5} NR==2{print "reference: \t" $5} NR==3{print}' >> $result.txt
        rm temp.txt
        # ffmpeg -i $input -i $reference -lavfi  "ssim;[0:v][1:v]psnr" -f null - 1>> $result 2>> temp.txt

    done
done

