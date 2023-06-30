#version 330 core
#define PI 3.1415926538

layout(location = 0) out vec4 fragColor;
uniform vec2 iResolution;
uniform sampler2D iChannel0;
float pi = 3.14159265;


float lerp2_1d(float a, float b, float t) {
    return (b - a) * t + a;
}

vec2 lerp2(vec2 a, vec2 b, float t) {
    return vec2((b.x - a.x) * t + a.x, (b.y - a.y) * t + a.y);
}

vec2 lerp3(vec2 a,vec2 b,vec2 c,float t) {
    return lerp2(lerp2(a,b,t),lerp2(b,c,t),t);
}

vec2 lerp4(vec2 a, vec2 b, vec2 c, vec2 d, float t) {
    return lerp2(lerp3(a,b,c,t),lerp3(b,c,d,t),t);
}

mat2 getMatrix(vec2 O, vec2 X, vec2 Y) {
    return mat2(X.x - O.x, Y.x - O.x, X.y - O.y, Y.y - O.y);
}

float dotP(vec2 a, vec2 b) {
    return (a.x * b.x) + (a.y * b.y);
}

float atan2(in float y, in float x)
{
    bool s = abs(x) > abs(y);
    return mod(mix(pi/2.0 - atan(x,y), atan(y,x), s), pi * 2.0);
}

float atan2(vec2 vec) 
{
    return atan2(vec.y,vec.x);
}

float rad2deg(float f) {
    return f * (180.0 / pi);
}

bool isPointInParallelogram(vec2 bottomleft, vec2 bottomright, vec2 topleft, vec2 topright, vec2 pt)
{
    vec2 TR = normalize(topright - pt);
    vec2 TL = normalize(topleft - pt);
    vec2 BL = normalize(bottomleft - pt);
    vec2 BR = normalize(bottomright - pt);
    
    float a1 = acos(dot(TR, TL));
    float a2 = acos(dot(TL, BL));
    float a3 = acos(dot(BL, BR));
    float a4 = acos(dot(BR, TR));
    
    float sum = a1 + a2 + a3 + a4;
    
    //bool returnValue = abs(rad2deg(sum) - 360.0) < 0.1;
    
    //returnValue = pt.x < 0.5;
    return abs(sum - (pi * 2.0)) < 0.1;
}

vec2 gridGet(vec2[64] grid, int x, int y) {
    return grid[(y * 8) + x];
}

void gridSet(inout vec2[64] grid, int x, int y, vec2 value) {
    grid[(y * 8) + x] = value;
}

vec2 plotGridGet(vec2[49] plotGrid, int x, int y) {
    return plotGrid[(y * 7) + x];
}

void plotGridSet(inout vec2[49] plotGrid, int x, int y, vec2 value) {
    plotGrid[(y * 7) + x] = value;
}

vec2[64] generateGrid(vec2[4] a, vec2[4] b) {
    vec2[64] grid;
    for (int x = 0; x < 8; x += 1) {
        for (int y = 0; y < 8; y += 1) {
            vec2 ptA = lerp4(a[0],a[1],a[2],a[3], float(x) / 8.0);
            vec2 ptB = lerp4(b[0],b[1],b[2],b[3], float(x) / 8.0);
            vec2 pt = lerp2(ptA,ptB, float(y) / 8.0);
            gridSet(grid,x,y,pt);
        }
    }
    return grid;
}

vec2[49] generatePlotGrid(vec2[4] a, vec2[4] b) {
    vec2[49] plotGrid;
    for (int x = 0; x < 7; x += 1) {
        for (int y = 0; y < 7; y += 1) {
            vec2 ptA = lerp4(a[0],a[1],a[2],a[3], float(float(x) + 0.5) / 8.0);
            vec2 ptB = lerp4(b[0],b[1],b[2],b[3], float(float(x) + 0.5) / 8.0);
            vec2 pt = lerp2(ptA,ptB, float(y) / 8.0);
            plotGridSet(plotGrid,x,y,pt);
        }
    }
    return plotGrid;
}


/*bool locatePointOnGrid(vec2[64] grid, vec2 pt, out int gridx, out int gridy) {
    gridx = -1;
    gridy = -1;
    for (int x = 0; x < 7; x += 1) {
        for (int y = 0; y < 7; y += 1) {
            vec2 a = gridGet(grid,x,y);
            vec2 b = gridGet(grid,x+1,y);
            vec2 c = gridGet(grid,x,y+1);
            vec2 d = gridGet(grid,x+1,y+1);
            if (isPointInParallelogram(a, b, c, d, pt)) {
                gridx = x;
                gridy = y;
                return true;
            }
        }
    }
    return false;
}*/


