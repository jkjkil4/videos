#version 330 core

in vec4 v_color;
in vec2 v_texcoord;

out vec4 f_color;

uniform sampler2D image;

void main()
{
	vec4 color;
	if (v_texcoord.x > 1.0 || v_texcoord.y > 1.0 || v_texcoord.x < 0.0 || v_texcoord.y < 0.0) {
		color = vec4(0, 50.0, 62.0, 255.0) / 255.0;
	} else {
		color = texture(image, v_texcoord);
	}
	f_color = color * v_color;
}
