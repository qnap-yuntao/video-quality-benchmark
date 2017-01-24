# input : xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4
# input : xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4
# reference : xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4
# reference : xxx_1440p_10M_skylake-1080-4500k-vaapi-sdhe.mp4
# reference : xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-vbr.mp4
# reference : xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-cbr.mp4
# reference : xxx_1440p_10M_kabylake-1080-4500k-vaapi-hdhe.mp4 
# reference : xxx_1440p_10M_kabylake-1080-4500k-vaapi-sdhe.mp4

datetime=$(date +%Y%m%d_%H%M%S)
result=$datetime"_result.txt"
result_output=$datetime"_result_output.txt"

# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4 xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4 xxx_1440p_10M_skylake-1080-4500k-vaapi-sdhe.mp4 xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-vbr.mp4 xxx_1440p_10M-m2000-1080-4500k-nvenc-hdhe-cbr.mp4)

# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_skylake-1080-4500k-vaapi-hdhe.mp4)

# input_arr=(xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4 xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4)
# reference_arr=(xxx_1440p_10M_kabylake-1080-4500k-vaapi-hdhe.mp4 xxx_1440p_10M_kabylake-1080-4500k-vaapi-sdhe.mp4)


for input in ${input_arr[@]};
do
    for reference in ${reference_arr[@]}; 
    do
        echo $datetime
        echo "input " $input
        echo "reference " $reference
        echo $'\n==================================================================== \n ' >> $result_output
        echo "input "$input >> $result_output
        echo "reference "$reference >> $result_output
        echo $'\n' >> $result_output
        ffmpeg -i $input -i $reference -filter_complex psnr -f null - 1>> $result 2>> temp.txt
        grep -n 'Parsed' temp.txt >> $result_output
    done
  
done
echo $'\n==================================================================== \n ' >> $result_output

rm temp.txt
rm $result

