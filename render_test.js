function main(lines, side, then) {
    console.log(lines[0])
    var canvas = document.querySelector(side);
    var gl = canvas.getContext('webgl');
    if (!gl) {
      alert('Unable to initialize WebGL. Your browser or machine may not support it.');
      return;
    }

    const vsSource = `
        attribute vec4 aVertexPosition;

        uniform mat4 uModelViewMatrix;
        uniform mat4 uProjectionMatrix;

        void main() {
          gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
          gl_PointSize = 5.0;
        }
    `;
    const fsSource = `
            void main() {
              gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
            }
      `;
    const shaderProgram = initShaderProgram(gl, vsSource, fsSource);
    const programInfo = {
        program: shaderProgram,
        attribLocations: {
            vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
        },
        uniformLocations: {
            projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
            modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
        },
    };

    const buffers = initBuffers(gl, lines);

    function render(now) {
        now *= 0.001;
        const deltaTime = Math.max(0, now - then);
        t_idx = parseInt(deltaTime * 24)
        drawScene(gl, programInfo, buffers, t_idx, lines);
        if (t_idx < lines.length-1) {
            requestAnimationFrame(render);
        }
    }
    // var then = performance.now()*0.001;
    requestAnimationFrame(render);
}

function drawScene(gl, programInfo, position, t_idx, lines){
    gl.clearColor(0.5, 0.5, 0.5, 1.0);  // Clear to black, fully opaque
    gl.clearDepth(1.0);                 // Clear everything
    gl.enable(gl.DEPTH_TEST);           // Enable depth testing
    gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    const fieldOfView = 45 * Math.PI / 180;   // in radians
    const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
    const zNear = 0.1;
    const zFar = 200.0;
    const projectionMatrix = mat4.create();
    mat4.perspective(projectionMatrix,
                   fieldOfView,
                   aspect,
                   zNear,
                   zFar);

    // Tell WebGL how to pull out the positions from the position
    // buffer into the vertexPosition attribute.
    {
        const numComponents = 3;
        const type = gl.FLOAT;
        const normalize = false;
        const stride = 0;
        const offset = 0;
        gl.bindBuffer(gl.ARRAY_BUFFER, position);
        gl.vertexAttribPointer(
            programInfo.attribLocations.vertexPosition,
            numComponents,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(
            programInfo.attribLocations.vertexPosition);
    }
    gl.bufferData(gl.ARRAY_BUFFER,
                  new Float32Array(lines[t_idx]),
                  gl.STATIC_DRAW);
    gl.useProgram(programInfo.program);

    // Set the shader uniforms
    gl.uniformMatrix4fv(
      programInfo.uniformLocations.projectionMatrix,
      false,
      projectionMatrix);

    const modelViewMatrix = mat4.create();

    // Now move the drawing position a bit to where we want to
    // start drawing the square.
    mat4.translate(modelViewMatrix,     // destination matrix
                   modelViewMatrix,     // matrix to translate
                   [-10, -7, -40]);  // amount to translate [-10, -7, -40])

    mat4.rotate(modelViewMatrix,
        modelViewMatrix,
        0.5,
        [0, 1, 0]); // wenn man die zweite Zahl auf 1 oder -1 setzt, kann man das Bild spiegeln
    mat4.rotate(modelViewMatrix,
        modelViewMatrix,
        0.15,
        [1, 0, 1]);
    mat4.rotate(modelViewMatrix,
        modelViewMatrix,
        0,
        [0, -1, 0]);
    gl.uniformMatrix4fv(
      programInfo.uniformLocations.modelViewMatrix,
      false,
      modelViewMatrix);

    {
        const offset = 0;
        // const vertexCount = 19;
        const vertexCount = 32;
        const type = gl.UNSIGNED_SHORT;
        gl.drawArrays(gl.LINES, 0, vertexCount);
    }
}

function initBuffers(gl, lines) {
    var vertices = lines[0];
    const positionBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);
    gl.bufferData(gl.ARRAY_BUFFER,
                  new Float32Array(vertices),
                  gl.STATIC_DRAW);
    return positionBuffer
};
