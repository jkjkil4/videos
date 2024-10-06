#version 330 core

in vec4 v_color;
in vec2 v_texcoord;

out vec4 f_color;

uniform sampler2D image;

void main()
{
	f_color = texture(image, clamp(v_texcoord, 0.0, 1.0)) * v_color;
}
