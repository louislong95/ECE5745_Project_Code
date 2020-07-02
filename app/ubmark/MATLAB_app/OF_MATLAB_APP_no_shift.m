clear all;
% Intel(R) Xeon(R) CPU E5-2660 v3 @ 2.60GHz
% parameters
n_rows = 96;
n_cols = 128;
resize_scale = [n_rows n_cols]; 
image_number = 10;
trim_w = 5;
w = 1;
frame_rate = 5;
cpu_f = 2.6*(10^9);
%===================================


delete 'result_MATLAB/result_video_matlab_no_shift.avi'
%Video = VideoWriter('traffic_test_video_480p_fps10/Optical_Flow_Result_Video_MATLAB.avi');  % create a video object file
Video = VideoWriter('result_MATLAB/result_video_matlab_no_shift.avi');  % create a video object file
Video.FrameRate= frame_rate;
Video.Quality = 100;
open(Video);

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

for n = 1:(image_number)
    image_load_in = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', n));
    next_frame      = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', n+1));
    image_resize = imresize(image_load_in, resize_scale);
    next_frame_resize = imresize(next_frame, resize_scale);
    image_gray = rgb2gray(image_resize);
    image_gray = im2double(image_gray);
    next_frame_gray = rgb2gray(next_frame_resize);
    %next_frame_gray = im2int16(next_frame_gray);
    next_frame_gray = im2double(next_frame_gray);
    %subplot(1,1,1);
    %imshow(image_gray);
    image_corner = corner(image_gray);
    
    %=========Trim the number of corners ==========%
    k = 1;
    for i = 1:size(image_corner,1)
        x_i = image_corner (i, 2);
        y_i = image_corner (i, 1);
        if x_i-trim_w>=1 && y_i-trim_w>=1 && x_i+trim_w<=size(image_gray,1)-1 && y_i+trim_w<=size(image_gray,2)-1
            image_corner_trim(k,:) = image_corner(i,:);
            k = k+1;
        end
    end
    
    %hold on
    %plot(image_corner(:,1), image_corner(:,2), 'r*'); 
    
    %=======Processing of the image===========%
    lx = conv2(image_gray, [-1 0 1], 'same');
    ly = conv2(image_gray, [-1; 0; 1], 'same');
    %lt  = next_frame_gray - image_gray;
    lt = image_gray - next_frame_gray;
    %imshow(Ix);
    u = zeros(length(image_corner_trim), 1);  % build two vector to store the velocity of u and v.
    v = zeros(length(image_corner_trim), 1);  % they have the same number of rows of corner matirx and just 1 column
    
    for k = 1:length(image_corner_trim(:, 2))
        corner_i = image_corner_trim(k, 2);
        corner_j = image_corner_trim(k, 1);
        
        tic    % start timing measuring here
        lx_window = lx(corner_i - w : corner_i + w, corner_j - w : corner_j + w);
        ly_window = ly(corner_i - w : corner_i + w, corner_j - w : corner_j + w);
        lt_window = lt(corner_i - w : corner_i + w, corner_j - w : corner_j + w);
        
        lx_window = lx_window(:);
        ly_window = ly_window(:);
        lt_window = lt_window(:);
        
        % Basiclly, we want to implement this equation:
        % [ u ]    (  [ sum(Ix_w.^2)   sum(Ix_w.*Iy_w) ] ) ^-1  [-sum(Ix_w.*It_w)]
        % [ v ] = (  [ sum(Iy_w.*Ix)   sum(Iy_y.^2)     ] )         [-sum(Iy_w.*It_w)]
        % For simple inspection:
        % [ u ]    (  [ Ix_sum                lx_ly_mul_sum ] ) ^-1  [lx_lt_mul_sum]
        % [ v ] = (  [ lx_ly_mul_sum   ly_sum              ] )         [ly_lt_mul_sum]
        % The inverse function is:
        % 1 / (lx_sum * ly_sum - lx_ly_mul_sum^2) * [ ly_sum                -lx_ly_mul_sum]
        %                                                                      [-lx_ly_mul_sum    ly_sum             ]
        % Now the original function turns to:
        % [ u ]    (  [Iy_sum_inv         lx_ly_mul_inv ] )   [lx_lt_mul_sum]
        % [ v ] = (  [lx_ly_mul_inv     lx_sum_inv     ] )   [ly_lt_mul_sum]
        %
        % Then we can find the equation about u and v:
        % u = Iy_sum_inv * Ix_It_mul_sum + lx_ly_mul_inv * ly_lt_mul
        % v = lx_ly_mul_inv * lx_lt_mul_sum + lx_sum_inv * ly_lt_mul
        
        lx_square = lx_window.^2;
        lx_sum     = sum(lx_square(:));
        Iy_square = ly_window .^2;
        ly_sum     = sum(Iy_square(:));
        lx_ly_mul  = lx_window .* ly_window;
        lx_ly_mul_sum = sum(lx_ly_mul(:));
        lx_lt_mul  = lx_window .* lt_window .* (-1);
        lx_lt_mul_sum = sum(lx_lt_mul(:));
        ly_lt_mul  = ly_window .* lt_window .* (-1);
        ly_lt_mul_sum = sum(ly_lt_mul);
        
        determinant = 1 / (lx_sum * ly_sum - lx_ly_mul_sum^2);
        %determinant = 1;
        lx_sum_inv = lx_sum * determinant;
        ly_sum_inv = ly_sum * determinant;
        lx_ly_mul_inv = lx_ly_mul_sum * determinant * (-1);
        
        u(k) = ly_sum_inv * lx_lt_mul_sum + lx_ly_mul_inv * ly_lt_mul_sum;
        v(k) = lx_ly_mul_inv * lx_lt_mul_sum + lx_sum_inv * ly_lt_mul_sum;
        timeElapsed = toc;    % stop the time measuring
        
    end
    
    %=======plot the arrow on the image based on u and v==========
    %=======and save that plot as jpg, then write as frame to video=====%
    OF_result_figure = figure('visible', 'off');
    a = imshow(image_resize);
    hold on;
    quiver(image_corner_trim(:,1), image_corner_trim(:,2), u,v, 1,'r');
    saveas(OF_result_figure, sprintf('result_MATLAB/result_image_no_shift/OF_result%03d.jpg', n));
    %saveas(a, sprintf('traffic_test_video_OP_result_MATLAB/OF_result%03d.jpg', n));
    write_frame = imread(sprintf('result_MATLAB/result_image_no_shift/OF_result%03d.jpg', n));
    writeVideo(Video, write_frame);
    
end

close(Video);
fprintf('Video Generating Done!');
cycles = timeElapsed / (1/cpu_f);  % estimate the cycles the OF algorithm consumes

%===================== read from .dat file ==================

%fileID = fopen('test_small.dat','r');
%formatSpec = '%d';
%result_1d = fscanf(fileID,formatSpec);
%fclose(fileID);
%result_2d = reshape(result_1d, [n_cols, n_rows]);
%result_final = transpose(result_2d);
%result_image = mat2gray(result_final);
%subplot(1,2,2);
%imshow(result_image);