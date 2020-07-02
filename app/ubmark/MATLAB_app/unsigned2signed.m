function [b] = unsigned2signed(data, width)

data_size = size(data);
sign_mask = 2^(width-1);
data_mask = ones(data_size)*sign_mask;

data_sign = -1*bitand(data_mask,data);
data_remainder = bitand((data_mask - 1),data);

b = data_sign + data_remainder;