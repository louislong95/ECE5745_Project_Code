clear all;  
n_rows = 96;
n_cols = 128;
resize_scale = [n_rows n_cols]; 
image_number = 10;
trim_w = 5;
w = 1;
frame_rate = 5;

delete 'result_MATLAB/result_image_xcel/*.jpg'
delete 'result_MATLAB/result_video_xcel.avi'
Video = VideoWriter('result_MATLAB/result_video_xcel.avi');  % create a video object file
Video.FrameRate= frame_rate;
Video.Quality = 100;
open(Video);

%=================read from xcel-data.txt file and do 2s complement=======
delimiter = '#';

result_table = readtable('result_MATLAB/xcel-data.txt', 'delimiter', delimiter);
result_array = table2array(result_table);

for i=1:length(result_array)
    raw_vx(i, 1) = result_array(i, 1);  
    raw_vx_signed(i, 1) = unsigned2signed(raw_vx(i,1), 32);
    
    raw_vy(i, 1) = result_array(i, 2);
    raw_vy_signed(i, 1) = unsigned2signed(raw_vy(i,1), 32);
    
    de(i, 1)        = result_array(i, 3);
    de_signed(i, 1) = unsigned2signed(de(i,1), 32);
    
    final_vx(i, 1) = raw_vx_signed(i, 1) / de_signed(i, 1);
    final_vy(i, 1) = raw_vy_signed(i, 1) / de_signed(i, 1);
end
%======================================================

first_image = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', 1));
first_image = imresize(first_image, resize_scale);
first_image = rgb2gray(first_image);
first_image = int32(first_image);
first_image_corner = corner(first_image);


k = 1;
    for i = 1:size(first_image_corner, 1)
        x_i = first_image_corner (i, 2);
        y_i = first_image_corner (i, 1);
        if x_i-trim_w>=1 && y_i-trim_w>=1 && x_i+trim_w<=size(first_image,1)-1 && y_i+trim_w<=size(first_image,2)-1
            first_image_corner_trim(k,:) = first_image_corner(i,:);
            k = k+1;
        end
    end
    
 fixed_cn = length(first_image_corner_trim);
 
 for n=1:image_number
    image_load_in = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', n));
    image_resize = imresize(image_load_in, resize_scale);
    image_gray = rgb2gray(image_resize);
    image_gray = int32(image_gray);
    image_corner = corner(image_gray);
        
    %=========Trim the number of corners ==========%
    k = 1;
    for i = 1:size(image_corner, 1)
        x_i = image_corner (i, 2);
        y_i = image_corner (i, 1);
        if x_i-trim_w>=1 && y_i-trim_w>=1 && x_i+trim_w<=size(image_gray,1)-1 && y_i+trim_w<=size(image_gray,2)-1
            image_corner_trim(k,:) = image_corner(i,:);
            k = k+1;
        end
    end
    
    OF_result_figure = figure('visible', 'off');
    a = imshow(image_resize);
    hold on;
    range_1 = (image_number-1)*fixed_cn+1;
    range_2 = image_number * fixed_cn;
    quiver(image_corner_trim(:,1), image_corner_trim(:,2), final_vx(range_1:range_2 ,1), final_vy(range_1:range_2 ,1), 1,'r');
    saveas(OF_result_figure, sprintf('result_MATLAB/result_image_xcel/OF_result%03d.jpg', n));
    %saveas(a, sprintf('traffic_test_video_OP_result_MATLAB/OF_result%03d.jpg', n));
    write_frame = imread(sprintf('result_MATLAB/result_image_xcel/OF_result%03d.jpg', n));
    writeVideo(Video, write_frame);
    
 end
 
 close(Video);
 fprintf('Xcel Video is generated! \n');