bool optimizedLocatePointOnGrid(vec2[64] grid, vec2 pt, out int gridx, out int gridy) {
    gridx = -1;
    gridy = -1;
    for (int x = 0; x < 2; x += 1) {
        vec2 ax = gridGet(grid,x,0);
        vec2 bx = gridGet(grid,x+1,0);
        vec2 cx = gridGet(grid,x,7);
        vec2 dx = gridGet(grid,x+1,7);
        if (isPointInParallelogram(ax, bx, cx, dx, pt)) {
            gridx = x;
            for (int y = 0; y < 2; y += 1) {
                vec2 ay = gridGet(grid,x,y);
                vec2 by = gridGet(grid,x+1,y);
                vec2 cy = gridGet(grid,x,y+1);
                vec2 dy = gridGet(grid,x+1,y+1);
                if (isPointInParallelogram(ay, by, cy, dy, pt)) {
                    gridy = y;
                    return true;
                }
            }
            return false;
        }
    }
    return false;
}

bool locatePointOnGrid2(vec2[64] grid, vec2[49] plotGrid, vec2 pt, out int gridx, out int gridy) {
    bool cLengthNull = true;
    float closestLength = -1.0;
    int cX = -1;
    int cY = -1;
    for (int x = 0; x < 7; x += 1) {
        for (int y = 0; y < 7; y += 1) {
            float len = length(plotGridGet(plotGrid, x, y) - pt);
            if (cLengthNull || len < closestLength) {
                cLengthNull = false;
                closestLength = len;
                cX = x;
                cY = y;
            }
        }
    }
    vec2 a1 = gridGet(grid,cX,cY);
    vec2 b1 = gridGet(grid,cX+1,cY);
    vec2 c1 = gridGet(grid,cX,cY+1);
    vec2 d1 = gridGet(grid,cX+1,cY+1);
    //if (isPointInParallelogram(a1, b1, c1, d1, pt)) {
        gridx = cX;
        gridy = cY;
        return true;
    //}
    //return false;
}

vec2 getPoint(int x, int y, vec2[4] a, vec2[4] b) {
    vec2 ptA = lerp4(a[0],a[1],a[2],a[3], float(x) / 7.0);
    vec2 ptB = lerp4(b[0],b[1],b[2],b[3], float(x) / 7.0);
    vec2 pt = lerp2(ptA,ptB, float(y) / 7.0);
    return pt;
}

vec2[4] topLine;
vec2[4] bottomLine;
vec2[64] grid;
vec2[49] plotGrid;

void main()
{
    vec2 uv = gl_FragCoord.xy/iResolution.xy;
    
    topLine[0] = vec2(72.0,14.0) / 400.0;
    topLine[1] = vec2(160.0,14.0) / 400.0;
    topLine[2] = vec2(245.0,14.0) / 400.0;
    topLine[3] = vec2(330.0,14.0) / 400.0;

    bottomLine[0] = vec2(53,370) / 400.0;
    bottomLine[1] = vec2(151,332) / 400.0;
    bottomLine[2] = vec2(251,332) / 400.0;
    bottomLine[3] = vec2(352,371) / 400.0;
    
    grid = generateGrid(topLine, bottomLine);
    plotGrid = generatePlotGrid(topLine, bottomLine);
    // Normalized pixel coordinates (from 0 to 1)
    
    //vec4 col = texture(iChannel0, uv);
    
    int gridX = -1;
    int gridY = -1;  
    fragColor = vec4(0.0,0.0,0.0,1.0);
    for (int x = 0; x < 8; x += 1) {
        for (int y = 0; y < 8; y += 1) {
            vec2 pt = gridGet(grid,x,y);
            if (length(pt - uv) < 0.02) {
                fragColor = vec4(float(x) / 8.0,  float(y) / 8.0,0.0,1.0);
            }
            if (length(pt - uv) < 0.01) {
                fragColor = vec4(pt,0.0,1.0);
            }
        }
    }
    bool isIn = isPointInParallelogram(gridGet(grid, 0, 0), gridGet(grid, 7, 0), gridGet(grid, 0, 7), gridGet(grid, 7, 7), uv);
    
    if (isIn) {
        bool isLoc = locatePointOnGrid2(grid, plotGrid, uv, gridX, gridY);
        //isLoc = false;
        
        if (isLoc) {
            fragColor = vec4(float(gridX) / 7.0, float(gridY) / 7.0, 0.0, 1.0);
            //fragColor = texture(iChannel0, uv);
        }
    }
    /*if (locatePointOnGrid(grid, uv, gridX, gridY)) {
        /*
        vec2 origin = gridGet(grid, gridX, gridY);
        vec2 xPoint = gridGet(grid, gridX + 1, gridY);
        vec2 yPoint = gridGet(grid, gridX, gridY + 1);
        mat2 matrix = inverse(getMatrix(origin, xPoint, yPoint));
        vec2 result = matrix * uv;
        
        
        
        //col = vec4(floor(uv * 7.0) / 7.0, 0.0, 1.0);
        //col = vec4(uv,0.0,1.0);
        // Output to screen
        fragColor = vec4(uv, 0.0, 1.0);
    }
    else {
        fragColor = vec4(0.0,0.9,1.0,1.0);
    }
    */
    
}
