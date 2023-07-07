# examples RGB mode

## examples RGB mode: short codes
[short codes](../README.md#short-codes)

code - r  
encoded:
```glsl
vec3 channelR = vec3(1, 0, 0);
vec3 channelG = vec3(0, 0, 0);
vec3 channelB = vec3(0, 0, 0);
```

code - gb  
encoded:
```glsl
vec3 channelR = vec3(0, 0, 0);
vec3 channelG = vec3(0, 1, 0);
vec3 channelB = vec3(0, 0, 1);
```

code - bb  
encoded:
```glsl
vec3 channelR = vec3(0, 0, 0);
vec3 channelG = vec3(0, 0, 0);
vec3 channelB = vec3(0, 0, 1);
```

## examples RGB mode: medium codes
[medium codes](../README.md#medium-codes)

code - rgb  
encoded:
```glsl
vec3 channelR = vec3(1, 0, 0);
vec3 channelG = vec3(0, 1, 0);
vec3 channelB = vec3(0, 0, 1);
```

code - brg  
encoded:
```glsl
vec3 channelR = vec3(0, 1, 0);
vec3 channelG = vec3(0, 0, 1);
vec3 channelB = vec3(1, 0, 1);
```

code - rrr  
encoded:
```glsl
vec3 channelR = vec3(1, 1, 1);
vec3 channelG = vec3(0, 0, 0);
vec3 channelB = vec3(0, 0, 0);
```

code - __r  
encoded:
```glsl
vec3 channelR = vec3(0, 0, 1);
vec3 channelG = vec3(0, 0, 0);
vec3 channelB = vec3(0, 0, 0);
```

## examples RGB mode: large codes
[large codes](../README.md#large-codes)

code - rgb..  
encoded:
```glsl
vec3 channelR = vec3(1/3, 0, 0);
vec3 channelG = vec3(1/3, 0, 0);
vec3 channelB = vec3(1/3, 0, 0);
```

code - rgb.brg.gbr  
encoded:
```glsl
vec3 channelR = vec3(1/3, 1/3, 1/3);
vec3 channelG = vec3(1/3, 1/3, 1/3);
vec3 channelB = vec3(1/3, 1/3, 1/3);
```

code - rrgb..  
encoded:
```glsl
vec3 channelR = vec3(1/2, 0, 0);
vec3 channelG = vec3(1/4, 0, 0);
vec3 channelB = vec3(1/4, 0, 0);
```

code - r98gb..  
encoded:
```glsl
vec3 channelR = vec3(0.98, 0, 0);
vec3 channelG = vec3(0.1, 0, 0);
vec3 channelB = vec3(0.1, 0, 0);
```