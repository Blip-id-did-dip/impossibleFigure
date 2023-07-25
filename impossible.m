CUBE_SIZE = 8;
TILE_SIZE = CUBE_SIZE *2 -1;



tile = ones(TILE_SIZE,TILE_SIZE);

TILE_HIGH = 0;

tile(1:CUBE_SIZE,1) = TILE_HIGH;
tile(1:CUBE_SIZE,CUBE_SIZE) = TILE_HIGH;
tile(1,1:CUBE_SIZE) = TILE_HIGH;
tile(CUBE_SIZE,1:CUBE_SIZE) = TILE_HIGH;

tile(CUBE_SIZE:TILE_SIZE,TILE_SIZE) =TILE_HIGH;
tile(TILE_SIZE,CUBE_SIZE:TILE_SIZE) = TILE_HIGH;

for k=1:CUBE_SIZE
    tile(k,k+CUBE_SIZE-1) = TILE_HIGH;
    tile(k+CUBE_SIZE-1,k+CUBE_SIZE-1) =TILE_HIGH;
    tile(k+CUBE_SIZE-1,k) = TILE_HIGH;
end



NUM_TILES = 18;
my_map = randi(5,NUM_TILES);

CUBE_MINUS_ONE = CUBE_SIZE-1;

my_image = ones(CUBE_MINUS_ONE*NUM_TILES, CUBE_MINUS_ONE*NUM_TILES);

for xind = NUM_TILES-1:-1:2
    for yind = NUM_TILES-1:-1:2
        if my_map(xind,yind) ==1
            my_image(CUBE_MINUS_ONE*(xind-1):CUBE_MINUS_ONE*(xind-1)+TILE_SIZE-1,CUBE_MINUS_ONE*(yind-1):CUBE_MINUS_ONE*(yind-1)+TILE_SIZE-1) = tile;
        end
    end
end



imshow(my_image)