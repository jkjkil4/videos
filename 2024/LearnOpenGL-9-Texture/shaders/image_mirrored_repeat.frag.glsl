#version 330 core

in vec4 v_color;
in vec2 v_texcoord;

out vec4 f_color;

uniform sampler2D image;

void main()
{
	vec2 texcoord = fract(v_texcoord / 2.0) * 2.0;
	texcoord = min(texcoord, 2.0 - texcoord);
	f_color = texture(image, texcoord) * v_color;
}
