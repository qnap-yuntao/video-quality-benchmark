# input : xxx_1440p_10M_skylake-1080-4500k-x264-sdse.mp4
# input : xxx_1440p_10M_skylake-1080-unlimited-x264-sdse.mp4

datetime=$(date +%Y%m%d_%H%M%S)
result=$datetime"_result.txt"

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
        echo -e "\n====================================================================\n" | tee -a $result
        echo "ffmpeg start"
        #ffmpeg -i $input -i $reference -filter_complex psnr -f null - 2>> temp.txt
        ffmpeg -i $input -i $reference -lavfi  "ssim;[0:v][1:v]psnr" -f null - |& \
        grep 'Input\|Parsed_psnr\|Parsed_ssim' | awk 'NR==1{print "input: \t\t"  $5} NR==2{print "reference: \t" $5} NR==3{print} NR==4{print}' | tee -a $result
        echo "ffmpeg end"
        echo -e "\n"
    done
done

