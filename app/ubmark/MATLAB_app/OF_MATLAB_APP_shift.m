clear all;
% Intel(R) Xeon(R) CPU E5-2660 v3 @ 2.60GHz
% parameters
n_rows = 96;
n_cols = 128;
resize_scale = [n_rows n_cols]; 
image_number = 2;
trim_w = 5;
w = 1;
frame_rate = 5;
cpu_f = 2.6*(10^9);
%===================================

%delete 'traffic_test_video_480p_fps10/traffic_test_video_data/*.dat'          %delete the old data files
%delete 'traffic_test_video_480p_fps10/traffic_test_video_OP_result_MATLAB/*.jpg'
%delete 'traffic_test_video_480p_fps10/Optical_Flow_Result_Video_MATLAB.avi'
delete 'result_MATLAB/result_data/*.dat'          %delete the old data files
delete 'result_MATLAB/result_image_shift/*.jpg'
delete 'result_MATLAB/result_video_matlab_shift.avi'
%Video = VideoWriter('traffic_test_video_480p_fps10/Optical_Flow_Result_Video_MATLAB.avi');  % create a video object file
Video = VideoWriter('result_MATLAB/result_video_matlab_shift.avi');  % create a video object file
Video.FrameRate= frame_rate;
Video.Quality = 100;
open(Video);

