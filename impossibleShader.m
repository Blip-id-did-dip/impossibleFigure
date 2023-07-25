image_width = 500;
image_height = 500;

image = zeros(image_height,image_width, 'uint8');


vc1 = [0 ; -1];
vc2 = [ -1; 0.5];
vc3 = [ 1; 1];

image_magnitude = 3/500;


offset = [-image_height /2 ,- image_width/2];


for xind = 1:image_height
    for yind = 1:image_width
        xcoord = (-xind - offset(1)) * image_magnitude ;
        ycoord = (yind + offset(2))* image_magnitude  ;

        posL = [vc1 , vc2] \ [ycoord ; xcoord];
        posR = [vc1 , vc3] \ [ycoord ; xcoord];
        posT = [vc3 , vc2] \ [ycoord ; xcoord];

        if max(posL) < 1 && min(posL) >=0 
            image(xind,yind,1) = 255;
            image(xind,yind,2) = 255;
            image(xind,yind,3) = 255;
        elseif max(posR) < 1 && min(posR) >=0 
            image(xind,yind,1) = 0;
            image(xind,yind,2) = 0;
            image(xind,yind,3) = 255;
        elseif max(posT) < 1 && min(posT) >=0 
            image(xind,yind,1) = 0;
            image(xind,yind,2) = 255;
            image(xind,yind,3) = 255;
        end
        
    end
end