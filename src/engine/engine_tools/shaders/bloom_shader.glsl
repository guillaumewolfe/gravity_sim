 #version 330 core


in vec2 TexCoords;
out vec4 FragColor;


uniform sampler2D scene;  // The scene texture
uniform float threshold;  // Brightness threshold for bloom
uniform float exposure;   // Exposure control
uniform float decay;      // Decay factor for the rays
uniform int numRays;      // Number of rays


void main()
{
    // Sample the scene texture
    vec4 color = texture(scene, TexCoords);


    // Calculate brightness
    float brightness = dot(color.rgb, vec3(0.2126, 0.7152, 0.0722));


    // Apply bloom only to bright pixels
    if (brightness > threshold)
    {
        // Calculate ray angle and step size
        float angleStep = 6.283185 / float(numRays);  // 2 * PI
        float angle = atan(TexCoords.y - 0.5, TexCoords.x - 0.5);
        
        // Apply rays
        for (int i = 0; i < numRays; i++)
        {
            float alpha = abs(sin(angle - float(i) * angleStep));
            color.rgb += vec3(alpha) * exposure * color.rgb;
        }
    }


    FragColor = color;
}