first_image = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', 1));
first_image = imresize(first_image, resize_scale);
first_image = rgb2gray(first_image);
first_image = int32(first_image);
first_image_corner = corner(first_image);
image_number = image_number + 1;


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
    %image_load_in = imread(sprintf('traffic_test_video_480p_fps10/ezgif-frame-%03d.jpg', n));
    %next_frame      = imread(sprintf('traffic_test_video_480p_fps10/ezgif-frame-%03d.jpg', n+1));
    %image_load_in = imread(sprintf('toast_test_fps20/ezgif-frame-%03d.jpg', n));
    %next_frame      = imread(sprintf('toast_test_fps20/ezgif-frame-%03d.jpg', n+1));
    image_load_in = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', n));
    next_frame      = imread(sprintf('walking_man_test_fps20/ezgif-frame-%03d.jpg', n+1));
    image_resize = imresize(image_load_in, resize_scale);
    next_frame_resize = imresize(next_frame, resize_scale);
    image_gray = rgb2gray(image_resize);
    image_test = rgb2gray(image_resize);
    image_gray = int32(image_gray);
    next_frame_gray = rgb2gray(next_frame_resize);
    next_frame_gray = int32(next_frame_gray);
    %subplot(1,1,n);
    %imshow(image_gray);
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
    
    %hold on
    %plot(image_corner_trim(:,1), image_corner_trim(:,2), 'r*'); 
    
    %=======Processing of the image===========%
    %Ix = conv2(image_gray, [-1 0 1], 'same');
    for ii=1:n_rows
         for jj=2:n_cols-1
              lx(ii,jj) = image_gray(ii, jj+1) - image_gray(ii, jj-1);
         end
    end
    %Iy = conv2(image_gray, [-1; 0; 1], 'same');
    for jjj=1:n_cols
         for iii=2:n_rows-1
              ly(iii,jjj) = image_gray(iii+1, jjj) - image_gray(iii-1, jjj);
         end
    end
    lt  = next_frame_gray - image_gray;
    u = zeros(length(image_corner_trim), 1);  % build two vector to store the velocity of u and v.
    v = zeros(length(image_corner_trim), 1);  % they have the same number of rows of corner matirx and just 1 column
    
    for k = 1:length(image_corner_trim(:, 2))
    %for k = 1:1
        corner_i = image_corner_trim(k, 1);
        corner_j = image_corner_trim(k, 2);
        
        tic    % start timing measuring here
        lx_window = lx(corner_j - w : corner_j + w, corner_i - w : corner_i + w);
        ly_window = ly(corner_j - w : corner_j + w, corner_i - w : corner_i + w);
        lt_window  = lt(corner_j - w : corner_j + w, corner_i - w : corner_i + w);
        
        lx_window_tmp = lx_window(:);
        ly_window_tmp = ly_window(:);
        lt_window_tmp = lt_window(:);
        
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
        
        lx_square = lx_window_tmp.^2;
        lx_sum     = sum(lx_square(:));
        lx_sum_mod_flag = mod(lx_sum, 32);
        lx_sum     = bitsra(lx_sum, 5);
        if lx_sum < 0 && (lx_sum_mod_flag ~= 0)
            lx_sum = lx_sum - 1;
        end
        lx_sum     = fix(lx_sum);
        lx_sum     = int32(lx_sum);
        
        Iy_square = ly_window_tmp .^2;
        ly_sum     = sum(Iy_square(:));
        ly_sum_mod_flag = mod(ly_sum, 32);
        ly_sum     = bitsra(ly_sum, 5);
        if ly_sum < 0 && (ly_sum_mod_flag ~= 0)
            ly_sum = ly_sum - 1;
        end
        ly_sum     = fix(ly_sum);
        ly_sum     = int32(ly_sum);
        
        lx_ly_mul  = lx_window_tmp .* ly_window_tmp;
        lx_ly_mul_sum = sum(lx_ly_mul(:));
        lx_ly_mul_mod_flag = mod(lx_ly_mul_sum, 32);
        lx_ly_mul_sum = bitsra(lx_ly_mul_sum, 5);
        if (lx_ly_mul_sum < 0) && (lx_ly_mul_mod_flag ~= 0) 
            lx_ly_mul_sum = lx_ly_mul_sum - 1;
        end
        lx_ly_mul_sum = fix(lx_ly_mul_sum);
        lx_ly_mul_sum = int32(lx_ly_mul_sum);
        
        
        lx_lt_mul  = lx_window_tmp .* lt_window_tmp;
        lx_lt_mul_sum = sum(lx_lt_mul(:));
        lx_lt_mul_mod_flag = mod(lx_lt_mul_sum, 32);
        lx_lt_mul_sum = bitsra(lx_lt_mul_sum, 5);
        if (lx_lt_mul_sum < 0) && (lx_lt_mul_mod_flag ~= 0)
            lx_lt_mul_sum = lx_lt_mul_sum - 1;
        end
        lx_lt_mul_sum = fix(lx_lt_mul_sum);
        lx_lt_mul_sum = int32(lx_lt_mul_sum);
        lx_lt_mul_sum = lx_lt_mul_sum * (-1);
        
        ly_lt_mul  = ly_window_tmp .* lt_window_tmp;
        ly_lt_mul_sum = sum(ly_lt_mul(:));
        ly_lt_mul_mod_flag = mod(ly_lt_mul_sum, 32);
        ly_lt_mul_sum = bitsra(ly_lt_mul_sum, 5);
       if (ly_lt_mul_sum < 0) && (ly_lt_mul_mod_flag ~=0) 
            ly_lt_mul_sum = ly_lt_mul_sum - 1;
        end
        ly_lt_mul_sum = fix(ly_lt_mul_sum);
        ly_lt_mul_sum = int32(ly_lt_mul_sum);
        ly_lt_mul_sum = ly_lt_mul_sum * (-1);
        
        
        determinant_tmp(k) = lx_sum * ly_sum - lx_ly_mul_sum^2;
        determinant_tmp_double(k) = double(determinant_tmp(k));
        determinant(k) = 1 / determinant_tmp_double(k);
        %determinant = 1;
        %lx_sum_inv = lx_sum * determinant;
        %ly_sum_inv = ly_sum * determinant;
        %lx_ly_mul_inv = lx_ly_mul_sum * determinant * (-1);
        inverse_func = [ly_sum, lx_ly_mul_sum; lx_ly_mul_sum, lx_sum];
        matrix_2x1 = [lx_lt_mul_sum; ly_lt_mul_sum];
        %big_part = inverse_func * matrix_2x1;
        raw_vx(k) = ly_sum * lx_lt_mul_sum + lx_ly_mul_sum * (-1) * ly_lt_mul_sum;
        raw_vy(k) = lx_ly_mul_sum * (-1) * lx_lt_mul_sum + lx_sum * ly_lt_mul_sum;
        
        
        vx(k) = raw_vx(k) * determinant(k);
        vy(k) = raw_vy(k) * determinant(k);
        timeElapsed = toc;    % stop the time measuring
        
    end
    
    %=======plot the arrow on the image based on u and v==========
    %=======and save that plot as jpg, then write as frame to video=====%
    if n == 1
      vx = transpose(vx);
      vy = transpose(vy);
    end
    OF_result_figure = figure('visible', 'off');
    a = imshow(image_resize);
    hold on;
    quiver(image_corner_trim(:,1), image_corner_trim(:,2), vx,vy, 1,'r');
    saveas(OF_result_figure, sprintf('result_MATLAB/result_image_shift/OF_result%03d.jpg', n));
    %saveas(a, sprintf('traffic_test_video_OP_result_MATLAB/OF_result%03d.jpg', n));
    write_frame = imread(sprintf('result_MATLAB/result_image_shift/OF_result%03d.jpg', n));
    writeVideo(Video, write_frame);
    
    %===================== write to .dat file ===================
    % we have to transpose the image first then write to .dat
    % because MATLAB will fprintf the data by the column first
    % !!! now we only write the resized image to the data file
    %image_1_transpose = transpose(image_1_resize);
    %datFileName = ['traffic_test_video_480p_fps10/traffic_test_video_data/traffic_test_video_data' num2str(n) '.dat'];
    
    %=============write 3D Image sets to data file ==================
    datFileName_image = ['result_MATLAB/result_data/image_data_3d.dat'];
    fid_image = fopen(datFileName_image, 'a+');
    if n==1 
        fprintf(fid_image, '#include "stdint.h" \n');
        fprintf(fid_image, '\n');
        fprintf(fid_image, 'int32_t image_set_3d [%i][%i][%i] = { \n ', image_number, n_rows, n_cols);
        fprintf(fid_image, '\n');
        for wr_row_counter = 1:n_rows
            for wr_col_counter = 1:n_cols
                if wr_row_counter == 1 && wr_col_counter  == 1
                    fprintf(fid_image, '{ %i, ', image_gray(wr_row_counter, wr_col_counter));
                elseif wr_row_counter == n_rows && wr_col_counter == n_cols
                    fprintf(fid_image, '%i }, \n', image_gray(wr_row_counter, wr_col_counter));
                else
                    fprintf(fid_image, '%i, ', image_gray(wr_row_counter, wr_col_counter));
                end
            end
        end
        
    else
        
        for wr_row_counter = 1:n_rows
            for wr_col_counter = 1:n_cols
                if wr_row_counter == 1 && wr_col_counter == 1    % the first element should have frount bracket
                    fprintf(fid_image, '{ %i, ', image_gray(wr_row_counter, wr_col_counter));
                elseif wr_row_counter == n_rows && wr_col_counter == n_cols
                    if n == image_number
                        fprintf(fid_image, '%i } \n', image_gray(wr_row_counter, wr_col_counter));
                    else
                         fprintf(fid_image, '%i }, \n', image_gray(wr_row_counter, wr_col_counter));
                    end
                else
                    fprintf(fid_image, '%i, ', image_gray(wr_row_counter, wr_col_counter));
                end
            end
        end
        
        if n == image_number
            fprintf(fid_image, ' }; \n');
        else
            fprintf(fid_image, '\n');
        end
        
    end
    fprintf(fid_image, '\n');
    %===========================================
    
    %======write corner_x array to data file======================
    datFileName_cx = ['result_MATLAB/result_data/corner_x_coordi.dat'];
    fid_cx = fopen(datFileName_cx, 'a+');
    if n == 1
        fprintf(fid_cx, '#include "stdint.h" \n');
        fprintf(fid_cx, '\n');
        fprintf(fid_cx, 'int32_t corner_x [%i][%i] = { \n ', image_number, fixed_cn);
        fprintf(fid_cx, '\n');
        for wr_x_counter = 1:fixed_cn
            if wr_x_counter == fixed_cn
                fprintf(fid_cx, '%i, ', image_corner_trim(wr_x_counter, 1));
            else
                fprintf(fid_cx, '%i, ',image_corner_trim (wr_x_counter,1));
            end
        end
    else
         for wr_x_counter = 1:fixed_cn
            if wr_x_counter == fixed_cn
                if n == image_number
                    fprintf(fid_cx, '%i }; \n', image_corner_trim(wr_x_counter, 1));
                else
                    fprintf(fid_cx, '%i, ', image_corner_trim(wr_x_counter, 1));
                end
            else
                fprintf(fid_cx, '%i, ',image_corner_trim (wr_x_counter,1));
            end
        end
        
        
    end
    %==============================================
    
     %======write corner_y array to data file======================
    datFileName_cy = ['result_MATLAB/result_data/corner_y_coordi.dat'];
    fid_cy = fopen(datFileName_cy, 'a+');
    if n == 1
        fprintf(fid_cy, '#include "stdint.h" \n');
        fprintf(fid_cy, '\n');
        fprintf(fid_cy, 'int32_t corner_y [%i][%i] = { \n ', image_number, fixed_cn);
        fprintf(fid_cy, '\n');
        for wr_y_counter = 1:fixed_cn
            if wr_y_counter == fixed_cn
                fprintf(fid_cy, '%i, ', image_corner_trim(wr_y_counter, 2));
            else
                fprintf(fid_cy, '%i, ',image_corner_trim (wr_y_counter,2));
            end
        end
    else
        
         for wr_y_counter = 1:fixed_cn
            if wr_y_counter == fixed_cn
                if n == image_number
                    fprintf(fid_cy, '%i }; \n', image_corner_trim(wr_y_counter, 2));
                else
                    fprintf(fid_cy, '%i, ', image_corner_trim(wr_y_counter, 2));
                end
            else
                fprintf(fid_cy, '%i, ',image_corner_trim (wr_y_counter,2));
            end
        end
        
        
    end
    %=============================================
    
    %===============write vx_ref to data file =================
    datFileName_vx = ['result_MATLAB/result_data/vx_ref.dat'];
    fid_vx = fopen(datFileName_vx, 'a+');
    if n == 1
        fprintf(fid_vx, '#include "stdint.h" \n');
        fprintf(fid_vx, '\n');
        fprintf(fid_vx, 'int32_t vx_ref [%i] = { \n ', image_number * fixed_cn);
        fprintf(fid_vx, '\n');
        for wr_vx_counter = 1:fixed_cn
            if wr_vx_counter == fixed_cn
                fprintf(fid_vx, '%i, ', raw_vx(1, wr_vx_counter));
            else
                fprintf(fid_vx, '%i, ',raw_vx (1, wr_vx_counter));
            end
        end
    else
         for wr_vx_counter = 1:fixed_cn
            if wr_vx_counter == fixed_cn
                if n == image_number
                    fprintf(fid_vx, '%i }; \n', raw_vx(1, wr_vx_counter));
                else
                    fprintf(fid_vx, '%i, ', raw_vx(1, wr_vx_counter));
                end
            else
                fprintf(fid_vx, '%i, ',raw_vx (1, wr_vx_counter));
            end
        end
        
        
    end
    %==============================================
    
    %===============write vx_ref to data file =================
    datFileName_vy = ['result_MATLAB/result_data/vy_ref.dat'];
    fid_vy = fopen(datFileName_vy, 'a+');
    if n == 1
        fprintf(fid_vy, '#include "stdint.h" \n');
        fprintf(fid_vy, '\n');
        fprintf(fid_vy, 'int32_t vy_ref [%i] = { \n ', image_number * fixed_cn);
        fprintf(fid_vy, '\n');
        for wr_vy_counter = 1:fixed_cn
            if wr_vy_counter == fixed_cn
                fprintf(fid_vy, '%i, ', raw_vy(1, wr_vy_counter));
            else
                fprintf(fid_vy, '%i, ',raw_vy(1, wr_vy_counter));
            end
        end
    else
         for wr_vy_counter = 1:fixed_cn
            if wr_vy_counter == fixed_cn
                if n == image_number
                    fprintf(fid_vy, '%i }; \n', raw_vy(1, wr_vy_counter));
                else
                    fprintf(fid_vy, '%i, ', raw_vy(1, wr_vy_counter));
                end
            else
                fprintf(fid_vy, '%i, ',raw_vy (1, wr_vy_counter));
            end
        end
        
        
    end
    %==============================================
   
    %===============write de_ref to data file =================
    datFileName_de = ['result_MATLAB/result_data/de_ref.dat'];
    fid_de = fopen(datFileName_de, 'a+');
    if n == 1
        fprintf(fid_de, '#include "stdint.h" \n');
        fprintf(fid_de, '\n');
        fprintf(fid_de, 'int32_t de_ref [%i] = { \n ', image_number * fixed_cn);
        fprintf(fid_de, '\n');
        for wr_de_counter = 1:fixed_cn
            if wr_de_counter == fixed_cn
                fprintf(fid_de, '%i, ', determinant_tmp(1, wr_de_counter));
            else
                fprintf(fid_de, '%i, ',determinant_tmp(1, wr_de_counter));
            end
        end
    else
         for wr_de_counter = 1:fixed_cn
            if wr_de_counter == fixed_cn
                if n == image_number
                    fprintf(fid_de, '%i }; \n', determinant_tmp(1, wr_de_counter));
                else
                    fprintf(fid_de, '%i, ', determinant_tmp(1, wr_de_counter));
                end
            else
                fprintf(fid_de, '%i, ', determinant_tmp (1, wr_de_counter));
            end
        end
        
        
    end
    %==============================================
    
    fprintf('successfully write to data file! \n');
end
    

datFileName_cn = ['result_MATLAB/result_data/corner_nums.dat'];
fid_cn = fopen(datFileName_cn, 'w');
fprintf(fid_cn, '#include "stdint.h" \n');
fprintf(fid_cn, '\n');
fprintf(fid_cn, 'int32_t corner_number = %i ; \n', fixed_cn);

fclose(fid_image);
fclose(fid_cx);
fclose(fid_cy);
fclose(fid_cn);
fclose(fid_vx);
fclose(fid_vy);
fclose(fid_de);
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
