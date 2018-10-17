/*
 * grailkit.spout
 * ~~~~~~~~~~~~~~
 *
 * Spout Library
 *
 * :copyright: (c) 2018 by Oleksii Lytvyn.
 * :license: MIT, see LICENSE for more details.
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <windows.h>
#include <GL/GL.h>
#include <Spout.h>

namespace py = pybind11;


class Sender {

public:

	Spout spout;
	unsigned int width;
	unsigned int height;

	Sender(){
	    // todo: remove create method, and move it to constructor
	}

	~Sender() {
	    // todo: release sender when class is destructed in Python
	}

	bool create(const char *name, unsigned int width, unsigned int height) {
		return spout.CreateSender(name, width, height);
	}

	// Upodate sender information
	bool update(const char *name, unsigned int width, unsigned int height) {
		return spout.UpdateSender(name, width, height);
	}

	// release sender 
	void release() {
		spout.ReleaseSender();
	}

	// Send array of pixels
	bool send_image(std::vector<unsigned char> pixels, unsigned int width, unsigned int height, GLenum glFormat, bool bInvert = false, GLuint HostFBO = 0) {
		return spout.SendImage(pixels.data(), width, height, glFormat, bInvert, HostFBO);
	}

	// Send OpenGL texture
	bool send_texture(GLuint TextureID, GLuint TextureTarget, unsigned int width, unsigned int height, bool bInvert = true, GLuint HostFBO = 0) {
		return spout.SendTexture(TextureID, TextureTarget, width, height, bInvert, HostFBO);
	}

};


class Receiver {

public:

	Spout spout;
	
	char* name;
	unsigned int width;
	unsigned int height;

    Receiver (){
		// todo: move create method to initializer
		// todo: make use of properties width, height & name
	}

    ~Receiver (){
		// todo: Add python destructor
    }

	bool create(char* Sendername, unsigned int &width, unsigned int &height, bool bUseActive = false) {
		return spout.CreateReceiver(Sendername, width, height, bUseActive);
	}

	bool receive_texture(char* Sendername, unsigned int &width, unsigned int &height, GLuint TextureID = 0, GLuint TextureTarget = 0, bool bInvert = false, GLuint HostFBO = 0) {
		return spout.ReceiveTexture(Sendername, width, height, TextureID, TextureTarget, bInvert, HostFBO);
	}

	bool receive_image(char* Sendername, unsigned int &width, unsigned int &height, std::vector<unsigned char> pixels, GLenum glFormat = GL_RGBA, bool bInvert = false, GLuint HostFBO = 0) {
		return spout.ReceiveImage(Sendername, width, height, pixels.data(), glFormat, bInvert, HostFBO);
	}

	bool get_image_size(char* Sendername, unsigned int &width, unsigned int &height, bool &bMemoryMode) {
		// todo: make more pythonic, as width & height passed by reference

		return spout.GetImageSize(Sendername, width, height, bMemoryMode);
	}
	
	void release() {
		spout.ReleaseReceiver();
	}

};

// Python Module declaration
PYBIND11_MODULE(_spout, m) {

	m.doc() = "Spout Python extension for inter-application video sharing";

	py::class_<Sender>(m, "Sender")
		.def(py::init<>())
		.def("create", &Sender::create)
		.def("update", &Sender::update)
		.def("release", &Sender::release)
		.def("send_image", &Sender::send_image)
		.def("send_texture", &Sender::send_texture);

	py::class_<Receiver>(m, "Receiver")
		.def(py::init<>())
		.def("create", &Receiver::create)
		.def("release", &Receiver::release)
		.def("receive_image", &Receiver::receive_image)
		.def("receive_texture", &Receiver::receive_texture)
		.def("get_image_size", &Receiver::get_image_size);

}
